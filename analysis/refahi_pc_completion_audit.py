#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rep', REPO/'analysis/refahi_state_completion_replication.py')
rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
OUT=REPO/'results'; OUT.mkdir(exist_ok=True)
SEED=20260829

def maker(name):
    if name=='ridge': return make_pipeline(StandardScaler(),Ridge(alpha=10.0))
    if name=='extra_trees': return ExtraTreesRegressor(n_estimators=250,min_samples_leaf=5,max_features=0.7,random_state=SEED,n_jobs=-1)
    if name=='histgb': return HistGradientBoostingRegressor(max_iter=300,max_leaf_nodes=15,min_samples_leaf=20,l2_regularization=2.0,random_state=SEED)
    raise ValueError(name)

def fit_oof(df,genes,model_name,kpc=None,include_all_genes=False,include_history=False):
    y=df.target.to_numpy(float); groups=df.group.to_numpy(); splits=rep.make_splits(groups)
    geom=[f'cur_{k}' for k in ['logv','x','y','z']]
    cur=[f'cur_g_{g}' for g in genes]
    hist=[f'hist_{k}' for k in ['logv','x','y','z']]+[f'hist_g_{g}' for g in genes]
    pred=np.full(len(df),np.nan); ev=[]; folds=[]
    for tr,te in splits:
        blocks_tr=[df.iloc[tr][geom].to_numpy(float)]; blocks_te=[df.iloc[te][geom].to_numpy(float)]
        if include_all_genes:
            blocks_tr.append(df.iloc[tr][cur].to_numpy(float)); blocks_te.append(df.iloc[te][cur].to_numpy(float))
        elif kpc is not None:
            pca=PCA(n_components=kpc,random_state=SEED)
            pca.fit(df.iloc[tr][cur].to_numpy(float))
            blocks_tr.append(pca.transform(df.iloc[tr][cur].to_numpy(float)))
            blocks_te.append(pca.transform(df.iloc[te][cur].to_numpy(float)))
            ev.append(float(np.sum(pca.explained_variance_ratio_)))
        if include_history:
            blocks_tr.append(df.iloc[tr][hist].to_numpy(float)); blocks_te.append(df.iloc[te][hist].to_numpy(float))
        Xtr=np.hstack(blocks_tr); Xte=np.hstack(blocks_te)
        m=maker(model_name); m.fit(Xtr,y[tr]); pp=m.predict(Xte); pred[te]=pp; folds.append(float(r2_score(y[te],pp)))
    return {'r2_oof':float(r2_score(y,pred)),'fold_r2':folds,'fold_r2_mean':float(np.mean(folds)),'pc_explained_variance_mean':None if not ev else float(np.mean(ev))}

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--subset',choices=['L1','all'],default='L1'); ap.add_argument('--model',choices=['ridge','extra_trees','histgb'],default='ridge'); args=ap.parse_args()
    dt=rep.load_dtissue(); df,genes=rep.build_window(dt,96,120,132,args.subset=='L1')
    rows={}; rows['geom']=fit_oof(df,genes,args.model)
    for k in [1,2,4,8,16]: rows[f'geom+PC{k}']=fit_oof(df,genes,args.model,kpc=k)
    rows['geom+all25']=fit_oof(df,genes,args.model,include_all_genes=True)
    rows['geom+PC1+history']=fit_oof(df,genes,args.model,kpc=1,include_history=True)
    rows['geom+all25+history']=fit_oof(df,genes,args.model,include_all_genes=True,include_history=True)
    out={'source_commit':'95fde8b3b9a0bd09d556ce765a2235093362306f','design':'late 96->120->132; PCA fit within each training fold; grouped by 96h ancestor','subset':args.subset,'model':args.model,'n':len(df),'groups':int(df.group.nunique()),'rows':rows}
    op=OUT/f'refahi_pc_completion_{args.subset}_{args.model}.json'; op.write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
