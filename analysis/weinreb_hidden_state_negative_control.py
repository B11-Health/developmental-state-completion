import argparse, gzip, math, urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import mmread
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE='https://kleintools.hms.harvard.edu/paper_websites/state_fate2020/'
FILES=['stateFate_inVitro_metadata.txt.gz','stateFate_inVitro_clone_matrix.mtx.gz']
MAJOR={'Neutrophil','Monocyte','Baso'}

def ensure(data_dir):
    data_dir.mkdir(parents=True,exist_ok=True)
    for f in FILES:
        out=data_dir/f
        if not out.exists():
            print('downloading',f)
            urllib.request.urlretrieve(BASE+f,out)

def dominant_mature(w,mature):
    vc=w[w['Cell type annotation'].isin(mature)]['Cell type annotation'].value_counts()
    if len(vc)==0 or (len(vc)>1 and vc.iloc[0]==vc.iloc[1]): return None
    return vc.index[0]

def cmi(a,b,s):
    n=len(a); out=0.0
    for z in np.unique(s):
        ix=np.where(s==z)[0]; nz=len(ix)
        if nz<2: continue
        for x in np.unique(a[ix]):
            for y in np.unique(b[ix]):
                nxy=np.sum((a[ix]==x)&(b[ix]==y)); nx=np.sum(a[ix]==x); ny=np.sum(b[ix]==y)
                if nxy: out+=(nxy/n)*math.log2((nxy*nz)/(nx*ny))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data-dir',default='klein_data')
    ap.add_argument('--permutations',type=int,default=3000)
    ap.add_argument('--cv-repeats',type=int,default=40)
    args=ap.parse_args(); data=Path(args.data_dir); ensure(data)
    md=pd.read_csv(data/FILES[0],sep='\t')
    A=mmread(data/FILES[1]).tocsc()
    mature=set(md['Cell type annotation'].unique())-{'Undifferentiated'}

    # Cross-well fate-set concordance at day 6.
    rec=[]
    strict=[]
    for j in range(A.shape[1]):
        sub=md.iloc[A[:,j].indices]
        d2=sub[sub['Time point']==2.0]
        d6=sub[sub['Time point']==6.0]
        w1,w2=d6[d6.Well==1],d6[d6.Well==2]
        if len(w1) and len(w2):
            s1=frozenset(x for x in w1['Cell type annotation'] if x in mature)
            s2=frozenset(x for x in w2['Cell type annotation'] if x in mature)
            rec.append((s1,s2))
            if len(d2):
                f1,f2=dominant_mature(w1,mature),dominant_mature(w2,mature)
                if f1 and f2:
                    strict.append((d2['SPRING-x'].mean(),d2['SPRING-y'].mean(),d2['Starting population'].mode().iloc[0],f1,f2))
    rec=pd.DataFrame(rec,columns=['w1','w2'])
    good=rec[(rec.w1.map(len)>0)&(rec.w2.map(len)>0)].reset_index(drop=True)
    rng=np.random.default_rng(20260829)
    obs=float(np.mean(good.w1==good.w2)); null=[]; w2=good.w2.to_numpy()
    for _ in range(5000): null.append(np.mean(good.w1.to_numpy()==rng.permutation(w2)))
    null=np.array(null)
    print('split_clones_both_day6',len(rec),'mature_nonempty',len(good))
    print('exact_fate_set_concordance',round(obs,6),'perm_mean',round(float(null.mean()),6),'perm_q95',round(float(np.quantile(null,.95)),6),'p',round(float((1+np.sum(null>=obs))/(len(null)+1)),6))

    R=pd.DataFrame(strict,columns=['x','y','start','f1','f2'])
    R=R[R.f1.isin(MAJOR)&R.f2.isin(MAJOR)].reset_index(drop=True)
    print('strict_3class_n',len(R),'dominant_fate_agreement',round(float(np.mean(R.f1==R.f2)),6))

    # Repeated held-out classifier: current day-2 landscape vs current + sister-well fate.
    X0=R[['x','y','start']]; X1=R[['x','y','start','f1']]; y=R.f2.to_numpy()
    cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=args.cv_repeats,random_state=20260829)
    rows=[]
    for tr,te in cv.split(X0,y):
        for tag,X,cats in [('state',X0,['start']),('state+sister',X1,['start','f1'])]:
            pre=ColumnTransformer([('num',StandardScaler(),['x','y']),('cat',OneHotEncoder(handle_unknown='ignore'),cats)])
            model=Pipeline([('pre',pre),('lr',LogisticRegression(C=1,max_iter=2000,class_weight='balanced'))])
            model.fit(X.iloc[tr],y[tr]); pred=model.predict(X.iloc[te]); prob=model.predict_proba(X.iloc[te])
            rows.append((tag,accuracy_score(y[te],pred),balanced_accuracy_score(y[te],pred),log_loss(y[te],prob,labels=model.named_steps['lr'].classes_)))
    cvres=pd.DataFrame(rows,columns=['model','accuracy','balanced_accuracy','log_loss'])
    print(cvres.groupby('model').mean().round(6).to_string())
    a=cvres[cvres.model=='state'].reset_index(drop=True); b=cvres[cvres.model=='state+sister'].reset_index(drop=True)
    print('paired_gain_accuracy',round(float((b.accuracy-a.accuracy).mean()),6),'balanced_accuracy',round(float((b.balanced_accuracy-a.balanced_accuracy).mean()),6),'log_loss_reduction',round(float((a.log_loss-b.log_loss).mean()),6))

    # Conditional mutual information of separated sister fates given coarse current-state neighborhoods.
    labels=sorted(MAJOR); li={x:i for i,x in enumerate(labels)}
    aa=np.array([li[x] for x in R.f1]); bb=np.array([li[x] for x in R.f2])
    xy=StandardScaler().fit_transform(R[['x','y']]); st=OneHotEncoder(sparse_output=False).fit_transform(R[['start']]); Z=np.c_[xy,st]
    for k in [4,6,8,10]:
        s=KMeans(k,random_state=17,n_init=50).fit_predict(Z); observed=cmi(aa,bb,s); pn=[]
        for _ in range(args.permutations):
            ap=aa.copy()
            for z in np.unique(s):
                ix=np.where(s==z)[0]; ap[ix]=rng.permutation(ap[ix])
            pn.append(cmi(ap,bb,s))
        pn=np.array(pn); p=(1+np.sum(pn>=observed))/(len(pn)+1)
        print('state_bins',k,'CMI_bits',round(observed,6),'null_mean',round(float(pn.mean()),6),'null_q95',round(float(np.quantile(pn,.95)),6),'p',round(float(p),6))

if __name__=='__main__': main()
