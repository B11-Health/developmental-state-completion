from __future__ import annotations
import json, math, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'source_data'
RESULTS=ROOT/'results'; RESULTS.mkdir(exist_ok=True)
S_COLS=['start','depth','embryo_code']
H_COLS=['parent_duration','grandparent_duration','parent_minus_grandparent']

def load_rows():
    out=[]
    for embryo in ['01','02']:
        df=pd.read_csv(DATA/f'{embryo}_man_track.txt',sep=r'\s+',names=['id','start','end','parent'])
        rec={int(r.id):r for r in df.itertuples(index=False)}
        children={i:[] for i in rec}
        for r in df.itertuples(index=False):
            if r.parent in children: children[int(r.parent)].append(int(r.id))
        depth={}
        def dep(i):
            if i in depth:return depth[i]
            p=int(rec[i].parent); depth[i]=0 if p==0 else dep(p)+1; return depth[i]
        def ancestor_at(i,target_depth):
            j=i
            while dep(j)>target_depth:
                j=int(rec[j].parent)
            return j
        for i,r in rec.items():
            if len(children[i])!=2: continue
            p=int(r.parent)
            if p==0 or p not in rec: continue
            gp=int(rec[p].parent)
            if gp==0 or gp not in rec: continue
            d=dep(i)
            if d<2: continue
            pdur=int(rec[p].end-rec[p].start+1); gdur=int(rec[gp].end-rec[gp].start+1)
            out.append(dict(embryo=embryo,embryo_code=int(embryo)-1,id=i,start=int(r.start),end=int(r.end),duration=int(r.end-r.start+1),depth=d,parent=p,grandparent=gp,parent_duration=pdur,grandparent_duration=gdur,parent_minus_grandparent=pdur-gdur,group_depth2=f'{embryo}:{ancestor_at(i,2)}',group_depth1=f'{embryo}:{ancestor_at(i,1)}'))
    return pd.DataFrame(out).sort_values(['embryo','id']).reset_index(drop=True)

def models(seed):
    return {
      'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10.0)),
      'random_forest':RandomForestRegressor(n_estimators=120,min_samples_leaf=4,max_features=1.0,random_state=seed,n_jobs=-1),
      'hist_gb':HistGradientBoostingRegressor(max_iter=160,learning_rate=0.05,max_leaf_nodes=15,min_samples_leaf=10,l2_regularization=1.0,random_state=seed)
    }

def split_indices(groups,n=100,test_size=.25,offset=0):
    X=np.zeros((len(groups),1)); idx=np.arange(len(groups))
    for k in range(n):
        g=GroupShuffleSplit(n_splits=1,test_size=test_size,random_state=offset+k)
        tr,te=next(g.split(X,groups=groups)); yield k,tr,te

def eval_outcome(df,y,group_col='group_depth2',n_splits=100,offset=1000):
    rows=[]
    for k,tr,te in split_indices(df[group_col].to_numpy(),n_splits,.25,offset):
        tr_groups=set(df.iloc[tr][group_col]); te_groups=set(df.iloc[te][group_col])
        if tr_groups & te_groups: raise RuntimeError('group leakage')
        for name,m in models(5000+k).items():
            vals={}
            for label,cols in [('S',S_COLS),('SH',S_COLS+H_COLS)]:
                mm=clone(m); mm.fit(df.iloc[tr][cols],y[tr]); pred=mm.predict(df.iloc[te][cols])
                vals[label]=(r2_score(y[te],pred),mean_absolute_error(y[te],pred))
            rows.append(dict(split=k,estimator=name,r2_s=vals['S'][0],r2_sh=vals['SH'][0],delta_r2=vals['SH'][0]-vals['S'][0],mae_s=vals['S'][1],mae_sh=vals['SH'][1],delta_mae=vals['SH'][1]-vals['S'][1],n_train=len(tr),n_test=len(te),train_groups=len(tr_groups),test_groups=len(te_groups),group_overlap=0))
    return pd.DataFrame(rows)

def summarize(ev):
    return ev.groupby('estimator').agg(n_splits=('split','nunique'),median_r2_s=('r2_s','median'),median_r2_sh=('r2_sh','median'),median_delta_r2=('delta_r2','median'),q025_delta_r2=('delta_r2',lambda x:np.quantile(x,.025)),q975_delta_r2=('delta_r2',lambda x:np.quantile(x,.975)),positive_fraction=('delta_r2',lambda x:np.mean(x>0)),gt_002_fraction=('delta_r2',lambda x:np.mean(x>.02)),median_mae_s=('mae_s','median'),median_mae_sh=('mae_sh','median')).reset_index()

