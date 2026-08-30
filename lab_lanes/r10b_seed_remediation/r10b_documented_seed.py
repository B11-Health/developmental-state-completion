import argparse, importlib.util, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

BASE=Path(__file__).parent; ROOT=BASE.parents[1]
R10=ROOT/'lab_lanes'/'r10_registered_history_calibration'
spec=importlib.util.spec_from_file_location('r10mod',R10/'r10_history_calibration.py')
r10=importlib.util.module_from_spec(spec); spec.loader.exec_module(r10)
OUT=BASE/'results'; OUT.mkdir(parents=True,exist_ok=True)

def run(start,count):
    A,cols,S,H,g,y=r10.load(); ysd=float(np.std(y)); rows=[]; decs=[]
    for rep in range(start,start+count):
        rng=np.random.RandomState(r10.SEED+rep)
        w=rng.normal(size=H.shape[1]); w=w/np.linalg.norm(w)
        z=H@w
        rz=Ridge(alpha=1.0).fit(S,z)
        hres=z-rz.predict(S); sd=float(np.std(hres)); hres=hres/(sd if sd>1e-12 else 1.0)
        ys=y+0.30*ysd*hres
        df=r10.fit_pair(S,H,ys,g); dec=r10.gate2(df)
        dec={'replicate':rep,'direction_seed':int(r10.SEED+rep),'injected_scale_target_sd':0.30,**dec,'success':bool(dec['gate2_pass'] and dec['s_adequacy_preserved'])}
        decs.append(dec); q=df.copy(); q['replicate']=rep; q['direction_seed']=int(r10.SEED+rep); rows.append(q)
    pd.concat(rows,ignore_index=True).to_csv(OUT/f'metrics_{start:02d}_{start+count-1:02d}.csv',index=False)
    (OUT/f'decisions_{start:02d}_{start+count-1:02d}.json').write_text(json.dumps(decs,indent=2),encoding='utf-8')
    print(json.dumps({'start':start,'count':count,'successes':sum(x['success'] for x in decs),'adequacy':sum(x['s_adequacy_preserved'] for x in decs),'gate2':sum(x['gate2_pass'] for x in decs)},indent=2))

def aggregate():
    files=sorted(OUT.glob('decisions_*.json')); decs=[]
    for f in files: decs.extend(json.loads(f.read_text(encoding='utf-8')))
    reps=[int(x['replicate']) for x in decs]
    if sorted(reps)!=list(range(30)): raise SystemExit(f'expected reps 0..29 exactly; got {sorted(reps)}')
    result={'replicates':30,'seed_rule':'20260830 + replicate','success_count':sum(x['success'] for x in decs),'success_rate':sum(x['success'] for x in decs)/30,'adequacy_count':sum(x['s_adequacy_preserved'] for x in decs),'gate2_count':sum(x['gate2_pass'] for x in decs),'required_success_count':24,'calibration_pass':sum(x['success'] for x in decs)>=24}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--start',type=int); ap.add_argument('--count',type=int); ap.add_argument('--aggregate',action='store_true'); a=ap.parse_args()
    if a.aggregate: aggregate()
    else: run(a.start,a.count)
