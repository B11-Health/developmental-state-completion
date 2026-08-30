from itertools import combinations

def supdist(a,b): return max(abs(x-y) for x,y in zip(a,b))

# T5: 2 eta distance perturbation bound.
true={'a':(0.0,1.0),'b':(2.0,-1.0),'c':(0.4,0.5)}
eta=0.1
est={'a':(0.1,0.9),'b':(1.9,-0.9),'c':(0.3,0.6)}
for u,v in combinations(true,2):
    assert abs(supdist(est[u],est[v])-supdist(true[u],true[v])) <= 2*eta+1e-12

# C2: arbitrarily small perturbation can split threshold graph at a critical edge.
def comps(vals,delta):
    n=len(vals); adj=[set() for _ in range(n)]
    for i,j in combinations(range(n),2):
        if abs(vals[i]-vals[j]) <= delta:
            adj[i].add(j); adj[j].add(i)
    seen=set(); out=[]
    for i in range(n):
        if i in seen: continue
        stack=[i]; seen.add(i); c=[]
        while stack:
            x=stack.pop(); c.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
        out.append(tuple(sorted(c)))
    return sorted(out)
assert comps([0,1,2],1)==[(0,1,2)]
assert comps([0,1+1e-9,2],1)!=[(0,1,2)]

# T4: finite Test Cover separation criterion.
worlds=['00','01','10','11']
tests={'q0':lambda w:w[0], 'q1':lambda w:w[1]}
def sig(w,panel): return tuple(tests[q](w) for q in panel)
def separates(panel): return len({sig(w,panel) for w in worlds})==len(worlds)
assert not separates(['q0']) and not separates(['q1']) and separates(['q0','q1'])

# T7 robust-min non-submodularity witness.
def f1(Q): return int('a' in Q)
def f2(Q): return int('b' in Q)
def g(Q): return min(f1(Q),f2(Q))
A=frozenset({'a'}); B=frozenset({'b'})
assert g(A)+g(B) < g(A|B)+g(A&B)

# Observational-vs-interventional SCM counterexample: A=H observationally -> Y=0; do(A=0) -> Y=H.
obs=[(h,h,h^h) for h in (0,1)]
interv=[(h,0,h^0) for h in (0,1)]
assert {y for _,_,y in obs}=={0}
assert {y for _,_,y in interv}=={0,1}
print('T4 theory tests PASS')
