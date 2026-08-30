import json, math
from pathlib import Path


def sphere_constant_decoder_error(samples=2000):
    # deterministic latitude/angle samples on S^2; decoder y=0
    worst=0.0
    for i in range(samples):
        z=-1.0+2.0*(i+0.5)/samples
        theta=(i*2.399963229728653)%(2*math.pi)
        r=math.sqrt(max(0.0,1-z*z))
        x=(r*math.cos(theta),r*math.sin(theta),z)
        err=math.sqrt(sum(a*a for a in x))
        worst=max(worst,err)
    return worst


def antipodal_margin_identity(samples=4096):
    m=float('inf')
    for i in range(samples):
        t=2*math.pi*i/samples
        x=(math.cos(t),math.sin(t))
        xm=(-x[0],-x[1])
        d=math.dist(x,xm)
        m=min(m,d)
    return m


def circle_scalar_collision(samples=4096):
    # B(theta)=cos(theta)+0.37*sin(2theta); D(theta)=B(theta)-B(theta+pi)
    vals=[]
    for i in range(samples+1):
        t=2*math.pi*i/samples
        B=lambda u: math.cos(u)+0.37*math.sin(2*u)
        vals.append(B(t)-B(t+math.pi))
    min_abs=min(abs(v) for v in vals)
    sign_change=any(vals[i]==0 or vals[i]*vals[i+1]<0 for i in range(samples))
    return min_abs, sign_change


def finite_cover_margin():
    # 3-sheet trivial compact cover over sampled circle with moving, noncolliding R^2 sheet values.
    m=float('inf')
    for i in range(4096):
        t=2*math.pi*i/4096
        pts=[(math.cos(t)+3*j, math.sin(t)) for j in range(3)]
        for a in range(3):
            for b in range(a+1,3):
                m=min(m,math.dist(pts[a],pts[b]))
    return m


def noise_threshold_demo(delta=2.0):
    # Two sensor points at 0 and delta on R. Closed eta-balls first touch at delta/2.
    return {'delta':delta,'safe_eta_example':0.49*delta/2,'touch_eta':delta/2,'overlap_eta':0.51*delta}


def tv_midpoint_discrete():
    # P=(1,0), Q=(0,1), M=(.5,.5), TV=.5*l1
    P=(1.0,0.0);Q=(0.0,1.0);M=(0.5,0.5)
    tv=lambda A,B:0.5*sum(abs(a-b) for a,b in zip(A,B))
    return tv(P,Q),tv(P,M),tv(Q,M)


def w1_two_point_midpoint():
    # delta_-1, delta_+1, mixture midpoint. On line, W1 via CDF gives 2 and 1,1.
    return 2.0,1.0,1.0


def noncompact_margin(sequence_n=100000):
    return 1.0/(1.0+sequence_n)


def main():
    min_abs, sign_change=circle_scalar_collision()
    results={
        'sphere_constant_decoder_worst_error': sphere_constant_decoder_error(),
        'identity_antipodal_margin_S1': antipodal_margin_identity(),
        'circle_scalar_sample_min_abs_difference': min_abs,
        'circle_scalar_sign_change_detected': sign_change,
        'compact_trivial_3cover_sample_margin': finite_cover_margin(),
        'noise_threshold_demo': noise_threshold_demo(),
        'tv_pair_and_midpoint_distances': tv_midpoint_discrete(),
        'w1_pair_and_midpoint_distances': w1_two_point_midpoint(),
        'noncompact_margin_at_t_100000': noncompact_margin(),
    }
    out=Path(__file__).with_name('t7_results.json')
    out.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
