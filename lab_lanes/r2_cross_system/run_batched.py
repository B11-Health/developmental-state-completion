import argparse, importlib.util
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('core',P/'analyze_ctc_ce_lineage.py'); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
R=P/'results'; R.mkdir(exist_ok=True)
def eval_chunk(kind,start,count):
    df=core.load_rows(); y=df.duration.to_numpy(float); group='group_depth2'; base=1000
    if kind=='strict': group='group_depth1'; base=12000
    if kind=='noemb': df=df.copy(); df['embryo_code']=0; base=22000
    ev=core.eval_outcome(df,y,group,count,base+start); ev['split']=ev['split']+start
    ev.to_csv(R/f'{kind}_{start:03d}_{start+count-1:03d}.csv',index=False)
def calibration_chunk(start,count):
    df=core.load_rows(); Xs=df[core.S_COLS].to_numpy(float); yh=df.duration.to_numpy(float)
    bm=make_pipeline(StandardScaler(),Ridge(alpha=10.0)).fit(Xs,yh); base=bm.predict(Xs); sigma=float(np.std(yh-base,ddof=1))
    h=df[['parent_duration']].to_numpy(float); hr=h-make_pipeline(StandardScaler(),Ridge(alpha=1.0)).fit(Xs,h).predict(Xs); hr=(hr[:,0]-hr[:,0].mean())/(hr[:,0].std(ddof=1)+1e-12)
    rows=[]; groups=df.group_depth2.to_numpy()
    for sim in range(start,start+count):
        rng=np.random.default_rng(90000+sim); noise=rng.normal(0,sigma,len(df)); yc=base+noise; yi=yc+0.30*float(np.std(yc,ddof=1))*hr
        k=sim%100; _,tr,te=next(core.split_indices(groups,1,.25,7000+k))
        for outcome,y in [('complete',yc),('incomplete',yi)]:
            for name,m in core.models(200000+sim).items():
                rs=[]
                for cols in [core.S_COLS,core.S_COLS+core.H_COLS]:
                    mm=clone(m); mm.fit(df.iloc[tr][cols],y[tr]); rs.append(r2_score(y[te],mm.predict(df.iloc[te][cols])))
                rows.append(dict(sim=sim,split=k,outcome=outcome,estimator=name,delta_r2=rs[1]-rs[0],noise_sd=sigma))
    pd.DataFrame(rows).to_csv(R/f'cal_{start:03d}_{start+count-1:03d}.csv',index=False)
def permutation_chunk():
    df=core.load_rows(); rng=np.random.default_rng(314159); yp=rng.permutation(df.duration.to_numpy(float)); ev=core.eval_outcome(df,yp,'group_depth2',30,30000); ev.to_csv(R/'permutation_results.csv',index=False)
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('kind'); a.add_argument('start',type=int,nargs='?',default=0); a.add_argument('count',type=int,nargs='?',default=10); z=a.parse_args()
    if z.kind in {'observed','strict','noemb'}: eval_chunk(z.kind,z.start,z.count)
    elif z.kind=='cal': calibration_chunk(z.start,z.count)
    elif z.kind=='perm': permutation_chunk()
    else: raise SystemExit(z.kind)
