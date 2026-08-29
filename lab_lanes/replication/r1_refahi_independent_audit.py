import importlib.util, json, hashlib, subprocess
from pathlib import Path
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT.parent/"refahi_diag"
spec=importlib.util.spec_from_file_location("rep",ROOT/"analysis/refahi_state_completion_replication.py")
rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep); rep.ROOT=UP

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def model(name):
    if name=="ridge": return make_pipeline(StandardScaler(),Ridge(alpha=10.0))
    if name=="extra": return ExtraTreesRegressor(n_estimators=30,min_samples_leaf=5,max_features=.7,random_state=31,n_jobs=-1)
    if name=="histgb": return HistGradientBoostingRegressor(max_iter=100,max_leaf_nodes=15,min_samples_leaf=20,l2_regularization=2.0,random_state=31)

def score(df,genes,name,seed,pc1=False,history=False):
    y=df.target.to_numpy(float); g=df.group.to_numpy(); geom=[f"cur_{k}" for k in ["logv","x","y","z"]]; cur=[f"cur_g_{x}" for x in genes]; hist=[f"hist_{k}" for k in ["logv","x","y","z"]]+[f"hist_g_{x}" for x in genes]
    pred=np.full(len(y),np.nan); overlaps=[]
    for tr,te in GroupKFold(5,shuffle=True,random_state=seed).split(np.zeros((len(y),1)),y,g):
        overlaps.append(len(set(g[tr]) & set(g[te])))
        if pc1:
            from sklearn.decomposition import PCA
            q=PCA(n_components=1).fit(df.iloc[tr][cur].to_numpy(float)); Xtr=np.hstack([df.iloc[tr][geom].to_numpy(float),q.transform(df.iloc[tr][cur].to_numpy(float))]); Xte=np.hstack([df.iloc[te][geom].to_numpy(float),q.transform(df.iloc[te][cur].to_numpy(float))])
        else:
            cols=geom+cur; Xtr=df.iloc[tr][cols].to_numpy(float); Xte=df.iloc[te][cols].to_numpy(float)
        if history:
            Xtr=np.hstack([Xtr,df.iloc[tr][hist].to_numpy(float)]); Xte=np.hstack([Xte,df.iloc[te][hist].to_numpy(float)])
        m=model(name); m.fit(Xtr,y[tr]); pred[te]=m.predict(Xte)
    return float(r2_score(y,pred)),max(overlaps)

def summarize(a):
    a=np.array(a,float); return {"mean":float(a.mean()),"median":float(np.median(a)),"q025":float(np.quantile(a,.025)),"q975":float(np.quantile(a,.975)),"positive_fraction":float(np.mean(a>0)),"gt_005_fraction":float(np.mean(a>.05))}

def calibrate(df,genes,reps=100):
    y0=df.target.to_numpy(float); g=df.group.to_numpy(); geom=[f"cur_{k}" for k in ["logv","x","y","z"]]; cur=[f"cur_g_{x}" for x in genes]; hist=[f"hist_{k}" for k in ["logv","x","y","z"]]+[f"hist_g_{x}" for x in genes]; S=df[geom+cur].to_numpy(float); H=df[hist].to_numpy(float); rng=np.random.default_rng(7719); Z=(S-S.mean(0))/(S.std(0)+1e-9); ZH=(H-H.mean(0))/(H.std(0)+1e-9); b=rng.normal(size=Z.shape[1]); b/=np.linalg.norm(b); signal=Z@b; signal=(signal-signal.mean())/signal.std(); hr=ZH[:,0]-Ridge(1).fit(Z,ZH[:,0]).predict(Z); hr=(hr-hr.mean())/(hr.std()+1e-9); noise=np.sqrt(.4/.6); splits=list(GroupKFold(5,shuffle=True,random_state=991).split(S,y0,g))
    def oo(X,y):
        p=np.empty(len(y))
        for tr,te in splits:
            m=make_pipeline(StandardScaler(),Ridge(alpha=10));m.fit(X[tr],y[tr]);p[te]=m.predict(X[te])
        return p
    def sim(gamma):
        z=[]
        for _ in range(reps):
            y=signal+gamma*hr+rng.normal(0,noise,len(g)); z.append(r2_score(y,oo(np.c_[S,H],y))-r2_score(y,oo(S,y)))
        return np.array(z)
    null=sim(0); alt=sim(.30); th=np.quantile(null,.95); return {"reps":reps,"null":summarize(null),"null_q95":float(th),"alt_gamma_target_sd":.30,"alt":summarize(alt),"power_vs_null_q95":float(np.mean(alt>th))}

dt=rep.load_dtissue(); out={"upstream_commit":subprocess.check_output(["git","-C",str(UP),"rev-parse","HEAD"],text=True).strip(),"project_commit_at_branch":subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip(),"source_hashes":{}}
for q in [UP/"stateAnalysis/FM1_dtissue.tis",UP/"data/geneExpression/t_96h.txt",UP/"data/geneExpression/t_120h.txt",UP/"common/common/L1L2_cells_ids.py",ROOT/"analysis/refahi_state_completion_replication.py",ROOT/"analysis/refahi_pc_completion_audit.py"]: out["source_hashes"][str(q)]=sha(q)
for label,w in {"middle_L1":(40,96,120),"late_L1":(96,120,132)}.items():
    df,genes=rep.build_window(dt,*w,True); case={"n":len(df),"groups":int(df.group.nunique()),"genes":len(genes),"duplicate_current_cells":int(df.cid.duplicated().sum()),"max_rows_per_group":int(df.groupby("group").size().max())}; seeds=list(range(8)); rr=[]
    for seed in seeds:
        a,ov=score(df,genes,"ridge",seed); b,_=score(df,genes,"ridge",seed,history=True); rr.append(b-a); case.setdefault("max_train_test_group_overlap",0); case["max_train_test_group_overlap"]=max(case["max_train_test_group_overlap"],ov)
    case["ridge_history_delta_8splits"]=summarize(rr)
    for mn in ["extra","histgb"]:
        vals=[]
        for seed in range(2):
            a,_=score(df,genes,mn,seed); b,_=score(df,genes,mn,seed,history=True); vals.append(b-a)
        case[mn+"_history_delta_2splits"]=summarize(vals)
    if label=="late_L1":
        vals={};
        for mn in ["ridge","extra","histgb"]:
            g0,_=score(df,genes,mn,20260829); p1,_=score(df,genes,mn,20260829,pc1=True); all25,_=score(df,genes,mn,20260829); vals[mn]={"geometry_plus_all25":all25,"geometry_plus_pc1":p1}
        case["pc1_fixed_split"]=vals; case["calibration"]=calibrate(df,genes,20)
    out[label]=case
Path(ROOT/"lab_lanes/replication/r1_fresh_audit.json").write_text(json.dumps(out,indent=2),encoding="utf-8"); print(json.dumps(out,indent=2))
