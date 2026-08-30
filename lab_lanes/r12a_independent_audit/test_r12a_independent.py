import json
from pathlib import Path
BASE=Path(__file__).parent
r=json.loads((BASE/'audit_results.json').read_text())
assert r['checks']['primary']['joint']==16
assert r['checks']['secondary']['adequacy']==30
assert r['checks']['secondary']['gate2']==18
assert r['checks']['secondary']['joint']==18
assert r['checks']['primary_success_set_equals_r10b'] is True
assert r['checks']['primary_metric_decision_mismatches']==[]
assert r['checks']['secondary_metric_decision_mismatches']==[]
assert all(x['max_abs_metric_diff'] < 1e-12 for x in r['spot_refits'])
print('R12A_TESTS_PASS')
