import json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error

BASE=Path(__file__).parent; SEED=20260830; FRAMES=[15,20,23,24,25,40]
df=pd.read_csv(BASE/'source_data'/'tric_selected_centroids.csv',dtype={'sequence':str})
df['sequence']=df.sequence.str.zfill(2)
# continuous-label cohort frozen from track metadata
eligible={}
for seq in ('01','02'):
    x=[]
    for line in (BASE/'source_data'/f'{seq}_man_track.txt').read_text().splitlines():
        lab,st,en,par=map(int,line.split())
        if st<=15 and en>=40: x.append(lab)
    eligible[seq]=set(x)
# group-level present center/scale from all gold labels present at frame25
norm={}
for seq in ('01','02'):
    g=df[(df.sequence==seq)&(df.frame==25)]
    center=g[['x_px','y_px']].to_numpy(float).mean(0)
    q=g[['x_px','y_px']].to_numpy(float)-center
    scale=float(np.sqrt(np.mean(np.sum(q*q,axis=1))))
    norm[seq]=(center,scale)
rows=[]
for seq in ('01','02'):
    sub=df[(df.sequence==seq)&(df.label.isin(eligible[seq]))]
    for lab,g in sub.groupby('label'):
        if not set(FRAMES).issubset(set(g.frame)): continue
        b={int(r.frame):r for _,r in g.iterrows()}; center,scale=norm[seq]
        rec={'sequence':seq,'label':int(lab),'scale':scale}
        for t in FRAMES:
            rec[f'x{t}']=(float(b[t].x_px)-center[0])/scale
            rec[f'y{t}']=(float(b[t].y_px)-center[1])/scale
            rec[f'lv{t}']=np.log1p(float(b[t].voxel_count))
        rows.append(rec)
D=pd.DataFrame(rows)
P=lambda t:D[[f'x{t}',f'y{t}']].to_numpy(float)
p15,p20,p23,p24,p25,p40=[P(t) for t in FRAMES]
r=np.linalg.norm(p25,axis=1); unit=p25/(r[:,None]+1e-12)
vold=(p20-p15)/5.0; vrecent=p25-p24; acc=p25-2*p24+p23; future=(p40-p25)/15.0
old_speed=np.linalg.norm(vold,axis=1); recent_speed=np.linalg.norm(vrecent,axis=1); accmag=np.linalg.norm(acc,axis=1)
old_rad=(vold*unit).sum(1); recent_rad=(vrecent*unit).sum(1); acc_rad=(acc*unit).sum(1); future_rad=(future*unit).sum(1); future_speed=np.linalg.norm(future,axis=1)
old_dlv=(D.lv20-D.lv15).to_numpy(); recent_dlv=(D.lv25-D.lv24).to_numpy()
S0=np.c_[r,D.lv25.to_numpy()]
S1=np.c_[S0,recent_speed,recent_rad,recent_dlv]
S2=np.c_[S1,accmag,acc_rad]
H=np.c_[vold,old_speed,old_rad,old_dlv]
Ss={'S0':S0,'S1':S1,'S2':S2}; Ys={'future_radial_velocity':future_rad,'future_speed':future_speed}; groups=D.sequence.to_numpy()
models={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=1.0)),'random_forest':RandomForestRegressor(n_estimators=160,min_samples_leaf=4,max_features=.9,random_state=SEED,n_jobs=-1),'extra_trees':ExtraTreesRegressor(n_estimators=160,min_samples_leaf=3,max_features=1.0,random_state=SEED,n_jobs=-1)}
rows_out=[]; dummy=[]
for yn,Y in Ys.items():
    for test in sorted(set(groups)):
        tr=groups!=test; te=groups==test; mu=float(Y[tr].mean()); pred=np.full(te.sum(),mu)
        dummy.append({'outcome':yn,'test_sequence':test,'r2':float(r2_score(Y[te],pred)),'rmse':float(np.sqrt(mean_squared_error(Y[te],pred)))})
    for sn,S in Ss.items():
        for mn,m in models.items():
            for test in sorted(set(groups)):
                tr=groups!=test; te=groups==test
                for tag,X in [('S',S),('S_plus_H',np.c_[S,H])]:
                    md=clone(m); md.fit(X[tr],Y[tr]); pr=md.predict(X[te]); rows_out.append({'outcome':yn,'S_level':sn,'estimator':mn,'test_sequence':test,'features':tag,'r2':float(r2_score(Y[te],pr)),'rmse':float(np.sqrt(mean_squared_error(Y[te],pr))),'n_train':int(tr.sum()),'n_test':int(te.sum())})
R=pd.DataFrame(rows_out); Du=pd.DataFrame(dummy)
summary=R.groupby(['outcome','S_level','estimator','features'])[['r2','rmse']].mean().reset_index(); gains=[]
for (yn,sn,mn),g in summary.groupby(['outcome','S_level','estimator']):
    a=g[g.features=='S'].iloc[0]; b=g[g.features=='S_plus_H'].iloc[0]
    # foldwise signs and adequacy
    fg=R[(R.outcome==yn)&(R.S_level==sn)&(R.estimator==mn)].pivot(index='test_sequence',columns='features',values=['r2','rmse'])
    deltas=fg['r2']['S_plus_H']-fg['r2']['S']
    db=Du[Du.outcome==yn].set_index('test_sequence')
    better_dummy=[float(fg.loc[s,('rmse','S_plus_H')]) < float(db.loc[s,'rmse']) for s in fg.index]
    positive_r2=[float(fg.loc[s,('r2','S_plus_H')])>0 for s in fg.index]
    gains.append({'outcome':yn,'S_level':sn,'estimator':mn,'r2_S':float(a.r2),'r2_S_plus_H':float(b.r2),'r2_gain':float(b.r2-a.r2),'fold_delta_positive_all':bool((deltas>0).all()),'augmented_positive_r2_all_folds':bool(all(positive_r2)),'augmented_beats_train_mean_dummy_all_folds':bool(all(better_dummy)),'fold_deltas':{str(k):float(v) for k,v in deltas.items()}})
G=pd.DataFrame(gains)
# Gate 1 for primary outcome at richest S2: at least two estimators positive R2 in both folds and beat dummy in both folds
q=G[(G.outcome=='future_radial_velocity')&(G.S_level=='S2')]
gate1_estimators=int(((q.augmented_positive_r2_all_folds)&(q.augmented_beats_train_mean_dummy_all_folds)).sum())
gate1=gate1_estimators>=2
gate2_estimators=int(((q.r2_gain>0)&(q.fold_delta_positive_all)).sum()) if gate1 else 0
gate2=(gate2_estimators>=2) if gate1 else False
out=BASE/'results'; out.mkdir(exist_ok=True); R.to_csv(out/'fold_metrics.csv',index=False); Du.to_csv(out/'dummy_baselines.csv',index=False); summary.to_csv(out/'summary.csv',index=False); G.to_csv(out/'history_gains.csv',index=False)
res={'dataset':'CTC Fluo-N3DL-TRIC','cohort_counts':{str(k):int(v) for k,v in D.sequence.value_counts().sort_index().items()},'n_total':int(len(D)),'frames':FRAMES,'time_step_min':1.5,'primary_outcome':'future_radial_velocity','gates':{'absolute_adequacy_gate1_pass':gate1,'estimators_passing_gate1_at_S2':gate1_estimators,'history_stability_gate2_pass':gate2,'estimators_passing_gate2_at_S2':gate2_estimators,'calibration_gate3_run':False},'gains':G.to_dict(orient='records'),'dummy':Du.to_dict(orient='records'),'seed':SEED}
(out/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8'); print(json.dumps(res,indent=2))
