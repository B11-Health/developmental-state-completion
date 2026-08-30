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
F=sorted((BASE/'source_data').glob('dro_centroids_*.csv')); df=pd.concat([pd.read_csv(p) for p in F],ignore_index=True); frames=[15,20,23,24,25,40]; rows=[]
for (seq,lab),g in df.groupby(['sequence','label']):
 if not set(frames).issubset(set(g.frame)): continue
 b={int(r.frame):r for _,r in g.iterrows()}; rec={'sequence':str(seq).zfill(2),'label':int(lab)}
 for t in frames:
  for c in 'xyz': rec[f'{c}{t}']=float(getattr(b[t],f'{c}_um'))
  rec[f'vol{t}']=float(b[t].voxel_count)
 rows.append(rec)
D=pd.DataFrame(rows); P=lambda t:D[[f'x{t}',f'y{t}',f'z{t}']].to_numpy(float); p15,p20,p23,p24,p25,p40=[P(t) for t in frames]
# center present coordinates within each sequence, then use rotation-invariant radius
pc=p25.copy()
for seq in sorted(D.sequence.unique()): pc[D.sequence.to_numpy()==seq]-=pc[D.sequence.to_numpy()==seq].mean(0)
r=np.linalg.norm(pc,axis=1); rscale=pd.Series(r).groupby(D.sequence.reset_index(drop=True)).transform('mean').to_numpy(); rnorm=r/(rscale+1e-9); unit=pc/(r[:,None]+1e-9)
vold=(p20-p15)/5; vrecent=p25-p24; acc=p25-2*p24+p23; future=(p40-p25)/15
speed_old=np.linalg.norm(vold,axis=1); speed_recent=np.linalg.norm(vrecent,axis=1); accmag=np.linalg.norm(acc,axis=1); future_speed=np.linalg.norm(future,axis=1)
radial_recent=(vrecent*unit).sum(1); radial_old=(vold*unit).sum(1); future_radial=(future*unit).sum(1)
logv=np.log1p(D.vol25.to_numpy()); lvr=(np.log1p(D.vol25)-np.log1p(D.vol24)).to_numpy(); lvo=(np.log1p(D.vol20)-np.log1p(D.vol15)).to_numpy()
S0=np.c_[rnorm,logv]; S1=np.c_[S0,speed_recent,radial_recent,lvr]; S2=np.c_[S1,accmag]; H=np.c_[speed_old,radial_old,lvo]
groups=D.sequence.to_numpy(); Ys={'future_speed':future_speed,'future_radial_velocity':future_radial}
models={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=1.0)),'random_forest':RandomForestRegressor(n_estimators=120,min_samples_leaf=4,max_features=.9,random_state=SEED,n_jobs=-1),'extra_trees':ExtraTreesRegressor(n_estimators=120,min_samples_leaf=3,max_features=1.0,random_state=SEED,n_jobs=-1)}; Ss={'S0':S0,'S1':S1,'S2':S2}; rr=[]
for yname,Y in Ys.items():
 for sn,S in Ss.items():
  for mn,m in models.items():
   for test in sorted(set(groups)):
    tr=groups!=test; te=groups==test
    for tag,X in [('S',S),('S_plus_H',np.c_[S,H])]:
     md=clone(m); md.fit(X[tr],Y[tr]); pr=md.predict(X[te]); rr.append({'outcome':yname,'S_level':sn,'estimator':mn,'test_sequence':test,'features':tag,'r2':r2_score(Y[te],pr),'rmse':float(np.sqrt(mean_squared_error(Y[te],pr)))})
R=pd.DataFrame(rr); Sm=R.groupby(['outcome','S_level','estimator','features'])[['r2','rmse']].mean().reset_index(); gg=[]
for (yn,sn,mn),g in Sm.groupby(['outcome','S_level','estimator']):
 a=g[g.features=='S'].iloc[0]; b=g[g.features=='S_plus_H'].iloc[0]; gg.append({'outcome':yn,'S_level':sn,'estimator':mn,'r2_S':float(a.r2),'r2_S_plus_H':float(b.r2),'r2_gain':float(b.r2-a.r2),'rmse_improvement':float(a.rmse-b.rmse)})
G=pd.DataFrame(gg); out=BASE/'results'; R.to_csv(out/'invariant_fold_metrics.csv',index=False); G.to_csv(out/'invariant_history_gains.csv',index=False); res={'task':'rotation/translation-invariant sensitivity','n_cells':len(D),'gains':G.to_dict(orient='records'),'note':'Secondary sensitivity after raw-vector task showed poor sequence transfer; not a preregistered primary result.'}; (out/'invariant_results.json').write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))
