from pathlib import Path
import json, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.base import clone
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'lab_lanes'/'r15_slice1_multiacquisition'
F=['mean_cx','mean_cy','mean_sx','mean_sy','mean_covxy','mean_entropy','mean_occupancy','mean_edge']; T=[9,13,17,21,25,29,33,37,41]
MODELS={'ridge':Ridge(alpha=10.0),'random_forest':RandomForestRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.8,random_state=20260830,n_jobs=-1),'extra_trees':ExtraTreesRegressor(n_estimators=500,min_samples_leaf=2,max_features=0.9,random_state=20260830,n_jobs=-1)}
def rows(ds):
 d=pd.read_csv(SRC/f'{ds}_preview_features.csv').set_index('time_index'); return [(d.loc[t-8,F].to_numpy(float),d.loc[t,F].to_numpy(float),d.loc[t+8,F].to_numpy(float)) for t in T]
def score(y,p):
 naive=np.zeros_like(y); sse=((y-p)**2).sum(); sse0=((y-naive)**2).sum(); return float(1-sse/sse0),float(np.sqrt(np.mean((y-p)**2))),float(np.sqrt(np.mean((y-naive)**2)))
def run(test):
 tr=rows('DS0004')+rows('DS0005'); te=rows(test)
 H=np.stack([x[0] for x in tr]);S=np.stack([x[1] for x in tr]);Y=np.stack([x[2] for x in tr]);Ht=np.stack([x[0] for x in te]);St=np.stack([x[1] for x in te]);Yt=np.stack([x[2] for x in te])
 ss=StandardScaler().fit(S); hs=StandardScaler().fit(H); ys=StandardScaler().fit(Y); S=ss.transform(S);St=ss.transform(St);H=hs.transform(H);Ht=hs.transform(Ht);Y=ys.transform(Y);Yt=ys.transform(Yt)
 out=[]; hist=[]
 for n,m0 in MODELS.items():
  m=clone(m0).fit(S,Y); r,rm,nm=score(Yt,m.predict(St)); out.append({'estimator':n,'r2_vector':r,'rmse_vector':rm,'naive_rmse_vector':nm,'pass':r>0 and rm<nm})
  mh=clone(m0).fit(np.c_[S,H],Y); rh,rmh,nmh=score(Yt,mh.predict(np.c_[St,Ht])); hist.append({'estimator':n,'r2_s':r,'r2_sh':rh,'delta':rh-r})
 return {'test':test,'gate1':sum(x['pass'] for x in out)>=2,'s_only':out,'history':hist}
res={'primary':run('DS0007'),'secondary':run('DS0035')}
# structural checks
res['structure']={ds:{'rows':len(pd.read_csv(SRC/f'{ds}_preview_features.csv')),'time_min':int(pd.read_csv(SRC/f'{ds}_preview_features.csv').time_index.min()),'time_max':int(pd.read_csv(SRC/f'{ds}_preview_features.csv').time_index.max())} for ds in ['DS0004','DS0005','DS0007','DS0035']}
# compare to committed JSON
p0=json.loads((SRC/'R15_PRIMARY_RESULT.json').read_text()); p1=json.loads((SRC/'R15_SECONDARY_RESULT.json').read_text())
res['matches']={'primary_gate':res['primary']['gate1']==p0['gate1_pass'],'secondary_gate':res['secondary']['gate1']==p1['gate1_pass'],'primary_r2_max_abs':max(abs(a['r2_vector']-b['r2_vector']) for a,b in zip(res['primary']['s_only'],p0['s_only'])),'secondary_r2_max_abs':max(abs(a['r2_vector']-b['r2_vector']) for a,b in zip(res['secondary']['s_only'],p1['s_only'])),'primary_delta_max_abs':max(abs(a['delta']-b['delta_r2_vector']) for a,b in zip(res['primary']['history'],p0['history'])),'secondary_delta_max_abs':max(abs(a['delta']-b['delta_r2_vector']) for a,b in zip(res['secondary']['history'],p1['history']))}
(Path(__file__).parent/'RECOMPUTED.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
