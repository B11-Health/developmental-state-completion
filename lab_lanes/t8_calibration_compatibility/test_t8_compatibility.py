import importlib.util
from pathlib import Path
p=Path(__file__).with_name('t8_compatibility.py')
spec=importlib.util.spec_from_file_location('t8',p); t8=importlib.util.module_from_spec(spec); spec.loader.exec_module(t8)

def test_identity():
    for r0 in [0.2,0.5,0.8,1.0]:
        for x in [0,0.1,1,10]:
            c=t8.curves(r0,x)
            assert abs((c['r2_sh']-c['r2_s'])-c['delta'])<1e-12

def test_compatibility_boundary():
    rho=.6; delta=.2; boundary=rho/(1-delta)
    assert not t8.compatible(boundary-1e-9,rho,delta)
    assert t8.compatible(boundary,rho,delta)
    lo,hi=t8.interval_x(boundary,rho,delta); assert abs(lo-hi)<1e-12

def test_impossible_threshold_pair(): assert not t8.compatible(1.0,.8,.25)

def test_witness():
    r0=.8; rho=.5; delta=.1; lo,hi=t8.interval_x(r0,rho,delta); c=t8.curves(r0,(lo+hi)/2); assert c['r2_s']>=rho and c['delta']>=delta

def test_generalized_q():
    c=t8.generalized_curves(.8,.025,.2)
    assert abs(c['r2_s']-32/41)<1e-12
    assert abs(c['r2_sh']-1.0)<1e-12
    assert abs(c['delta']-9/41)<1e-12
    lo,hi=t8.generalized_interval_x(.8,.75,.1,.2)
    assert lo==0.0 and hi>0
    assert t8.generalized_compatible(.8,.75,.1,.2)

if __name__=='__main__':
    test_identity(); test_compatibility_boundary(); test_impossible_threshold_pair(); test_witness(); test_generalized_q(); print('T8_TESTS_PASS')
