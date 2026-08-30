import json, hashlib
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss, accuracy_score

SEED=20260830
rng=np.random.default_rng(SEED)
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'source_data'; OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
META=SRC/'GSE167135_Smartseq2_FACSmetadata.csv.gz'
FILES=[SRC/'GSE167135_ATML1p_Smartseq2_TPM.csv.gz',SRC/'GSE167135_TMMp_Smartseq2_TPM.csv.gz']
H_COLS=['log2(P1.FSC.A.Median)','log2(P1.FSC.W.Median)','log2(P1.FSC.H.Median)','log2(P1.SSC.A.Median)','log2(P1.SSC.W.Median)','log2(P1.SSC.H.Median)','log2(P1.FITC.A.Median)']

def load_matrix(path):
    x=pd.read_csv(path,index_col=0,engine='python')
    x=x.drop(index='Pool')
    x=x.apply(pd.to_numeric,errors='coerce').fillna(0.0)
    return x.T

md=pd.read_csv(META)
Xa=load_matrix(FILES[0]); Xt=load_matrix(FILES[1])
X=pd.concat([Xa,Xt],axis=0,join='inner')
md=md.set_index('fastq_file_name').loc[X.index].copy()
md['reporter']=(md['Pool'].str.startswith('TMMp')).astype(int)
md['pool_group']=md['Pool'].str.extract(r'(pool_[12])', expand=False)
# Gene expression is present state S; FACS is auxiliary present measurement H. This is intentionally a proxy task, not a future-outcome claim.
X=np.log1p(X.astype(float))
y=md['reporter'].to_numpy(int); groups=md['pool_group'].to_numpy(); H=md[H_COLS].to_numpy(float)

estimators={
 'logistic': lambda: LogisticRegression(max_iter=3000,C=1.0,solver='liblinear',random_state=SEED),
 'random_forest': lambda: RandomForestClassifier(n_estimators=300,min_samples_leaf=4,max_features='sqrt',class_weight='balanced',random_state=SEED,n_jobs=-1),
 'hist_gb': lambda: HistGradientBoostingClassifier(max_iter=250,max_leaf_nodes=15,l2_regularization=1.0,random_state=SEED),
}

def prep_fold(train,test,H_override=None):
    Xtr=X.iloc[train].to_numpy(); Xte=X.iloc[test].to_numpy()
    # train-only gene selection by variance
    var=Xtr.var(axis=0); k=min(300, Xtr.shape[1]); idx=np.argpartition(var,-k)[-k:]
    sx=StandardScaler().fit(Xtr[:,idx]); Ztr0=sx.transform(Xtr[:,idx]); Zte0=sx.transform(Xte[:,idx])
    ncomp=min(20,Ztr0.shape[0]-2,Ztr0.shape[1])
    pca=PCA(n_components=ncomp,random_state=SEED).fit(Ztr0)
    Str=pca.transform(Ztr0); Ste=pca.transform(Zte0)
    HH=H if H_override is None else H_override
    sh=StandardScaler().fit(HH[train]); Htr=sh.transform(HH[train]); Hte=sh.transform(HH[test])
    return Str,Ste,Htr,Hte,idx,pca.explained_variance_ratio_.sum()

def score_model(model,Xtr,ytr,Xte,yte):
    model.fit(Xtr,ytr); p=model.predict_proba(Xte)[:,1]
    return {'auc':float(roc_auc_score(yte,p)),'logloss':float(log_loss(yte,p,labels=[0,1])),'brier':float(brier_score_loss(yte,p)),'accuracy':float(accuracy_score(yte,p>=0.5))},p

rows=[]; pred_rows=[]
unique_groups=sorted(np.unique(groups))
for test_group in unique_groups:
    test=np.where(groups==test_group)[0]; train=np.where(groups!=test_group)[0]
    Str,Ste,Htr,Hte,idx,ev=prep_fold(train,test)
    for name,make in estimators.items():
        for feature_set,Atr,Ate in [('S',Str,Ste),('S_plus_H',np.c_[Str,Htr],np.c_[Ste,Hte])]:
            met,p=score_model(make(),Atr,y[train],Ate,y[test])
            rows.append({'fold_group':test_group,'estimator':name,'feature_set':feature_set,'n_train':len(train),'n_test':len(test),'pca_var':ev,**met})
            for ii,pp in zip(test,p): pred_rows.append({'sample':X.index[ii],'fold_group':test_group,'estimator':name,'feature_set':feature_set,'y':int(y[ii]),'p':float(pp)})
