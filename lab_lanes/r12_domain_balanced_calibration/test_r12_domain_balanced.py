import json
from pathlib import Path
BASE=Path(__file__).parent
ROOT=BASE.parents[1]
OUT=BASE/'results'

def load(prefix):
    xs=[]
    for f in sorted(OUT.glob(prefix+'_decisions_*.json')): xs += json.loads(f.read_text())
    return xs

def success_set(xs): return {int(x['replicate']) for x in xs if x['success']}

def main():
    pri=load('domain_balanced'); sec=load('domainwise_residualizer')
    assert sorted(int(x['replicate']) for x in pri)==list(range(30))
    assert sorted(int(x['replicate']) for x in sec)==list(range(30))
    ref=[]
    for f in sorted((ROOT/'lab_lanes/r10b_seed_remediation/results').glob('decisions_*.json')): ref += json.loads(f.read_text())
    assert success_set(pri)==success_set(ref)
    assert sum(x['success'] for x in pri)==16
    assert sum(x['s_adequacy_preserved'] for x in pri)==22
    assert sum(x['gate2_pass'] for x in pri)==19
    assert sum(x['success'] for x in sec)==18
    assert sum(x['s_adequacy_preserved'] for x in sec)==30
    assert sum(x['gate2_pass'] for x in sec)==18
    for xs in (pri,sec):
        for x in xs:
            for st in x['sequence_stats'].values():
                assert abs(st['balanced_mean'])<1e-10
                assert abs(st['balanced_sd']-1.0)<1e-10
    print('R12_TESTS_PASS')
if __name__=='__main__': main()
