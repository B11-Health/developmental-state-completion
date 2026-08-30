import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
R8=ROOT/'lab_lanes'/'r8_morphology_intensity_rescue'/'results'
R12=ROOT/'lab_lanes'/'r12_domain_balanced_calibration'
R10B=ROOT/'lab_lanes'/'r10b_seed_remediation'
SEED=20260830
HISTORY=['old_speed_relcentroid','old_radial_relcentroid','old_tangential_relcentroid','old_log_volume_change_rate']
MODELS={
 'random_forest':RandomForestRegressor(n_estimators=300,min_samples_leaf=4,max_features=0.8,random_state=SEED,n_jobs=-1),
 'extra_trees':ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,max_features=0.9,random_state=SEED,n_jobs=-1),
}

def pct(x):
    return pd.DataFrame(x).rank(axis=0,method='average',pct=True).to_numpy(float)

def load_raw():
    A=pd.read_csv(R8/'tribolium_analysis_table.csv')
    A['sequence']=A.sequence.map(lambda v:f'{int(v):02d}')
    schema=json.loads((R8/'feature_schema.json').read_text(encoding='utf-8'))
    cols=schema['Tribolium']['full_cols']
    S=A[cols].to_numpy(float); H=A[HISTORY].to_numpy(float); g=A.sequence.to_numpy(); y=A.future_radial_velocity.to_numpy(float)
    Sr=np.zeros_like(S); Hr=np.zeros_like(H)
    for seq in sorted(np.unique(g)):
        q=g==seq; Sr[q]=pct(S[q]); Hr[q]=pct(H[q])
    return Sr,Hr,g,y

def within(v,g):
    out=np.zeros_like(v,float)
    for seq in sorted(np.unique(g)):
        q=g==seq; x=v[q]; out[q]=(x-x.mean())/(x.std() if x.std()>1e-12 else 1.0)
    return out

def hidden(rep,geometry,S,H,g):
    rng=np.random.RandomState(SEED+rep)
    w=rng.normal(size=H.shape[1]); w/=np.linalg.norm(w)
    z=H@w
    if geometry=='domain_balanced':
        raw=z-Ridge(alpha=1.0).fit(S,z).predict(S)
        return within(raw,g)
    if geometry=='domainwise_residualizer':
        raw=np.zeros_like(z,float)
        for seq in sorted(np.unique(g)):
            q=g==seq; raw[q]=z[q]-Ridge(alpha=1.0).fit(S[q],z[q]).predict(S[q])
        return within(raw,g)
    if geometry=='r10b':
        raw=z-Ridge(alpha=1.0).fit(S,z).predict(S)
        sd=raw.std(); return raw/(sd if sd>1e-12 else 1.0)
    raise ValueError(geometry)

def score(y,p):
    return float(r2_score(y,p)),float(math.sqrt(mean_squared_error(y,p)))

def fit_pair(S,H,y,g):
    rows=[]
    for test_seq in sorted(np.unique(g)):
        tr=g!=test_seq; te=g==test_seq
        naive=np.full(te.sum(),float(y[tr].mean())); _,nrmse=score(y[te],naive)
        for name,m0 in MODELS.items():
            ms=clone(m0).fit(S[tr],y[tr]); mh=clone(m0).fit(np.c_[S[tr],H[tr]],y[tr])
            r2s,rmses=score(y[te],ms.predict(S[te])); r2h,rmseh=score(y[te],mh.predict(np.c_[S[te],H[te]]))
            rows.append({'test_sequence':test_seq,'estimator':name,'r2_s':r2s,'r2_s_plus_h':r2h,'delta_r2':r2h-r2s,'rmse_s':rmses,'rmse_s_plus_h':rmseh,'naive_rmse':nrmse,'s_fold_pass':bool(r2s>0 and rmses<nrmse),'sh_fold_pass':bool(r2h>0 and rmseh<nrmse)})
    return pd.DataFrame(rows)

def decision(df):
    gate=True
    for name in MODELS:
        z=df[df.estimator==name].sort_values('test_sequence')
        gate &= len(z)==2 and bool((z.delta_r2>0).all()) and float(z.delta_r2.mean())>=0.02 and bool(z.sh_fold_pass.all())
    adequacy=all(bool(df[df.estimator==name].s_fold_pass.all()) for name in MODELS)
    return {'gate2_pass':bool(gate),'s_adequacy_preserved':bool(adequacy),'success':bool(gate and adequacy)}

def load_decisions(prefix):
    xs=[]
    for f in sorted((R12/'results').glob(prefix+'_decisions_*.json')): xs.extend(json.loads(f.read_text(encoding='utf-8')))
    return xs

def load_metrics(prefix):
    return pd.concat([pd.read_csv(f) for f in sorted((R12/'results').glob(prefix+'_metrics_*.csv'))],ignore_index=True)

