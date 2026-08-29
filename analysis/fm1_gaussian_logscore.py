import argparse, math
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from refahi_fm1_stage_sweep import load, make_window


def gaussian_oof_nll(X,y,g,splits):
    nll=np.empty(len(y)); sigmas=[]
    for tr,te in splits:
        grid=GridSearchCV(Pipeline([('s',StandardScaler()),('r',Ridge())]),{'r__alpha':[0.1,1,10,100]},cv=GroupKFold(3),scoring='neg_mean_squared_error',n_jobs=-1)
        grid.fit(X[tr],y[tr],groups=g[tr]); alpha=grid.best_params_['r__alpha']
        # Estimate predictive noise from grouped OOF residuals inside the training fold.
        inner_pred=np.empty(len(tr)); gt=g[tr]
        for itr,iva in GroupKFold(3).split(X[tr],y[tr],gt):
            m=Pipeline([('s',StandardScaler()),('r',Ridge(alpha=alpha))]);m.fit(X[tr][itr],y[tr][itr]);inner_pred[iva]=m.predict(X[tr][iva])
        var=max(float(np.mean((y[tr]-inner_pred)**2)),1e-9);sigmas.append(math.sqrt(var))
        m=Pipeline([('s',StandardScaler()),('r',Ridge(alpha=alpha))]);m.fit(X[tr],y[tr]);mu=m.predict(X[te])
        nll[te]=0.5*np.log(2*np.pi*var)+0.5*((y[te]-mu)**2/var)
    return nll,sigmas


def analyze(repo,obj,layers,h,c,f,l1,bootstrap=5000):
    S,Hg,Ha,y,g=make_window(repo,obj,h,c,f,l1,layers)
    S,Hg,Ha,y,g=map(np.array,(S,Hg,Ha,y,g)); X=np.c_[S,Hg,Ha]
    splits=list(GroupKFold(5).split(S,y,g))
    cur,sc=gaussian_oof_nll(S,y,g,splits); hist,sh=gaussian_oof_nll(X,y,g,splits)
    diff=(cur-hist)/np.log(2)
    rng=np.random.default_rng(20260829);ugs=np.unique(g); vals=[]
    for _ in range(bootstrap):
        chosen=rng.choice(ugs,len(ugs),replace=True); idx=np.concatenate([np.where(g==z)[0] for z in chosen]); vals.append(float(diff[idx].mean()))
    return dict(n=len(y),groups=len(ugs),nll_current=float(cur.mean()),nll_history=float(hist.mean()),history_bits=float(diff.mean()),bootstrap=np.quantile(vals,[.5,.025,.975]),sigma_current=sc,sigma_history=sh)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--upstream',default='refahi_diag');ap.add_argument('--bootstrap',type=int,default=5000);args=ap.parse_args()
    repo=Path(args.upstream);obj,layers=load(repo)
    cases={'middle_L1':(40,96,120,True),'late_L1':(96,120,132,True),'late_all':(96,120,132,False)}
    for name,pars in cases.items():
        r=analyze(repo,obj,layers,*pars,bootstrap=args.bootstrap)
        print(name,'n',r['n'],'groups',r['groups'],'NLL_current',round(r['nll_current'],6),'NLL_history',round(r['nll_history'],6),'history_value_bits_per_cell',round(r['history_bits'],6),'bootstrap_median_q025_q975',np.round(r['bootstrap'],6).tolist())

if __name__=='__main__': main()
