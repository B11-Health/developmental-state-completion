#!/usr/bin/env python3
"""Exploratory replication of developmental state-completion diagnostics
using the authors' released Refahi et al. Arabidopsis flower atlas files.

Frozen design before first run:
- two windows: 40 -> 96 -> 120 h and 96 -> 120 -> 132 h
- target: log(total descendant volume at future / current cell volume)
- M0: current geometry (log-volume + x,y,z)
- M1: M0 + current 25-gene binary atlas state
- M2: M1 + older geometry + older 25-gene state
- grouped 5-fold CV by older ancestor cell ID
- primary model: Ridge(alpha=10) with full shuffled-history placebo
- nonlinear robustness: ExtraTrees with fixed hyperparameters, no permutation refits
- history placebo: shuffle complete older-state vectors between ancestor groups for the primary Ridge model
- repeat for all eligible cells and L1 epidermal cells

This is an exploratory reanalysis of atlas-mapped expression patterns, not a
prospective measurement and not proof of biological Markovity.
"""
from pathlib import Path
import io, json, math, pickle, re, runpy, os
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

REPO = Path(__file__).resolve().parents[1]
_candidates = []
if os.environ.get('REFAHI_ROOT'): _candidates.append(Path(os.environ['REFAHI_ROOT']))
_candidates += [REPO.parent / 'refahi_diag', Path('refahi_diag')]
ROOT = next((x for x in _candidates if x.exists()), _candidates[0])
OUT = REPO / 'results'
OUT.mkdir(exist_ok=True)
RNG_SEED = 20260829
N_PERM = 100

class Stub: pass
class LegacyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'atlasviewer.dtissue' and name == 'DTissue':
            return Stub
        if module == 'copy_reg': module = 'copyreg'
        if module == '__builtin__': module = 'builtins'
        return super().find_class(module, name)

def load_dtissue():
    b=(ROOT/'stateAnalysis/FM1_dtissue.tis').read_bytes().replace(b'\r\n',b'\n')
    return LegacyUnpickler(io.BytesIO(b),encoding='latin1').load()

def read_expr(t):
    return pd.read_csv(ROOT/f'data/geneExpression/t_{t}h.txt', sep=r'\s+').set_index('CID')

def read_geom(t):
    rows=[]
    pat=re.compile(r'cid:\s*(\d+), volume:\s*([^,]+), center:\s*\[([^\]]+)\]')
    for ln in (ROOT/f'data/FM1/tv/{t}h_segmented_tvformat_volume_position.txt').read_text().splitlines():
        m=pat.search(ln)
        if not m: continue
        cid=int(m.group(1)); vol=float(m.group(2)); xyz=[float(x) for x in m.group(3).split()]
        rows.append((cid,vol,*xyz))
    return pd.DataFrame(rows,columns=['CID','volume','x','y','z']).set_index('CID')

def ancestor(dt, cid, cur, hist):
    times=dt.timePoints
    i=times.index(f'{cur}h'); j=times.index(f'{hist}h')
    c=int(cid)
    while i>j:
        tp=times[i]
        c=int(dt.dtissue[tp]['mother'].get(c,-1))
        if c <= 1: return None
        i-=1
    return c

def descendants(dt, cid, cur, fut):
    times=dt.timePoints
    i=times.index(f'{cur}h'); j=times.index(f'{fut}h')
    cs=[int(cid)]
    while i<j:
        tp=times[i]
        nxt=[]
        dmap=dt.dtissue[tp].get('daughters',{})
        for c in cs: nxt.extend(int(x) for x in dmap.get(c,[]))
        cs=[x for x in nxt if x>1]
        if not cs: return []
        i+=1
    return cs

def build_window(dt,hist,cur,fut,l1_only=False):
    expr_h,expr_c=read_expr(hist),read_expr(cur)
    geom_h,geom_c=read_geom(hist),read_geom(cur)
    l1=runpy.run_path(str(ROOT/'common/common/L1L2_cells_ids.py'))
    l1c=set(l1[f'L1_{cur}h']); l1h=set(l1[f'L1_{hist}h'])
    genes=list(expr_c.columns)
    rows=[]
    for cid in expr_c.index:
        cid=int(cid)
        if cid not in geom_c.index: continue
        if l1_only and cid not in l1c: continue
        aid=ancestor(dt,cid,cur,hist)
        if aid is None or aid not in expr_h.index or aid not in geom_h.index: continue
        if l1_only and aid not in l1h: continue
        ds=descendants(dt,cid,cur,fut)
        if not ds: continue
        vols=dt.dtissue[f'{fut}h']['volumes']
        if any(d not in vols for d in ds): continue
        vcur=float(geom_c.loc[cid,'volume']); vfut=float(sum(float(vols[d]) for d in ds))
        if vcur<=0 or vfut<=0: continue
        r={'cid':cid,'group':aid,'target':math.log(vfut/vcur)}
        gc=geom_c.loc[cid]; gh=geom_h.loc[aid]
        for k in ['x','y','z']: r[f'cur_{k}']=float(gc[k])
        r['cur_logv']=math.log(float(gc['volume']))
        for g in genes: r[f'cur_g_{g}']=float(expr_c.loc[cid,g])
        for k in ['x','y','z']: r[f'hist_{k}']=float(gh[k])
        r['hist_logv']=math.log(float(gh['volume']))
        for g in genes: r[f'hist_g_{g}']=float(expr_h.loc[aid,g])
        rows.append(r)
    return pd.DataFrame(rows),genes

