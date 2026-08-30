import json
from pathlib import Path
P=Path(__file__).parent/'results'/'surface_summary.json'; d=json.loads(P.read_text())
s=d['summary']; got=[(x['scale'],x['adequacy_count'],x['gate2_count'],x['joint_count']) for x in s]
assert got==[(0.15,30,1,1),(0.3,30,18,18),(0.45,27,23,22),(0.6,27,22,20)]
assert max(x['joint_count'] for x in s)==22
assert all(x['joint_count']<24 for x in s)
paired=d['paired']; assert len(paired)==30 and sorted(x['replicate'] for x in paired)==list(range(30))
for r in paired: assert len(r['adequacy'])==len(r['detection'])==len(r['joint'])==4
assert [r['replicate'] for r in paired if r['detection']==[False,True,True,False]]==[3]
print('R13_RESULTS_TEST_PASS')
