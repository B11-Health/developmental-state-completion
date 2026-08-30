import argparse, json, urllib.request, urllib.parse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import mmread
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE = "https://kleintools.hms.harvard.edu/paper_websites/state_fate2020/"
SPRING_GENE_URL = "https://kleintools.hms.harvard.edu/tools/cgi-bin2/grab_one_gene.py"
SMALL_FILES = ["stateFate_inVitro_metadata.txt.gz", "stateFate_inVitro_clone_matrix.mtx.gz"]
GENES = ["Kit","Ly6a","Flt3","Hlf","Hoxa9","Meis1","Pbx1","Myb","Runx1","Gata2","Tal1","Lmo2","Erg","Fli1","Lyl1","Mpl","Spi1","Cebpa","Cebpb","Gfi1","Irf8","Csf1r","Csf3r","Mpo","Elane","Prtn3","Ctsg","Ltf","S100a8","S100a9","Lyz2","Fcgr3"]
MAJOR = {"Neutrophil","Monocyte","Baso"}
SEED = 20260830

def fetch(url, out):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0: return
    with urllib.request.urlopen(url, timeout=120) as r:
        out.write_bytes(r.read())

def ensure(data_dir):
    data_dir = Path(data_dir); data_dir.mkdir(parents=True, exist_ok=True)
    for f in SMALL_FILES: fetch(BASE + f, data_dir / f)
    panel = data_dir / "panel"; panel.mkdir(exist_ok=True)
    for g in GENES:
        out = panel / f"{g}.txt"
        if out.exists() and out.stat().st_size > 100000: continue
        payload = urllib.parse.urlencode({"base_dir":"cgi-bin/client_datasets/SF_all","sub_dir":"cgi-bin/client_datasets/SF_all/all_combined","gene":g}).encode()
        with urllib.request.urlopen(urllib.request.Request(SPRING_GENE_URL, data=payload), timeout=120) as r:
            out.write_bytes(r.read())

def dominant(w, mature):
    vc = w[w["Cell type annotation"].isin(mature)]["Cell type annotation"].value_counts()
    if len(vc) == 0 or (len(vc) > 1 and vc.iloc[0] == vc.iloc[1]): return None
    return vc.index[0]

def build_cohort(data_dir):
    data_dir = Path(data_dir)
    md = pd.read_csv(data_dir / SMALL_FILES[0], sep="\t")
    A = mmread(data_dir / SMALL_FILES[1]).tocsc()
    expr = {}
    for g in GENES:
        arr = np.fromstring((data_dir / "panel" / f"{g}.txt").read_text(), sep="\n")
        if len(arr) != len(md): raise RuntimeError(f"{g}: {len(arr)} values != {len(md)} cells")
        expr[g] = arr
    mature = set(md["Cell type annotation"].unique()) - {"Undifferentiated"}
    rows = []
    for j in range(A.shape[1]):
        ix = A[:, j].indices
        sub = md.iloc[ix]
        d2_mask = sub["Time point"].to_numpy() == 2.0
        if not np.any(d2_mask): continue
        d2_ix = ix[d2_mask]
        d6 = sub[sub["Time point"] == 6.0]
        w1, w2 = d6[d6.Well == 1], d6[d6.Well == 2]
        if len(w1) == 0 or len(w2) == 0: continue
        f1, f2 = dominant(w1, mature), dominant(w2, mature)
        if f1 not in MAJOR or f2 not in MAJOR: continue
        d2 = md.iloc[d2_ix]
        rec = {"clone":j, "n_d2":len(d2_ix), "x":float(d2["SPRING-x"].mean()), "y2d":float(d2["SPRING-y"].mean()), "start":d2["Starting population"].mode().iloc[0], "sister_fate":f1, "target_fate":f2}
        for g in GENES: rec[g] = float(np.log1p(expr[g][d2_ix]).mean())
        rows.append(rec)
    return pd.DataFrame(rows)

def estimator(name):
    if name == "logistic":
        return LogisticRegression(C=1.0, max_iter=4000, class_weight="balanced", random_state=SEED)
    if name == "histgb":
        return HistGradientBoostingClassifier(max_iter=200, max_leaf_nodes=9, learning_rate=0.05, l2_regularization=1.0, random_state=SEED, class_weight="balanced")
    raise ValueError(name)

def make_model(num_cols, cat_cols, est_name, use_pca):
    steps = [("scale", StandardScaler())]
    if use_pca:
        steps.append(("pca", PCA(n_components=min(8, len(num_cols)), random_state=SEED)))
    num_pipe = Pipeline(steps)
    pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)], sparse_threshold=0)
    return Pipeline([("pre", pre), ("model", estimator(est_name))])

