#!/usr/bin/env python3
"""Finite-sample calibration for a state-completion CMI diagnostic.

We estimate I(Y; H | S, A) with a plug-in discrete estimator in two controlled
binary dynamical systems:

Markov:
    logit P(X[t+1]=1 | X[t], A[t], X[t-1])
      = -0.6 + 1.2 X[t] + 0.8 A[t]

History-dependent:
    same + 0.6 X[t-1]

S=X[t], H=X[t-1], Y=X[t+1].  In the Markov system the population CMI is zero
by construction, but the plug-in estimator is positively biased at finite N.
The non-Markov system is used to measure power against an empirical Markov
null cutoff.  Each Monte Carlo replicate is one trajectory after burn-in.
"""
from __future__ import annotations
from collections import Counter
import csv, math, random, statistics
from pathlib import Path

INTERCEPT=-0.6
BETA_STATE=1.2
BETA_ACTION=0.8
BETA_HISTORY_ALT=0.6
BURN_IN=250
REPLICATES=1000
BASE_SEED=20260829


def sigmoid(z):
    return 1.0/(1.0+math.exp(-z))


def plugin_cmi_bits(rows):
    """I(Y;H | S,A) in bits for rows (h,s,a,y)."""
    n=len(rows)
    c_hsay=Counter(rows)
    c_sa=Counter((s,a) for h,s,a,y in rows)
    c_hsa=Counter((h,s,a) for h,s,a,y in rows)
    c_ysa=Counter((y,s,a) for h,s,a,y in rows)
    total=0.0
    for (h,s,a,y), count in c_hsay.items():
        numerator=count*c_sa[(s,a)]
        denominator=c_hsa[(h,s,a)]*c_ysa[(y,s,a)]
        if numerator and denominator:
            total += (count/n)*math.log2(numerator/denominator)
    return total


def simulate_trajectory(n, beta_history, seed):
    rng=random.Random(seed)
    x_prev=rng.randrange(2)
    x=rng.randrange(2)
    rows=[]
    for t in range(n+BURN_IN):
        action=rng.randrange(2)
        z=(INTERCEPT+BETA_STATE*x+BETA_ACTION*action+
           beta_history*x_prev)
        y=int(rng.random()<sigmoid(z))
        if t>=BURN_IN:
            rows.append((x_prev,x,action,y))
        x_prev,x=x,y
    return rows


def quantile_higher(values, q):
    vals=sorted(values)
    # Conservative empirical q-quantile: first order statistic with CDF >= q.
    idx=max(0, min(len(vals)-1, math.ceil(q*len(vals))-1))
    return vals[idx]


def calibrate(n):
    null=[]; alt=[]
    for i in range(REPLICATES):
        null.append(plugin_cmi_bits(simulate_trajectory(
            n,0.0,BASE_SEED + 10_000_000*n + i)))
        alt.append(plugin_cmi_bits(simulate_trajectory(
            n,BETA_HISTORY_ALT,BASE_SEED + 20_000_000*n + i)))
    cutoff=quantile_higher(null,0.95)
    power=sum(v>cutoff for v in alt)/REPLICATES
    return {
        'N':n,
        'replicates':REPLICATES,
        'markov_mean_cmi_bits':statistics.mean(null),
        'markov_median_cmi_bits':statistics.median(null),
        'markov_empirical_95pct_cutoff_bits':cutoff,
        'history_dependent_mean_cmi_bits':statistics.mean(alt),
        'history_dependent_median_cmi_bits':statistics.median(alt),
        'empirical_power_at_markov_95pct_cutoff':power,
    }


def main():
    rows=[calibrate(n) for n in (250,500,1000,2000)]
    out=Path(__file__).with_name('state_completion_cmi_calibration_results.csv')
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    for r in rows:
        print(
            f"N={r['N']:4d}  null_mean={r['markov_mean_cmi_bits']:.5f}  "
            f"null95={r['markov_empirical_95pct_cutoff_bits']:.5f}  "
            f"alt_mean={r['history_dependent_mean_cmi_bits']:.5f}  "
            f"power={r['empirical_power_at_markov_95pct_cutoff']:.3f}"
        )
    # Qualitative invariants required by the scientific claim.
    assert all(r['markov_mean_cmi_bits'] > 0 for r in rows)
    assert all(rows[i+1]['markov_mean_cmi_bits'] < rows[i]['markov_mean_cmi_bits'] for i in range(len(rows)-1))
    assert rows[-1]['history_dependent_mean_cmi_bits'] > rows[-1]['markov_empirical_95pct_cutoff_bits']
    assert rows[-1]['empirical_power_at_markov_95pct_cutoff'] > rows[0]['empirical_power_at_markov_95pct_cutoff']
    print(f"wrote {out}")

if __name__=='__main__':
    main()
