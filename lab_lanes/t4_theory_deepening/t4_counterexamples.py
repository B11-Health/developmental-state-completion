import itertools, json, math
from collections import defaultdict
from pathlib import Path


def cmi_bits(rows):
    # rows are (h,s,y,p)
    p_hsy=defaultdict(float); p_hs=defaultdict(float); p_sy=defaultdict(float); p_s=defaultdict(float)
    for h,s,y,p in rows:
        p_hsy[h,s,y]+=p; p_hs[h,s]+=p; p_sy[s,y]+=p; p_s[s]+=p
    out=0.0
    for (h,s,y),p in p_hsy.items():
        if p:
            out += p*math.log2((p*p_s[s])/(p_hs[h,s]*p_sy[s,y]))
    return out


def intervention_rows(mode):
    rows=[]
    for h in (0,1):
        for s in (0,1):
            y = s if mode == 'observational' else (s ^ h)
            rows.append((h,s,y,0.25))
    return rows


def latent_task_rows(task):
    rows=[]
    # H carries a hidden factor Z; S is a separate present measurement.
    for z in (0,1):
        for s in (0,1):
            h=z
            y = s if task == 'declared' else z
            rows.append((h,s,y,0.25))
    return rows


def powerset(items):
    items=list(items)
    for r in range(len(items)+1):
        for c in itertools.combinations(items,r):
            yield frozenset(c)


def check_submodular(universe, f):
    U=list(universe)
    violations=[]
    subsets=list(powerset(U))
    for A in subsets:
        for B in subsets:
            if not A.issubset(B):
                continue
            for e in U:
                if e in B:
                    continue
                da=f(A|{e})-f(A)
                db=f(B|{e})-f(B)
                if da+1e-12 < db:
                    violations.append({'A':sorted(A),'B':sorted(B),'e':e,'delta_A':da,'delta_B':db})
    return violations


def experiment_signature(exp, world):
    sigs={
        'e1': {0:0,1:0,2:1,3:1},
        'e2': {0:0,1:1,2:0,3:1},
        'e3': {0:0,1:1,2:1,3:0},
    }
    return sigs[exp][world]


def separated_pairs(experiments, worlds=(0,1,2,3)):
    out=set()
    for i,j in itertools.combinations(worlds,2):
        if any(experiment_signature(e,i)!=experiment_signature(e,j) for e in experiments):
            out.add((i,j))
    return out


def main():
    results={}

    # CE1: observational screening-off does not transfer to interventions.
    results['observational_vs_interventional']={
        'I_Y_H_given_S_observational_bits':cmi_bits(intervention_rows('observational')),
        'I_Y_H_given_S_interventional_bits':cmi_bits(intervention_rows('interventional')),
    }

    # CE2: sufficiency is task-indexed; another future can still require H.
    results['task_specificity']={
        'declared_task_CMI_bits':cmi_bits(latent_task_rows('declared')),
        'alternate_task_CMI_bits':cmi_bits(latent_task_rows('alternate')),
    }

    # CE3: pointwise 1-D differential kernel condition can hold while global factorization fails.
    # h=x^2, F=x on two branches; Dh and DF are nonzero at all sampled points, so both kernels are {0}.
    xs=[-2.0,-1.0,1.0,2.0]
    pairs=[]
    for x in xs:
        for xp in xs:
            if x<xp and abs(x*x-xp*xp)<1e-12:
                pairs.append({'x':x,'x_prime':xp,'h':x*x,'F_x':x,'F_x_prime':xp})
    results['local_kernel_not_global_without_fiber_condition']={
        'all_sampled_Dh_nonzero':all(abs(2*x)>0 for x in xs),
        'all_sampled_DF_nonzero':True,
        'same_h_different_F_pairs':pairs,
    }

    # CE4: measurement closeness alone gives no future-response bound.
    results['no_approximate_bound_without_assumption']={
        'x0':0.0,'x1':1.0,'h_difference':0.0,'F_difference':1.0,
        'h':'constant zero','F':'identity'
    }

    # CE5: k-horizon equivalence need not imply k+1 horizon equivalence.
    k=3
    a=[0]*k+[0]
    b=[0]*k+[1]
    results['finite_horizon_not_longer']={
        'k':k,'world_A':a,'world_B':b,
        'same_first_k':a[:k]==b[:k],
        'same_first_k_plus_1':a[:k+1]==b[:k+1],
    }

    # CE6: pointwise minimum of modular functions can be non-submodular.
    # f1=1[a present], f2=1[b present], g=min(f1,f2)=AND.
    def f1(A): return 1.0 if 'a' in A else 0.0
    def f2(A): return 1.0 if 'b' in A else 0.0
    def g(A): return min(f1(A),f2(A))
    v=check_submodular(['a','b'],g)
    results['min_of_modular_non_submodular']={'violations':v,'is_submodular':not bool(v)}

    # TH1 finite separating family <-> pair coverage for the full-family equivalence relation.
    E={'e1','e2','e3'}
    full_pairs=separated_pairs(E)
    subset_checks=[]
    for Q in powerset(E):
        q_pairs=separated_pairs(Q)
        identifies=(q_pairs==full_pairs)
        covers_all=all(pair in q_pairs for pair in full_pairs)
        subset_checks.append({'Q':sorted(Q),'identifies_full_equivalence':identifies,'covers_all_distinguishable_pairs':covers_all,'agreement':identifies==covers_all})
    results['finite_identification_equals_pair_cover']={
        'full_distinguishable_pairs':sorted(map(list,full_pairs)),
        'all_subsets_agree':all(x['agreement'] for x in subset_checks),
        'subset_checks':subset_checks,
    }

    # TH2 numerical sanity for approximate factorization bound:
    # F(x)=g(h(x))+e(x), |e|<=eps => |F-F'|<=L_g |h-h'|+2eps.
    eps=0.1; Lg=2.0
    samples=[-1.0,-0.4,0.0,0.7,1.3]
    def h(x): return x
    def gfun(z): return 2*z
    def err(x): return eps*math.sin(x)
    def F(x): return gfun(h(x))+err(x)
    checks=[]
    for x,xp in itertools.combinations(samples,2):
        lhs=abs(F(x)-F(xp)); rhs=Lg*abs(h(x)-h(xp))+2*eps
        checks.append({'x':x,'x_prime':xp,'lhs':lhs,'rhs':rhs,'holds':lhs<=rhs+1e-12})
    results['approximate_factorization_bound_sanity']={'epsilon':eps,'L_g':Lg,'all_hold':all(c['holds'] for c in checks),'checks':checks}

    out=Path(__file__).with_name('t4_results.json')
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps({k:(v if isinstance(v,(int,float,str,bool)) else 'ok') for k,v in results.items()},indent=2))

if __name__=='__main__':
    main()
