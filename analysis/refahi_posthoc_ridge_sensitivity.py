#!/usr/bin/env python3
"""POST-HOC Ridge regularization sensitivity after primary analysis."""
import importlib.util,json
from pathlib import Path
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def one(hist,cur,fut,l1):
 dt=r.load_dtissue(); df,genes=r.build_window(dt,hist,cur,fut,l1)
 geom=[f'cur_{k}' for k in ['logv','x','y','z']]; curgenes=[f'cur_g_{g}' for g in genes]
 hgeom=[f'hist_{k}' for k in ['logv','x','y','z']]; hgenes=[f'hist_g_{g}' for g in genes]
 X1=df[geom+curgenes].to_numpy(float); X2=df[geom+curgenes+hgeom+hgenes].to_numpy(float)
 y=df.target.to_numpy(float); splits=r.make_splits(df.group.to_numpy())
 rows=[]
 for alpha in [0.1,1,10,100,1000]:
  model=make_pipeline(StandardScaler(),Ridge(alpha=alpha))
  p1,_=r.cv_predict(X1,y,splits,model); p2,_=r.cv_predict(X2,y,splits,model)
  a=float(r2_score(y,p1)); b=float(r2_score(y,p2)); rows.append({'alpha':alpha,'M1_current_r2':a,'M2_history_r2':b,'delta_r2':b-a})
 return {'window':f'{hist}->{cur}->{fut}','subset':'L1' if l1 else 'all','n':len(df),'groups':int(df.group.nunique()),'rows':rows}
res=[]
for w in [(40,96,120),(96,120,132)]:
 for l1 in [False,True]: res.append(one(*w,l1))
(r.OUT / 'refahi_posthoc_ridge_sensitivity.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
