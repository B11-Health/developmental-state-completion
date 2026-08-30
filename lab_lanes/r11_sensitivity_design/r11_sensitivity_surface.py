import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

BASE=Path(__file__).parent
ROOT=BASE.parents[1]
R10=ROOT/'lab_lanes'/'r10_registered_history_calibration'
spec=importlib.util.spec_from_file_location('r10mod',R10/'r10_history_calibration.py')
r10=importlib.util.module_from_spec(spec); spec.loader.exec_module(r10)
OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)
SCALES=[0.15,0.30,0.45,0.60]
N=20

def one(scale,rep,S,H,g,y,ysd):
    rng=np.random.RandomState(r10.SEED+500000+rep)
    w=rng.normal(size=H.shape[1]); w=w/np.linalg.norm(w)
    z=H@w
    rz=Ridge(alpha=1.0).fit(S,z)
    hres=z-rz.predict(S)
    sd=float(np.std(hres)); hres=hres/(sd if sd>1e-12 else 1.0)
    ys=y+scale*ysd*hres
    df=r10.fit_pair(S,H,ys,g)
    dec=r10.gate2(df)
    return df,dec

def run_scale(scale,start=0,count=N):
    if abs(scale-0.30)<1e-12:
        raise SystemExit('0.30 is inherited from R10 and must not be refit')
    A,cols,S,H,g,y=r10.load(); ysd=float(np.std(y)); rows=[]; decs=[]
    for rep in range(start,start+count):
        df,dec=one(scale,rep,S,H,g,y,ysd)
        dec={'scale':scale,'replicate':rep,**dec,'joint_success':bool(dec['gate2_pass'] and dec['s_adequacy_preserved'])}
        decs.append(dec); q=df.copy(); q['scale']=scale; q['replicate']=rep; rows.append(q)
    pd.concat(rows,ignore_index=True).to_csv(OUT/f'metrics_scale_{scale:.2f}_{start:02d}_{start+count-1:02d}.csv',index=False)
    (OUT/f'decisions_scale_{scale:.2f}_{start:02d}_{start+count-1:02d}.json').write_text(json.dumps(decs,indent=2),encoding='utf-8')
    print(json.dumps(summary(decs),indent=2))

def validate_exact_reps(decs, n, label):
    ids=[int(x['replicate']) for x in decs]
    expected=list(range(n))
    if len(ids)!=n or len(set(ids))!=n or sorted(ids)!=expected:
        raise SystemExit(f'{label}: expected unique replicate ids 0..{n-1}; got {sorted(ids)}')
    return sorted(decs,key=lambda x:int(x['replicate']))

def inherited_030():
    all_r10=json.loads((R10/'results'/'calibration_decisions.json').read_text(encoding='utf-8'))
    first=[x for x in all_r10 if 0 <= int(x['replicate']) < N]
    decs=validate_exact_reps(first,N,'inherited R10 0.30 arm')
    return [{'scale':0.30,'replicate':int(x['replicate']),'gate2_pass':bool(x['gate2_pass']),'s_adequacy_preserved':bool(x['s_adequacy_preserved']),'joint_success':bool(x['success'])} for x in decs]

def summary(decs):
    n=len(decs); A=sum(x['s_adequacy_preserved'] for x in decs); D=sum(x['gate2_pass'] for x in decs); J=sum(x['joint_success'] for x in decs)
    return {'scale':float(decs[0]['scale']) if decs else None,'n':n,'adequacy_count':A,'adequacy_rate':A/n,'gate2_count':D,'gate2_rate':D/n,'joint_count':J,'joint_rate':J/n,'detection_given_adequacy':(J/A if A else None),'adequacy_only':sum(x['s_adequacy_preserved'] and not x['gate2_pass'] for x in decs),'detection_only':sum(x['gate2_pass'] and not x['s_adequacy_preserved'] for x in decs),'neither':sum((not x['gate2_pass']) and (not x['s_adequacy_preserved']) for x in decs)}

def aggregate():
    all_decs=[]
    for scale in SCALES:
        if scale==0.30: decs=inherited_030()
        else:
            parts=sorted(OUT.glob(f'decisions_scale_{scale:.2f}_*.json'))
            if not parts: raise SystemExit(f'missing scale {scale:.2f} chunks')
            decs=[]
            for p in parts: decs.extend(json.loads(p.read_text(encoding='utf-8')))
            decs=validate_exact_reps(decs,N,f'scale {scale:.2f}')
        all_decs.extend(decs)
    sums=[summary([x for x in all_decs if abs(float(x['scale'])-s)<1e-9]) for s in SCALES]
    pd.DataFrame(sums).to_csv(OUT/'sensitivity_surface_summary.csv',index=False)
    (OUT/'sensitivity_surface_summary.json').write_text(json.dumps(sums,indent=2),encoding='utf-8')
    print(json.dumps(sums,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--scale',type=float); ap.add_argument('--start',type=int,default=0); ap.add_argument('--count',type=int,default=N); ap.add_argument('--aggregate',action='store_true'); a=ap.parse_args()
    if a.aggregate: aggregate()
    elif a.scale is not None: run_scale(a.scale,a.start,a.count)
    else: raise SystemExit('use --scale or --aggregate')
