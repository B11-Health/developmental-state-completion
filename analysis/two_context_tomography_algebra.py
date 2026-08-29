"""Algebraic sanity checks for the restricted two-context tomography model.

The positive/negative-part identity is established rectifier algebra (CReLU-like),
not claimed as new mathematics. This file records the exact model consequence and
simple deterministic noise margins used by the Code Gym simulator analysis.
"""
import itertools
import numpy as np


def relu(x):
    return np.maximum(np.asarray(x,float),0.0)


def apply_mask(s,mask):
    """Flip the signed coordinates whose mask entries are 1."""
    s=np.asarray(s,float);mask=np.asarray(mask,int)
    return s*(1-2*mask)


def rectified_context(s,mask):
    """Restricted latent response u_q = [-R_q s]_+."""
    return relu(-apply_mask(s,mask))


def reconstruct_full_complement(u0,uq):
    """When q flips every coordinate: s = u_q - u_0 exactly."""
    return np.asarray(uq)-np.asarray(u0)


def reconstruct_fixed_budget(u0,uq,mask,total_l1):
    """Recover s when mask flips n-1 coordinates and ||s||_1 is known.

    Flipped coordinates are direct differences. The sole unflipped magnitude is
    the remaining L1 budget; its sign is selected by whether its rectified channel
    is active (negative) or inactive (positive).
    """
    u0=np.asarray(u0,float);uq=np.asarray(uq,float);mask=np.asarray(mask,int)
    n=len(mask);un=np.flatnonzero(mask==0)
    if len(un)==0:return uq-u0
    if len(un)!=1:raise ValueError('fixed-budget reconstruction requires n-1 flips')
    s=np.zeros(n)
    flipped=np.flatnonzero(mask==1)
    s[flipped]=uq[flipped]-u0[flipped]
    j=int(un[0])
    residual=max(0.0,float(total_l1)-float(np.sum(np.abs(s[flipped]))))
    obs=0.5*(u0[j]+uq[j])
    s[j]=-residual if abs(obs-residual)<abs(obs) else residual
    return s


def deterministic_noise_bounds(n,e):
    """Linf decoded-u error <= e in each of the two contexts.

    Full complement:
      coordinate state error <= 2e; L2 state error <= 2e sqrt(n).

    n-1 fixed-budget mask, provided the unflipped sign is correctly selected:
      each flipped error <=2e;
      unflipped magnitude error <=2e(n-1);
      total L2 error <=2e sqrt(n(n-1)).

    A sufficient sign margin is |s_j|>2e for flipped coordinates and
    |s_k|>2ne for the sole unflipped coordinate.
    """
    return {
        'full_coord':2*e,
        'full_l2':2*e*np.sqrt(n),
        'fixed_flipped_coord':2*e,
        'fixed_unflipped_magnitude':2*e*(n-1),
        'fixed_l2_if_sign_correct':2*e*np.sqrt(n*(n-1)),
        'flipped_sign_margin':2*e,
        'unflipped_sign_margin':2*n*e,
    }


def exact_trials(seed=20260829,trials=5000,n=4,total_l1=1.8):
    rng=np.random.default_rng(seed)
    full=np.ones(n,int)
    masks=[np.array(m,int) for m in itertools.product([0,1],repeat=n) if sum(m)==n-1]
    for _ in range(trials):
        g=rng.dirichlet(np.ones(n))*total_l1
        signs=rng.choice([-1.0,1.0],size=n)
        s=signs*g
        u0=rectified_context(s,np.zeros(n,int))
        uq=rectified_context(s,full)
        assert np.allclose(reconstruct_full_complement(u0,uq),s,atol=1e-12)
        for mask in masks:
            um=rectified_context(s,mask)
            assert np.allclose(reconstruct_fixed_budget(u0,um,mask,total_l1),s,atol=1e-12)
    print('EXACT_TRIALS_PASS',trials,'vectors x',1+len(masks),'masks')


def noise_trials(seed=17,trials=20000,n=4,total_l1=1.8,e=1e-4):
    """Numerically stress the deterministic sufficient bounds.

    We only assert sign recovery on samples satisfying the analytic margin.
    """
    rng=np.random.default_rng(seed);full=np.ones(n,int)
    masks=[np.array(m,int) for m in itertools.product([0,1],repeat=n) if sum(m)==n-1]
    B=deterministic_noise_bounds(n,e);checked_full=0;checked_fixed=0
    for _ in range(trials):
        g=rng.dirichlet(np.ones(n))*total_l1
        signs=rng.choice([-1.0,1.0],size=n);s=signs*g
        u0=rectified_context(s,np.zeros(n,int))
        n0=rng.uniform(-e,e,size=n);nf=rng.uniform(-e,e,size=n)
        sh=reconstruct_full_complement(u0+n0,rectified_context(s,full)+nf)
        assert np.max(np.abs(sh-s)) <= B['full_coord']+1e-12
        assert np.linalg.norm(sh-s) <= B['full_l2']+1e-12
        if np.min(np.abs(s))>B['flipped_sign_margin']:
            assert np.all(np.sign(sh)==np.sign(s));checked_full+=1
        for mask in masks:
            un=int(np.flatnonzero(mask==0)[0]);fl=np.flatnonzero(mask==1)
            nm=rng.uniform(-e,e,size=n)
            sh=reconstruct_fixed_budget(u0+n0,rectified_context(s,mask)+nm,mask,total_l1)
            if np.all(np.abs(s[fl])>B['flipped_sign_margin']) and abs(s[un])>B['unflipped_sign_margin']:
                assert np.all(np.sign(sh)==np.sign(s))
                assert np.linalg.norm(sh-s) <= B['fixed_l2_if_sign_correct']+1e-12
                checked_fixed+=1
    print('NOISE_BOUND_PASS','e',e,'full_margin_cases',checked_full,'fixed_margin_cases',checked_fixed)
    print('BOUNDS', {k:float(v) for k,v in B.items()})


if __name__=='__main__':
    exact_trials()
    noise_trials()
