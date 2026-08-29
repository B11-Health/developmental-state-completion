import argparse, runpy
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from refahi_fm1_state_completion import build_dataset, ridge_oof

def fixed_oof(X, y, groups, splits, alpha=10):
    pred=np.empty(len(y))
    for tr,te in splits:
        m=make_pipeline(StandardScaler(),Ridge(alpha=alpha)); m.fit(X[tr],y[tr]); pred[te]=m.predict(X[te])
    return pred

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--upstream',default='refahi_diag'); ap.add_argument('--power-reps',type=int,default=250); args=ap.parse_args()
    repo=Path(args.upstream)
    _,Xg,Xs,Xh,y,groups,cids=build_dataset(repo,return_ids=True)
    layers=runpy.run_path(str(repo/'common/common/L1L2_cells_ids.py'))
    l1=set(layers['L1_120h']); mask=np.array([c in l1 for c in cids])
    Xg,Xs,Xh,y,groups=Xg[mask],Xs[mask],Xh[mask],y[mask],groups[mask]
    print('L1_120_list_size',len(l1),'eligible',len(y),'ancestor_groups',len(np.unique(groups)))
    splits=list(GroupKFold(5).split(Xg,y,groups))
    for name,X in [('geometry',Xg),('current_atlas',Xs),('current_plus_96h_history',Xh)]:
        p,a=ridge_oof(X,y,groups,splits); print(name,'nested_ridge_R2',round(r2_score(y,p),6),'MAE',round(mean_absolute_error(y,p),6),'alphas',a)
    for name,X in [('geometry',Xg),('current_atlas',Xs),('current_plus_96h_history',Xh)]:
        p=np.empty(len(y))
        for tr,te in splits:
            m=RandomForestRegressor(n_estimators=500,min_samples_leaf=5,max_features=.7,random_state=17,n_jobs=-1);m.fit(X[tr],y[tr]);p[te]=m.predict(X[te])
        print(name,'rf_R2',round(r2_score(y,p),6),'MAE',round(mean_absolute_error(y,p),6))
    H=Xh[:,Xs.shape[1]:]; pc=fixed_oof(Xs,y,groups,splits); ph=fixed_oof(Xh,y,groups,splits); print('fixed_ridge_history_delta',round(r2_score(y,ph)-r2_score(y,pc),6))
    rng=np.random.default_rng(441); Z=(Xs-Xs.mean(0))/(Xs.std(0)+1e-9); ZH=(H-H.mean(0))/(H.std(0)+1e-9); b=rng.normal(size=Z.shape[1]); b/=np.linalg.norm(b); sig=Z@b; sig=(sig-sig.mean())/sig.std(); hr=ZH[:,0]-Ridge(1).fit(Z,ZH[:,0]).predict(Z); hr=(hr-hr.mean())/(hr.std()+1e-9); sd=np.sqrt(.4/.6)
    def sim(gamma,n):
        out=[]
        for _ in range(n):
            yy=sig+gamma*hr+rng.normal(0,sd,len(y)); out.append(r2_score(yy,fixed_oof(Xh,yy,groups,splits))-r2_score(yy,fixed_oof(Xs,yy,groups,splits)))
        return np.array(out)
    null=sim(0,max(400,args.power_reps)); thr=np.quantile(null,.95); print('known_markov_95_delta',round(float(thr),6))
    for gamma in [.10,.15,.20,.25,.30,.35,.40]:
        alt=sim(gamma,args.power_reps); print('history_effect_sd',gamma,'mean_delta',round(float(alt.mean()),6),'power',round(float(np.mean(alt>thr)),4))

if __name__=='__main__': main()
