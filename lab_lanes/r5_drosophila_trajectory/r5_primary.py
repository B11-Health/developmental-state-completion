import json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error
BASE=Path(__file__).parent; SEED=20260830
files=sorted((BASE/'source_data').glob('dro_centroids_*.csv')); df=pd.concat([pd.read_csv(p) for p in files],ignore_index=True)
frames=[15,20,23,24,25,40]; rows=[]
for (seq,lab),g in df.groupby(['sequence','label']):
 if not set(frames).issubset(set(g.frame)): continue
 b={int(r.frame):r for _,r in g.iterrows()}; rec={'sequence':str(seq).zfill(2),'label':int(lab)}
 for t in frames:
  for c in 'xyz': rec[f'{c}{t}']=float(getattr(b[t],f'{c}_um'))
  rec[f'vol{t}']=float(b[t].voxel_count)
 rows.append(rec)
D=pd.DataFrame(rows)
for c in 'xyz': D[f'{c}25c']=D.groupby('sequence')[f'{c}25'].transform(lambda x:x-x.mean())
rad=np.sqrt((D[['x25c','y25c','z25c']]**2).sum(1)); rms=np.sqrt((rad**2).groupby(D.sequence).transform('mean')).replace(0,1)
for c in 'xyz': D[f'{c}25n']=D[f'{c}25c']/rms
P=lambda t:D[[f'x{t}',f'y{t}',f'z{t}']].to_numpy(float)
p15,p20,p23,p24,p25,p40=[P(t) for t in frames]
vold=(p20-p15)/5; vrecent=p25-p24; acc=p25-2*p24+p23; Y=(p40-p25)/15
lv25=np.log1p(D.vol25.to_numpy())[:,None]; lvr=(np.log1p(D.vol25)-np.log1p(D.vol24)).to_numpy()[:,None]; lvo=(np.log1p(D.vol20)-np.log1p(D.vol15)).to_numpy()[:,None]
pos=D[[f'{c}25n' for c in 'xyz']].to_numpy(float); S0=np.c_[pos,lv25]; S1=np.c_[S0,vrecent,lvr]; S2=np.c_[S1,acc]; H=np.c_[vold,np.linalg.norm(vold,axis=1)[:,None],lvo]; groups=D.sequence.to_numpy()
models={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=1.0)),'random_forest':RandomForestRegressor(n_estimators=80,min_samples_leaf=4,max_features=.8,random_state=SEED,n_jobs=-1),'extra_trees':ExtraTreesRegressor(n_estimators=80,min_samples_leaf=3,max_features=.9,random_state=SEED,n_jobs=-1)}
Ss={'S0_position_volume':S0,'S1_recent_velocity':S1,'S2_recent_acceleration':S2}; rr=[]
for sn,S in Ss.items():
 for mn,m in models.items():
  for test in sorted(set(groups)):
   tr=groups!=test; te=groups==test
   vals=[]
   for tag,X in [('S',S),('S_plus_H',np.c_[S,H])]:
    md=clone(m); md.fit(X[tr],Y[tr]); pr=md.predict(X[te]); vals.append((tag,r2_score(Y[te],pr,multioutput='variance_weighted'),float(np.sqrt(mean_squared_error(Y[te],pr))),float(np.mean(np.linalg.norm(Y[te]-pr,axis=1)))))
   for tag,r2,rmse,ve in vals: rr.append({'S_level':sn,'estimator':mn,'test_sequence':test,'features':tag,'r2':r2,'rmse':rmse,'vector_error':ve,'n_train':int(tr.sum()),'n_test':int(te.sum())})
R=pd.DataFrame(rr); S=R.groupby(['S_level','estimator','features'])[['r2','rmse','vector_error']].mean().reset_index(); gg=[]
for (sn,mn),g in S.groupby(['S_level','estimator']):
 a=g[g.features=='S'].iloc[0]; b=g[g.features=='S_plus_H'].iloc[0]; gg.append({'S_level':sn,'estimator':mn,'r2_gain':float(b.r2-a.r2),'rmse_improvement':float(a.rmse-b.rmse),'vector_error_improvement':float(a.vector_error-b.vector_error),'r2_S':float(a.r2),'r2_S_plus_H':float(b.r2)})
G=pd.DataFrame(gg); out=BASE/'results'; out.mkdir(exist_ok=True); R.to_csv(out/'primary_fold_metrics.csv',index=False); S.to_csv(out/'primary_summary.csv',index=False); G.to_csv(out/'primary_history_gains.csv',index=False)
res={'n_cells':len(D),'sequence_counts':{str(k):int(v) for k,v in D.sequence.value_counts().sort_index().items()},'frames':frames,'H':'older velocity 15->20 + speed + volume change','S_levels':['position+volume at 25','+ velocity 24->25 + volume change','+ acceleration 23,24,25'],'Y':'average future 3D velocity 25->40','grouping':'leave-one-acquisition-sequence-out','gains':G.to_dict(orient='records'),'seed':SEED}
(out/'primary_results.json').write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))
