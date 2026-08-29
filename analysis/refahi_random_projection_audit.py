#!/usr/bin/env python3
import importlib.util, json, argparse
from pathlib import Path
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rep',REPO/'analysis/refahi_state_completion_replication.py'); rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
OUT=REPO/'results'; OUT.mkdir(exist_ok=True)

def maker(name,seed):
    if name=='extra_trees': return ExtraTreesRegressor(n_estimators=150,min_samples_leaf=5,max_features=0.7,random_state=seed,n_jobs=-1)
    return HistGradientBoostingRegressor(max_iter=180,max_leaf_nodes=15,min_samples_leaf=20,l2_regularization=2.0,random_state=seed)

def pred_scalar(df,genes,model,scalar_mode,seed,w=None):
    y=df.target.to_numpy(float); splits=rep.make_splits(df.group.to_numpy()); geom=[f'cur_{k}' for k in ['logv','x','y','z']]; cur=[f'cur_g_{g}' for g in genes]; Xg=df[geom].to_numpy(float); Xm=df[cur].to_numpy(float); pred=np.full(len(df),np.nan)
    for tr,te in splits:
        if scalar_mode=='none': Xtr=Xg[tr]; Xte=Xg[te]
        elif scalar_mode=='all25': Xtr=np.hstack([Xg[tr],Xm[tr]]); Xte=np.hstack([Xg[te],Xm[te]])
        elif scalar_mode=='pc1':
            p=PCA(n_components=1).fit(Xm[tr]); Xtr=np.hstack([Xg[tr],p.transform(Xm[tr])]); Xte=np.hstack([Xg[te],p.transform(Xm[te])])
        else:
            z=(Xm@w).reshape(-1,1); Xtr=np.hstack([Xg[tr],z[tr]]); Xte=np.hstack([Xg[te],z[te]])
        m=maker(model,seed); m.fit(Xtr,y[tr]); pred[te]=m.predict(Xte)
    return float(r2_score(y,pred))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--model',choices=['extra_trees','histgb'],required=True); ap.add_argument('--n',type=int,default=30); args=ap.parse_args()
    dt=rep.load_dtissue(); df,genes=rep.build_window(dt,96,120,132,True); Xm=df[[f'cur_g_{g}' for g in genes]].to_numpy(float)
    uniq=np.unique(Xm,axis=0); base=pred_scalar(df,genes,args.model,'none',20260829); pc=pred_scalar(df,genes,args.model,'pc1',20260829); all25=pred_scalar(df,genes,args.model,'all25',20260829)
    rng=np.random.default_rng(20260829); rows=[]
    for i in range(args.n):
        w=rng.normal(size=Xm.shape[1]); w=w/np.linalg.norm(w); codes=uniq@w; unique=len(np.unique(np.round(codes,12))); r=pred_scalar(df,genes,args.model,'random',20260829+i,w=w); rows.append({'i':i,'r2':r,'unique_state_codes':int(unique)})
    a=np.array([r['r2'] for r in rows]); out={'model':args.model,'n_random':args.n,'n_states':int(len(uniq)),'geometry_r2':base,'pc1_r2':pc,'all25_r2':all25,'random_projection':{'mean':float(a.mean()),'median':float(np.median(a)),'q025':float(np.quantile(a,.025)),'q975':float(np.quantile(a,.975)),'max':float(a.max()),'min':float(a.min()),'fraction_ge_pc1':float(np.mean(a>=pc)),'fraction_ge_all25':float(np.mean(a>=all25)),'fraction_injective':float(np.mean([r['unique_state_codes']==len(uniq) for r in rows]))},'rows':rows}
    (OUT/f'refahi_random_projection_{args.model}.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
