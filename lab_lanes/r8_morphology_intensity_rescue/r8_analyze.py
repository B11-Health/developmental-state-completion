import json, math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE=Path(__file__).parent; ROOT=BASE.parents[1]; OUT=BASE/'results'; SRC=BASE/'source_data'; OUT.mkdir(exist_ok=True)
R7=ROOT/'lab_lanes'/'r7_relational_adequacy_rescue'/'results'
SEED=20260830; EPS=1e-12
MODELS={
 'ridge': make_pipeline(StandardScaler(),Ridge(alpha=1.0)),
 'random_forest': RandomForestRegressor(n_estimators=300,min_samples_leaf=4,max_features=0.8,random_state=SEED,n_jobs=-1),
 'extra_trees': ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,max_features=0.9,random_state=SEED,n_jobs=-1),
}
OUTCOMES=['future_radial_velocity','future_speed']
HISTORY=['old_speed_relcentroid','old_radial_relcentroid','old_tangential_relcentroid','old_log_volume_change_rate']
ID={'label','sequence','organism'}
EXCLUDE_FRAME_FEATURES={'frame','center_x','center_y','center_z','mask_voxels'}
GEOM_BASE=['eigfrac1','eigfrac2','eigfrac3','axis_ratio21','axis_ratio31','bbox_major','bbox_mid','bbox_minor','bbox_ratio_minor_major','proxy_volume_phys','surface_area_phys','projected_area_px','perimeter_px','sphericity','roundness']
INT_BASE=['intensity_mean','intensity_var','intensity_q25','intensity_median','intensity_q75','gradient_mean_inplane','gradient_q75_inplane','boundary_mean_intensity','outside_neighbor_mean_intensity','boundary_contrast_norm','intensity_polarity_norm','intensity_axis_asym_abs']
CHANGE_BASE=['eigfrac1','axis_ratio21','bbox_ratio_minor_major','sphericity','roundness','intensity_mean','intensity_var','intensity_median','gradient_mean_inplane','boundary_contrast_norm','intensity_polarity_norm','intensity_axis_asym_abs']
CONTEXT_BASE=['eigfrac1','axis_ratio21','bbox_ratio_minor_major','sphericity','roundness','intensity_mean','intensity_var','boundary_contrast_norm','intensity_polarity_norm']

def rank01(x): return pd.Series(x).rank(method='average',pct=True).to_numpy(float)
def score(y,p): return {'r2':float(r2_score(y,p)),'rmse':float(math.sqrt(mean_squared_error(y,p)))}

def load_frame_features(slug):
    parts=[]
    for seq in ['01','02']:
      for fr in [23,24,25]:
        q=SRC/f'{slug}_{seq}_{fr:03d}_features.csv'
        if not q.exists(): raise FileNotFoundError(q)
        z=pd.read_csv(q); z['sequence']=z['sequence'].map(lambda v:f'{int(v):02d}'); parts.append(z)
    return pd.concat(parts,ignore_index=True)

