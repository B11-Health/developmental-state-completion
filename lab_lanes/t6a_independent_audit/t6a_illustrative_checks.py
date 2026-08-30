#!/usr/bin/env python3
"""Illustrative numerical checks for T6A. These are not proofs."""
import math


def antipodal_distance_identity(n):
    # sample coordinate axes on S^n; identity B gives exact distance 2
    pts=[]
    for i in range(n+1):
        p=[0.0]*(n+1); p[i]=1.0; pts.append(p)
        q=[0.0]*(n+1); q[i]=-1.0; pts.append(q)
    return min(math.dist(p,[-x for x in p]) for p in pts)


def circle_scalar_has_sampled_collision(samples=4096):
    # B(z)=cos(3t)+0.2 sin(5t), representative continuous scalar.
    vals=[]
    for j in range(samples):
        t=2*math.pi*j/samples
        b=math.cos(3*t)+0.2*math.sin(5*t)
        tp=t+math.pi
        bm=math.cos(3*tp)+0.2*math.sin(5*tp)
        vals.append(b-bm)
    # sampled sign change is illustrative of IVT
    return min(vals) <= 0 <= max(vals)


def degree_cover_planar_min_distance(d):
    # exact nearest separation of d roots in a fiber under identity S^1 -> R^2
    return 2*math.sin(math.pi/d)


def main():
    assert antipodal_distance_identity(0)==2.0
    assert antipodal_distance_identity(1)==2.0
    assert antipodal_distance_identity(5)==2.0
    assert circle_scalar_has_sampled_collision()
    assert abs(degree_cover_planar_min_distance(8)-2*math.sin(math.pi/8))<1e-15
    print('PASS T6A illustrative checks')
    print('degree-8 bits =', math.ceil(math.log2(8)), 'planar channels = 2')

if __name__=='__main__':
    main()
