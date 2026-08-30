import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd

BASE=Path(__file__).parent
ROOT=BASE.parents[1]
R10=ROOT/'lab_lanes'/'r10_registered_history_calibration'
R12=ROOT/'lab_lanes'/'r12_domain_balanced_calibration'
s10=importlib.util.spec_from_file_location('r10mod',R10/'r10_history_calibration.py'); r10=importlib.util.module_from_spec(s10); s10.loader.exec_module(r10)
s12=importlib.util.spec_from_file_location('r12mod',R12/'r12_domain_balanced.py'); r12=importlib.util.module_from_spec(s12); s12.loader.exec_module(r12)
OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)
SCALES=[0.15,0.30,0.45,0.60]
NEW_SCALES={0.15,0.45,0.60}
N=30

def run(scale,start,count):
    if scale not in NEW_SCALES: raise SystemExit('new fits allowed only at 0.15, 0.45, 0.60; 0.30 is inherited')
    A,cols,S,H,g,y=r10.load(); ysd=float(np.std(y)); rows=[]; decs=[]
    for rep in range(start,start+count):
        h,w,raw=r12.make_hidden(rep,'domainwise_residualizer',S,H,g)
        ys=y+scale*ysd*h
        df=r10.fit_pair(S,H,ys,g); dec=r10.gate2(df)
        d={'scale':scale,'replicate':rep,'direction_seed':int(r10.SEED+rep),**dec,'joint_success':bool(dec['gate2_pass'] and dec['s_adequacy_preserved'])}
        decs.append(d); q=df.copy(); q['scale']=scale; q['replicate']=rep; q['direction_seed']=int(r10.SEED+rep); rows.append(q)
    pd.concat(rows,ignore_index=True).to_csv(OUT/f'metrics_{scale:.2f}_{start:02d}_{start+count-1:02d}.csv',index=False)
    (OUT/f'decisions_{scale:.2f}_{start:02d}_{start+count-1:02d}.json').write_text(json.dumps(decs,indent=2),encoding='utf-8')
    print(json.dumps(summary(decs),indent=2))

def inherited_030():
    xs=[]
    for f in sorted((R12/'results').glob('domainwise_residualizer_decisions_*.json')): xs += json.loads(f.read_text(encoding='utf-8'))
    reps=[int(x['replicate']) for x in xs]
    if sorted(reps)!=list(range(N)) or len(set(reps))!=N: raise SystemExit('bad inherited 0.30 replicate set')
    return [{'scale':0.30,'replicate':int(x['replicate']),'direction_seed':int(x['direction_seed']),'gate2_pass':bool(x['gate2_pass']),'s_adequacy_preserved':bool(x['s_adequacy_preserved']),'joint_success':bool(x['success'])} for x in xs]

def summary(xs):
    n=len(xs); A=sum(x['s_adequacy_preserved'] for x in xs); D=sum(x['gate2_pass'] for x in xs); J=sum(x['joint_success'] for x in xs)
    return {'scale':float(xs[0]['scale']),'n':n,'adequacy_count':A,'adequacy_rate':A/n,'gate2_count':D,'gate2_rate':D/n,'joint_count':J,'joint_rate':J/n,'detection_given_adequacy':J/A if A else None,'success_replicates':[int(x['replicate']) for x in xs if x['joint_success']]}

def aggregate():
    allx=[]
    for scale in SCALES:
        if scale==0.30: xs=inherited_030()
        else:
            xs=[]
            for f in sorted(OUT.glob(f'decisions_{scale:.2f}_*.json')): xs += json.loads(f.read_text(encoding='utf-8'))
            reps=[int(x['replicate']) for x in xs]
            if sorted(reps)!=list(range(N)) or len(set(reps))!=N: raise SystemExit(f'bad reps for {scale}: {sorted(reps)}')
        allx.extend(xs)
    sums=[summary([x for x in allx if abs(float(x['scale'])-s)<1e-12]) for s in SCALES]
    paired=[]
    by={(float(x['scale']),int(x['replicate'])):x for x in allx}
    for rep in range(N):
        paired.append({'replicate':rep,'adequacy':[bool(by[(s,rep)]['s_adequacy_preserved']) for s in SCALES],'detection':[bool(by[(s,rep)]['gate2_pass']) for s in SCALES],'joint':[bool(by[(s,rep)]['joint_success']) for s in SCALES]})
    (OUT/'surface_summary.json').write_text(json.dumps({'summary':sums,'paired':paired},indent=2),encoding='utf-8')
    pd.DataFrame([{k:v for k,v in x.items() if k!='success_replicates'} for x in sums]).to_csv(OUT/'surface_summary.csv',index=False)
    print(json.dumps(sums,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--scale',type=float); ap.add_argument('--start',type=int,default=0); ap.add_argument('--count',type=int,default=N); ap.add_argument('--aggregate',action='store_true'); a=ap.parse_args()
    if a.aggregate: aggregate()
    elif a.scale is not None: run(a.scale,a.start,a.count)
    else: raise SystemExit('use --scale or --aggregate')
