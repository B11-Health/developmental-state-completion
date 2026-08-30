from pathlib import Path
import numpy as np,pandas as pd
from sklearn.metrics import r2_score,mean_squared_error
BASE=Path(__file__).parent; F=sorted((BASE/'source_data').glob('dro_centroids_*.csv')); df=pd.concat([pd.read_csv(p) for p in F]); frames=[15,20,23,24,25,40]; rows=[]
for (seq,lab),g in df.groupby(['sequence','label']):
 if not set(frames).issubset(set(g.frame)): continue
 b={int(r.frame):r for _,r in g.iterrows()}; rec={'sequence':str(seq).zfill(2),'label':lab}
 for t in frames:
  for c in 'xyz': rec[f'{c}{t}']=float(getattr(b[t],f'{c}_um'))
 rows.append(rec)
D=pd.DataFrame(rows); P=lambda t:D[[f'x{t}',f'y{t}',f'z{t}']].to_numpy(); p25,p40=P(25),P(40); future=(p40-p25)/15; groups=D.sequence.to_numpy(); rr=[]
# radial unit at present within sequence
pc=p25.copy()
for s in sorted(set(groups)): pc[groups==s]-=pc[groups==s].mean(0)
unit=pc/(np.linalg.norm(pc,axis=1)[:,None]+1e-9); outcomes={'future_vector':future,'future_speed':np.linalg.norm(future,axis=1),'future_radial_velocity':(future*unit).sum(1)}
for name,Y in outcomes.items():
 for test in sorted(set(groups)):
  tr=groups!=test; te=groups==test; mu=Y[tr].mean(axis=0); pred=np.repeat(mu[None,:],te.sum(),axis=0) if Y.ndim==2 else np.full(te.sum(),mu)
  r2=r2_score(Y[te],pred,multioutput='variance_weighted') if Y.ndim==2 else r2_score(Y[te],pred); rmse=float(np.sqrt(mean_squared_error(Y[te],pred))); rr.append({'outcome':name,'test_sequence':test,'r2_train_mean_dummy':r2,'rmse':rmse})
R=pd.DataFrame(rr); R.to_csv(BASE/'results'/'dummy_baselines.csv',index=False); print(R.to_string(index=False))
