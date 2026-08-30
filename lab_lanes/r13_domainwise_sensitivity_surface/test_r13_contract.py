import importlib.util
from pathlib import Path
P=Path(__file__).with_name('r13_surface.py'); s=importlib.util.spec_from_file_location('r13',P); r=importlib.util.module_from_spec(s); s.loader.exec_module(r)
assert r.SCALES==[0.15,0.30,0.45,0.60]
assert r.NEW_SCALES=={0.15,0.45,0.60}
assert r.N==30
x=r.inherited_030(); assert len(x)==30 and sorted(z['replicate'] for z in x)==list(range(30))
assert sum(z['joint_success'] for z in x)==18
print('R13_CONTRACT_TEST_PASS')
