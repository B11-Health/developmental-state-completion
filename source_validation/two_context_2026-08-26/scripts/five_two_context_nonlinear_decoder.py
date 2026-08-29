import json,numpy as np,time
from pathlib import Path
from scipy.optimize import minimize
R=Path('/root/plant_m2_reeb_global');z=np.load(R/'RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz');C=z['coef'];P=z['powers'];LB=np.load(R/'TWO_PHENOTYPE_LINEAR_U_DECODER_FROZEN_2026-08-26.npz')['B'];Gtot=1.8
MASKS=[7,11,13,14,15]
def raw(path):
 a=[]
 for l in open(path):
  if l.startswith('#'):continue
  q=l.rstrip().split('\t');a += [float(q[1]),float(q[2])]
 return np.array(a,float)
def F(u):return np.prod(np.power(np.asarray(u)[None,:],P),axis=1)@C
def init(y):
 u=np.clip(np.r_[1,y]@LB,0,1)
 if u.sum()>Gtot:u*=Gtot/u.sum()
 return u
def dec(y):
 starts=[init(y),np.ones(4)*.2,np.ones(4)*.45];best=None
 for x in starts:
  rr=minimize(lambda u:float(np.sum((F(u)-y)**2)),x,method='SLSQP',bounds=[(0,1)]*4,constraints=[{'type':'ineq','fun':lambda u:Gtot-u.sum()}],options={'ftol':1e-16,'maxiter':400})
  if rr.success and (best is None or rr.fun<best.fun):best=rr
 return best.x
def reconstruct(u0,uq,q):
 qb=np.array([int(c) for c in f'{q:04b}']);s=np.zeros(4);known=[];un=[]
 for j in range(4):
  if qb[j]:
   s[j]=uq[j]-u0[j];known.append(abs(s[j]))
  else:un.append(j)
 if len(un)==0:return s
 assert len(un)==1;j=un[0];res=max(0,Gtot-sum(known));obs=(u0[j]+uq[j])/2
 # active (negative) predicts obs=res; inactive positive predicts obs=0
 s[j]=-res if abs(obs-res)<abs(obs) else res
 return s
def evalset(name,laws,folder,nested):
 cache={};
 for l,v in laws.items():
  for st in range(16):cache[(l,st)]=dec(raw(R/f'{folder}/{l}__{st:04b}.tsv'))
 out={}
 for q in MASKS:
  rr=[]
  for l,v in laws.items():
   g=np.array(v['gains'] if nested else v,float)
   for st in range(16):
    b=np.array([int(c) for c in f'{st:04b}']);true=(1-2*b)*g;hat=reconstruct(cache[(l,st)],cache[(l,st^q)],q);rr.append((np.linalg.norm(hat-true),np.linalg.norm(hat-true)/np.linalg.norm(true),np.all(np.sign(hat)==np.sign(true)),l,st,true,hat))
  E=np.array([x[0] for x in rr]);out[f'{q:04b}']={'sign_accuracy':float(np.mean([x[2] for x in rr])),'L2_median':float(np.median(E)),'L2_p95':float(np.quantile(E,.95)),'L2_max':float(E.max()),'rel_p95':float(np.quantile([x[1] for x in rr],.95)),'worst':{'law':max(rr,key=lambda x:x[0])[3],'state':f'{max(rr,key=lambda x:x[0])[4]:04b}','true':max(rr,key=lambda x:x[0])[5].tolist(),'hat':max(rr,key=lambda x:x[0])[6].tolist()}}
  print(name,f'{q:04b}',out[f'{q:04b}'])
 return out
old=json.load(open(R/'gain_search_candidates.json'));near=json.load(open(R/'near_seam_spectral_frozen.json'))['laws'];out={'old14':evalset('old14',old,'vector_joint_geometry',False),'near12':evalset('near12',near,'near_seam_spectral_dumps',True)};json.dump(out,open(R/'five_two_context_nonlinear_decoder_results.json','w'),indent=2)