def augment(organism):
    slug=organism.lower(); r7file=R7/f'{slug}_analysis_table.csv'; D=pd.read_csv(r7file)
    D['sequence']=D['sequence'].map(lambda v:f'{int(v):02d}')
    F=load_frame_features(slug)
    rows=[]
    for seq,G in D.groupby('sequence',sort=True):
        fseq=F[F.sequence==seq].copy()
        by={fr:fseq[fseq.frame==fr].set_index('label') for fr in [23,24,25]}
        for _,r in G.iterrows():
            lab=int(r.label); out=r.to_dict()
            if any(lab not in by[fr].index for fr in [23,24,25]): raise RuntimeError(f'missing {organism} {seq} label {lab}')
            for c in GEOM_BASE+INT_BASE:
                val=by[25].at[lab,c] if c in by[25].columns else np.nan
                if pd.notna(val): out['r8_'+c]=float(val)
            for c in CHANGE_BASE:
                if c not in by[25].columns: continue
                vals=[]
                for fr in [23,24,25]: vals.append(by[fr].at[lab,c])
                if all(pd.notna(v) for v in vals):
                    out[f'r8_d23_25_{c}']=float(vals[2]-vals[0]); out[f'r8_d24_25_{c}']=float(vals[2]-vals[1])
            rows.append(out)
        # ranks and k5 context added after row assembly
    A=pd.DataFrame(rows)
    # Current-acquisition ranks over all labels visible at frame25, not only focal cohort.
    for seq in sorted(A.sequence.unique()):
        aidx=A.index[A.sequence==seq]; f25=F[(F.sequence==seq)&(F.frame==25)].copy().set_index('label')
        # ranks from entire measured acquisition frame25.
        for c in GEOM_BASE+INT_BASE:
            if c not in f25.columns or f25[c].notna().sum()==0: continue
            ranks=pd.Series(rank01(f25[c]),index=f25.index)
            A.loc[aidx,'r8_rank_'+c]=A.loc[aidx,'label'].map(ranks).to_numpy()
        # k=5 context uses physical/projection mask centroids within released frame25.
        labels=f25.index.to_numpy(int); P=f25[['center_x','center_y','center_z']].to_numpy(float)
        if organism=='Tribolium': P=P[:,:2]
        for ix in aidx:
            lab=int(A.at[ix,'label']); pos=np.where(labels==lab)[0]
            if len(pos)!=1: raise RuntimeError('context focal missing')
            i=pos[0]; dist=np.linalg.norm(P-P[i],axis=1); order=np.argsort(dist); neigh=order[order!=i][:5]
            for c in CONTEXT_BASE:
                if c not in f25.columns: continue
                vals=f25.iloc[neigh][c].to_numpy(float); focal=float(f25.loc[lab,c])
                if np.isfinite(vals).all() and np.isfinite(focal):
                    A.at[ix,f'r8_knn5_{c}_mean']=float(vals.mean()); A.at[ix,f'r8_knn5_{c}_sd']=float(vals.std()); A.at[ix,f'r8_knn5_{c}_contrast']=float(focal-vals.mean())
    return A

