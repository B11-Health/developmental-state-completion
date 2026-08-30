import hashlib, json, glob
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
R10=ROOT/'lab_lanes'/'r10_registered_history_calibration'
R11=ROOT/'lab_lanes'/'r11_sensitivity_design'
OUT=Path(__file__).resolve().parent
SCALES=[0.15,0.30,0.45,0.60]
MODELS=['random_forest','extra_trees']

def sha(path):
    h=hashlib.sha256(); h.update(Path(path).read_bytes()); return h.hexdigest()

def gate_from_metrics(df):
    passing=[]
    for name in MODELS:
        z=df[df.estimator==name].sort_values('test_sequence')
        ok=(len(z)==2 and (z.delta_r2>0).all() and float(z.delta_r2.mean())>=0.02 and z.sh_fold_pass.astype(bool).all())
        if ok: passing.append(name)
    return {
        'gate2_pass': len(passing)==2,
        's_adequacy_preserved': all(df[df.estimator==name].s_fold_pass.astype(bool).all() for name in MODELS),
    }

def load_r11(scale):
    xs=[]
    for f in sorted((R11/'results').glob(f'decisions_scale_{scale:.2f}_*.json')):
        xs.extend(json.loads(f.read_text()))
    return xs

def load_r11_metrics(scale):
    fs=sorted((R11/'results').glob(f'metrics_scale_{scale:.2f}_*.csv'))
    return pd.concat([pd.read_csv(f) for f in fs],ignore_index=True)

def summarize(xs, joint_key='joint_success'):
    n=len(xs); A=sum(bool(x['s_adequacy_preserved']) for x in xs); D=sum(bool(x['gate2_pass']) for x in xs); J=sum(bool(x[joint_key]) for x in xs)
    return {'n':n,'A':A,'D':D,'J':J,'A_only':sum(bool(x['s_adequacy_preserved']) and not bool(x['gate2_pass']) for x in xs),'D_only':sum(bool(x['gate2_pass']) and not bool(x['s_adequacy_preserved']) for x in xs),'neither':sum((not bool(x['gate2_pass'])) and (not bool(x['s_adequacy_preserved'])) for x in xs)}

def main():
    report={'hashes':{},'checks':{},'surface':{},'paired':{}}
    for f in [R10/'PREREGISTRATION.md',R10/'r10_history_calibration.py',R11/'PREREGISTRATION.md',R11/'r11_sensitivity_surface.py',R11/'results'/'sensitivity_surface_summary.json']:
        report['hashes'][str(f.relative_to(ROOT))]=sha(f)

    r10=json.loads((R10/'results'/'calibration_decisions.json').read_text())
    ids=[int(x['replicate']) for x in r10]
    report['checks']['r10_exact_reps_0_29']=(len(ids)==30 and sorted(ids)==list(range(30)) and len(set(ids))==30)
    report['r10_four_way']=summarize(r10,'success')

    # Re-derive every R10 decision from its metric rows.
    cm=pd.read_csv(R10/'results'/'calibration_metrics.csv')
    mism=[]
    byid={int(x['replicate']):x for x in r10}
    for rep,z in cm.groupby('replicate'):
        d=gate_from_metrics(z); x=byid[int(rep)]
        if d['gate2_pass']!=bool(x['gate2_pass']) or d['s_adequacy_preserved']!=bool(x['s_adequacy_preserved']) or (d['gate2_pass'] and d['s_adequacy_preserved'])!=bool(x['success']): mism.append(int(rep))
    report['checks']['r10_metric_decision_mismatches']=mism

    data={0.30:{int(x['replicate']):{'gate2_pass':bool(x['gate2_pass']),'s_adequacy_preserved':bool(x['s_adequacy_preserved']),'joint_success':bool(x['success'])} for x in r10[:20]}}
    for scale in [0.15,0.45,0.60]:
        xs=load_r11(scale); ids=[int(x['replicate']) for x in xs]
        report['checks'][f'scale_{scale:.2f}_exact_reps_0_19']=(len(ids)==20 and sorted(ids)==list(range(20)) and len(set(ids))==20)
        report['surface'][f'{scale:.2f}']=summarize(xs)
        data[scale]={int(x['replicate']):x for x in xs}
        m=load_r11_metrics(scale); mism=[]
        byid={int(x['replicate']):x for x in xs}
        for rep,z in m.groupby('replicate'):
            d=gate_from_metrics(z); x=byid[int(rep)]
            if d['gate2_pass']!=bool(x['gate2_pass']) or d['s_adequacy_preserved']!=bool(x['s_adequacy_preserved']) or (d['gate2_pass'] and d['s_adequacy_preserved'])!=bool(x['joint_success']): mism.append(int(rep))
        report['checks'][f'scale_{scale:.2f}_metric_decision_mismatches']=mism
    first20=r10[:20]
    report['surface']['0.30']=summarize(first20,'success')
    report['checks']['r10_first20_are_reps_0_19']=[int(x['replicate']) for x in first20]==list(range(20))

    # Compare committed summary against independent recomputation.
    committed=json.loads((R11/'results'/'sensitivity_surface_summary.json').read_text())
    summary_match=True
    for row in committed:
        key=f"{float(row['scale']):.2f}"; s=report['surface'][key]
        summary_match &= (int(row['n'])==s['n'] and int(row['adequacy_count'])==s['A'] and int(row['gate2_count'])==s['D'] and int(row['joint_count'])==s['J'] and int(row['adequacy_only'])==s['A_only'] and int(row['detection_only'])==s['D_only'] and int(row['neither'])==s['neither'])
    report['checks']['committed_summary_matches_recompute']=bool(summary_match)

    # Pairwise monotonicity diagnostics on identical replicate IDs.
    dviol=[]; aviol=[]; jseq={}
    for rep in range(20):
        ds=[bool(data[s][rep]['gate2_pass']) for s in SCALES]
        aa=[bool(data[s][rep]['s_adequacy_preserved']) for s in SCALES]
        js=[bool(data[s][rep]['joint_success']) for s in SCALES]
        if any(ds[i] and not ds[i+1] for i in range(3)): dviol.append({'replicate':rep,'sequence':ds})
        if any((not aa[i]) and aa[i+1] for i in range(3)): aviol.append({'replicate':rep,'sequence':aa})
        jseq[str(rep)]=js
    report['paired']['detection_nonmonotone_replicates']=dviol
    report['paired']['adequacy_recovery_replicates']=aviol
    report['paired']['joint_success_sets']={f'{s:.2f}':[r for r in range(20) if bool(data[s][r]['joint_success'])] for s in SCALES}

    r10src=(R10/'r10_history_calibration.py').read_text()
    r11src=(R11/'r11_sensitivity_surface.py').read_text()
    r10pre=(R10/'PREREGISTRATION.md').read_text()
    report['checks']['preregistered_seed_text_20260830_plus_r']=('seed 20260830+r' in r10pre)
    report['checks']['r10_implemented_seed_offset_500000']=('SEED+500000+rep' in r10src)
    report['checks']['r11_reuses_r10_implemented_seed_offset_500000']=('r10.SEED+500000+rep' in r11src)
    report['checks']['r11_refuses_refit_0_30']=("0.30 is inherited from R10 and must not be refit" in r11src)
    report['checks']['pooled_outcome_sd_used_for_injection']=('ysd=float(np.std(y))' in r10src and 'ysd=float(np.std(y))' in r11src)
    report['checks']['pooled_SH_residualizer_used']=('Ridge(alpha=1.0).fit(S,z)' in r10src and 'Ridge(alpha=1.0).fit(S,z)' in r11src)

    (OUT/'recomputed_audit_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