def calibration(df,n_sim=200):
    Xs=df[S_COLS].to_numpy(float); yh=df.duration.to_numpy(float)
    base_model=make_pipeline(StandardScaler(),Ridge(alpha=10.0)).fit(Xs,yh)
    base=base_model.predict(Xs); sigma=float(np.std(yh-base,ddof=1))
    h=df[['parent_duration']].to_numpy(float)
    hres=h-make_pipeline(StandardScaler(),Ridge(alpha=1.0)).fit(Xs,h).predict(Xs)
    hres=(hres[:,0]-hres[:,0].mean())/(hres[:,0].std(ddof=1)+1e-12)
    splits=list(split_indices(df.group_depth2.to_numpy(),100,.25,7000))
    rows=[]
    for sim in range(n_sim):
        rng=np.random.default_rng(90000+sim); noise=rng.normal(0,sigma,len(df)); yc=base+noise
        target_sd=float(np.std(yc,ddof=1)); yi=yc+0.30*target_sd*hres
        k,tr,te=splits[sim%len(splits)]
        for outcome,y in [('complete',yc),('incomplete',yi)]:
            for name,m in models(200000+sim).items():
                rs=[]
                for cols in [S_COLS,S_COLS+H_COLS]:
                    mm=clone(m); mm.fit(df.iloc[tr][cols],y[tr]); rs.append(r2_score(y[te],mm.predict(df.iloc[te][cols])))
                rows.append(dict(sim=sim,split=k,outcome=outcome,estimator=name,delta_r2=rs[1]-rs[0]))
    cal=pd.DataFrame(rows)
    cut=cal[cal.outcome=='complete'].groupby('estimator').delta_r2.quantile(.95).rename('complete_p95')
    power=cal[cal.outcome=='incomplete'].join(cut,on='estimator').assign(hit=lambda x:x.delta_r2>x.complete_p95).groupby('estimator').hit.mean().rename('incomplete_power')
    summary=pd.concat([cut,power],axis=1).reset_index(); summary['n_sim']=n_sim; summary['history_effect_target_sd']=0.30; summary['noise_sd']=sigma
    return cal,summary

def permutation_check(df):
    rng=np.random.default_rng(314159); yp=rng.permutation(df.duration.to_numpy(float))
    ev=eval_outcome(df,yp,'group_depth2',30,30000); return summarize(ev)

def main():
    df=load_rows(); df.to_csv(RESULTS/'analysis_rows.csv',index=False)
    y=df.duration.to_numpy(float)
    ev=eval_outcome(df,y); ev.to_csv(RESULTS/'grouped_split_results.csv',index=False); sm=summarize(ev); sm.to_csv(RESULTS/'summary.csv',index=False)
    strict=eval_outcome(df,y,'group_depth1',100,12000); strict.to_csv(RESULTS/'depth1_group_sensitivity.csv',index=False); summarize(strict).to_csv(RESULTS/'depth1_group_summary.csv',index=False)
    noemb=df.copy(); noemb['embryo_code']=0
    ne=eval_outcome(noemb,y,'group_depth2',100,22000); summarize(ne).to_csv(RESULTS/'no_embryo_indicator_summary.csv',index=False)
    cal,cals=calibration(df,200); cal.to_csv(RESULTS/'calibration_split_results.csv',index=False); cals.to_csv(RESULTS/'calibration_summary.csv',index=False)
    perm=permutation_check(df); perm.to_csv(RESULTS/'permutation_summary.csv',index=False)
    merged=sm.merge(cals,on='estimator'); merged['criterion_median_gt_002']=merged.median_delta_r2>.02; merged['criterion_positive_ge_080']=merged.positive_fraction>=.80; merged['criterion_above_complete_p95']=merged.median_delta_r2>merged.complete_p95; merged['criterion_power_ge_080']=merged.incomplete_power>=.80; merged['all_estimator_conditions']=merged[['criterion_median_gt_002','criterion_positive_ge_080','criterion_above_complete_p95','criterion_power_ge_080']].all(axis=1)
    stable=int(merged.all_estimator_conditions.sum())>=2; merged.to_csv(RESULTS/'decision_table.csv',index=False)
    meta={'n_rows':len(df),'embryos':df.embryo.value_counts().to_dict(),'groups_depth2':int(df.group_depth2.nunique()),'groups_depth1':int(df.group_depth1.nunique()),'duration_mean':float(df.duration.mean()),'duration_sd':float(df.duration.std()),'stable_residual_history_rule_met':stable,'estimators_meeting_all_conditions':merged.loc[merged.all_estimator_conditions,'estimator'].tolist(),'feature_audit':{'S':S_COLS,'H':H_COLS,'Y':'duration','forbidden':['end','id','parent id','grandparent id','children/future descendant timing']}}
    (RESULTS/'run_metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print(sm.to_string(index=False)); print('\nCALIBRATION\n',cals.to_string(index=False)); print('\nDECISION\n',merged.to_string(index=False)); print('\nMETA\n',json.dumps(meta,indent=2))
if __name__=='__main__': main()