def evaluate(R, richness, repeats=10):
    y = R.target_fate.to_numpy()
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=repeats, random_state=SEED)
    rows = []
    if richness == 0:
        num = ["x","y2d"]; label = "spring2d"; use_pca = False
    else:
        num = GENES[:richness]; label = f"expr{richness}"; use_pca = richness > 4
    for fold, (tr, te) in enumerate(cv.split(R, y)):
        for est in ["logistic","histgb"]:
            for plus in [False, True]:
                cats = ["start"] + (["sister_fate"] if plus else [])
                model = make_model(num, cats, est, use_pca)
                model.fit(R.iloc[tr], y[tr])
                pred = model.predict(R.iloc[te]); prob = model.predict_proba(R.iloc[te]); classes = model.named_steps["model"].classes_
                rows.append({"representation":label,"n_numeric":len(num),"estimator":est,"fold":fold,"plus_sister":plus,"accuracy":accuracy_score(y[te],pred),"balanced_accuracy":balanced_accuracy_score(y[te],pred),"log_loss":log_loss(y[te],prob,labels=classes)})
    return pd.DataFrame(rows)

def summarize(cv):
    out=[]
    for (rep,est), g in cv.groupby(["representation","estimator"]):
        a=g[~g.plus_sister].sort_values("fold").reset_index(drop=True); b=g[g.plus_sister].sort_values("fold").reset_index(drop=True)
        out.append({"representation":rep,"estimator":est,"n_folds":len(a),"state_log_loss":a.log_loss.mean(),"state_plus_sister_log_loss":b.log_loss.mean(),"sister_log_loss_gain":(a.log_loss-b.log_loss).mean(),"state_balanced_accuracy":a.balanced_accuracy.mean(),"state_plus_sister_balanced_accuracy":b.balanced_accuracy.mean(),"sister_balanced_accuracy_gain":(b.balanced_accuracy-a.balanced_accuracy).mean(),"state_accuracy":a.accuracy.mean(),"state_plus_sister_accuracy":b.accuracy.mean()})
    return pd.DataFrame(out)

def permutation_null(R, n_perm=30):
    y=R.target_fate.to_numpy(); skf=StratifiedKFold(n_splits=5,shuffle=True,random_state=SEED); folds=list(skf.split(R,y)); rng=np.random.default_rng(SEED+7); rows=[]; num=GENES
    for est in ["logistic","histgb"]:
        base=[]
        for tr,te in folds:
            m=make_model(num,["start"],est,True); m.fit(R.iloc[tr],y[tr]); p=m.predict_proba(R.iloc[te]); base.append(log_loss(y[te],p,labels=m.named_steps["model"].classes_))
        base=np.mean(base)
        for perm in range(n_perm):
            Rp=R.copy(); Rp["sister_fate"]=rng.permutation(Rp["sister_fate"].to_numpy()); vals=[]
            for tr,te in folds:
                m=make_model(num,["start","sister_fate"],est,True); m.fit(Rp.iloc[tr],y[tr]); p=m.predict_proba(Rp.iloc[te]); vals.append(log_loss(y[te],p,labels=m.named_steps["model"].classes_))
            rows.append({"estimator":est,"perm":perm,"null_sister_log_loss_gain":base-float(np.mean(vals))})
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data-dir",default=".tmp-r3-larry-data"); ap.add_argument("--out-dir",default="lab_lanes/r3_larry_highdim/results"); ap.add_argument("--repeats",type=int,default=10); ap.add_argument("--permutations",type=int,default=30); args=ap.parse_args()
    ensure(args.data_dir); out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    R=build_cohort(args.data_dir); R.to_csv(out/"cohort.csv",index=False)
    allcv=pd.concat([evaluate(R,k,args.repeats) for k in [0,4,8,16,32]],ignore_index=True); allcv.to_csv(out/"cv_fold_metrics.csv",index=False)
    summ=summarize(allcv); summ.to_csv(out/"summary.csv",index=False)
    null=permutation_null(R,args.permutations); null.to_csv(out/"permutation_null.csv",index=False)
    obs=summ[summ.representation=="expr16"][["estimator","sister_log_loss_gain"]]
    cal=[]
    for _,r in obs.iterrows():
        q=null[null.estimator==r.estimator].null_sister_log_loss_gain; cal.append({"estimator":r.estimator,"observed_expr16_sister_log_loss_gain":r.sister_log_loss_gain,"null_mean":q.mean(),"null_q95":q.quantile(.95),"empirical_p":(1+(q>=r.sister_log_loss_gain).sum())/(1+len(q))})
    payload={"seed":SEED,"cohort_n":len(R),"unique_clones":int(R.clone.nunique()),"day2_cells":int(R.n_d2.sum()),"target_counts":R.target_fate.value_counts().to_dict(),"sister_target_agreement":float((R.sister_fate==R.target_fate).mean()),"genes":GENES,"summary":summ.to_dict(orient="records"),"calibration":cal}
    (out/"results.json").write_text(json.dumps(payload,indent=2))
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
