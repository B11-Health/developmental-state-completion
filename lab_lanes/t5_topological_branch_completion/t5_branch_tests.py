import itertools, json, math
from collections import defaultdict
from pathlib import Path


def entropy_bits(ps):
    return -sum(p*math.log2(p) for p in ps if p>0)


def cmi(rows, ix, iy, iz):
    # rows=(tuple variables, probability); calculate I(X;Y|Z)
    xyz=defaultdict(float); xz=defaultdict(float); yz=defaultdict(float); zc=defaultdict(float)
    for vals,p in rows:
        x=tuple(vals[i] for i in ix); y=tuple(vals[i] for i in iy); z=tuple(vals[i] for i in iz)
        xyz[x,y,z]+=p; xz[x,z]+=p; yz[y,z]+=p; zc[z]+=p
    out=0.0
    for (x,y,z),p in xyz.items():
        if p:
            out += p*math.log2((p*zc[z])/(xz[x,z]*yz[y,z]))
    return out


def sign_branch_demo():
    xs=[-3,-2,-1,1,2,3]
    rows=[]
    for x in xs:
        h=x*x; b=1 if x>0 else 0; f=x
        reconstructed=(1 if b else -1)*math.sqrt(h)
        rows.append({'x':x,'h':h,'branch':b,'F':f,'reconstructed':reconstructed,'ok':abs(f-reconstructed)<1e-12})
    same_h_conflicts=[]
    for a,b in itertools.combinations(rows,2):
        if a['h']==b['h'] and a['F']!=b['F']:
            same_h_conflicts.append({'h':a['h'],'F_values':[a['F'],b['F']]})
    return {'rows':rows,'h_alone_not_factorizing':bool(same_h_conflicts),'conflicts':same_h_conflicts,'h_plus_branch_factorizes':all(r['ok'] for r in rows)}


def history_proxy_demo(noise=0.15):
    # Z is measured continuous-ish present coordinate class; B is hidden branch.
    # Future Y is branch-dependent. Older history H is a noisy proxy for B.
    # Once B is added to present, H has zero residual information about Y.
    rows=[]
    for z in (0,1):
        for b in (0,1):
            y=(z,b)  # future signature needs both measured z and hidden branch b
            for h in (0,1):
                ph=(1-noise) if h==b else noise
                rows.append(((z,b,y,h),0.25*ph))
    # indices 0=Z,1=B,2=Y(tuple),3=H
    ih_given_z=cmi(rows,[2],[3],[0])
    ih_given_zb=cmi(rows,[2],[3],[0,1])
    theoretical=1-entropy_bits([noise,1-noise])
    return {'noise':noise,'I_Y_H_given_Z_bits':ih_given_z,'I_Y_H_given_Z_B_bits':ih_given_zb,'binary_channel_expected_bits':theoretical,'history_becomes_redundant_after_branch_measurement':abs(ih_given_zb)<1e-12}


def bit_lower_bound_demo(max_m=17):
    out=[]
    for m in range(1,max_m+1):
        lower=math.ceil(math.log2(m)) if m>1 else 0
        # A k-bit code has <=2^k labels. Pigeonhole test.
        insufficient=(2**max(0,lower-1)<m) if lower>0 else False
        sufficient=2**lower>=m
        out.append({'future_distinct_branch_classes':m,'min_bits_lower_bound':lower,'lower_minus_one_insufficient':insufficient,'lower_bits_capacity_sufficient':sufficient})
    return out


def intervention_component_demo():
    # Six connected components C0..C5 at same measured z.
    # Full intervention signature merges components with identical futures.
    comps=['C0','C1','C2','C3','C4','C5']
    sig={
      'e0':{'C0':0,'C1':0,'C2':0,'C3':1,'C4':1,'C5':1},
      'e1':{'C0':0,'C1':0,'C2':1,'C3':0,'C4':0,'C5':1},
      'e2':{'C0':0,'C1':0,'C2':1,'C3':1,'C4':1,'C5':0},
    }
    E=list(sig)
    def signature(c,Q): return tuple(sig[e][c] for e in Q)
    full_groups=defaultdict(list)
    for c in comps: full_groups[signature(c,E)].append(c)
    classes=list(full_groups.values())
    # C0/C1 are deliberately future-equivalent; C3/C4 also equivalent.
    pairs=[]
    for i,a in enumerate(classes):
        for b in classes[i+1:]:
            pairs.append((a[0],b[0]))
    def separates(Q,a,b): return signature(a,Q)!=signature(b,Q)
    valid=[]
    for k in range(len(E)+1):
        for Q in itertools.combinations(E,k):
            if all(separates(Q,a,b) for a,b in pairs): valid.append(Q)
        if valid: break
    min_k=len(valid[0]) if valid else None
    return {'components':comps,'full_response_classes':classes,'raw_component_count':len(comps),'future_response_class_count':len(classes),'branch_label_bits_raw':math.ceil(math.log2(len(comps))),'branch_label_bits_after_future_equivalence':math.ceil(math.log2(len(classes))),'minimum_separating_experiment_count':min_k,'minimum_panels':[list(x) for x in valid]}


def approximate_class_demo():
    # Scalar future signatures for disconnected components at fixed measured z.
    vals=[0.00,0.03,0.08,0.51,0.55,1.20]
    eps=0.10
    # Find minimum partition into groups each having diameter <= eps.
    n=len(vals); best=n
    # sorted 1D optimum by dynamic programming
    dp=[10**9]*(n+1); dp[0]=0
    prev=[None]*(n+1)
    for i in range(n):
        for j in range(i,n):
            if vals[j]-vals[i]<=eps:
                if dp[j+1]>dp[i]+1:
                    dp[j+1]=dp[i]+1; prev[j+1]=i
            else: break
    k=dp[n]; groups=[]; j=n
    while j>0:
        i=prev[j]; groups.append(vals[i:j]); j=i
    groups.reverse()
    return {'future_values':vals,'diameter_tolerance':eps,'minimum_response_classes':k,'groups':groups,'minimum_bits':math.ceil(math.log2(k)) if k>1 else 0}


def intervention_refinement_demo():
    # Observation alone merges A/B. Intervention splits them; C remains equivalent to B here.
    worlds=['A','B','C']
    obs={'A':0,'B':0,'C':1}
    pert={'A':0,'B':1,'C':1}
    def classes(maps):
        g=defaultdict(list)
        for w in worlds: g[tuple(mp[w] for mp in maps)].append(w)
        return list(g.values())
    return {'observational_classes':classes([obs]),'observation_plus_intervention_classes':classes([obs,pert]),'refines':len(classes([obs,pert]))>=len(classes([obs]))}


def main():
    out={
      'sign_branch_factorization':sign_branch_demo(),
      'history_proxy_branch_completion':history_proxy_demo(),
      'bit_lower_bound':bit_lower_bound_demo(),
      'component_response_equivalence_and_test_cover':intervention_component_demo(),
      'approximate_branch_compression':approximate_class_demo(),
      'intervention_refinement':intervention_refinement_demo(),
    }
    path=Path(__file__).with_name('t5_results.json'); path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
