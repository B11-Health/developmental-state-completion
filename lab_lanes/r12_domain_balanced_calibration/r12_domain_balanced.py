import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

BASE=Path(__file__).parent
ROOT=BASE.parents[1]
R10=ROOT/'lab_lanes'/'r10_registered_history_calibration'
R10B=ROOT/'lab_lanes'/'r10b_seed_remediation'
spec=importlib.util.spec_from_file_location('r10mod',R10/'r10_history_calibration.py')
r10=importlib.util.module_from_spec(spec); spec.loader.exec_module(r10)
OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)
GEOMS=['domain_balanced','domainwise_residualizer']

def _within_group_standardize(v,g):
    out=np.zeros_like(v,dtype=float)
    for seq in sorted(np.unique(g)):
        q=g==seq; x=v[q]; sd=float(np.std(x)); out[q]=(x-float(np.mean(x)))/(sd if sd>1e-12 else 1.0)
    return out

def make_hidden(rep,geometry,S,H,g):
    rng=np.random.RandomState(r10.SEED+rep)
    w=rng.normal(size=H.shape[1]); w=w/np.linalg.norm(w)
    z=H@w
    if geometry=='domain_balanced':
        rz=Ridge(alpha=1.0).fit(S,z)
        raw=z-rz.predict(S)
        h=_within_group_standardize(raw,g)
    elif geometry=='domainwise_residualizer':
        raw=np.zeros_like(z,dtype=float)
        for seq in sorted(np.unique(g)):
            q=g==seq
            rz=Ridge(alpha=1.0).fit(S[q],z[q])
            raw[q]=z[q]-rz.predict(S[q])
        h=_within_group_standardize(raw,g)
    else:
        raise ValueError(geometry)
    return h,w,raw

def run(geometry,start,count):
    if geometry not in GEOMS: raise SystemExit('bad geometry')
    A,cols,S,H,g,y=r10.load(); ysd=float(np.std(y)); rows=[]; decs=[]
    for rep in range(start,start+count):
        h,w,raw=make_hidden(rep,geometry,S,H,g)
        ys=y+0.30*ysd*h
        df=r10.fit_pair(S,H,ys,g); dec=r10.gate2(df)
        seqstats={}
        for seq in sorted(np.unique(g)):
            q=g==seq
            seqstats[str(seq)]={'balanced_mean':float(np.mean(h[q])),'balanced_sd':float(np.std(h[q])),'raw_mean':float(np.mean(raw[q])),'raw_sd':float(np.std(raw[q]))}
        d={'geometry':geometry,'replicate':rep,'direction_seed':int(r10.SEED+rep),'scale':0.30,**dec,'success':bool(dec['gate2_pass'] and dec['s_adequacy_preserved']),'sequence_stats':seqstats}
        decs.append(d); q=df.copy(); q['geometry']=geometry; q['replicate']=rep; q['direction_seed']=int(r10.SEED+rep); rows.append(q)
    pd.concat(rows,ignore_index=True).to_csv(OUT/f'{geometry}_metrics_{start:02d}_{start+count-1:02d}.csv',index=False)
    (OUT/f'{geometry}_decisions_{start:02d}_{start+count-1:02d}.json').write_text(json.dumps(decs,indent=2),encoding='utf-8')
    print(json.dumps({'geometry':geometry,'start':start,'count':count,'successes':sum(x['success'] for x in decs),'adequacy':sum(x['s_adequacy_preserved'] for x in decs),'gate2':sum(x['gate2_pass'] for x in decs)},indent=2))

def aggregate(geometry):
    parts=sorted(OUT.glob(f'{geometry}_decisions_*.json')); decs=[]
    for f in parts: decs.extend(json.loads(f.read_text(encoding='utf-8')))
    reps=[int(x['replicate']) for x in decs]
    if sorted(reps)!=list(range(30)) or len(set(reps))!=30: raise SystemExit(f'expected exact unique reps 0..29; got {sorted(reps)}')
    ref=json.loads((R10B/'results'/'results.json').read_text(encoding='utf-8'))
    result={'geometry':geometry,'replicates':30,'seed_rule':'20260830 + replicate','scale':0.30,'success_count':sum(x['success'] for x in decs),'success_rate':sum(x['success'] for x in decs)/30,'adequacy_count':sum(x['s_adequacy_preserved'] for x in decs),'gate2_count':sum(x['gate2_pass'] for x in decs),'required_success_count':24,'planning_threshold_reached':sum(x['success'] for x in decs)>=24,'r10b_reference_success_count':int(ref['success_count']),'r10b_reference_success_rate':float(ref['success_rate'])}
    (OUT/f'{geometry}_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--geometry',choices=GEOMS,required=True); ap.add_argument('--start',type=int); ap.add_argument('--count',type=int); ap.add_argument('--aggregate',action='store_true'); a=ap.parse_args()
    if a.aggregate: aggregate(a.geometry)
    else: run(a.geometry,a.start,a.count)