def make_splits(groups):
    ug=np.unique(groups)
    ns=min(5,len(ug))
    if ns<3: raise RuntimeError('too few lineage groups')
    cv=GroupKFold(n_splits=ns,shuffle=True,random_state=RNG_SEED)
    dummy=np.zeros((len(groups),1))
    return list(cv.split(dummy,groups=groups))

def model_specs():
    return {
      'ridge': make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
      'extra_trees': ExtraTreesRegressor(n_estimators=200,min_samples_leaf=5,max_features=0.7,random_state=RNG_SEED,n_jobs=-1)
    }

def cv_predict(X,y,splits,model):
    pred=np.full(len(y),np.nan)
    fold_r2=[]
    for tr,te in splits:
        model.fit(X[tr],y[tr]); p=model.predict(X[te]); pred[te]=p
        fold_r2.append(r2_score(y[te],p))
    return pred,fold_r2

def shuffled_history(df,hcols,rng):
    out=df[hcols].copy()
    groups=df['group'].to_numpy()
    ug=np.unique(groups)
    rep={g:df.loc[df.group==g,hcols].iloc[0].to_numpy() for g in ug}
    perm=ug.copy(); rng.shuffle(perm)
    mp={g:rep[p] for g,p in zip(ug,perm)}
    vals=np.vstack([mp[g] for g in groups])
    return vals

def analyze(df,genes,window,label):
    y=df.target.to_numpy(float); groups=df.group.to_numpy()
    splits=make_splits(groups)
    geom=[f'cur_{k}' for k in ['logv','x','y','z']]
    curgenes=[f'cur_g_{g}' for g in genes]
    histgeom=[f'hist_{k}' for k in ['logv','x','y','z']]
    histgenes=[f'hist_g_{g}' for g in genes]
    sets={'M0_geom':geom,'M1_current':geom+curgenes,'M2_history':geom+curgenes+histgeom+histgenes}
    result={'window':window,'subset':label,'n':len(df),'groups':int(df.group.nunique()),'target_mean':float(y.mean()),'target_sd':float(y.std(ddof=1)),'models':{}}
    rng=np.random.default_rng(RNG_SEED)
    for mname,model in model_specs().items():
        mr={}
        preds={}
        for sname,cols in sets.items():
            X=df[cols].to_numpy(float)
            p,fr=cv_predict(X,y,splits,model)
            preds[sname]=p
            mr[sname]={'r2':float(r2_score(y,p)),'mae':float(mean_absolute_error(y,p)),'fold_r2_mean':float(np.mean(fr)),'fold_r2':list(map(float,fr))}
        actual_gain=mr['M2_history']['r2']-mr['M1_current']['r2']
        if mname == 'ridge':
            null=[]
            base=df[geom+curgenes].to_numpy(float)
            hcols=histgeom+histgenes
            for _ in range(N_PERM):
                hs=shuffled_history(df,hcols,rng)
                X=np.hstack([base,hs])
                p,_=cv_predict(X,y,splits,model)
                null.append(float(r2_score(y,p)-mr['M1_current']['r2']))
            mr['history_gain']={'actual_delta_r2':float(actual_gain),'shuffle_mean':float(np.mean(null)),'shuffle_p95':float(np.quantile(null,.95)),'shuffle_pvalue_ge_actual':float((1+sum(x>=actual_gain for x in null))/(N_PERM+1))}
        else:
            mr['history_gain']={'actual_delta_r2':float(actual_gain),'shuffle_test':'not run; nonlinear robustness only'}
        result['models'][mname]=mr
    return result

def main():
    import argparse
    ap=argparse.ArgumentParser(description='Run frozen Refahi atlas replication')
    ap.add_argument('--hist',type=int,choices=[40,96])
    ap.add_argument('--cur',type=int,choices=[96,120])
    ap.add_argument('--fut',type=int,choices=[120,132])
    ap.add_argument('--subset',choices=['all','L1'])
    args=ap.parse_args()
    dt=load_dtissue()
    if any(v is not None for v in [args.hist,args.cur,args.fut,args.subset]):
        if None in [args.hist,args.cur,args.fut,args.subset]: ap.error('case mode requires --hist --cur --fut --subset')
        cases=[(args.hist,args.cur,args.fut,args.subset=='L1')]
    else:
        cases=[(40,96,120,False),(40,96,120,True),(96,120,132,False),(96,120,132,True)]
    allres=[]
    for hist,cur,fut,l1 in cases:
        df,genes=build_window(dt,hist,cur,fut,l1)
        label='L1' if l1 else 'all'
        print('WINDOW',hist,cur,fut,label,'n=',len(df),'groups=',df.group.nunique())
        res=analyze(df,genes,f'{hist}->{cur}->{fut}',label)
        wrapped={'source_commit':'95fde8b3b9a0bd09d556ce765a2235093362306f','design_frozen_before_first_run':True,'n_permutations':N_PERM,'result':res}
        (OUT/f'refahi_{hist}_{cur}_{fut}_{label}.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
        allres.append(res)
    if len(cases)>1:
        out={'source_commit':'95fde8b3b9a0bd09d556ce765a2235093362306f','design_frozen_before_first_run':True,'n_permutations':N_PERM,'results':allres}
        (OUT/'refahi_state_completion_replication.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
        print(json.dumps(out,indent=2))
    else:
        print(json.dumps(wrapped,indent=2))
if __name__=='__main__':
    main()
