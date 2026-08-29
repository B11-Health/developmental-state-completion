import math
import numpy as np


def entropy_bits(p):
    p=np.asarray(p,dtype=float); p=p[p>0]
    return float(-(p*np.log2(p)).sum())


def xor_counterexample():
    rows=[]
    for h in [0,1]:
        for z in [0,1]:
            y=h^z
            rows.append((h,z,y,0.25))
    # I(Y;H)
    py=np.array([sum(w for h,z,y,w in rows if y==v) for v in [0,1]])
    ph=np.array([sum(w for h,z,y,w in rows if h==v) for v in [0,1]])
    pyh=np.array([[sum(w for h,z,y,w in rows if y==yy and h==hh) for hh in [0,1]] for yy in [0,1]])
    iyh=0.0
    for yy in [0,1]:
        for hh in [0,1]:
            p=pyh[yy,hh]
            if p>0: iyh+=p*math.log2(p/(py[yy]*ph[hh]))
    # I(Y;H|Z)
    cmi=0.0
    for zz in [0,1]:
        pz=sum(w for h,z,y,w in rows if z==zz)
        sub=[(h,y,w/pz) for h,z,y,w in rows if z==zz]
        for hh in [0,1]:
            for yy in [0,1]:
                p=sum(w for h,y,w in sub if h==hh and y==yy)
                phh=sum(w for h,y,w in sub if h==hh)
                pyy=sum(w for h,y,w in sub if y==yy)
                if p>0:cmi+=pz*p*math.log2(p/(phh*pyy))
    return iyh,cmi


def variance_only_example(n=2_000_000,seed=7):
    rng=np.random.default_rng(seed)
    h=rng.integers(0,2,n)
    sigma=np.where(h==0,1.0,3.0)
    y=rng.normal(0,sigma)
    # Squared-loss Bayes means are 0 with and without H.
    mse_no=float(np.mean(y*y))
    pred_h=np.zeros_like(y)
    mse_h=float(np.mean((y-pred_h)**2))
    # Exact CMI is I(Y;H) here; estimate via histogram only for demonstration.
    bins=np.quantile(y,np.linspace(0,1,101)); bins[0]-=1e-9;bins[-1]+=1e-9
    b=np.digitize(y,bins[1:-1])
    joint=np.zeros((100,2))
    for j in [0,1]:
        joint[:,j]=np.bincount(b[h==j],minlength=100)
    joint/=joint.sum(); py=joint.sum(1); ph=joint.sum(0)
    mi=0.0
    for i in range(100):
        for j in range(2):
            p=joint[i,j]
            if p>0:mi+=p*math.log2(p/(py[i]*ph[j]))
    return mse_no,mse_h,mi


if __name__=='__main__':
    a,b=xor_counterexample()
    print('XOR I(Y;H)=',round(a,6),'bits')
    print('XOR I(Y;H|Z)=',round(b,6),'bits')
    m0,m1,mi=variance_only_example()
    print('variance-only squared-loss gain=',round(m0-m1,8))
    print('variance-only estimated I(Y;H)=',round(mi,6),'bits')
