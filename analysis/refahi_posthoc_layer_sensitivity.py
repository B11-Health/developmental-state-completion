#!/usr/bin/env python3
"""POST-HOC sensitivity analysis, specified after primary four-case results.
Question: does older-history gain in pooled cells fall when CURRENT tissue layer
(L1/L2/other) is explicitly added to the present-state representation?
This is diagnostic only and is not part of the frozen primary analysis.
"""
import importlib.util, json, runpy
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def run(hist,cur,fut):
 dt=r.load_dtissue(); df,genes=r.build_window(dt,hist,cur,fut,False)
 ids=runpy.run_path(str(r.ROOT/'common/common/L1L2_cells_ids.py'))
 L1=set(ids[f'L1_{cur}h']); L2=set(ids[f'L2_{cur}h'])
 df['cur_L1']=df.cid.isin(L1).astype(float); df['cur_L2']=df.cid.isin(L2).astype(float)
 geom=[f'cur_{k}' for k in ['logv','x','y','z']]
 curgenes=[f'cur_g_{g}' for g in genes]
 histgeom=[f'hist_{k}' for k in ['logv','x','y','z']]
 histgenes=[f'hist_g_{g}' for g in genes]
 y=df.target.to_numpy(float); splits=r.make_splits(df.group.to_numpy())
 sets={
  'current_no_layer':geom+curgenes,
  'current_plus_layer':geom+curgenes+['cur_L1','cur_L2'],
  'current_plus_layer_plus_history':geom+curgenes+['cur_L1','cur_L2']+histgeom+histgenes,
 }
 out={'window':f'{hist}->{cur}->{fut}','posthoc':True,'n':len(df),'groups':int(df.group.nunique()),'layer_counts':{'L1':int(df.cur_L1.sum()),'L2':int(df.cur_L2.sum()),'other':int(((df.cur_L1+df.cur_L2)==0).sum())},'ridge':{}}
 model=make_pipeline(StandardScaler(),Ridge(alpha=10.0))
 for name,cols in sets.items():
  p,_=r.cv_predict(df[cols].to_numpy(float),y,splits,model)
  out['ridge'][name]=float(r2_score(y,p))
 out['ridge']['history_gain_after_layer']=out['ridge']['current_plus_layer_plus_history']-out['ridge']['current_plus_layer']
 out['ridge']['layer_gain']=out['ridge']['current_plus_layer']-out['ridge']['current_no_layer']
 return out

res=[run(40,96,120),run(96,120,132)]
(r.OUT / 'refahi_posthoc_layer_sensitivity.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
