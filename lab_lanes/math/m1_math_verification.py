#!/usr/bin/env python3
"""M1 falsification-first mathematics verification for developmental-state-completion.

This file is intentionally self-contained.  It verifies finite versions of the
main claims, reconstructs a 128-world x 16-context response matrix from the
public two-context source bundle, and stress-tests connected-component design
on an explicitly declared finite topology graph.

Nothing here pushes or publishes anything.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import csv
import heapq
import json
import math
import random
from typing import Iterable

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUNDLE = ROOT / "source_validation" / "two_context_2026-08-26"
OUT_JSON = HERE / "m1_results.json"


def popcount(x: int) -> int:
    return x.bit_count()


def iter_bits(mask: int):
    while mask:
        b = mask & -mask
        yield b, b.bit_length() - 1
        mask ^= b


def parse_xy(path: Path) -> np.ndarray:
    vals: list[float] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        f = line.split("\t")
        vals.extend((float(f[1]), float(f[2])))
    return np.asarray(vals, dtype=float)


@dataclass
class SourceBundle:
    laws: list[str]
    gains: dict[str, np.ndarray]
    worlds: list[tuple[str, int]]
    responses: np.ndarray   # worlds x contexts x phenotype coordinates
    latent: np.ndarray      # worlds x 4 signed hidden coordinates


def load_source_bundle() -> SourceBundle:
    meta = json.loads((BUNDLE / "metadata" / "meta.json").read_text(encoding="utf-8"))["meta"]
    gains = {v["law"]: np.asarray(v["gains"], dtype=float) for v in meta.values()}
    laws = sorted(gains)
    files: dict[str, Path] = {}
    for sub in ("parent_source", "extension_source"):
        for path in (BUNDLE / sub).glob("*.tsv"):
            files[path.stem] = path
    assert len(laws) == 8, len(laws)
    assert len(files) == 128, len(files)
    worlds = [(law, state) for law in laws for state in range(16)]
    cache = {(law, state): parse_xy(files[f"{law}_{state:04b}"]) for law, state in worlds}
    shapes = {v.shape for v in cache.values()}
    assert shapes == {(34,)}, shapes

    # The source construction acts by XOR reflection of the 4-bit state mask:
    # response((law,state), q) is the frozen source phenotype law_(state xor q).
    responses = np.stack([
        [cache[(law, state ^ q)] for q in range(16)]
        for law, state in worlds
    ])

    # State strings are written in coordinate order, most-significant bit first.
    latent = np.stack([
        gains[law] * np.asarray([(-1.0 if c == "1" else 1.0) for c in f"{state:04b}"])
        for law, state in worlds
    ])
    return SourceBundle(laws, gains, worlds, responses, latent)


def pair_data(bundle: SourceBundle):
    n = len(bundle.worlds)
    ii, jj = np.triu_indices(n, 1)
    d_by_q = np.stack([
        np.max(np.abs(bundle.responses[ii, q] - bundle.responses[jj, q]), axis=1)
        for q in range(16)
    ])
    structural = np.linalg.norm(bundle.latent[ii] - bundle.latent[jj], axis=1)
    return ii, jj, d_by_q, structural


def bits_from_bool(a: np.ndarray) -> int:
    out = 0
    for i in np.flatnonzero(a):
        out |= 1 << int(i)
    return out


def min_cover(cover: list[int], universe: int):
    if universe == 0:
        return 0, ()
    union = 0
    for c in cover:
        union |= c
    if union != universe:
        return math.inf, ()
    for k in range(1, len(cover) + 1):
        for comb in combinations(range(len(cover)), k):
            x = 0
            for q in comb:
                x |= cover[q]
            if x == universe:
                return k, comb
    raise AssertionError("unreachable")


def greedy_cover(cover: list[int], universe: int):
    chosen: list[int] = []
    done = 0
    while done != universe:
        best_q = None
        best_gain = -1
        for q, c in enumerate(cover):
            if q in chosen:
                continue
            gain = popcount((done | c) ^ done)
            if gain > best_gain:
                best_gain = gain
                best_q = q
        if best_q is None or best_gain <= 0:
            return math.inf, tuple(chosen)
        chosen.append(best_q)
        done |= cover[best_q]
    return len(chosen), tuple(chosen)


def source_separation_audit(bundle: SourceBundle):
    ii, jj, d_by_q, structural = pair_data(bundle)
    m_pairs = len(ii)
    all_pairs = (1 << m_pairs) - 1

    exact_cover = [bits_from_bool(d_by_q[q] > 0.0) for q in range(16)]
    k_exact, panel_exact = min_cover(exact_cover, all_pairs)
    assert k_exact == 2

    sufficient_pairs = []
    for a, b in combinations(range(16), 2):
        if (exact_cover[a] | exact_cover[b]) == all_pairs:
            sufficient_pairs.append((a, b, popcount(a ^ b)))
    expected = {(a, b) for a, b in combinations(range(16), 2) if popcount(a ^ b) >= 3}
    observed = {(a, b) for a, b, _ in sufficient_pairs}
    assert observed == expected

    robust_rows = []
    for delta in (0.0, 1e-5, 2.5e-5, 3e-5, 3.2e-5, 1e-4, 1e-3, 1e-2):
        cover = [bits_from_bool(d_by_q[q] > delta) for q in range(16)]
        k, panel = min_cover(cover, all_pairs)
        full_d = np.max(d_by_q, axis=0)
        unresolved = full_d <= delta
        eps_floor = float(np.max(structural[unresolved])) if np.any(unresolved) else 0.0
        robust_rows.append({
            "delta": delta,
            "kappa_all_pairs": None if math.isinf(k) else int(k),
            "one_optimal_panel": [f"{q:04b}" for q in panel],
            "unresolved_full_panel_pairs": int(np.sum(unresolved)),
            "epsilon_floor_latent_l2": eps_floor,
        })

    two_panel_margins = []
    for a, b, h in sufficient_pairs:
        margin = float(np.min(np.maximum(d_by_q[a], d_by_q[b])))
        two_panel_margins.append((margin, a, b, h))
    two_panel_margins.sort(reverse=True)

    return {
        "worlds": len(bundle.worlds),
        "contexts": 16,
        "phenotype_coordinates_per_context": int(bundle.responses.shape[2]),
        "exact_min_panel_size": int(k_exact),
        "exact_one_optimal_panel": [f"{q:04b}" for q in panel_exact],
        "exact_sufficient_two_panels": len(sufficient_pairs),
        "exact_two_panel_hamming_counts": {
            str(h): sum(1 for _, _, hh in sufficient_pairs if hh == h) for h in range(5)
        },
        "best_two_panel_uniform_margin": two_panel_margins[0][0],
        "best_two_panel": [f"{two_panel_margins[0][1]:04b}", f"{two_panel_margins[0][2]:04b}"],
        "worst_exact_sufficient_two_panel_margin": min(x[0] for x in two_panel_margins),
        "robust_resolution": robust_rows,
    }


class DSU:
    def __init__(self, n: int):
        self.p = list(range(n))
    def find(self, x: int):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a: int, b: int):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[b] = a
        return True


def build_source_graph(bundle: SourceBundle):
    """Declared finite topology proxy: law-gain MST x 4-cube state graph."""
    n_laws = len(bundle.laws)
    candidates = []
    for i, j in combinations(range(n_laws), 2):
        d = float(np.linalg.norm(bundle.gains[bundle.laws[i]] - bundle.gains[bundle.laws[j]]))
        candidates.append((d, i, j))
    candidates.sort()
    dsu = DSU(n_laws)
    law_edges = []
    for d, i, j in candidates:
        if dsu.union(i, j):
            law_edges.append((i, j, d))
    assert len(law_edges) == n_laws - 1

    n = len(bundle.worlds)
    adj = [0] * n
    index = {w: i for i, w in enumerate(bundle.worlds)}
    def add(a: int, b: int):
        adj[a] |= 1 << b
        adj[b] |= 1 << a

    # Four-cube state adjacency inside each law.
    for law in bundle.laws:
        for s in range(16):
            a = index[(law, s)]
            for bit in range(4):
                t = s ^ (1 << bit)
                if s < t:
                    add(a, index[(law, t)])

    # Same-state links along an MST in gain-law space.
    for i, j, _ in law_edges:
        li, lj = bundle.laws[i], bundle.laws[j]
        for s in range(16):
            add(index[(li, s)], index[(lj, s)])

    # Connectivity sanity check.
    all_mask = (1 << n) - 1
    assert component_mask(all_mask, index[(bundle.laws[0], 0)], adj) == all_mask
    return adj, law_edges, index


def component_mask(survivor: int, root: int, adj: list[int]) -> int:
    rb = 1 << root
    if not (survivor & rb):
        return 0
    seen = rb
    frontier = rb
    while frontier:
        nbrs = 0
        x = frontier
        while x:
            b = x & -x
            i = b.bit_length() - 1
            nbrs |= adj[i]
            x ^= b
        frontier = nbrs & survivor & ~seen
        seen |= frontier
    return seen


def source_truth_distances(bundle: SourceBundle, truth: int):
    return np.max(np.abs(bundle.responses - bundle.responses[truth:truth+1]), axis=2).T  # q x world


def survivor_bits_from_dist(d_qw: np.ndarray, delta: float):
    return [bits_from_bool(d_qw[q] <= delta) for q in range(d_qw.shape[0])]


def utility_single_pair(d_qw: np.ndarray, delta: float, root: int, adj: list[int]):
    n = d_qw.shape[1]
    all_mask = (1 << n) - 1
    surv_q = survivor_bits_from_dist(d_qw, delta)
    f1 = []
    for q in range(16):
        c = component_mask(surv_q[q], root, adj)
        f1.append(n - popcount(c))
    best = None
    for a, b in combinations(range(16), 2):
        c = component_mask(surv_q[a] & surv_q[b], root, adj)
        fab = n - popcount(c)
        synergy = fab - f1[a] - f1[b]  # positive => increasing marginal at empty set
        cand = (synergy, fab, a, b, f1[a], f1[b])
        if best is None or cand > best:
            best = cand
    return best


def find_source_synergy_case(bundle: SourceBundle, adj: list[int]):
    deltas = (0.0, 1e-5, 2.5e-5, 3e-5, 3.2e-5, 1e-4, 1e-3, 1e-2, 5e-2)
    best = None
    for truth in range(len(bundle.worlds)):
        d_qw = source_truth_distances(bundle, truth)
        for delta in deltas:
            row = utility_single_pair(d_qw, delta, truth, adj)
            cand = (row[0], row[1], truth, delta, row)
            if best is None or cand > best:
                best = cand
    return best


def full_panel_table(d_qw: np.ndarray, delta: float, root: int, adj: list[int]):
    m, n = d_qw.shape
    assert m == 16
    nmask = 1 << m
    all_worlds = (1 << n) - 1
    surv_q = survivor_bits_from_dist(d_qw, delta)
    survivor = [0] * nmask
    comps = [0] * nmask
    util = [0] * nmask
    survivor[0] = all_worlds
    comps[0] = component_mask(all_worlds, root, adj)
    for mask in range(1, nmask):
        b = mask & -mask
        q = b.bit_length() - 1
        prev = mask ^ b
        s = survivor[prev] & surv_q[q]
        survivor[mask] = s
        c = component_mask(s, root, adj)
        comps[mask] = c
        util[mask] = n - popcount(c)
    return comps, util


def monotonicity_edge_violations(comps: list[int], m: int = 16):
    violations = []
    full = (1 << m) - 1
    for mask, c in enumerate(comps):
        missing = full ^ mask
        for b, q in iter_bits(missing):
            c2 = comps[mask | b]
            extra = c2 & ~c
            if extra:
                violations.append((mask, q, extra))
                if len(violations) >= 5:
                    return violations
    return violations


def worst_submodularity_violation(util: list[int], m: int = 16):
    # Check pairwise diminishing returns: Delta_q(S) >= Delta_q(S U {r}).
    full = (1 << m) - 1
    worst = (0, None)
    for s in range(1 << m):
        missing = full ^ s
        bits = [b for b, _ in iter_bits(missing)]
        for i in range(len(bits)):
            qb = bits[i]
            lhs = util[s | qb] - util[s]
            for j in range(i + 1, len(bits)):
                rb = bits[j]
                rhs = util[s | qb | rb] - util[s | rb]
                gap = rhs - lhs
                if gap > worst[0]:
                    worst = (gap, (s, qb.bit_length()-1, rb.bit_length()-1, lhs, rhs))
                # Symmetric check for r as the added item.
                lhs2 = util[s | rb] - util[s]
                rhs2 = util[s | qb | rb] - util[s | qb]
                gap2 = rhs2 - lhs2
                if gap2 > worst[0]:
                    worst = (gap2, (s, rb.bit_length()-1, qb.bit_length()-1, lhs2, rhs2))
    return worst


def greedy_vs_optimal(util: list[int], max_budget: int = 5, m: int = 16):
    best_by_k = [(-1, 0) for _ in range(max_budget + 1)]
    for mask, val in enumerate(util):
        k = popcount(mask)
        if k <= max_budget and val > best_by_k[k][0]:
            best_by_k[k] = (val, mask)
    rows = []
    chosen = 0
    for k in range(1, max_budget + 1):
        base = util[chosen]
        best = None
        for q in range(m):
            b = 1 << q
            if chosen & b:
                continue
            cand = (util[chosen | b] - base, -q, q)
            if best is None or cand > best:
                best = cand
        chosen |= 1 << best[2]
        g = util[chosen]
        opt, optmask = best_by_k[k]
        rows.append({
            "budget": k,
            "greedy_utility": g,
            "optimal_utility": opt,
            "ratio": (g / opt) if opt > 0 else 1.0,
            "greedy_panel": [f"{q:04b}" for q in range(m) if chosen & (1 << q)],
            "optimal_panel": [f"{q:04b}" for q in range(m) if optmask & (1 << q)],
        })
    return rows


def bottleneck_thresholds(field: np.ndarray, root: int, adj: list[int]) -> np.ndarray:
    """lambda(v)=min_{path root->v} max field on the path."""
    n = len(field)
    out = np.full(n, np.inf)
    out[root] = float(field[root])
    heap = [(out[root], root)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != out[u]:
            continue
        x = adj[u]
        while x:
            b = x & -x
            v = b.bit_length() - 1
            x ^= b
            nd = max(d, float(field[v]))
            if nd < out[v]:
                out[v] = nd
                heapq.heappush(heap, (nd, v))
    return out


def source_component_and_noise_audit(bundle: SourceBundle, adj: list[int]):
    # Stress case found by scanning representative source worlds/tolerances.
    # It is useful because the source-derived connected utility is genuinely
    # non-submodular here, even though greedy still happens to be optimal.
    truth = bundle.worlds.index(("P06", 0))
    delta = 0.05
    d_qw = source_truth_distances(bundle, truth)
    comps, util = full_panel_table(d_qw, delta, truth, adj)
    monotone_viol = monotonicity_edge_violations(comps)
    assert not monotone_viol
    submod_gap, submod_witness = worst_submodularity_violation(util)
    greedy_rows = greedy_vs_optimal(util, max_budget=5)

    # Nested-panel bottleneck thresholds must increase as experiments are added.
    nested = [1 << 0, (1 << 0) | (1 << 7), (1 << 0) | (1 << 7) | (1 << 15)]
    lambdas = []
    for pmask in nested:
        qs = [q for q in range(16) if pmask & (1 << q)]
        field = np.max(d_qw[qs], axis=0)
        lambdas.append(bottleneck_thresholds(field, truth, adj))
    for a, b in zip(lambdas, lambdas[1:]):
        assert np.all(a <= b + 1e-12)

    # Bounded signature perturbation: direct 2*eta metric error, component sandwich,
    # and bottleneck-threshold stability.
    rng = np.random.default_rng(20260829)
    eta = 1e-5
    noisy = bundle.responses + rng.uniform(-eta, eta, size=bundle.responses.shape)
    panel = [0, 7, 15]
    true_field = np.max(np.max(np.abs(bundle.responses[:, panel] - bundle.responses[truth, panel]), axis=2), axis=1)
    noisy_field = np.max(np.max(np.abs(noisy[:, panel] - noisy[truth, panel]), axis=2), axis=1)
    field_error = float(np.max(np.abs(noisy_field - true_field)))
    assert field_error <= 2 * eta + 1e-12
    kappa = 2 * eta

    candidate_deltas = sorted(set(float(x) for x in np.quantile(true_field, [0.1, 0.25, 0.5, 0.75, 0.9])))
    sandwich_checks = 0
    all_worlds = (1 << len(bundle.worlds)) - 1
    for d in candidate_deltas:
        lo = max(0.0, d - kappa)
        hi = d + kappa
        c_lo = component_mask(bits_from_bool(true_field <= lo), truth, adj)
        c_mid = component_mask(bits_from_bool(noisy_field <= d), truth, adj)
        c_hi = component_mask(bits_from_bool(true_field <= hi), truth, adj)
        assert (c_lo & ~c_mid) == 0
        assert (c_mid & ~c_hi) == 0
        sandwich_checks += 1

    lam_true = bottleneck_thresholds(true_field, truth, adj)
    lam_noisy = bottleneck_thresholds(noisy_field, truth, adj)
    merge_threshold_error = float(np.max(np.abs(lam_true - lam_noisy)))
    assert merge_threshold_error <= kappa + 1e-12

    return {
        "topology_proxy": "law-gain MST Cartesian-linked to 4-cube state graph",
        "selected_truth": [bundle.worlds[truth][0], f"{bundle.worlds[truth][1]:04b}"],
        "selected_delta": delta,
        "nested_panel_monotonicity_edge_violations": len(monotone_viol),
        "worst_submodularity_gap": int(submod_gap),
        "worst_submodularity_witness": None if submod_witness is None else {
            "base_mask": int(submod_witness[0]),
            "added_q": f"{submod_witness[1]:04b}",
            "conditioning_q": f"{submod_witness[2]:04b}",
            "marginal_before": int(submod_witness[3]),
            "marginal_after": int(submod_witness[4]),
        },
        "greedy_vs_optimal": greedy_rows,
        "signature_noise_eta": eta,
        "max_target_relative_distance_error": field_error,
        "two_eta_bound": 2 * eta,
        "component_sandwich_checks": sandwich_checks,
        "max_merge_threshold_error": merge_threshold_error,
    }


def grid_graph(n: int):
    adj = [0] * (n * n)
    def idx(r, c): return r * n + c
    for r in range(n):
        for c in range(n):
            u = idx(r, c)
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    adj[u] |= 1 << idx(rr, cc)
    return adj, idx


def grid_counterexample_audit():
    rows = []
    for n in (10, 20, 40, 80, 160):
        adj, idx = grid_graph(n)
        root = idx(0, 0)
        allv = (1 << (n*n)) - 1
        mid = n // 2
        d1 = sum(1 << idx(r, mid) for r in range(n) if r % 2 == 0)
        d2 = sum(1 << idx(r, mid) for r in range(n) if r % 2 == 1)
        d0 = sum(1 << idx(r, n-1) for r in range(n))
        dels = [d0, d1, d2]
        def f(sel: Iterable[int]):
            d = 0
            for q in sel:
                d |= dels[q]
            c = component_mask(allv & ~d, root, adj)
            return n*n - popcount(c)
        single = [f([q]) for q in range(3)]
        assert single == [n, n//2, n//2]
        opt = f([1,2])
        greedy = f([0,1])
        ratio = greedy / opt
        assert opt == n*n//2
        assert greedy == 3*n//2
        assert abs(ratio - 3/n) < 1e-12
        assert f([1,2]) - f([1]) > f([2]) - f([])
        rows.append({"n": n, "greedy": greedy, "optimal": opt, "ratio": ratio, "theory_3_over_n": 3/n})
    return rows


def rooted_tree(n: int, rng: random.Random):
    parent = [-1]
    adj = [0] * n
    for v in range(1, n):
        p = rng.randrange(v)
        parent.append(p)
        adj[v] |= 1 << p
        adj[p] |= 1 << v
    return parent, adj


def tree_descendant_mask(parent: list[int], deleted: int):
    n = len(parent)
    out = 0
    for v in range(n):
        u = v
        while u != -1:
            if deleted & (1 << u):
                out |= 1 << v
                break
            u = parent[u]
    return out


def tree_greedy_safety_audit():
    rng = random.Random(20260829)
    trials = 40
    min_ratio = 1.0
    for _ in range(trials):
        n = 18
        m = 7
        parent, adj = rooted_tree(n, rng)
        allv = (1 << n) - 1
        deletion = []
        for q in range(m):
            d = 0
            for v in range(1, n):
                if rng.random() < 0.16:
                    d |= 1 << v
            deletion.append(d)
        closure = [tree_descendant_mask(parent, d) for d in deletion]
        util = []
        for mask in range(1 << m):
            d = 0
            cov = 0
            for q in range(m):
                if mask & (1 << q):
                    d |= deletion[q]
                    cov |= closure[q]
            c = component_mask(allv & ~d, 0, adj)
            f = n - popcount(c)
            assert f == popcount(cov)  # exact coverage representation on a tree
            util.append(f)

        gap, witness = worst_submodularity_violation(util, m=m)
        assert gap == 0, witness

        # Cardinality budget 3: greedy should meet the standard 1-1/e bound.
        k = 3
        opt = max(util[mask] for mask in range(1 << m) if popcount(mask) <= k)
        chosen = 0
        for _step in range(k):
            base = util[chosen]
            q = max((q for q in range(m) if not chosen & (1 << q)), key=lambda qq: (util[chosen | (1 << qq)] - base, -qq))
            chosen |= 1 << q
        g = util[chosen]
        ratio = g / opt if opt else 1.0
        min_ratio = min(min_ratio, ratio)
        assert ratio + 1e-12 >= 1 - 1/math.e
    return {"random_tree_trials": trials, "minimum_observed_greedy_over_optimal": min_ratio, "submodularity_violations": 0}


def finite_resolution_compactness_toy():
    """Finite Hilbert-cube analogue: exact finite coordinates fail, fixed resolution succeeds."""
    d = 12
    points = np.asarray([[int(c) for c in f"{i:0{d}b}"] for i in range(1 << d)], dtype=int)
    weights = np.asarray([2.0 ** (-(j+1)) for j in range(d)])
    # Weighted l1 metric.  Any finite prefix misses pairs differing only later.
    exact_prefix_fail = []
    for m in (1, 2, 4, 8):
        collisions = 0
        seen = {}
        for i, x in enumerate(points):
            key = tuple(x[:m])
            if key in seen:
                collisions += 1
            else:
                seen[key] = i
        exact_prefix_fail.append((m, collisions))
        assert collisions > 0

    eps = 0.04
    # Choose M so the total metric tail is < eps. Then any eps-distant pair
    # must differ in the first M coordinates and is separated by that finite panel.
    tail = np.cumsum(weights[::-1])[::-1]
    M = next(m for m in range(1, d+1) if (tail[m] if m < d else 0.0) < eps)
    # Exhaustive check over 4096 points would create ~8m pairs; sample deterministically.
    rng = np.random.default_rng(20260829)
    for _ in range(20000):
        i, j = rng.integers(0, len(points), size=2)
        if i == j:
            continue
        dist = float(np.sum(weights * np.abs(points[i] - points[j])))
        if dist >= eps:
            assert np.any(points[i, :M] != points[j, :M])
    return {"dimension_truncation": d, "epsilon": eps, "finite_prefix_M": M, "exact_prefix_collision_counts": exact_prefix_fail}


def main():
    bundle = load_source_bundle()
    sep = source_separation_audit(bundle)
    adj, law_edges, _index = build_source_graph(bundle)
    comp = source_component_and_noise_audit(bundle, adj)
    grid = grid_counterexample_audit()
    tree = tree_greedy_safety_audit()
    compact = finite_resolution_compactness_toy()

    results = {
        "source_bundle": sep,
        "source_component_audit": comp,
        "law_mst_edges": [[bundle.laws[i], bundle.laws[j], d] for i, j, d in law_edges],
        "grid_counterexample": grid,
        "tree_greedy_safe_regime": tree,
        "finite_resolution_compactness_toy": compact,
        "frozen_rejections": [
            "arbitrary experiment-score aggregation preserves refinement",
            "fixed-delta connected components are Lipschitz-stable as sets",
            "compactness alone gives one finite exact separator for an infinite world space",
            "finite-library exact Euclidean embedding dimension is informative under arbitrary real projections",
            "connected-ambiguity utility is generally submodular",
            "tree topology alone implies adaptive submodularity under unknown outcomes",
        ],
    }
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("M1 verification PASS")
    print("source worlds/contexts:", sep["worlds"], sep["contexts"])
    print("exact minimum source panel:", sep["exact_min_panel_size"], sep["exact_one_optimal_panel"])
    print("sufficient exact 2-panels:", sep["exact_sufficient_two_panels"], sep["exact_two_panel_hamming_counts"])
    print("best exact 2-panel uniform margin:", sep["best_two_panel_uniform_margin"])
    print("source connected stress case:", comp["selected_truth"], "delta", comp["selected_delta"])
    print("source worst submodularity gap:", comp["worst_submodularity_gap"])
    print("source max bounded-noise field error:", comp["max_target_relative_distance_error"], "<=", comp["two_eta_bound"])
    print("source max merge-threshold error:", comp["max_merge_threshold_error"], "<=", comp["two_eta_bound"])
    print("grid ratios:", [r["ratio"] for r in grid])
    print("tree min greedy/opt:", tree["minimum_observed_greedy_over_optimal"])
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
