#!/usr/bin/env python3
import importlib.util, json, argparse
from pathlib import Path
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import GroupKFold

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rep',REPO/'analysis/refahi_state_completion_replication.py'); rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
OUT=REPO/'results'; OUT.mkdir(exist_ok=True)

def maker(name,seed):
    if name=='extra_trees': return ExtraTreesRegressor(n_estimators=100,min_samples_leaf=5,max_features=0.7,random_state=seed,n_jobs=-1)
    return HistGradientBoostingRegressor(max_iter=180,max_leaf_nodes=15,min_samples_leaf=20,l2_regularization=2.0,random_state=seed)

def oof(df,genes,model,seed,mode):
    y=df.target.to_numpy(float); groups=df.group.to_numpy(); cv=GroupKFold(n_splits=5,shuffle=True,random_state=seed); splits=list(cv.split(np.zeros((len(df),1)),groups=groups))
    geom=[f'cur_{k}' for k in ['logv','x','y','z']]; cur=[f'cur_g_{g}' for g in genes]
    pred=np.full(len(df),np.nan)
    for tr,te in splits:
        Xtr=df.iloc[tr][geom].to_numpy(float); Xte=df.iloc[te][geom].to_numpy(float)
        if mode=='pc1':
            p=PCA(n_components=1).fit(df.iloc[tr][cur].to_numpy(float)); Xtr=np.hstack([Xtr,p.transform(df.iloc[tr][cur].to_numpy(float))]); Xte=np.hstack([Xte,p.transform(df.iloc[te][cur].to_numpy(float))])
        elif mode=='all25':
            Xtr=np.hstack([Xtr,df.iloc[tr][cur].to_numpy(float)]); Xte=np.hstack([Xte,df.iloc[te][cur].to_numpy(float)])
        m=maker(model,seed); m.fit(Xtr,y[tr]); pred[te]=m.predict(Xte)
    return float(r2_score(y,pred))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--model',choices=['extra_trees','histgb'],required=True); ap.add_argument('--n',type=int,default=30); ap.add_argument('--start',type=int,default=0); args=ap.parse_args()
    dt=rep.load_dtissue(); df,genes=rep.build_window(dt,96,120,132,True); rows=[]
    for i in range(args.n):
        seed=20260829+(args.start+i)*7919
        g=oof(df,genes,args.model,seed,'geom'); p=oof(df,genes,args.model,seed,'pc1'); a=oof(df,genes,args.model,seed,'all25')
        total=a-g; rec=(p-g)/total if abs(total)>1e-9 else float('nan')
        rows.append({'seed':seed,'geom':g,'pc1':p,'all25':a,'pc1_minus_all25':p-a,'pc1_gain_recovery':rec})
    arr=lambda k:np.array([r[k] for r in rows],float)
    out={'model':args.model,'n_partitions':args.n,'n':len(df),'groups':int(df.group.nunique()),'summary':{k:{'mean':float(np.nanmean(arr(k))),'median':float(np.nanmedian(arr(k))),'q025':float(np.nanquantile(arr(k),.025)),'q975':float(np.nanquantile(arr(k),.975))} for k in ['geom','pc1','all25','pc1_minus_all25','pc1_gain_recovery']},'fraction_pc1_ge_all25':float(np.mean(arr('pc1_minus_all25')>=0)),'rows':rows}
    (OUT/f'refahi_pc_split_stability_{args.model}_{args.start}_{args.start+args.n}.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out['summary'],indent=2)); print('fraction_pc1_ge_all25',out['fraction_pc1_ge_all25'])
if __name__=='__main__': main()
