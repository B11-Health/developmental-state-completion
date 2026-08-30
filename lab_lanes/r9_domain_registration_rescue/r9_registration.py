import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.covariance import LedoitWolf
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer, StandardScaler

BASE=Path(__file__).parent
ROOT=BASE.parents[1]
R8=ROOT/'lab_lanes'/'r8_morphology_intensity_rescue'/'results'
OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)
SEED=20260830; EPS=1e-9
OUTCOMES=['future_radial_velocity','future_speed']
MODELS={
 'ridge': make_pipeline(StandardScaler(),Ridge(alpha=1.0)),
 'random_forest': RandomForestRegressor(n_estimators=300,min_samples_leaf=4,max_features=0.8,random_state=SEED,n_jobs=-1),
 'extra_trees': ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,max_features=0.9,random_state=SEED,n_jobs=-1),
}
PRIMARY={'inductive_invariant_panel','transductive_domain_percentile'}
SECONDARY={'inductive_source_quantile','inductive_source_pca30','transductive_robust_z','transductive_coral'}


def score(y,p):
    return {'r2':float(r2_score(y,p)),'rmse':float(math.sqrt(mean_squared_error(y,p)))}


def invariant_cols(cols):
    exact={'radius_norm','radius_rank','volume_rank','recent_radial_relcentroid','recent_speed_relcentroid','recent_tangential_relcentroid','accel_mag_relcentroid','accel_radial_relcentroid','accel_tangential_relcentroid','focal_neighbor_velocity_alignment'}
    tokens=('rank_','_rank','ratio','eigfrac','_norm','contrast','log_density','alignment','polarity','asym','relcentroid')
    return [c for c in cols if c in exact or any(t in c for t in tokens)]


def percentile_transform(X):
    D=pd.DataFrame(X)
    return D.rank(axis=0,method='average',pct=True).to_numpy(float)


def robust_z(X):
    med=np.median(X,axis=0)
    q25=np.quantile(X,.25,axis=0); q75=np.quantile(X,.75,axis=0)
    scale=q75-q25
    sd=np.std(X,axis=0)
    scale=np.where(scale>EPS,scale,np.where(sd>EPS,sd,1.0))
    return (X-med)/scale


def sym_sqrt(C, inverse=False):
    v,Q=np.linalg.eigh((C+C.T)/2)
    v=np.maximum(v,1e-8)
    d=1/np.sqrt(v) if inverse else np.sqrt(v)
    return (Q*d)@Q.T


def coral_source_to_target(Xs,Xt):
    ms=Xs.mean(axis=0); mt=Xt.mean(axis=0)
    Xsc=Xs-ms; Xtc=Xt-mt
    Cs=LedoitWolf().fit(Xsc).covariance_
    Ct=LedoitWolf().fit(Xtc).covariance_
    A=sym_sqrt(Cs,inverse=True)@sym_sqrt(Ct,inverse=False)
    return Xsc@A+mt, Xt.copy()


def transform_variant(name,Xtr,Xte):
    if name in ('r8_full_reference','inductive_invariant_panel'):
        return Xtr.copy(),Xte.copy()
    if name=='transductive_domain_percentile':
        return percentile_transform(Xtr),percentile_transform(Xte)
    if name=='transductive_robust_z':
        return robust_z(Xtr),robust_z(Xte)
    if name=='transductive_coral':
        return coral_source_to_target(Xtr,Xte)
    if name=='inductive_source_quantile':
        q=QuantileTransformer(n_quantiles=min(100,len(Xtr)),output_distribution='normal',random_state=SEED,subsample=100000)
        return q.fit_transform(Xtr),q.transform(Xte)
    if name=='inductive_source_pca30':
        ncomp=max(1,min(30,len(Xtr)-1,Xtr.shape[1]))
        pipe=make_pipeline(StandardScaler(),PCA(n_components=ncomp,whiten=True,random_state=SEED))
        return pipe.fit_transform(Xtr),pipe.transform(Xte)
    raise KeyError(name)


