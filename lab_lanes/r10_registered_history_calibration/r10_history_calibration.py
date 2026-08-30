import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

BASE=Path(__file__).parent; ROOT=BASE.parents[1]
R8=ROOT/'lab_lanes'/'r8_morphology_intensity_rescue'/'results'; OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)
SEED=20260830; OUTCOME='future_radial_velocity'
HISTORY=['old_speed_relcentroid','old_radial_relcentroid','old_tangential_relcentroid','old_log_volume_change_rate']
MODELS={
 'random_forest': RandomForestRegressor(n_estimators=300,min_samples_leaf=4,max_features=0.8,random_state=SEED,n_jobs=-1),
 'extra_trees': ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,max_features=0.9,random_state=SEED,n_jobs=-1),
}

def pct(X): return pd.DataFrame(X).rank(axis=0,method='average',pct=True).to_numpy(float)
def score(y,p): return {'r2':float(r2_score(y,p)),'rmse':float(math.sqrt(mean_squared_error(y,p)))}

def load():
    A=pd.read_csv(R8/'tribolium_analysis_table.csv'); A['sequence']=A.sequence.map(lambda v:f'{int(v):02d}')
    schema=json.loads((R8/'feature_schema.json').read_text(encoding='utf-8')); cols=schema['Tribolium']['full_cols']
    S=A[cols].to_numpy(float); H=A[HISTORY].to_numpy(float); groups=A.sequence.to_numpy(); y=A[OUTCOME].to_numpy(float)
    Sr=np.zeros_like(S); Hr=np.zeros_like(H)
    for seq in sorted(A.sequence.unique()):
        q=groups==seq; Sr[q]=pct(S[q]); Hr[q]=pct(H[q])
    return A,cols,Sr,Hr,groups,y

def fit_pair(S,H,y,groups):
    rows=[]
    for test_seq in sorted(np.unique(groups)):
        tr=groups!=test_seq; te=groups==test_seq; naive=np.full(te.sum(),float(y[tr].mean())); ns=score(y[te],naive)
        for name,m0 in MODELS.items():
            ms=clone(m0).fit(S[tr],y[tr]); mh=clone(m0).fit(np.c_[S[tr],H[tr]],y[tr])
            ps=ms.predict(S[te]); ph=mh.predict(np.c_[S[te],H[te]]); ss=score(y[te],ps); sh=score(y[te],ph)
            rows.append({'test_sequence':test_seq,'estimator':name,'r2_s':ss['r2'],'r2_s_plus_h':sh['r2'],'delta_r2':sh['r2']-ss['r2'],'rmse_s':ss['rmse'],'rmse_s_plus_h':sh['rmse'],'naive_rmse':ns['rmse'],'s_fold_pass':bool(ss['r2']>0 and ss['rmse']<ns['rmse']),'sh_fold_pass':bool(sh['r2']>0 and sh['rmse']<ns['rmse'])})
    return pd.DataFrame(rows)

def gate2(df):
    good=[]
    for name in MODELS:
        z=df[df.estimator==name].sort_values('test_sequence')
        ok=len(z)==2 and (z.delta_r2>0).all() and z.delta_r2.mean()>=.02 and z.sh_fold_pass.all()
        if ok: good.append(name)
    return {'gate2_pass':len(good)==2,'estimators_passing':good,'per_model_mean_delta':{n:float(df[df.estimator==n].delta_r2.mean()) for n in MODELS},'s_adequacy_preserved':all(df[df.estimator==n].s_fold_pass.all() for n in MODELS)}

def observed():
    A,cols,S,H,g,y=load(); df=fit_pair(S,H,y,g); dec=gate2(df); df.to_csv(OUT/'observed_history_metrics.csv',index=False); (OUT/'observed_decision.json').write_text(json.dumps(dec,indent=2),encoding='utf-8'); print(json.dumps(dec,indent=2))

