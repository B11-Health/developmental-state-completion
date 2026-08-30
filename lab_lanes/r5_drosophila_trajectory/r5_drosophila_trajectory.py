import json, math, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error

BASE=Path(__file__).parent
SEED=20260830
rng=np.random.default_rng(SEED)

files=sorted((BASE/'source_data').glob('dro_centroids_*.csv'))
if not files: raise RuntimeError('centroid part files missing')
df=pd.concat([pd.read_csv(p) for p in files],ignore_index=True)
frames=[15,20,23,24,25,40]
rows=[]
for (seq,lab),g in df.groupby(['sequence','label']):
    if not set(frames).issubset(set(g.frame)): continue
    by={int(r.frame):r for _,r in g.iterrows()}
    def p(t): return np.array([by[t].x_um,by[t].y_um,by[t].z_um],float)
    rec={'sequence':str(seq).zfill(2),'label':int(lab)}
    for t in frames:
        q=p(t)
        for j,c in enumerate('xyz'): rec[f'{c}{t}']=q[j]
        rec[f'vol{t}']=float(by[t].voxel_count)
    rows.append(rec)
D=pd.DataFrame(rows)
# Current geometry centering uses only present-frame S information within each sequence.
for c in 'xyz':
    D[f'{c}25_centered']=D.groupby('sequence')[f'{c}25'].transform(lambda x:x-x.mean())
# isotropic sequence-specific present scale, derived only from S at frame 25
r2=(D[['x25_centered','y25_centered','z25_centered']]**2).sum(axis=1)
D['present_rms']=np.sqrt(r2.groupby(D.sequence).transform('mean')).replace(0,1)
for c in 'xyz': D[f'{c}25_norm']=D[f'{c}25_centered']/D['present_rms']

P=lambda t: D[[f'x{t}',f'y{t}',f'z{t}']].to_numpy(float)
p15,p20,p23,p24,p25,p40=[P(t) for t in frames]
v_old=(p20-p15)/5.0
v_recent=p25-p24
acc_recent=p25-2*p24+p23
future=(p40-p25)/15.0
logvol25=np.log1p(D.vol25.to_numpy())[:,None]
logvol_recent=(np.log1p(D.vol25)-np.log1p(D.vol24)).to_numpy()[:,None]
logvol_old=(np.log1p(D.vol20)-np.log1p(D.vol15)).to_numpy()[:,None]
posnorm=D[[f'{c}25_norm' for c in 'xyz']].to_numpy(float)
S0=np.c_[posnorm,logvol25]
S1=np.c_[S0,v_recent,logvol_recent]
S2=np.c_[S1,acc_recent]
H=np.c_[v_old,np.linalg.norm(v_old,axis=1)[:,None],logvol_old]
Y=future
groups=D.sequence.to_numpy()

models={
 'ridge':make_pipeline(StandardScaler(),Ridge(alpha=1.0)),
 'random_forest':RandomForestRegressor(n_estimators=300,min_samples_leaf=4,max_features=0.8,random_state=SEED,n_jobs=-1),
 'extra_trees':ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,max_features=0.9,random_state=SEED,n_jobs=-1),
}
Ss={'S0_position_volume':S0,'S1_plus_recent_velocity':S1,'S2_plus_recent_acceleration':S2}
fold_rows=[]; pred_rows=[]
for sname,S in Ss.items():
 for mname,model in models.items():
  for test_seq in sorted(set(groups)):
   tr=groups!=test_seq; te=groups==test_seq
   for plus_h,X in [('S',S),('S_plus_H',np.c_[S,H])]:
    mdl=clone(model); mdl.fit(X[tr],Y[tr]); pred=mdl.predict(X[te])
    r2v=r2_score(Y[te],pred,multioutput='variance_weighted')
    rmse=float(np.sqrt(mean_squared_error(Y[te],pred)))
    eu=float(np.mean(np.linalg.norm(Y[te]-pred,axis=1)))
    fold_rows.append({'S_level':sname,'estimator':mname,'test_sequence':test_seq,'features':plus_h,'r2':r2v,'rmse_component':rmse,'mean_vector_error':eu,'n_train':int(tr.sum()),'n_test':int(te.sum())})
    for idx,pr in zip(np.where(te)[0],pred): pred_rows.append({'S_level':sname,'estimator':mname,'test_sequence':test_seq,'features':plus_h,'row_index':int(idx),'sequence':groups[idx],'label':int(D.iloc[idx].label),'pred_x':pr[0],'pred_y':pr[1],'pred_z':pr[2],'true_x':Y[idx,0],'true_y':Y[idx,1],'true_z':Y[idx,2]})
