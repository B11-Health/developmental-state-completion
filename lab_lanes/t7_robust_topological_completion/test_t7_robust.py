import importlib.util
from pathlib import Path

P=Path(__file__).with_name('t7_robust_tests.py')
spec=importlib.util.spec_from_file_location('t7',P); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_constant_decoder():
    assert abs(m.sphere_constant_decoder_error()-1.0)<1e-12

def test_identity_margin():
    assert abs(m.antipodal_margin_identity()-2.0)<1e-12

def test_circle_scalar_collision_witness():
    _,sc=m.circle_scalar_collision(); assert sc

def test_compact_cover_margin():
    assert m.finite_cover_margin()>2.99

def test_tv_midpoint():
    pq,pm,qm=m.tv_midpoint_discrete(); assert pq==1.0 and pm==qm==0.5

def test_w1_midpoint():
    pq,pm,qm=m.w1_two_point_midpoint(); assert pq==2.0 and pm==qm==1.0

def test_noncompact_margin_decay():
    assert m.noncompact_margin(100000)<1e-4

if __name__=='__main__':
    tests=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
    for t in tests:
        t(); print('PASS',t.__name__)
