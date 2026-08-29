import json,numpy as np
from pathlib import Path
from scipy.optimize import minimize
R=Path('/root/plant_m2_reeb_global');O=R/'two_phenotype_prospective_source';fr=json.load(open(R/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json'));z=np.load(R/'RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz');C=z['coef'];P=z['powers'];LB=np.load(R/'TWO_PHENOTYPE_LINEAR_U_DECODER_FROZEN_2026-08-26.npz')['B']
def raw(p):
 a=[]
 for l in open(p):
  if l.startswith('#'):continue
  q=l.rstrip().split('\t');a += [float(q[1]),float(q[2])]
 return np.array(a,float)
def F(u):return np.prod(np.power(np.asarray(u)[None,:],P),axis=1)@C
def dec(y):
 u=np.clip(np.r_[1,y]@LB,0,1)
 if u.sum()>1.8:u*=1.8/u.sum()
 best=None
 for x in [u,np.ones(4)*.2,np.ones(4)*.45]:
  rr=minimize(lambda a:float(np.sum((F(a)-y)**2)),x,method='SLSQP',bounds=[(0,1)]*4,constraints=[{'type':'ineq','fun':lambda a:1.8-a.sum()}],options={'ftol':1e-16,'maxiter':500})
  if rr.success and (best is None or rr.fun<best.fun):best=rr
 return best.x,float(best.fun)
cache={}
for l in fr['laws']:
 for ss in fr['states']:cache[(l,int(ss,2))]=dec(raw(O/f'{l}_{ss}.tsv'))[0]
rows=[]
for l,g0 in fr['laws'].items():
 g=np.array(g0)
 for ss in fr['states'][:4]:
  st=int(ss,2);bits=np.array([int(c) for c in ss]);true=(1-2*bits)*g;hat=cache[(l,st^15)]-cache[(l,st)];rows.append({'law':l,'state':ss,'true_s':true.tolist(),'hat_s':hat.tolist(),'L2':float(np.linalg.norm(hat-true)),'rel':float(np.linalg.norm(hat-true)/np.linalg.norm(true)),'sign_correct':bool(np.all(np.sign(hat)==np.sign(true))),'min_gain':float(g.min())})
E=np.array([r['L2'] for r in rows]);res={'freeze_sha':fr['sha256_pre_render'],'n_pairs':len(rows),'sign_accuracy':float(np.mean([r['sign_correct'] for r in rows])),'signed_L2_median':float(np.median(E)),'signed_L2_p95':float(np.quantile(E,.95)),'signed_L2_max':float(E.max()),'rel_p95':float(np.quantile([r['rel'] for r in rows],.95)),'weak_001_all_sign_correct':bool(all(r['sign_correct'] for r in rows if r['min_gain']<=.001001)),'predictions_pass':bool(np.mean([r['sign_correct'] for r in rows])==1 and np.median(E)<.001 and E.max()<.002),'worst':sorted(rows,key=lambda r:r['L2'],reverse=True)[:12]};print(json.dumps(res,indent=2));json.dump(res,open(O/'results.json','w'),indent=2)