def run():
    schema=json.loads((R8/'feature_schema.json').read_text(encoding='utf-8'))
    metrics=[]; controls=[]; decisions=[]; schemas={}
    variants=['r8_full_reference','inductive_invariant_panel','transductive_domain_percentile','inductive_source_quantile','inductive_source_pca30','transductive_robust_z','transductive_coral']
    for organism in ['Drosophila','Tribolium']:
        A=pd.read_csv(R8/f'{organism.lower()}_analysis_table.csv')
        A['sequence']=A['sequence'].map(lambda v:f'{int(v):02d}')
        full=list(schema[organism]['full_cols']); inv=invariant_cols(full)
        schemas[organism]={'full_n':len(full),'invariant_n':len(inv),'invariant_cols':inv}
        groups=A.sequence.to_numpy()
        for outcome in OUTCOMES:
            y=A[outcome].to_numpy(float)
            for variant in variants:
                cols=inv if variant=='inductive_invariant_panel' else full
                X=A[cols].to_numpy(float)
                passmap={m:{} for m in MODELS}
                for fold_i,test_seq in enumerate(sorted(A.sequence.unique())):
                    tr=groups!=test_seq; te=groups==test_seq
                    Xtr,Xte=transform_variant(variant,X[tr],X[te])
                    yytr=y[tr]; yyte=y[te]
                    naive=np.full(te.sum(),float(yytr.mean())); ns=score(yyte,naive)
                    metrics.append({'organism':organism,'outcome':outcome,'representation':variant,'track':'primary' if variant in PRIMARY else ('secondary' if variant in SECONDARY else 'reference'),'estimator':'naive_train_mean','test_sequence':test_seq,**ns,'naive_rmse':ns['rmse'],'beats_naive':False,'fold_pass':False,'n_features':Xtr.shape[1]})
                    for model_i,(name,model0) in enumerate(MODELS.items()):
                        m=clone(model0); m.fit(Xtr,yytr); pred=m.predict(Xte); sc=score(yyte,pred); ok=(sc['r2']>0 and sc['rmse']<ns['rmse'])
                        metrics.append({'organism':organism,'outcome':outcome,'representation':variant,'track':'primary' if variant in PRIMARY else ('secondary' if variant in SECONDARY else 'reference'),'estimator':name,'test_sequence':test_seq,**sc,'naive_rmse':ns['rmse'],'beats_naive':bool(sc['rmse']<ns['rmse']),'fold_pass':bool(ok),'n_features':Xtr.shape[1]})
                        passmap[name][test_seq]=bool(ok)
                        if variant in PRIMARY:
                            rng=np.random.RandomState(SEED+1000*fold_i+37*model_i+(0 if organism=='Drosophila' else 101))
                            perm=rng.permutation(len(Xte)); neg=m.predict(Xte[perm]); nsc=score(yyte,neg)
                            controls.append({'organism':organism,'outcome':outcome,'representation':variant,'estimator':name,'test_sequence':test_seq,**nsc,'control':'target_row_permutation'})
                ep=[name for name,q in passmap.items() if len(q)==2 and all(q.values())]
                decisions.append({'organism':organism,'outcome':outcome,'representation':variant,'track':'primary' if variant in PRIMARY else ('secondary' if variant in SECONDARY else 'reference'),'gate1_pass':len(ep)>=2,'n_estimators_passing_both_folds':len(ep),'estimators_passing_both_folds':ep,'per_estimator_fold_pass':passmap})
    M=pd.DataFrame(metrics); C=pd.DataFrame(controls); D=pd.DataFrame(decisions)
    M.to_csv(OUT/'gate1_fold_metrics.csv',index=False); C.to_csv(OUT/'primary_negative_controls.csv',index=False); D.to_csv(OUT/'representation_decisions.csv',index=False)
    primary=[d for d in decisions if d['track']=='primary' and d['gate1_pass']]
    secondary=[d for d in decisions if d['track']=='secondary' and d['gate1_pass']]
    result={'seed':SEED,'frozen_from_r8':True,'primary_tracks':sorted(PRIMARY),'secondary_tracks':sorted(SECONDARY),'feature_schema':schemas,'decisions':decisions,'primary_gate_passes':primary,'secondary_gate_passes':secondary,'history_fit_run':False,'calibration_run':False,'permutation_history_run':False}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (OUT/'feature_schema.json').write_text(json.dumps(schemas,indent=2),encoding='utf-8')
    print(json.dumps({'primary_gate_passes':primary,'secondary_gate_passes':secondary},indent=2))