fold=pd.DataFrame(fold_rows)
summary=fold.groupby(['S_level','estimator','features'])[['r2','rmse_component','mean_vector_error']].mean().reset_index()
gains=[]
for (sname,mname),g in summary.groupby(['S_level','estimator']):
 a=g[g.features=='S'].iloc[0]; b=g[g.features=='S_plus_H'].iloc[0]
 gains.append({'S_level':sname,'estimator':mname,'r2_gain':b.r2-a.r2,'rmse_improvement':a.rmse_component-b.rmse_component,'vector_error_improvement':a.mean_vector_error-b.mean_vector_error})
gains=pd.DataFrame(gains)

# Directional permutation null for the richest present S2: shuffle H within each acquisition sequence.
perm=[]
for rep in range(30):
 Hp=H.copy()
 for seq in sorted(set(groups)):
  ix=np.where(groups==seq)[0]; Hp[ix]=Hp[rng.permutation(ix)]
 for mname in ['ridge','random_forest']:
  model=models[mname]; scores={}
  for tag,X in [('S',S2),('S_plus_H_perm',np.c_[S2,Hp])]:
   vals=[]
   for test_seq in sorted(set(groups)):
    tr=groups!=test_seq; te=groups==test_seq; mdl=clone(model); mdl.fit(X[tr],Y[tr]); pr=mdl.predict(X[te]); vals.append(r2_score(Y[te],pr,multioutput='variance_weighted'))
   scores[tag]=float(np.mean(vals))
  perm.append({'rep':rep,'estimator':mname,'r2_gain_perm':scores['S_plus_H_perm']-scores['S']})
perm=pd.DataFrame(perm)

# Matched directional calibration with Ridge only. The outcome is generated from actual S2, with/without an H-specific term.
def cv_gain(Ysim):
 vals=[]
 for test_seq in sorted(set(groups)):
  tr=groups!=test_seq; te=groups==test_seq
  ss=[]
  for X in (S2,np.c_[S2,H]):
   mdl=clone(models['ridge']); mdl.fit(X[tr],Ysim[tr]); pr=mdl.predict(X[te]); ss.append(r2_score(Ysim[te],pr,multioutput='variance_weighted'))
  vals.append(ss[1]-ss[0])
 return float(np.mean(vals))
Sstd=(S2-S2.mean(0))/(S2.std(0)+1e-9); Hstd=(H-H.mean(0))/(H.std(0)+1e-9)
cal=[]
for rep in range(40):
 B=rng.normal(size=(Sstd.shape[1],3)); C=rng.normal(size=(Hstd.shape[1],3)); base=Sstd@B; base=base/(base.std(0)+1e-9)
 noise=rng.normal(scale=0.5,size=base.shape)
 y_complete=base+noise
 hterm=Hstd@C; hterm=hterm/(hterm.std(0)+1e-9)
 y_incomplete=base+0.35*hterm+noise
 cal.append({'rep':rep,'complete_gain':cv_gain(y_complete),'incomplete_gain':cv_gain(y_incomplete)})
cal=pd.DataFrame(cal)

out=BASE/'results'; out.mkdir(exist_ok=True)
fold.to_csv(out/'fold_metrics.csv',index=False); summary.to_csv(out/'summary.csv',index=False); gains.to_csv(out/'history_gains.csv',index=False); pd.DataFrame(pred_rows).to_csv(out/'heldout_predictions.csv',index=False); perm.to_csv(out/'permutation_null.csv',index=False); cal.to_csv(out/'calibration.csv',index=False)
result={
 'dataset':'Cell Tracking Challenge Fluo-N3DL-DRO training gold TRA masks',
 'n_cells':int(len(D)),'sequence_counts':{str(k):int(v) for k,v in D.sequence.value_counts().sort_index().items()},
 'frames':frames,'time_step_seconds':30,'anchor_frame':25,'future_frame':40,
 'task':{'H':'older velocity frame15->20 plus old speed and volume change','S0':'present normalized position + volume at frame25','S1':'S0 + velocity frame24->25 + recent volume change','S2':'S1 + acceleration from frames23,24,25','Y':'average 3D future velocity frame25->40'},
 'grouping':'leave-one-CTC-acquisition-sequence-out; two folds only',
 'primary_gains':gains.to_dict(orient='records'),
 'permutation_null':perm.groupby('estimator').r2_gain_perm.agg(['mean','std','min','max']).reset_index().to_dict(orient='records'),
 'ridge_calibration':{'known_complete':cal.complete_gain.describe().to_dict(),'known_incomplete_0.35SD_H_term':cal.incomplete_gain.describe().to_dict()},
 'limitations':['Only two acquisition sequences; group-level replication is weak.','Trajectory history is kinematic information, not molecular memory.','Current state uses geometry/velocity/acceleration only; unmeasured morphology, forces and molecular state remain outside S.','Sequence-level current-position centering/scaling uses only frame25 present geometry but is transductive at the group level.'],
 'seed':SEED,
}
(out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
