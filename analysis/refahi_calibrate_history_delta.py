#!/usr/bin/env python3
"""Matched finite-sample calibration for the Ridge history-gain statistic.

Known-complete/null generator: Y is generated from current-state features only
plus independent Gaussian noise. Older-state features retain their real
correlation with current state but have no direct Y effect.

Known-incomplete/alternative generator: adds a direct older-history direction
constructed from history variation residualized against current features.

This calibration is diagnostic. It does not turn the atlas reanalysis into a
causal or prospective biological test.
"""
import argparse, importlib.util, json
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score
spec=importlib.util.spec_from_file_location('r','developmental-state-completion/analysis/refahi_state_completion_replication.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def pred(X,y,splits):
 model=make_pipeline(StandardScaler(),Ridge(alpha=10.0)); return r.cv_predict(X,y,splits,model)[0]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('hist',type=int); ap.add_argument('cur',type=int); ap.add_argument('fut',type=int); ap.add_argument('subset',choices=['all','L1']); ap.add_argument('--sims',type=int,default=100); a=ap.parse_args()
 l1=a.subset=='L1'; dt=r.load_dtissue(); df,genes=r.build_window(dt,a.hist,a.cur,a.fut,l1)
 geom=[f'cur_{k}' for k in ['logv','x','y','z']]; cg=[f'cur_g_{g}' for g in genes]
 hg=[f'hist_{k}' for k in ['logv','x','y','z']]+[f'hist_g_{g}' for g in genes]
 Xc=df[geom+cg].to_numpy(float); H=df[hg].to_numpy(float); Xfull=np.hstack([Xc,H]); y=df.target.to_numpy(float); groups=df.group.to_numpy(); splits=r.make_splits(groups)
 # real statistic
 real=float(r2_score(y,pred(Xfull,y,splits))-r2_score(y,pred(Xc,y,splits)))
 # Full-data current-state mean model; null is complete by construction.
 mean_model=make_pipeline(StandardScaler(),Ridge(alpha=10.0)); mean_model.fit(Xc,y); mu=mean_model.predict(Xc); sigma=float(np.std(y-mu,ddof=1)); ysd=float(np.std(y,ddof=1))
 # Construct a history-only direction not linearly carried by current features.
 hs=StandardScaler().fit_transform(H); hx=make_pipeline(StandardScaler(),Ridge(alpha=10.0)); hx.fit(Xc,hs); hres=hs-hx.predict(Xc); score=PCA(n_components=1,random_state=r.RNG_SEED).fit_transform(hres).ravel(); score=(score-score.mean())/score.std(ddof=1)
 effect=0.20*ysd
 rng=np.random.default_rng(r.RNG_SEED + a.hist*1000+a.cur)
 null=[]; alt=[]
 for i in range(a.sims):
  noise=rng.normal(0,sigma,len(y))
  yn=mu+noise
  ya=mu+effect*score+noise
  null.append(float(r2_score(yn,pred(Xfull,yn,splits))-r2_score(yn,pred(Xc,yn,splits))))
  alt.append(float(r2_score(ya,pred(Xfull,ya,splits))-r2_score(ya,pred(Xc,ya,splits))))
 q95=float(np.quantile(null,.95))
 out={'window':f'{a.hist}->{a.cur}->{a.fut}','subset':a.subset,'n':len(df),'groups':int(df.group.nunique()),'sims':a.sims,'real_delta_r2':real,'known_complete_null':{'mean':float(np.mean(null)),'sd':float(np.std(null,ddof=1)),'q95':q95,'false_positive_rate_at_q95':float(np.mean(np.array(null)>q95))},'known_incomplete_alt':{'history_effect_sd_units':0.20,'mean_delta':float(np.mean(alt)),'sd':float(np.std(alt,ddof=1)),'power_vs_null_q95':float(np.mean(np.array(alt)>q95))},'noise_sd':sigma,'target_sd':ysd}
 fn=r.OUT / f'refahi_calibration_{a.hist}_{a.cur}_{a.fut}_{a.subset}.json'; fn.write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