def perm_job(start,count):
    A,cols,S,H,g,y=load(); base={}; naive={}
    for test_seq in sorted(np.unique(g)):
        tr=g!=test_seq; te=g==test_seq; nv=np.full(te.sum(),float(y[tr].mean())); naive[test_seq]=score(y[te],nv)
        for name,m0 in MODELS.items():
            m=clone(m0).fit(S[tr],y[tr]); base[(test_seq,name)]=score(y[te],m.predict(S[te]))
    rows=[]; reps=[]
    for rep in range(start,start+count):
        rrows=[]
        for fold_i,test_seq in enumerate(sorted(np.unique(g))):
            tr=g!=test_seq; te=g==test_seq; rng=np.random.RandomState(SEED+rep*1000+fold_i); Htr=H[tr][rng.permutation(tr.sum())]; Hte=H[te][rng.permutation(te.sum())]
            for name,m0 in MODELS.items():
                mh=clone(m0).fit(np.c_[S[tr],Htr],y[tr]); sh=score(y[te],mh.predict(np.c_[S[te],Hte])); ss=base[(test_seq,name)]; ns=naive[test_seq]
                q={'replicate':rep,'test_sequence':test_seq,'estimator':name,'r2_s':ss['r2'],'r2_s_plus_h':sh['r2'],'delta_r2':sh['r2']-ss['r2'],'rmse_s':ss['rmse'],'rmse_s_plus_h':sh['rmse'],'naive_rmse':ns['rmse'],'s_fold_pass':bool(ss['r2']>0 and ss['rmse']<ns['rmse']),'sh_fold_pass':bool(sh['r2']>0 and sh['rmse']<ns['rmse'])}; rows.append(q); rrows.append(q)
        reps.append({'replicate':rep,**gate2(pd.DataFrame(rrows))})
    pd.DataFrame(rows).to_csv(OUT/f'perm_metrics_{start:03d}_{start+count-1:03d}.csv',index=False); (OUT/f'perm_decisions_{start:03d}_{start+count-1:03d}.json').write_text(json.dumps(reps,indent=2),encoding='utf-8'); print(json.dumps({'start':start,'count':count,'null_gate2_passes':sum(x['gate2_pass'] for x in reps)},indent=2))

def cal_job(start,count):
    A,cols,S,H,g,y=load(); rows=[]; reps=[]; ysd=float(np.std(y))
    for rep in range(start,start+count):
        rng=np.random.RandomState(SEED+500000+rep); w=rng.normal(size=H.shape[1]); w=w/np.linalg.norm(w); z=H@w; rz=Ridge(alpha=1.0).fit(S,z); hres=z-rz.predict(S); sd=float(np.std(hres)); hres=hres/(sd if sd>1e-12 else 1.0); ys=y+0.30*ysd*hres
        df=fit_pair(S,H,ys,g); dec=gate2(df); dec['replicate']=rep; dec['injected_scale_target_sd']=0.30; dec['success']=bool(dec['gate2_pass'] and dec['s_adequacy_preserved']); reps.append(dec); q=df.copy(); q['replicate']=rep; q['injected_scale_target_sd']=0.30; rows.append(q)
    pd.concat(rows,ignore_index=True).to_csv(OUT/f'cal_metrics_{start:03d}_{start+count-1:03d}.csv',index=False); (OUT/f'cal_decisions_{start:03d}_{start+count-1:03d}.json').write_text(json.dumps(reps,indent=2),encoding='utf-8'); print(json.dumps({'start':start,'count':count,'successes':sum(x['success'] for x in reps)},indent=2))

def aggregate():
    obs=pd.read_csv(OUT/'observed_history_metrics.csv'); od=json.loads((OUT/'observed_decision.json').read_text())
    pfiles=sorted(OUT.glob('perm_metrics_*.csv')); pdfiles=sorted(OUT.glob('perm_decisions_*.json')); cfiles=sorted(OUT.glob('cal_metrics_*.csv')); cdfiles=sorted(OUT.glob('cal_decisions_*.json'))
    P=pd.concat([pd.read_csv(x) for x in pfiles],ignore_index=True); C=pd.concat([pd.read_csv(x) for x in cfiles],ignore_index=True); pdx=[]; cdx=[]
    for f in pdfiles: pdx.extend(json.loads(f.read_text()))
    for f in cdfiles: cdx.extend(json.loads(f.read_text()))
    P.to_csv(OUT/'permutation_null_metrics.csv',index=False); C.to_csv(OUT/'calibration_metrics.csv',index=False); pd.DataFrame(pdx).to_json(OUT/'permutation_null_decisions.json',orient='records',indent=2); pd.DataFrame(cdx).to_json(OUT/'calibration_decisions.json',orient='records',indent=2)
    null_rate=float(np.mean([x['gate2_pass'] for x in pdx])); power=float(np.mean([x['success'] for x in cdx])); result={'observed':od,'permutation_replicates':len(pdx),'permutation_gate2_false_positive_rate':null_rate,'calibration_replicates':len(cdx),'injected_history_scale_target_sd':0.30,'calibration_success_rate':power,'calibration_success_count':int(sum(x['success'] for x in cdx)),'calibration_required_count_for_80pct':24,'calibration_power_pass':bool(sum(x['success'] for x in cdx)>=24),'history_interpretation':('stable_positive' if od['gate2_pass'] and null_rate<=0.10 else ('weak_or_null_with_adequate_power' if (not od['gate2_pass'] and sum(x['success'] for x in cdx)>=24) else 'unresolved'))}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['observed','perm','cal','aggregate'],required=True); ap.add_argument('--start',type=int,default=0); ap.add_argument('--count',type=int,default=10); a=ap.parse_args()
    if a.mode=='observed': observed()
    elif a.mode=='perm': perm_job(a.start,a.count)
    elif a.mode=='cal': cal_job(a.start,a.count)
    else: aggregate()
