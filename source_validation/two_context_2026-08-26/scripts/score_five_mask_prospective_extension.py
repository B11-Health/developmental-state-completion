import ast,json,hashlib,numpy as np
from pathlib import Path
R=Path('/root/plant_m2_reeb_global')
fr=json.load(open(R/'FIVE_MASK_PROSPECTIVE_EXTENSION_FROZEN_2026-08-26.json'))
# Load the exact already-frozen estimator definitions from the referenced script, without executing its old14/near12 evaluation tail.
ref=R/fr['estimator']['reference_algorithm']; rawsrc=ref.read_bytes(); assert hashlib.sha256(rawsrc).hexdigest()==fr['estimator']['reference_algorithm_sha256']
tree=ast.parse(rawsrc.decode()); nodes=[]
for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name=='evalset': break
    nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ref),'exec'),ns)
dec=ns['dec']; reconstruct=ns['reconstruct']; MASKS=ns['MASKS']; raw=ns['raw']; F=ns['F']
parent=R/'two_phenotype_prospective_source'; ext=R/'five_mask_prospective_extension_source'
seen=set(fr['already_rendered_states'])
def path(law,st):
    ss=f'{st:04b}'; return (parent if ss in seen else ext)/f'{law}_{ss}.tsv'
# decode all 128 source phenotypes once with frozen estimator
cache={}; ph=[]
for law,g0 in fr['laws'].items():
    g=np.array(g0,float)
    for st in range(16):
        y=raw(path(law,st)); u=dec(y); cache[(law,st)]=u
        bits=np.array([int(c) for c in f'{st:04b}'],float); utrue=bits*g; yhat=F(u); ytrue=F(utrue)
        ph.append({'law':law,'state':f'{st:04b}','new_render':f'{st:04b}' not in seen,
                   'u_L2':float(np.linalg.norm(u-utrue)),
                   'surrogate_inversion_raw_L2':float(np.linalg.norm(yhat-y)),
                   'surrogate_at_true_u_raw_L2':float(np.linalg.norm(ytrue-y))})
def summ(a):
    a=np.asarray(a,float);return {'median':float(np.median(a)),'p95':float(np.quantile(a,.95)),'max':float(a.max())}
outm={}; allpred=True
for q in MASKS:
    code=f'{q:04b}'; oriented=[]; unordered=[]
    for law,g0 in fr['laws'].items():
        g=np.array(g0,float); weak=np.where(g<=.001001)[0].tolist()
        for st in range(16):
            bits=np.array([int(c) for c in f'{st:04b}']); true=(1-2*bits)*g
            hat=reconstruct(cache[(law,st)],cache[(law,st^q)],q)
            rec={'law':law,'state':f'{st:04b}','partner':f'{st^q:04b}','L2':float(np.linalg.norm(hat-true)),
                 'sign_correct':bool(np.all(np.sign(hat)==np.sign(true))),
                 'weak_sign_correct':bool(all(np.sign(hat[j])==np.sign(true[j]) for j in weak)) if weak else None,
                 'min_gain':float(g.min())}
            oriented.append(rec)
            if st < (st^q): unordered.append(rec)
    sign=float(np.mean([r['sign_correct'] for r in oriented])); E=[r['L2'] for r in oriented]
    weak=[r for r in oriented if r['weak_sign_correct'] is not None]
    pred=sign==1 and np.median(E)<.001 and max(E)<.002 and all(r['weak_sign_correct'] for r in weak)
    allpred &= pred
    outm[code]={'n_oriented':len(oriented),'n_unordered_pairs':len(unordered),'sign_accuracy':sign,'signed_L2':summ(E),
                'weak_001_oriented_n':len(weak),'weak_001_sign_accuracy':float(np.mean([r['weak_sign_correct'] for r in weak])) if weak else None,
                'predictions_pass':bool(pred),'worst':sorted(oriented,key=lambda r:r['L2'],reverse=True)[:8]}
out={'freeze_sha':fr['sha256_pre_render'],'parent_freeze_sha':fr['parent_freeze_sha'],'estimator_reference_sha256':fr['estimator']['reference_algorithm_sha256'],
     'n_source_phenotypes_total':len(ph),'n_new_renders':sum(r['new_render'] for r in ph),
     'phenotype_decode_u_L2':summ([r['u_L2'] for r in ph]),
     'phenotype_surrogate_inversion_raw_L2':summ([r['surrogate_inversion_raw_L2'] for r in ph]),
     'phenotype_surrogate_at_true_u_raw_L2':summ([r['surrogate_at_true_u_raw_L2'] for r in ph]),
     'masks':outm,'all_preregistered_predictions_pass':bool(allpred),
     'scope_warning':fr['scope_warning'],'worst_phenotype_decode':sorted(ph,key=lambda r:r['u_L2'],reverse=True)[:10]}
json.dump(out,open(R/'FIVE_MASK_PROSPECTIVE_EXTENSION_RESULTS_2026-08-26.json','w'),indent=2)
print(json.dumps(out,indent=2))
