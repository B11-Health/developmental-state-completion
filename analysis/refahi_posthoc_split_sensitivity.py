#!/usr/bin/env python3
"""POST-HOC sensitivity of Ridge history delta to lineage-group CV split seed."""
import importlib.util,json
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def one(hist,cur,fut,l1):
 dt=r.load_dtissue(); df,genes=r.build_window(dt,hist,cur,fut,l1)
 geom=[f'cur_{k}' for k in ['logv','x','y','z']]; cg=[f'cur_g_{g}' for g in genes]
 hg=[f'hist_{k}' for k in ['logv','x','y','z']]+[f'hist_g_{g}' for g in genes]
 X1=df[geom+cg].to_numpy(float); X2=df[geom+cg+hg].to_numpy(float); y=df.target.to_numpy(float); groups=df.group.to_numpy()
 rows=[]
 for seed in range(30):
  cv=GroupKFold(n_splits=5,shuffle=True,random_state=1000+seed); splits=list(cv.split(X1,groups=groups))
  m=make_pipeline(StandardScaler(),Ridge(alpha=10.0)); p1,_=r.cv_predict(X1,y,splits,m); p2,_=r.cv_predict(X2,y,splits,m)
  a=float(r2_score(y,p1)); b=float(r2_score(y,p2)); rows.append({'seed':1000+seed,'M1':a,'M2':b,'delta':b-a})
 ds=np.array([x['delta'] for x in rows])
 return {'window':f'{hist}->{cur}->{fut}','subset':'L1' if l1 else 'all','n':len(df),'groups':int(df.group.nunique()),'delta_summary':{'mean':float(ds.mean()),'median':float(np.median(ds)),'min':float(ds.min()),'max':float(ds.max()),'q05':float(np.quantile(ds,.05)),'q95':float(np.quantile(ds,.95)),'fraction_positive':float((ds>0).mean())},'rows':rows}
res=[]
for w in [(40,96,120),(96,120,132)]:
 for l1 in [False,True]: res.append(one(*w,l1))
(r.OUT / 'refahi_posthoc_split_sensitivity.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k!='rows'} for x in res],indent=2))
