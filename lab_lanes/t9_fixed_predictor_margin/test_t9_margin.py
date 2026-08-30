import importlib.util
from pathlib import Path
import numpy as np
P=Path(__file__).with_name('t9_margin.py'); s=importlib.util.spec_from_file_location('t9',P); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)

def test_random_identity():
    rng=np.random.default_rng(7)
    for n in [5,17,100]:
        y=rng.normal(size=n); p=rng.normal(size=n); b=np.full(n,.3); z=rng.normal(size=n)
        for a in [-2,-.3,0,.4,3]: assert abs(t.margin(y,p,b,z,a)-t.fixed_formula(y,p,b,z,a))<1e-10

def test_orthogonal_invariance():
    rng=np.random.default_rng(8); n=100; y=rng.normal(size=n); p=rng.normal(size=n); b=np.full(n,y.mean()); v=p-b; z=rng.normal(size=n); z=z-v*np.dot(z,v)/np.dot(v,v)
    g=t.margin(y,p,b,z,0)
    for a in [-5,-1,.5,4]: assert abs(t.margin(y,p,b,z,a)-g)<1e-10

def test_refit_decomposition():
    rng=np.random.default_rng(9); n=40; y=rng.normal(size=n); p=rng.normal(size=n); b=np.full(n,.1); z=rng.normal(size=n); pa=p+.2*rng.normal(size=n); ba=np.full(n,.4)
    d=t.decomposition(y,p,b,z,.7,pa,ba); assert abs(d['lhs']-d['rhs'])<1e-10

def test_centered_r2_sign_margin():
    y=np.array([-2.,-1.,1.,2.]); p=np.array([-1.5,-.5,.5,1.5]); b=np.full(4,y.mean()); v=p-b; z=np.array([1.,-1.,-1.,1.]); z=z-z.mean(); z=z-v*np.dot(z,v)/np.dot(v,v); assert abs(z.mean())<1e-12; g=t.margin(y,p,b,z,0); assert g>0
    for a in [0,1,10,100]: assert t.margin(y,p,b,z,a)>0

def test_positive_alignment_can_cross_r2_sign():
    y=np.array([-1.,1.]); z=np.array([-1.,1.]); p=3*y; b=np.zeros(2)
    assert abs(z.mean())<1e-12
    assert np.dot(z,p-b)/len(z)>0
    assert t.margin(y,p,b,z,0)<0
    assert t.margin(y,p,b,z,1)>0

def test_r2_denominator_can_degenerate_under_orthogonality():
    y=np.array([-1.,-1.,1.,1.]); z=-y; p=np.array([1.,-1.,1.,-1.]); b=np.zeros(4)
    assert abs(np.dot(z,p-b)/len(z))<1e-12
    assert abs(t.margin(y,p,b,z,1)-t.margin(y,p,b,z,0))<1e-12
    assert np.var(y+z)==0

if __name__=='__main__': test_random_identity(); test_orthogonal_invariance(); test_refit_decomposition(); test_centered_r2_sign_margin(); test_positive_alignment_can_cross_r2_sign(); test_r2_denominator_can_degenerate_under_orthogonality(); print('T9_TESTS_PASS')
