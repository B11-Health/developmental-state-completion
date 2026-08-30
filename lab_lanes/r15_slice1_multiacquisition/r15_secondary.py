import json
from pathlib import Path
import numpy as np
from sklearn.base import clone
from sklearn.preprocessing import StandardScaler
import r15_pilot as r

BASE=Path(__file__).parent
TEST='DS0035'

def main():
    tr=sum([r.load(x) for x in r.TRAIN],[]); te=r.load(TEST)
    Xs=r.stack(tr,'S'); Xh=r.stack(tr,'H'); Y=r.stack(tr,'Y'); Xst=r.stack(te,'S'); Xht=r.stack(te,'H'); Yt=r.stack(te,'Y')
    sx=StandardScaler().fit(Xs); hx=StandardScaler().fit(Xh); yy=StandardScaler().fit(Y)
    S=sx.transform(Xs); H=hx.transform(Xh); T=sx.transform(Xst); HT=hx.transform(Xht); Z=yy.transform(Y); Zt=yy.transform(Yt); naive=np.zeros_like(Zt)
    rows=[]
    for name,m0 in r.MODELS.items():
        m=clone(m0).fit(S,Z); q=r.score(Zt,m.predict(T),naive); q.update({'estimator':name,'s_fold_pass':bool(q['r2_vector']>0 and q['rmse_vector']<q['naive_rmse_vector'])}); rows.append(q)
    gate1=sum(x['s_fold_pass'] for x in rows)>=2
    out={'training_embryos':r.TRAIN,'secondary_validation':TEST,'marker_domain':'Lamin #4','gate1_pass':gate1,'s_only':rows}
    if gate1:
        hist=[]
        for name,m0 in r.MODELS.items():
            ms=clone(m0).fit(S,Z); mh=clone(m0).fit(np.c_[S,H],Z)
            ss=r.score(Zt,ms.predict(T),naive); sh=r.score(Zt,mh.predict(np.c_[T,HT]),naive)
            hist.append({'estimator':name,'r2_s':ss['r2_vector'],'r2_s_plus_h':sh['r2_vector'],'delta_r2_vector':sh['r2_vector']-ss['r2_vector'],'s_plus_h_rmse':sh['rmse_vector'],'naive_rmse':sh['naive_rmse_vector']})
        out['history']=hist
    (BASE/'R15_SECONDARY_RESULT.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
