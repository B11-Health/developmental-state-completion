import json
from pathlib import Path

def curves(r0,x):
    """Simple audited envelope: q=0, i.e. E[E|S,H]=0."""
    return {"r2_s":r0/(1+x),"r2_sh":(r0+x)/(1+x),"delta":x/(1+x)}

def generalized_curves(r0,x,q):
    """General augmented-information form with q=Var(E[E|S,H])/B."""
    return {"r2_s":r0/(1+x),"r2_sh":(r0+x+q)/(1+x),"delta":(x+q)/(1+x)}

def compatible(r0,rho,delta):
    return r0 >= rho/(1-delta)

def interval_x(r0,rho,delta):
    return delta/(1-delta), r0/rho-1

def generalized_interval_x(r0,rho,delta,q):
    return max(0.0,(delta-q)/(1-delta)), r0/rho-1

def generalized_compatible(r0,rho,delta,q):
    if r0 < rho: return False
    lo,hi=generalized_interval_x(r0,rho,delta,q)
    return lo <= hi

def main():
    cases=[]
    for r0,rho,delta in [(0.8,0.5,0.1),(0.55,0.5,0.1),(0.9,0.8,0.25),(1.0,0.8,0.25),(0.7,0.6,0.2)]:
        lo,hi=interval_x(r0,rho,delta); ok=compatible(r0,rho,delta); witness=None
        if ok:
            x=(lo+hi)/2; c=curves(r0,x); witness={"x":x,**c,"passes":c["r2_s"]>=rho-1e-12 and c["delta"]>=delta-1e-12}
        cases.append({"r0":r0,"rho":rho,"delta_required":delta,"compatible":ok,"x_lower":lo,"x_upper":hi,"delta_max":(1-rho/r0 if r0>=rho else None),"witness":witness})
    q_case={"r0":0.8,"x":0.025,"q":0.2,**generalized_curves(0.8,0.025,0.2)}
    out={"cases":cases,"generalized_example":q_case}
    Path(__file__).with_name('t8_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
