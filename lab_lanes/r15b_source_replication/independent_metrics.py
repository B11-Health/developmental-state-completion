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
TRAIN=['DS0004','DS0005']
MODELS={
 'ridge':Ridge(alpha=10.0),
 'random_forest':RandomForestRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.8,random_state=20260830,n_jobs=-1),
 'extra_trees':ExtraTreesRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.9,random_state=20260830,n_jobs=-1),
}

def windows(ds):
    d=pd.read_csv(BASE/'derived'/f'{ds}_preview_features_independent.csv').set_index('time_index')
    return [{'ds':ds,'t':t,
             'H':d.loc[t-8,FEATURES].to_numpy(float),
             'S':d.loc[t,FEATURES].to_numpy(float),
             'Y':d.loc[t+8,FEATURES].to_numpy(float)} for t in TIMES]

def stack(rows,key): return np.stack([r[key] for r in rows])

def score(y,p,naive):
    sse=float(np.sum((y-p)**2)); sse0=float(np.sum((y-naive)**2))
    return {'r2_vector':1.0-sse/sse0,
            'rmse_vector':float(np.sqrt(np.mean((y-p)**2))),
            'naive_rmse_vector':float(np.sqrt(np.mean((y-naive)**2)))}

def evaluate(test,kind):
    tr=sum((windows(ds) for ds in TRAIN),[]); te=windows(test)
    xs=stack(tr,'S'); xh=stack(tr,'H'); y=stack(tr,'Y')
    xst=stack(te,'S'); xht=stack(te,'H'); yt=stack(te,'Y')
    sx=StandardScaler().fit(xs); hx=StandardScaler().fit(xh); yy=StandardScaler().fit(y)
    S=sx.transform(xs); H=hx.transform(xh); Z=yy.transform(y)
    T=sx.transform(xst); HT=hx.transform(xht); Zt=yy.transform(yt); naive=np.zeros_like(Zt)
    srows=[]
    for name,m0 in MODELS.items():
        pred=clone(m0).fit(S,Z).predict(T); q=score(Zt,pred,naive)
        q['estimator']=name; q['s_fold_pass']=bool(q['r2_vector']>0.0 and q['rmse_vector']<q['naive_rmse_vector'])
        srows.append(q)
    gate=sum(int(r['s_fold_pass']) for r in srows)>=2
    hrows=[]
    if gate:
        for name,m0 in MODELS.items():
            ms=clone(m0).fit(S,Z); mh=clone(m0).fit(np.c_[S,H],Z)
            qs=score(Zt,ms.predict(T),naive); qh=score(Zt,mh.predict(np.c_[T,HT]),naive)
            hrows.append({'estimator':name,'r2_s':qs['r2_vector'],'r2_s_plus_h':qh['r2_vector'],
                          'delta_r2_vector':qh['r2_vector']-qs['r2_vector'],
                          's_plus_h_rmse':qh['rmse_vector'],'naive_rmse':qh['naive_rmse_vector']})
    out={'training_embryos':TRAIN,'gate1_pass':gate,'s_only':srows,'history':hrows}
    if kind=='primary':
        out.update({'primary_validation':test,'n_train_rows':len(tr),'n_test_rows':len(te),'features':FEATURES,'times':TIMES})
    else:
        out.update({'secondary_validation':test,'marker_domain':'Lamin #4'})
    return out

if __name__=='__main__':
    out={'primary':evaluate('DS0007','primary'),'secondary':evaluate('DS0035','secondary')}
    (BASE/'INDEPENDENT_METRICS.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
