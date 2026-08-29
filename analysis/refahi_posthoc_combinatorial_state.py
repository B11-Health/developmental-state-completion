#!/usr/bin/env python3
"""POST-HOC sensitivity: encode the released binary gene vector as a
combinatorial categorical cell-state instead of 25 additive covariates.
Specified after primary model-dependence was observed. Diagnostic only.
"""
import importlib.util,json
from pathlib import Path
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def cvpred(df,y,splits,cols_num,cols_cat):
 pred=np.full(len(df),np.nan)
 for tr,te in splits:
  pre=ColumnTransformer([('num',StandardScaler(),cols_num),('cat',OneHotEncoder(handle_unknown='ignore'),cols_cat)])
  model=Pipeline([('pre',pre),('reg',Ridge(alpha=10.0))])
  model.fit(df.iloc[tr],y[tr]); pred[te]=model.predict(df.iloc[te])
 return pred

def one(hist,cur,fut,l1):
 dt=r.load_dtissue(); df,genes=r.build_window(dt,hist,cur,fut,l1)
 cg=[f'cur_g_{g}' for g in genes]; hg=[f'hist_g_{g}' for g in genes]
 df['cur_state']=df[cg].astype(int).astype(str).agg(''.join,axis=1)
 df['hist_state']=df[hg].astype(int).astype(str).agg(''.join,axis=1)
 curgeom=[f'cur_{k}' for k in ['logv','x','y','z']]; histgeom=[f'hist_{k}' for k in ['logv','x','y','z']]
 y=df.target.to_numpy(float); splits=r.make_splits(df.group.to_numpy())
 p0=cvpred(df,y,splits,curgeom,[])
 p1=cvpred(df,y,splits,curgeom,['cur_state'])
 p2=cvpred(df,y,splits,curgeom+histgeom,['cur_state','hist_state'])
 vals={'geom':float(r2_score(y,p0)),'current_combinatorial':float(r2_score(y,p1)),'plus_history_combinatorial':float(r2_score(y,p2))}
 vals['history_delta']=vals['plus_history_combinatorial']-vals['current_combinatorial']
 return {'window':f'{hist}->{cur}->{fut}','subset':'L1' if l1 else 'all','n':len(df),'groups':int(df.group.nunique()),'n_current_states':int(df.cur_state.nunique()),'n_history_states':int(df.hist_state.nunique()),'ridge_onehot':vals}
res=[]
for w in [(40,96,120),(96,120,132)]:
 for l1 in [False,True]: res.append(one(*w,l1))
(r.OUT / 'refahi_posthoc_combinatorial_state.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
