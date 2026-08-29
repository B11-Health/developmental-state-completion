import json,numpy as np
from pathlib import Path
from scipy.optimize import minimize
from shapely.geometry import Polygon
R=Path('/root/plant_m2_reeb_global');O=R/'two_phenotype_prospective_source'
fr=json.load(open(R/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json'))
z=np.load(R/'RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz');C=z['coef'];P=z['powers'];LB=np.load(R/'TWO_PHENOTYPE_LINEAR_U_DECODER_FROZEN_2026-08-26.npz')['B']
def raw(p):
 a=[]
 for l in open(p):
  if l.startswith('#'):continue
  q=l.rstrip().split('\t');a += [float(q[1]),float(q[2])]
 return np.array(a,float)
def F(u):return np.prod(np.power(np.asarray(u)[None,:],P),axis=1)@C
# EXACT same decoder as score_two_phenotype_prospective.py
def dec(y):
 u=np.clip(np.r_[1,y]@LB,0,1)
 if u.sum()>1.8:u*=1.8/u.sum()
 best=None
 for x in [u,np.ones(4)*.2,np.ones(4)*.45]:
  rr=minimize(lambda a:float(np.sum((F(a)-y)**2)),x,method='SLSQP',bounds=[(0,1)]*4,constraints=[{'type':'ineq','fun':lambda a:1.8-a.sum()}],options={'ftol':1e-16,'maxiter':500})
  if rr.success and (best is None or rr.fun<best.fun):best=rr
 return best.x,float(best.fun)
def poly(a):
 p=Polygon(np.asarray(a).reshape(-1,2));return p if p.is_valid else p.buffer(0)
def dio(a,b):
 p,q=poly(a),poly(b);u=p.union(q).area
 return 1-p.intersection(q).area/max(u,1e-30)
ph=[];cache={}
for law,g0 in fr['laws'].items():
 g=np.array(g0,float)
 for ss in fr['states']:
  st=int(ss,2);bits=np.array([int(c) for c in ss],float);utrue=bits*g;y=raw(O/f'{law}_{ss}.tsv');uhat,fun=dec(y);yhat=F(uhat);ytrue=F(utrue)
  r={'law':law,'state':ss,'u_true':utrue.tolist(),'u_hat':uhat.tolist(),'u_L2':float(np.linalg.norm(uhat-utrue)),
     'surrogate_inversion_raw_L2':float(np.sqrt(fun)),'surrogate_reconstruction_dIoU':float(dio(yhat,y)),
     'surrogate_at_true_u_raw_L2':float(np.linalg.norm(ytrue-y)),'surrogate_at_true_u_dIoU':float(dio(ytrue,y))}
  ph.append(r);cache[(law,st)]=uhat
pairs=[]
for law,g0 in fr['laws'].items():
 g=np.array(g0,float)
 for ss in fr['states'][:4]:
  st=int(ss,2);bits=np.array([int(c) for c in ss]);true=(1-2*bits)*g;hat=cache[(law,st^15)]-cache[(law,st)]
  pairs.append({'law':law,'state':ss,'mask':'1111','L2':float(np.linalg.norm(hat-true)),'sign_correct':bool(np.all(np.sign(hat)==np.sign(true))),
                'min_gain':float(g.min()),'weak_coords':[int(i) for i,x in enumerate(g) if x<=.001001]})
def summ(vals):
 a=np.asarray(vals,float);return {'median':float(np.median(a)),'p95':float(np.quantile(a,.95)),'max':float(a.max())}
weak=[p for p in pairs if p['min_gain']<=.001001]
bylaw={}
for law in fr['laws']:
 rr=[p for p in pairs if p['law']==law];bylaw[law]={'n':len(rr),'sign_accuracy':float(np.mean([p['sign_correct'] for p in rr])),'signed_L2':summ([p['L2'] for p in rr])}
out={'freeze_sha':fr['sha256_pre_render'],'estimator_statement':fr['decoder'],'n_source_phenotypes':len(ph),'n_complement_pairs':len(pairs),
 'phenotype_decode':{
   'u_L2':summ([r['u_L2'] for r in ph]),
   'surrogate_inversion_raw_L2':summ([r['surrogate_inversion_raw_L2'] for r in ph]),
   'surrogate_reconstruction_dIoU':summ([r['surrogate_reconstruction_dIoU'] for r in ph]),
   'surrogate_at_true_u_raw_L2':summ([r['surrogate_at_true_u_raw_L2'] for r in ph]),
   'surrogate_at_true_u_dIoU':summ([r['surrogate_at_true_u_dIoU'] for r in ph])},
 'pair_reconstruction':{'sign_accuracy':float(np.mean([p['sign_correct'] for p in pairs])),'signed_L2':summ([p['L2'] for p in pairs]),
   'weak_001_n_pairs':len(weak),'weak_001_sign_accuracy':float(np.mean([p['sign_correct'] for p in weak])),'weak_001_L2':summ([p['L2'] for p in weak]),
   'mask_by_mask':{'1111':{'n':len(pairs),'sign_accuracy':float(np.mean([p['sign_correct'] for p in pairs])),'signed_L2':summ([p['L2'] for p in pairs])}},
   'mask_availability_note':'The frozen source cohort contains four complementary state pairs only, so 1111 is the only mask prospectively evaluable without new source renders. The other Hamming>=3 masks require unrendered states.'},
 'by_law':bylaw,
 'worst_phenotype_u':sorted(ph,key=lambda r:r['u_L2'],reverse=True)[:8],
 'worst_pair':sorted(pairs,key=lambda r:r['L2'],reverse=True)[:8]}
json.dump(out,open(R/'TWO_PHENOTYPE_PROSPECTIVE_AUDIT_V2_2026-08-26.json','w'),indent=2)
print(json.dumps(out,indent=2))
