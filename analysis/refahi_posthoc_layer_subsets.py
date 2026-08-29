#!/usr/bin/env python3
"""POST-HOC localization of history gain by tissue layer.
Specified after primary all/L1 results. Requires current cell and older ancestor
to both belong to L2, or both belong to neither released L1 nor L2 lists.
"""
import importlib.util,json,runpy
from pathlib import Path
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def subset(hist,cur,fut,kind):
 dt=r.load_dtissue(); df,genes=r.build_window(dt,hist,cur,fut,False)
 ids=runpy.run_path(str(r.ROOT/'common/common/L1L2_cells_ids.py'))
 c1=set(ids[f'L1_{cur}h']); c2=set(ids[f'L2_{cur}h']); h1=set(ids[f'L1_{hist}h']); h2=set(ids[f'L2_{hist}h'])
 if kind=='L2': mask=df.cid.isin(c2) & df.group.isin(h2)
 elif kind=='other': mask=(~df.cid.isin(c1|c2)) & (~df.group.isin(h1|h2))
 else: raise ValueError(kind)
 df=df.loc[mask].reset_index(drop=True)
 geom=[f'cur_{k}' for k in ['logv','x','y','z']]; cg=[f'cur_g_{g}' for g in genes]
 hg=[f'hist_{k}' for k in ['logv','x','y','z']]+[f'hist_g_{g}' for g in genes]
 y=df.target.to_numpy(float); groups=df.group.to_numpy(); splits=r.make_splits(groups)
 out={'window':f'{hist}->{cur}->{fut}','subset':kind,'n':len(df),'groups':int(df.group.nunique()),'models':{}}
 models={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10.0)),'extra_trees':ExtraTreesRegressor(n_estimators=200,min_samples_leaf=5,max_features=.7,random_state=r.RNG_SEED,n_jobs=-1)}
 for name,m in models.items():
  p1,_=r.cv_predict(df[geom+cg].to_numpy(float),y,splits,m); p2,_=r.cv_predict(df[geom+cg+hg].to_numpy(float),y,splits,m)
  a=float(r2_score(y,p1)); b=float(r2_score(y,p2)); out['models'][name]={'current_r2':a,'history_r2':b,'delta_r2':b-a}
 return out
res=[]
for w in [(40,96,120),(96,120,132)]:
 for k in ['L2','other']:
  try: res.append(subset(*w,k))
  except Exception as e: res.append({'window':f'{w[0]}->{w[1]}->{w[2]}','subset':k,'error':repr(e)})
(r.OUT / 'refahi_posthoc_layer_subsets.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
