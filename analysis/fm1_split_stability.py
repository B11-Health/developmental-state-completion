import argparse, math
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from refahi_fm1_stage_sweep import load, make_window


def ridge_r2_delta(S,X,y,g,seed):
    pc=np.empty(len(y)); ph=np.empty(len(y))
    for tr,te in GroupKFold(5,shuffle=True,random_state=seed).split(S,y,g):
        a=make_pipeline(StandardScaler(),Ridge(alpha=10)); b=make_pipeline(StandardScaler(),Ridge(alpha=10))
        a.fit(S[tr],y[tr]); b.fit(X[tr],y[tr]); pc[te]=a.predict(S[te]); ph[te]=b.predict(X[te])
    return r2_score(y,ph)-r2_score(y,pc)


def gaussian_nll(X,y,g,splits):
    nll=np.empty(len(y))
    for tr,te in splits:
        inner=np.empty(len(tr)); gt=g[tr]
        for itr,iva in GroupKFold(3).split(X[tr],y[tr],gt):
            m=make_pipeline(StandardScaler(),Ridge(alpha=10));m.fit(X[tr][itr],y[tr][itr]);inner[iva]=m.predict(X[tr][iva])
        var=max(float(np.mean((y[tr]-inner)**2)),1e-9)
        m=make_pipeline(StandardScaler(),Ridge(alpha=10));m.fit(X[tr],y[tr]);mu=m.predict(X[te])
        nll[te]=0.5*np.log(2*np.pi*var)+0.5*((y[te]-mu)**2/var)
    return nll


def logscore_bits_delta(S,X,y,g,seed):
    splits=list(GroupKFold(5,shuffle=True,random_state=seed).split(S,y,g))
    a=gaussian_nll(S,y,g,splits); b=gaussian_nll(X,y,g,splits)
    return float(np.mean(a-b)/np.log(2))


def tree_r2_delta(S,X,y,g,seed,trees):
    pc=np.empty(len(y));ph=np.empty(len(y))
    for tr,te in GroupKFold(5,shuffle=True,random_state=seed).split(S,y,g):
        a=ExtraTreesRegressor(n_estimators=trees,min_samples_leaf=5,max_features=.7,random_state=17,n_jobs=-1)
        b=ExtraTreesRegressor(n_estimators=trees,min_samples_leaf=5,max_features=.7,random_state=17,n_jobs=-1)
        a.fit(S[tr],y[tr]);b.fit(X[tr],y[tr]);pc[te]=a.predict(S[te]);ph[te]=b.predict(X[te])
    return r2_score(y,ph)-r2_score(y,pc)


def summarize(name,v):
    v=np.asarray(v)
    print(name,'mean',round(float(v.mean()),6),'median',round(float(np.median(v)),6),'q025_q975',np.round(np.quantile(v,[.025,.975]),6).tolist(),'positive_fraction',round(float(np.mean(v>0)),4),'gt_0.05_fraction',round(float(np.mean(v>.05)),4),'min_max',np.round([v.min(),v.max()],6).tolist())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--upstream',default='refahi_diag');ap.add_argument('--ridge-seeds',type=int,default=50);ap.add_argument('--log-seeds',type=int,default=30);ap.add_argument('--tree-seeds',type=int,default=0);ap.add_argument('--trees',type=int,default=75);args=ap.parse_args()
    repo=Path(args.upstream);obj,layers=load(repo)
    for label,(h,c,f) in {'middle_L1':(40,96,120),'late_L1':(96,120,132)}.items():
        S,Hg,Ha,y,g=make_window(repo,obj,h,c,f,True,layers);S,Hg,Ha,y,g=map(np.array,(S,Hg,Ha,y,g));X=np.c_[S,Hg,Ha]
        print('\n'+label,'n',len(y),'groups',len(np.unique(g)))
        summarize('ridge_delta_r2',[ridge_r2_delta(S,X,y,g,s) for s in range(args.ridge_seeds)])
        summarize('gaussian_history_bits',[logscore_bits_delta(S,X,y,g,s) for s in range(args.log_seeds)])
        if args.tree_seeds:
            summarize('extra_trees_delta_r2',[tree_r2_delta(S,X,y,g,s,args.trees) for s in range(args.tree_seeds)])

if __name__=='__main__':main()
