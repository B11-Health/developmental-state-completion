from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

BASE=Path(__file__).parent
FEATURES=['mean_cx','mean_cy','mean_sx','mean_sy','mean_covxy','mean_entropy','mean_occupancy','mean_edge']
TIMES=[9,13,17,21,25,29,33,37,41]
TRAIN=['DS0004','DS0005']; PRIMARY='DS0007'
MODELS={
 'ridge': Ridge(alpha=10.0),
 'random_forest': RandomForestRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.8,random_state=20260830,n_jobs=-1),
 'extra_trees': ExtraTreesRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.9,random_state=20260830,n_jobs=-1),
}

def load(ds):
    d=pd.read_csv(BASE/f'{ds}_preview_features.csv').set_index('time_index')
    rows=[]
    for t in TIMES:
        rows.append({'ds':ds,'t':t,'H':d.loc[t-8,FEATURES].to_numpy(float),'S':d.loc[t,FEATURES].to_numpy(float),'Y':d.loc[t+8,FEATURES].to_numpy(float)})
    return rows

def stack(rows,key): return np.stack([r[key] for r in rows])
def score(Y,P,naive):
    sse=float(np.sum((Y-P)**2)); sse0=float(np.sum((Y-naive)**2));
    return {'r2_vector':1.0-sse/sse0,'rmse_vector':float(np.sqrt(np.mean((Y-P)**2))),'naive_rmse_vector':float(np.sqrt(np.mean((Y-naive)**2)))}

def main():
    tr=sum([load(x) for x in TRAIN],[]); te=load(PRIMARY)
    Xs=stack(tr,'S'); Xh=stack(tr,'H'); Y=stack(tr,'Y'); Xst=stack(te,'S'); Xht=stack(te,'H'); Yt=stack(te,'Y')
    sx=StandardScaler().fit(Xs); hx=StandardScaler().fit(Xh); yy=StandardScaler().fit(Y)
    S=sx.transform(Xs); H=hx.transform(Xh); T=sx.transform(Xst); HT=hx.transform(Xht); Z=yy.transform(Y); Zt=yy.transform(Yt); naive=np.zeros_like(Zt)
    rows=[]
    for name,m0 in MODELS.items():
        m=clone(m0).fit(S,Z); q=score(Zt,m.predict(T),naive); q.update({'estimator':name,'s_fold_pass':bool(q['r2_vector']>0 and q['rmse_vector']<q['naive_rmse_vector'])}); rows.append(q)
    gate1=sum(x['s_fold_pass'] for x in rows)>=2
    out={'training_embryos':TRAIN,'primary_validation':PRIMARY,'n_train_rows':len(tr),'n_test_rows':len(te),'features':FEATURES,'times':TIMES,'gate1_pass':gate1,'s_only':rows}
    if gate1:
        hist=[]
        for name,m0 in MODELS.items():
            ms=clone(m0).fit(S,Z); mh=clone(m0).fit(np.c_[S,H],Z)
            ss=score(Zt,ms.predict(T),naive); sh=score(Zt,mh.predict(np.c_[T,HT]),naive)
            hist.append({'estimator':name,'r2_s':ss['r2_vector'],'r2_s_plus_h':sh['r2_vector'],'delta_r2_vector':sh['r2_vector']-ss['r2_vector'],'s_plus_h_rmse':sh['rmse_vector'],'naive_rmse':sh['naive_rmse_vector']})
        out['history']=hist
    (BASE/'R15_PRIMARY_RESULT.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
