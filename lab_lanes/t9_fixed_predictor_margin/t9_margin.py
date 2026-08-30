import numpy as np

def mse(pred,y):
    pred=np.asarray(pred,float); y=np.asarray(y,float); return float(np.mean((y-pred)**2))

def inner(u,v):
    return float(np.mean(np.asarray(u,float)*np.asarray(v,float)))

def margin(y,p,b,z,a):
    ya=np.asarray(y,float)+a*np.asarray(z,float)
    return mse(b,ya)-mse(p,ya)

def fixed_formula(y,p,b,z,a):
    return margin(y,p,b,z,0.0)+2*a*inner(z,np.asarray(p,float)-np.asarray(b,float))

def decomposition(y,p,b,z,a,p_a,b_a):
    ya=np.asarray(y,float)+a*np.asarray(z,float)
    g0=margin(y,p,b,z,0.0)
    align=2*a*inner(z,np.asarray(p,float)-np.asarray(b,float))
    baseline_shift=mse(b_a,ya)-mse(b,ya)
    refit=mse(p,ya)-mse(p_a,ya)
    return {'lhs':mse(b_a,ya)-mse(p_a,ya),'rhs':g0+align+baseline_shift+refit,'g0':g0,'alignment':align,'baseline_shift':baseline_shift,'refit':refit}