def main():
    S,H,g,y=load_raw(); ysd=float(np.std(y))
    pri=load_decisions('domain_balanced'); sec=load_decisions('domainwise_residualizer')
    ref=[]
    for f in sorted((R10B/'results').glob('decisions_*.json')): ref.extend(json.loads(f.read_text(encoding='utf-8')))
    out={'ysd':ysd,'n_rows':len(y),'domains':sorted(set(g.tolist())),'checks':{},'spot_refits':[]}
    for label,xs in [('primary',pri),('secondary',sec),('r10b',ref)]:
        reps=[int(x['replicate']) for x in xs]
        out['checks'][label]={'n':len(xs),'unique_reps':len(set(reps)),'reps_exact_0_29':sorted(reps)==list(range(30)),'seed_formula_exact':all(int(x.get('direction_seed',SEED+int(x['replicate'])))==SEED+int(x['replicate']) for x in xs),'adequacy':sum(bool(x['s_adequacy_preserved']) for x in xs),'gate2':sum(bool(x['gate2_pass']) for x in xs),'joint':sum(bool(x.get('success',x.get('joint_success',False))) for x in xs),'success_set':sorted(int(x['replicate']) for x in xs if bool(x.get('success',x.get('joint_success',False))))}
    out['checks']['primary_success_set_equals_r10b']=out['checks']['primary']['success_set']==out['checks']['r10b']['success_set']
    out['checks']['secondary_new_vs_r10b']=sorted(set(out['checks']['secondary']['success_set'])-set(out['checks']['r10b']['success_set']))
    out['checks']['secondary_lost_vs_r10b']=sorted(set(out['checks']['r10b']['success_set'])-set(out['checks']['secondary']['success_set']))
    # Independent decision derivation from committed metric rows.
    for prefix,label in [('domain_balanced','primary'),('domainwise_residualizer','secondary')]:
        M=load_metrics(prefix); mism=[]
        for rep in range(30):
            got=decision(M[M.replicate==rep]); d=next(x for x in (pri if label=='primary' else sec) if int(x['replicate'])==rep)
            if got['gate2_pass']!=bool(d['gate2_pass']) or got['s_adequacy_preserved']!=bool(d['s_adequacy_preserved']): mism.append(rep)
        out['checks'][label+'_metric_decision_mismatches']=mism
    # Geometry normalization and pooled scale checks for all directions.
    norm={}
    for geom in ['domain_balanced','domainwise_residualizer','r10b']:
        max_abs_group_mean=0.0; max_abs_group_sd_err=0.0; max_abs_global_sd_err=0.0
        for rep in range(30):
            h=hidden(rep,geom,S,H,g)
            max_abs_global_sd_err=max(max_abs_global_sd_err,abs(float(h.std())-1.0))
            if geom!='r10b':
                for seq in sorted(np.unique(g)):
                    q=g==seq; max_abs_group_mean=max(max_abs_group_mean,abs(float(h[q].mean()))); max_abs_group_sd_err=max(max_abs_group_sd_err,abs(float(h[q].std())-1.0))
        norm[geom]={'max_abs_group_mean':max_abs_group_mean,'max_abs_group_sd_error':max_abs_group_sd_err,'max_abs_global_sd_error':max_abs_global_sd_err}
    out['checks']['normalization']=norm
    # Spot refits chosen to cover stable success, secondary-only gains, and losses vs R10B.
    spots=[('domain_balanced',0),('domain_balanced',3),('domainwise_residualizer',3),('domainwise_residualizer',20),('domainwise_residualizer',28),('r10b',0),('r10b',20)]
    for geom,rep in spots:
        h=hidden(rep,geom,S,H,g); ys=y+0.30*ysd*h; df=fit_pair(S,H,ys,g); dec=decision(df)
        rec={'geometry':geom,'replicate':rep,**dec,'max_abs_metric_diff':None}
        if geom!='r10b':
            M=load_metrics(geom); c=M[M.replicate==rep].sort_values(['test_sequence','estimator']).reset_index(drop=True); z=df.sort_values(['test_sequence','estimator']).reset_index(drop=True)
            cols=['r2_s','r2_s_plus_h','delta_r2','rmse_s','rmse_s_plus_h','naive_rmse']
            rec['max_abs_metric_diff']=max(float(np.max(np.abs(c[col].to_numpy(float)-z[col].to_numpy(float)))) for col in cols)
        else:
            files=sorted((R10B/'results').glob('metrics_*.csv')); M=pd.concat([pd.read_csv(f) for f in files],ignore_index=True); c=M[M.replicate==rep].sort_values(['test_sequence','estimator']).reset_index(drop=True); z=df.sort_values(['test_sequence','estimator']).reset_index(drop=True)
            cols=['r2_s','r2_s_plus_h','delta_r2','rmse_s','rmse_s_plus_h','naive_rmse']
            rec['max_abs_metric_diff']=max(float(np.max(np.abs(c[col].to_numpy(float)-z[col].to_numpy(float)))) for col in cols)
        out['spot_refits'].append(rec)
    (HERE/'audit_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
