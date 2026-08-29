#!/usr/bin/env python3
"""Independent reproduction of the greedy connected-ambiguity counterexample.

Candidate worlds are vertices of an n x n grid. Experiments delete vertices
that are inconsistent with the observed outcome at the true world. Utility is
f(Q) = |V| - |C_Q(w*)|, where C_Q(w*) is the surviving connected component
containing the truth.

q1 and q2 remove complementary halves of a middle column. Each alone leaves
passages, but together form a complete wall. q0 removes the far-right boundary
column and acts as a greedy decoy.
"""
from __future__ import annotations

from itertools import combinations
import csv
from pathlib import Path


def neighbors(v, n):
    r, c = v
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        rr, cc = r+dr, c+dc
        if 0 <= rr < n and 0 <= cc < n:
            yield rr, cc


def experiment_deletions(n):
    assert n % 2 == 0 and n >= 4
    mid = n // 2
    q1 = {(r, mid) for r in range(n) if r % 2 == 0}
    q2 = {(r, mid) for r in range(n) if r % 2 == 1}
    q0 = {(r, n-1) for r in range(n)}
    return {'q0': q0, 'q1': q1, 'q2': q2}


def component_size(n, deleted, truth=(0,0)):
    if truth in deleted:
        raise ValueError('truth deleted')
    seen = {truth}
    stack = [truth]
    while stack:
        v = stack.pop()
        for u in neighbors(v, n):
            if u not in deleted and u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen)


def utility(n, selected):
    exps = experiment_deletions(n)
    deleted = set()
    for q in selected:
        deleted |= exps[q]
    return n*n - component_size(n, deleted)


def greedy(n, budget=2):
    chosen = []
    remaining = ['q0','q1','q2']
    for _ in range(budget):
        base = utility(n, chosen)
        scored = []
        for q in remaining:
            val = utility(n, chosen + [q])
            scored.append((val-base, q, val))
        # deterministic tie-break by q name after maximizing gain
        gain, q, val = max(scored, key=lambda x: (x[0], x[1]))
        chosen.append(q)
        remaining.remove(q)
    return tuple(chosen), utility(n, chosen)


def optimal(n, budget=2):
    best = None
    for qs in combinations(['q0','q1','q2'], budget):
        val = utility(n, qs)
        cand = (val, qs)
        if best is None or cand > best:
            best = cand
    return best[1], best[0]


def audit(n):
    f0 = utility(n, [])
    fq1 = utility(n, ['q1'])
    fq2 = utility(n, ['q2'])
    fq12 = utility(n, ['q1','q2'])
    initial_marginal_q2 = fq2 - f0
    conditional_marginal_q2 = fq12 - fq1
    gset, gval = greedy(n)
    oset, oval = optimal(n)
    return {
        'n': n,
        'f_empty': f0,
        'f_q0': utility(n,['q0']),
        'f_q1': fq1,
        'f_q2': fq2,
        'f_q1_q2': fq12,
        'initial_marginal_q2': initial_marginal_q2,
        'conditional_marginal_q2_given_q1': conditional_marginal_q2,
        'submodularity_violated': conditional_marginal_q2 > initial_marginal_q2,
        'greedy_set': '+'.join(gset),
        'greedy_utility': gval,
        'optimal_set': '+'.join(oset),
        'optimal_utility': oval,
        'greedy_over_optimal': gval / oval,
        'theory_ratio_3_over_n': 3/n,
    }


def main():
    ns = [10,20,40,80,160]
    rows = [audit(n) for n in ns]
    out = Path(__file__).with_name('greedy_component_counterexample_results.csv')
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(
            f"n={r['n']:>3}  greedy={r['greedy_set']:<5} {r['greedy_utility']:>6}  "
            f"optimal={r['optimal_set']:<5} {r['optimal_utility']:>6}  "
            f"ratio={r['greedy_over_optimal']:.5f}  "
            f"3/n={r['theory_ratio_3_over_n']:.5f}  "
            f"submod_violation={r['submodularity_violated']}"
        )
    # exact analytic sanity checks
    for n in ns:
        r = audit(n)
        assert r['f_q1'] == n//2
        assert r['f_q2'] == n//2
        assert r['f_q1_q2'] == n*n//2
        assert r['f_q0'] == n
        assert r['greedy_utility'] == 3*n//2
        assert r['optimal_utility'] == n*n//2
        assert abs(r['greedy_over_optimal'] - 3/n) < 1e-12
        assert r['submodularity_violated']
    print(f"wrote {out}")

if __name__ == '__main__':
    main()