def run_job(organism,outcome):
    schema=json.loads((R8/'feature_schema.json').read_text(encoding='utf-8'))
    A=pd.read_csv(R8/f'{organism.lower()}_analysis_table.csv'); A['sequence']=A['sequence'].map(lambda v:f'{int(v):02d}')
    full=list(schema[organism]['full_cols']); inv=invariant_cols(full); groups=A.sequence.to_numpy(); y=A[outcome].to_numpy(float)
    variants=['r8_full_reference','inductive_invariant_panel','transductive_domain_percentile','inductive_source_quantile','inductive_source_pca30','transductive_robust_z','transductive_coral']
    metrics=[]; controls=[]; decisions=[]
    for variant in variants:
        cols=inv if variant=='inductive_invariant_panel' else full; X=A[cols].to_numpy(float); passmap={m:{} for m in MODELS}
        for fold_i,test_seq in enumerate(sorted(A.sequence.unique())):
            tr=groups!=test_seq; te=groups==test_seq; Xtr,Xte=transform_variant(variant,X[tr],X[te]); yytr=y[tr]; yyte=y[te]
            naive=np.full(te.sum(),float(yytr.mean())); ns=score(yyte,naive); track='primary' if variant in PRIMARY else ('secondary' if variant in SECONDARY else 'reference')
            metrics.append({'organism':organism,'outcome':outcome,'representation':variant,'track':track,'estimator':'naive_train_mean','test_sequence':test_seq,**ns,'naive_rmse':ns['rmse'],'beats_naive':False,'fold_pass':False,'n_features':Xtr.shape[1]})
            for model_i,(name,model0) in enumerate(MODELS.items()):
                m=clone(model0); m.fit(Xtr,yytr); pred=m.predict(Xte); sc=score(yyte,pred); ok=(sc['r2']>0 and sc['rmse']<ns['rmse'])
                metrics.append({'organism':organism,'outcome':outcome,'representation':variant,'track':track,'estimator':name,'test_sequence':test_seq,**sc,'naive_rmse':ns['rmse'],'beats_naive':bool(sc['rmse']<ns['rmse']),'fold_pass':bool(ok),'n_features':Xtr.shape[1]}); passmap[name][test_seq]=bool(ok)
                if variant in PRIMARY:
                    rng=np.random.RandomState(SEED+1000*fold_i+37*model_i+(0 if organism=='Drosophila' else 101)); neg=m.predict(Xte[rng.permutation(len(Xte))]); nsc=score(yyte,neg)
                    controls.append({'organism':organism,'outcome':outcome,'representation':variant,'estimator':name,'test_sequence':test_seq,**nsc,'control':'target_row_permutation'})
        ep=[name for name,q in passmap.items() if len(q)==2 and all(q.values())]
        decisions.append({'organism':organism,'outcome':outcome,'representation':variant,'track':'primary' if variant in PRIMARY else ('secondary' if variant in SECONDARY else 'reference'),'gate1_pass':len(ep)>=2,'n_estimators_passing_both_folds':len(ep),'estimators_passing_both_folds':ep,'per_estimator_fold_pass':passmap})
    stem=f'{organism.lower()}_{outcome}'; pd.DataFrame(metrics).to_csv(OUT/f'job_{stem}_metrics.csv',index=False); pd.DataFrame(controls).to_csv(OUT/f'job_{stem}_controls.csv',index=False); (OUT/f'job_{stem}_decisions.json').write_text(json.dumps(decisions,indent=2),encoding='utf-8')
    print(json.dumps({'organism':organism,'outcome':outcome,'passes':[d for d in decisions if d['gate1_pass']]},indent=2))


def aggregate_jobs():
    mets=[]; ctrls=[]; decisions=[]
    for organism in ['Drosophila','Tribolium']:
        for outcome in OUTCOMES:
            stem=f'{organism.lower()}_{outcome}'; mets.append(pd.read_csv(OUT/f'job_{stem}_metrics.csv')); ctrls.append(pd.read_csv(OUT/f'job_{stem}_controls.csv')); decisions.extend(json.loads((OUT/f'job_{stem}_decisions.json').read_text(encoding='utf-8')))
    M=pd.concat(mets,ignore_index=True); C=pd.concat(ctrls,ignore_index=True); D=pd.DataFrame(decisions); M.to_csv(OUT/'gate1_fold_metrics.csv',index=False); C.to_csv(OUT/'primary_negative_controls.csv',index=False); D.to_csv(OUT/'representation_decisions.csv',index=False)
    schema0=json.loads((R8/'feature_schema.json').read_text(encoding='utf-8')); schemas={}
    for organism in ['Drosophila','Tribolium']:
        full=list(schema0[organism]['full_cols']); inv=invariant_cols(full); schemas[organism]={'full_n':len(full),'invariant_n':len(inv),'invariant_cols':inv}
    primary=[d for d in decisions if d['track']=='primary' and d['gate1_pass']]; secondary=[d for d in decisions if d['track']=='secondary' and d['gate1_pass']]
    result={'seed':SEED,'frozen_from_r8':True,'primary_tracks':sorted(PRIMARY),'secondary_tracks':sorted(SECONDARY),'feature_schema':schemas,'decisions':decisions,'primary_gate_passes':primary,'secondary_gate_passes':secondary,'history_fit_run':False,'calibration_run':False,'permutation_history_run':False}; (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); (OUT/'feature_schema.json').write_text(json.dumps(schemas,indent=2),encoding='utf-8'); print(json.dumps({'primary_gate_passes':primary,'secondary_gate_passes':secondary},indent=2))

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--organism',choices=['Drosophila','Tribolium']); ap.add_argument('--outcome',choices=OUTCOMES); ap.add_argument('--aggregate',action='store_true'); args=ap.parse_args()
    if args.aggregate: aggregate_jobs()
    elif args.organism and args.outcome: run_job(args.organism,args.outcome)
    else: raise SystemExit('use --organism ... --outcome ... or --aggregate')
