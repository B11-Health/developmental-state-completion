import argparse, io, math, pickle, re, runpy, subprocess
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

class DummyDTissue: pass
class CompatUnpickler(pickle.Unpickler):
    def find_class(self,module,name):
        if module=='atlasviewer.dtissue' and name=='DTissue': return DummyDTissue
        if module=='copy_reg': module='copyreg'
        if module=='__builtin__': module='builtins'
        return super().find_class(module,name)

GEOM_RE=re.compile(r'cid:\s*(\d+), volume:\s*([^,]+), center:\s*\[([^\]]+)\]')

def load(repo):
    raw=subprocess.check_output(['git','-C',str(repo),'show','HEAD:stateAnalysis/FM1_dtissue.tis'])
    obj=CompatUnpickler(io.BytesIO(raw),encoding='latin1').load()
    layers=runpy.run_path(str(repo/'common/common/L1L2_cells_ids.py'))
    return obj,layers

def genes(repo,h):
    rows=(repo/f'data/geneExpression/t_{h}h.txt').read_text().splitlines()
    return {int(r.split()[0]):np.array(r.split()[1:],float) for r in rows[1:]}

def geometry(repo,h):
    out={}
    for line in (repo/f'data/FM1/tv/{h}h_segmented_tvformat_volume_position.txt').read_text().splitlines():
        m=GEOM_RE.search(line)
        if m: out[int(m.group(1))]=(float(m.group(2)),np.array(m.group(3).split(),float))
    return out

def make_window(repo,obj,h,c,f,l1_only=False,layers=None):
    dt,tps=obj.dtissue,obj.timePoints; idx={t:i for i,t in enumerate(tps)}
    gh,gc=genes(repo,h),genes(repo,c); zh,zc=geometry(repo,h),geometry(repo,c)
    allowed=set(layers[f'L1_{c}h']) if l1_only else set(gc)
    S=[]; Hgeom=[]; Hatlas=[]; y=[]; groups=[]
    for cid in sorted(set(gc)&set(zc)&allowed):
        a=cid
        for k in range(idx[f'{c}h'],idx[f'{h}h'],-1):
            a=dt[tps[k]]['mother'].get(a,-1)
        if a not in gh or a not in zh: continue
        ds=[cid]
        for k in range(idx[f'{c}h'],idx[f'{f}h']):
            ds=[x for q in ds for x in dt[tps[k]].get('daughters',{}).get(q,[])]
        vf=sum(dt[f'{f}h']['volumes'].get(d,0) for d in ds)
        if not ds or vf<=0: continue
        S.append(np.r_[math.log(zc[cid][0]),zc[cid][1],gc[cid]])
        Hgeom.append(np.r_[math.log(zh[a][0]),zh[a][1]])
        Hatlas.append(gh[a]); y.append(math.log(vf/zc[cid][0])); groups.append(a)
    return map(np.array,(S,Hgeom,Hatlas,y,groups))

def nested_ridge(X,y,g,splits):
    pred=np.empty(len(y))
    for tr,te in splits:
        grid=GridSearchCV(Pipeline([('s',StandardScaler()),('r',Ridge())]),{'r__alpha':[.1,1,10,100]},cv=GroupKFold(3),scoring='r2',n_jobs=-1)
        grid.fit(X[tr],y[tr],groups=g[tr]); pred[te]=grid.predict(X[te])
    return r2_score(y,pred)

def forest_score(X,y,g,splits,kind='rf',leaf=8):
    pred=np.empty(len(y))
    for tr,te in splits:
        if kind=='extra': m=ExtraTreesRegressor(n_estimators=250,min_samples_leaf=leaf,max_features=.7,random_state=17,n_jobs=-1)
        else: m=RandomForestRegressor(n_estimators=250,min_samples_leaf=leaf,max_features=.7,random_state=17,n_jobs=-1)
        m.fit(X[tr],y[tr]); pred[te]=m.predict(X[te])
    return r2_score(y,pred)

def sweep(repo,obj,layers):
    for l1 in [False,True]:
        print('L1' if l1 else 'ALL')
        for h,c,f in [(10,40,96),(40,96,120),(96,120,132)]:
            S,Hg,Ha,y,g=make_window(repo,obj,h,c,f,l1,layers); X=np.c_[S,Hg,Ha]; splits=list(GroupKFold(5).split(S,y,g))
            r0,r1=nested_ridge(S,y,g,splits),nested_ridge(X,y,g,splits); q0,q1=forest_score(S,y,g,splits,leaf=5 if l1 else 8),forest_score(X,y,g,splits,leaf=5 if l1 else 8)
            print(f'{h}->{c}->{f} n={len(y)} groups={len(np.unique(g))} ridge={r0:.4f}->{r1:.4f} delta={r1-r0:+.4f} rf={q0:.4f}->{q1:.4f} delta={q1-q0:+.4f}')

def middle_decomposition(repo,obj,layers):
    S,Hg,Ha,y,g=make_window(repo,obj,40,96,120,True,layers); splits=list(GroupKFold(5).split(S,y,g)); sets={'current':S,'old_geometry':np.c_[S,Hg],'old_atlas':np.c_[S,Ha],'full':np.c_[S,Hg,Ha]}
    print('MIDDLE_L1_DECOMPOSITION')
    for name,X in sets.items(): print('ridge',name,round(nested_ridge(X,y,g,splits),6))
    for kind in ['rf','extra']:
        print(kind,[(name,round(forest_score(X,y,g,splits,kind=kind,leaf=5),6)) for name,X in sets.items()])
    # fixed-Ridge group-preserving permutation of old atlas
    def fixed(X):
        pred=np.empty(len(y))
        for tr,te in splits:
            m=make_pipeline(StandardScaler(),Ridge(alpha=10));m.fit(X[tr],y[tr]);pred[te]=m.predict(X[te])
        return pred
    base=fixed(S); obs=fixed(np.c_[S,Ha]); dobs=r2_score(y,obs)-r2_score(y,base)
    u=np.unique(g); hv={z:Ha[np.where(g==z)[0][0]] for z in u}; rng=np.random.default_rng(20260829); null=[]
    for _ in range(200):
        perm=rng.permutation(u); mp={z:hv[p] for z,p in zip(u,perm)}; Hp=np.vstack([mp[z] for z in g]); q=fixed(np.c_[S,Hp]);null.append(r2_score(y,q)-r2_score(y,base))
    null=np.array(null); p=(1+np.sum(null>=dobs))/(len(null)+1)
    print('old_atlas_permutation observed_delta',round(dobs,6),'null95',round(float(np.quantile(null,.95)),6),'p',round(float(p),6))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--upstream',default='refahi_diag');args=ap.parse_args();repo=Path(args.upstream);obj,layers=load(repo);sweep(repo,obj,layers);middle_decomposition(repo,obj,layers)
if __name__=='__main__':main()