metrics=pd.DataFrame(rows); metrics.to_csv(OUT/'cv_fold_metrics.csv',index=False)
preds=pd.DataFrame(pred_rows); preds.to_csv(OUT/'heldout_predictions.csv',index=False)
summary=metrics.groupby(['estimator','feature_set'])[['auc','logloss','brier','accuracy']].mean().reset_index()
wide=summary.pivot(index='estimator',columns='feature_set',values=['auc','logloss','brier','accuracy'])
gains=[]
for est in estimators:
    a=summary[(summary.estimator==est)&(summary.feature_set=='S')].iloc[0]
    b=summary[(summary.estimator==est)&(summary.feature_set=='S_plus_H')].iloc[0]
    gains.append({'estimator':est,'auc_gain':b.auc-a.auc,'logloss_improvement':a.logloss-b.logloss,'brier_improvement':a.brier-b.brier,'accuracy_gain':b.accuracy-a.accuracy})
gains=pd.DataFrame(gains); gains.to_csv(OUT/'incremental_gains.csv',index=False)
summary.to_csv(OUT/'summary.csv',index=False)

# Group-preserving H-permutation null for the logistic incremental AUC gain.
null=[]
for rep in range(20):
    Hp=H.copy()
    for g in unique_groups:
        ix=np.where(groups==g)[0]; Hp[ix]=Hp[rng.permutation(ix)]
    fold_g=[]
    for test_group in unique_groups:
        test=np.where(groups==test_group)[0]; train=np.where(groups!=test_group)[0]
        Str,Ste,Htr,Hte,_,_=prep_fold(train,test,H_override=Hp)
        m0,p0=score_model(estimators['logistic'](),Str,y[train],Ste,y[test])
        m1,p1=score_model(estimators['logistic'](),np.c_[Str,Htr],y[train],np.c_[Ste,Hte],y[test])
        fold_g.append(m1['auc']-m0['auc'])
    null.append({'rep':rep,'mean_auc_gain':float(np.mean(fold_g))})
pd.DataFrame(null).to_csv(OUT/'permutation_null.csv',index=False)

# Sensitivity calibration: within each fold, construct labels from train-fitted S only (complete)
# or from S plus an orthogonalized FACS direction (incomplete). Report held-out gain using logistic models.
cal=[]
for mode in ['known_complete','known_incomplete']:
  for rep in range(20):
    fold_gain=[]
    for test_group in unique_groups:
      test=np.where(groups==test_group)[0]; train=np.where(groups!=test_group)[0]
      Str,Ste,Htr,Hte,_,_=prep_fold(train,test)
      beta=rng.normal(size=Str.shape[1]); beta/=np.linalg.norm(beta)+1e-12
      # stable S signal
      ls_tr=Str@beta; ls_te=Ste@beta
      if mode=='known_incomplete':
        # first FACS axis residualized against S on training data; apply train relation to test
        coef=np.linalg.lstsq(np.c_[np.ones(len(train)),Str],Htr[:,0],rcond=None)[0]
        rh_tr=Htr[:,0]-np.c_[np.ones(len(train)),Str]@coef
        rh_te=Hte[:,0]-np.c_[np.ones(len(test)),Ste]@coef
        ls_tr=ls_tr+1.25*rh_tr; ls_te=ls_te+1.25*rh_te
      # threshold chosen on training latent score only; labels deterministic for clean sensitivity audit
      thr=np.median(ls_tr); yytr=(ls_tr>thr).astype(int); yyte=(ls_te>thr).astype(int)
      if len(np.unique(yyte))<2: continue
      m0,_=score_model(estimators['logistic'](),Str,yytr,Ste,yyte)
      m1,_=score_model(estimators['logistic'](),np.c_[Str,Htr],yytr,np.c_[Ste,Hte],yyte)
      fold_gain.append(m1['auc']-m0['auc'])
    if fold_gain: cal.append({'mode':mode,'rep':rep,'mean_auc_gain':float(np.mean(fold_gain))})
caldf=pd.DataFrame(cal); caldf.to_csv(OUT/'sensitivity_calibration.csv',index=False)

hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [META,*FILES]}
res={
 'dataset':'GSE167135','n_cells':int(len(y)),'n_genes':int(X.shape[1]),'groups':md['Pool'].value_counts().to_dict(),
 'task':'reporter-defined lineage-enrichment class (TMMp vs ATML1p); S=transcriptome PCs; H=FACS present measurements',
 'not_future_outcome':True,'grouping':'leave-one-matched-pool-index-out (2 folds; each fold contains TMMp and ATML1p)','train_only_preprocessing':True,
 'gains':gains.to_dict(orient='records'),
 'permutation_null_mean':float(pd.DataFrame(null).mean_auc_gain.mean()),
 'permutation_null_max':float(pd.DataFrame(null).mean_auc_gain.max()),
 'calibration':caldf.groupby('mode').mean_auc_gain.agg(['mean','std','min','max']).to_dict(orient='index'),
 'input_sha256':hashes,'seed':SEED
}
(OUT/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