def run():
    allmetrics=[]; decisions=[]; schemas={}; datasets={}
    for organism in ['Drosophila','Tribolium']:
        A=augment(organism); A.to_csv(OUT/f'{organism.lower()}_analysis_table.csv',index=False)
        datasets[organism]={'n':len(A),'sequence_counts':{k:int(v) for k,v in A.sequence.value_counts().sort_index().items()}}
        r7_present=[c for c in A.columns if c not in ID and c not in OUTCOMES and c not in HISTORY and not c.startswith('r8_')]
        mask_tokens=('eig','axis_ratio','bbox','volume_phys','surface_area','projected_area','perimeter','sphericity','roundness')
        r8_mask=[c for c in A.columns if c.startswith('r8_') and any(t in c for t in mask_tokens)]
        r8_full=[c for c in A.columns if c.startswith('r8_')]
        mask_cols=sorted(r7_present+r8_mask); full_cols=sorted(r7_present+r8_full)
        # Drop columns that are not defined for organism or are constant/nonfinite.
        def usable(cols):
            z=[]
            for c in cols:
                x=A[c].to_numpy(float)
                if np.isfinite(x).all() and np.nanstd(x)>0: z.append(c)
            return z
        mask_cols=usable(mask_cols); full_cols=usable(full_cols)
        schemas[organism]={'r7_present_n':len(r7_present),'mask_augmented_n':len(mask_cols),'full_augmented_n':len(full_cols),'mask_cols':mask_cols,'full_cols':full_cols}
        groups=A.sequence.to_numpy()
        for outcome in OUTCOMES:
          y=A[outcome].to_numpy(float); passes={m:{} for m in MODELS}
          for rep,cols in [('mask_ablation',mask_cols),('full_primary',full_cols)]:
            X=A[cols].to_numpy(float)
            for test_seq in sorted(A.sequence.unique()):
              tr=groups!=test_seq; te=groups==test_seq; mu=float(y[tr].mean()); naive=np.full(te.sum(),mu); ns=score(y[te],naive)
              allmetrics.append({'organism':organism,'outcome':outcome,'representation':rep,'estimator':'naive_train_mean','test_sequence':test_seq,**ns,'naive_rmse':ns['rmse'],'beats_naive':False,'fold_pass':False})
              for name,model0 in MODELS.items():
                m=clone(model0); m.fit(X[tr],y[tr]); pred=m.predict(X[te]); sc=score(y[te],pred); ok=(sc['r2']>0 and sc['rmse']<ns['rmse'])
                allmetrics.append({'organism':organism,'outcome':outcome,'representation':rep,'estimator':name,'test_sequence':test_seq,**sc,'naive_rmse':ns['rmse'],'beats_naive':bool(sc['rmse']<ns['rmse']),'fold_pass':bool(ok)})
                if rep=='full_primary': passes[name][test_seq]=bool(ok)
          ep=[name for name,q in passes.items() if len(q)==2 and all(q.values())]
          decisions.append({'organism':organism,'outcome':outcome,'gate1_absolute_adequacy_pass':len(ep)>=2,'n_estimators_passing_both_folds':len(ep),'estimators_passing_both_folds':ep,'per_estimator_fold_pass':passes})
    pd.DataFrame(allmetrics).to_csv(OUT/'gate1_fold_metrics.csv',index=False)
    (OUT/'adequacy_decisions.json').write_text(json.dumps(decisions,indent=2),encoding='utf-8')
    (OUT/'feature_schema.json').write_text(json.dumps(schemas,indent=2),encoding='utf-8')
    result={'seed':SEED,'datasets':datasets,'feature_schema':schemas,'decisions':decisions,'history_fit_run':False,'permutation_run':False}
    # Conditional H only for passing task(s); use already-frozen R7 H, no new older image fetch.
    hrows=[]; prows=[]
    for d in decisions:
      if not d['gate1_absolute_adequacy_pass']: continue
      organism=d['organism']; A=pd.read_csv(OUT/f'{organism.lower()}_analysis_table.csv'); A['sequence']=A.sequence.map(lambda v:f'{int(v):02d}')
      cols=schemas[organism]['full_cols']; X=A[cols].to_numpy(float); H=A[HISTORY].to_numpy(float); y=A[d['outcome']].to_numpy(float); groups=A.sequence.to_numpy()
      for test_seq in sorted(A.sequence.unique()):
        tr=groups!=test_seq; te=groups==test_seq
        for name,model0 in MODELS.items():
          m0=clone(model0).fit(X[tr],y[tr]); m1=clone(model0).fit(np.c_[X[tr],H[tr]],y[tr]); r0=r2_score(y[te],m0.predict(X[te])); r1=r2_score(y[te],m1.predict(np.c_[X[te],H[te]])); hrows.append({'organism':organism,'outcome':d['outcome'],'test_sequence':test_seq,'estimator':name,'r2_s':r0,'r2_s_plus_h':r1,'delta_r2':r1-r0})
      # Gate2 mirrors R7: positive both folds and mean delta >= .02 for >=2 estimators.
      hd=pd.DataFrame([q for q in hrows if q['organism']==organism and q['outcome']==d['outcome']]); good=[]
      for name in MODELS:
        z=hd[hd.estimator==name];
        if len(z)==2 and (z.delta_r2>0).all() and z.delta_r2.mean()>=.02: good.append(name)
      d['gate2_history_pass']=len(good)>=2; d['gate2_estimators']=good
      if d['gate2_history_pass']:
        rng=np.random.RandomState(SEED)
        for test_seq in sorted(A.sequence.unique()):
          tr=groups!=test_seq; te=groups==test_seq
          for name,model0 in MODELS.items():
            m0=clone(model0).fit(X[tr],y[tr]); base=r2_score(y[te],m0.predict(X[te])); obs=hd[(hd.test_sequence==test_seq)&(hd.estimator==name)].delta_r2.iloc[0]
            null=[]
            for b in range(200):
              hp=H[tr].copy(); hp=hp[rng.permutation(len(hp))]
              mm=clone(model0).fit(np.c_[X[tr],hp],y[tr]); rr=r2_score(y[te],mm.predict(np.c_[X[te],H[te]])); null.append(rr-base)
            prows.append({'organism':organism,'outcome':d['outcome'],'test_sequence':test_seq,'estimator':name,'observed_delta_r2':float(obs),'null_mean':float(np.mean(null)),'null_sd':float(np.std(null)),'null_ge_observed_fraction':float(np.mean(np.array(null)>=obs))})
    if hrows:
      pd.DataFrame(hrows).to_csv(OUT/'history_fold_metrics.csv',index=False); result['history_fit_run']=True
    if prows:
      pd.DataFrame(prows).to_csv(OUT/'permutation_results.csv',index=False); result['permutation_run']=True
    (OUT/'adequacy_decisions.json').write_text(json.dumps(decisions,indent=2),encoding='utf-8')
    result['decisions']=decisions; (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(decisions,indent=2))
if __name__=='__main__': run()
