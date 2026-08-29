import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'source_validation' / 'two_context_2026-08-26'
META = ROOT / 'metadata'
EXPECTED = {
    'parent_freeze': 'b5fdc0bd257dbb57874f107b3c7a12b6c9fe5ec9f89cb48de585743846341c3a',
    'extension_freeze': '7d4845aa8a50da5e5d8ffd2b0bc65e02311882879a261df8c313b4557d47663f',
    'cubic': 'd7e4027e4ed252225b5f5db87b758df31c67d94c02af1680ce172dc9b6074340',
    'linear': '856bcc7076af37d7a548e720dfe1cebcfd7acc92f35997b683e1e7c56cffe904',
    'algorithm': 'bbebc27b2ec562c2d5d83b69dd2b8c45a6b43ca36adb87b91d9bd4994dfe4508',
    'parent_manifest': '276c7e66357604d44e2ff4cddd94d7c2fd3c8f2f64873c18898389d2f22d9dbd',
    'extension_manifest': '19c8c9e72e69fa4175ef6a15d80c897f362662f6cfa900adcc9fedf50287004a',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_freeze(path):
    d=json.loads(path.read_text())
    stored=d.pop('sha256_pre_render')
    raw=json.dumps(d,sort_keys=True,separators=(',',':')).encode()
    return stored, hashlib.sha256(raw).hexdigest()

def source_manifest(folder):
    rows=[]
    for p in sorted(folder.glob('*.tsv')):
        rows.append(p.name+'\0'+sha(p))
    return len(rows),hashlib.sha256('\n'.join(rows).encode()).hexdigest()

def check(cond,msg):
    if not cond: raise AssertionError(msg)
    print('PASS',msg)

def main():
    pstore,pcalc=canonical_freeze(META/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json')
    estore,ecalc=canonical_freeze(META/'FIVE_MASK_PROSPECTIVE_EXTENSION_FROZEN_2026-08-26.json')
    check(pstore==pcalc==EXPECTED['parent_freeze'],'parent canonical pre-render freeze hash')
    check(estore==ecalc==EXPECTED['extension_freeze'],'extension canonical pre-render freeze hash')
    check(sha(ROOT/'models/RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz')==EXPECTED['cubic'],'frozen cubic decoder hash')
    check(sha(ROOT/'models/TWO_PHENOTYPE_LINEAR_U_DECODER_FROZEN_2026-08-26.npz')==EXPECTED['linear'],'frozen linear initializer hash')
    check(sha(ROOT/'scripts/five_two_context_nonlinear_decoder.py')==EXPECTED['algorithm'],'frozen reference algorithm hash')
    pn,ph=source_manifest(ROOT/'parent_source'); en,eh=source_manifest(ROOT/'extension_source')
    check(pn==64 and ph==EXPECTED['parent_manifest'],'64 parent source renders + aggregate manifest')
    check(en==64 and eh==EXPECTED['extension_manifest'],'64 extension source renders + aggregate manifest')

    parent=json.loads((META/'results.json').read_text())
    audit=json.loads((META/'TWO_PHENOTYPE_PROSPECTIVE_AUDIT_V2_2026-08-26.json').read_text())
    check(parent['freeze_sha']==EXPECTED['parent_freeze'],'parent result points to frozen commitment')
    check(parent['n_pairs']==32,'parent has 32 complementary source pairs')
    check(parent['sign_accuracy']==1.0,'parent sign recovery = 100%')
    check(parent['signed_L2_median'] < 0.001,'parent median signed L2 < frozen 0.001 threshold')
    check(parent['signed_L2_max'] < 0.002,'parent max signed L2 < frozen 0.002 threshold')
    check(parent['weak_001_all_sign_correct'] is True,'all parent 0.001 weak-coordinate signs correct')
    check(parent['predictions_pass'] is True,'all parent preregistered predictions pass')
    check(audit['n_source_phenotypes']==64 and audit['n_complement_pairs']==32,'audit covers 64 phenotypes / 32 complement pairs')
    check(audit['phenotype_decode']['surrogate_reconstruction_dIoU']['max'] < 1e-6,'parent max surrogate reconstruction dIoU < 1e-6')

    ext=json.loads((META/'FIVE_MASK_PROSPECTIVE_EXTENSION_RESULTS_2026-08-26.json').read_text())
    check(ext['freeze_sha']==EXPECTED['extension_freeze'],'extension result points to frozen commitment')
    check(ext['parent_freeze_sha']==EXPECTED['parent_freeze'],'extension is linked to parent freeze')
    check(ext['all_preregistered_predictions_pass'] is True,'all extension preregistered predictions pass')
    masks=ext['masks']
    check(set(masks)=={'0111','1011','1101','1110','1111'},'all five frozen masks present')
    for m,r in sorted(masks.items()):
        check(r['sign_accuracy']==1.0,f'mask {m} sign recovery = 100%')
        check(r['signed_L2']['median'] < 0.001,f'mask {m} median signed L2 < 0.001')
        check(r['signed_L2']['max'] < 0.002,f'mask {m} max signed L2 < 0.002')
        check(r['weak_001_sign_accuracy'] == 1.0,f'mask {m} all 0.001 weak-coordinate signs correct')
        check(r['predictions_pass'] is True,f'mask {m} preregistered predictions pass')
    print('BUNDLE_VERIFICATION_COMPLETE')

if __name__=='__main__': main()
