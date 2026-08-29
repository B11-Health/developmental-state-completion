import itertools, math
import numpy as np


def far_pairs(structural, epsilon):
    n=structural.shape[0]
    return {(i,j) for i in range(n) for j in range(i+1,n) if structural[i,j] > epsilon}

def separation_sets(responses, structural, epsilon, delta):
    # responses shape: worlds x tests x coordinates
    U=far_pairs(structural,epsilon); covers=[]
    for q in range(responses.shape[1]):
        sq=set()
        for i,j in U:
            if np.max(np.abs(responses[i,q]-responses[j,q])) > delta:
                sq.add((i,j))
        covers.append(sq)
    return U,covers

def brute_kappa(U,covers):
    if not U:return 0,()
    if set().union(*covers) != U:return math.inf,()
    for k in range(1,len(covers)+1):
        for comb in itertools.combinations(range(len(covers)),k):
            if set().union(*(covers[q] for q in comb)) == U:return k,comb
    return math.inf,()

def greedy_cover(U,covers):
    uncovered=set(U);chosen=[]
    while uncovered:
        gains=[len(uncovered & s) if i not in chosen else -1 for i,s in enumerate(covers)]
        q=int(np.argmax(gains))
        if gains[q] <= 0:return math.inf,tuple(chosen)
        chosen.append(q);uncovered-=covers[q]
    return len(chosen),tuple(chosen)

def epsilon_floor(responses, structural, delta):
    n=structural.shape[0];mx=0.0
    for i in range(n):
        for j in range(i+1,n):
            dfull=max(np.max(np.abs(responses[i,q]-responses[j,q])) for q in range(responses.shape[1]))
            if dfull <= delta:mx=max(mx,float(structural[i,j]))
    return mx

def packing_lower_bound(P,R,Delta,r=1):
    if P <= 1:return 0
    return math.ceil(math.log(P)/(r*math.log(1+2*R/Delta)))

def random_panel_bound(M,p,beta):
    if M<=0:return 0
    return math.ceil(math.log(M/beta)/p)

def robust_distance_bound(true_a,true_b,obs_a,obs_b):
    true=float(np.max(np.abs(true_a-true_b)));obs=float(np.max(np.abs(obs_a-obs_b)))
    return true,obs,abs(true-obs)

def toy_demo():
    # Eight worlds encoded by three latent bits. Three informative binary tests
    # exactly recover the bits; a fourth test is redundant.
    bits=np.array([[int(c) for c in f'{i:03b}'] for i in range(8)],float)
    responses=np.zeros((8,4,1))
    responses[:,0,0]=bits[:,0]
    responses[:,1,0]=bits[:,1]
    responses[:,2,0]=bits[:,2]
    responses[:,3,0]=bits[:,0]  # redundant
    structural=np.linalg.norm(bits[:,None,:]-bits[None,:,:],axis=2)
    U,covers=separation_sets(responses,structural,epsilon=0,delta=0)
    opt=brute_kappa(U,covers);greedy=greedy_cover(U,covers)
    print('toy_worlds',len(bits),'far_pairs',len(U))
    print('exact_kappa',opt,'greedy',greedy,'binary_counting_lower_bound',math.ceil(math.log2(len(bits))))
    assert opt[0]==3 and greedy[0]==3
    # Full-panel floor after making worlds 0 and 1 observationally identical.
    aliased=responses.copy();aliased[1]=aliased[0]
    floor=epsilon_floor(aliased,structural,delta=0)
    U2,c2=separation_sets(aliased,structural,epsilon=0.5*floor,delta=0)
    k2=brute_kappa(U2,c2)[0]
    print('aliased_epsilon_floor',round(floor,6),'kappa_below_floor',k2)
    assert math.isinf(k2)
    # Exact finite-library monotonicities on the toy instance.
    kappas_e=[]
    for eps in [0,.9,1.1,1.5,2.0]:
        Ue,ce=separation_sets(responses,structural,eps,0)
        kappas_e.append(brute_kappa(Ue,ce)[0])
    assert all(kappas_e[i] >= kappas_e[i+1] for i in range(len(kappas_e)-1))
    print('kappa_vs_epsilon',kappas_e)
    kappas_d=[]
    for delt in [0,.25,.75,1.0]:
        Ud,cd=separation_sets(responses,structural,0,delt)
        kappas_d.append(brute_kappa(Ud,cd)[0])
    assert kappas_d[:3] == [3,3,3] and math.isinf(kappas_d[3])
    print('kappa_vs_delta',kappas_d)
    print('packing_example_m_lower',packing_lower_bound(P=64,R=1,Delta=.25,r=2))
    print('random_panel_example_m',random_panel_bound(M=1000,p=.2,beta=.05))
    # Verify 2*eta distance perturbation bound numerically.
    rng=np.random.default_rng(7);eta=.01
    for _ in range(1000):
        a=rng.normal(size=4);b=rng.normal(size=4)
        oa=a+rng.uniform(-eta,eta,size=4);ob=b+rng.uniform(-eta,eta,size=4)
        _,_,err=robust_distance_bound(a,b,oa,ob);assert err <= 2*eta+1e-12
    print('robust_metric_test','PASS')

if __name__=='__main__':toy_demo()
