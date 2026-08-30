#!/usr/bin/env python3
"""M2 exact perturbation optimization on the frozen 128-world source bundle.

Known-outcome/static objective, matching M1:
    f(Q; w*) = |V| - |C_Q(w*)|
where C_Q is the truth-containing connected component after retaining worlds
whose response differs from truth by at most delta for every q in Q.

The source construction is XOR-equivariant in the 4-bit state.  We exploit
that exact symmetry to compute 8 canonical state-0000 truths and then map all
16 truth states by the context permutation q -> q xor truth_state.  No truths
are subsampled.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
M1_PATH = ROOT / "lab_lanes" / "math" / "m1_math_verification.py"
spec = importlib.util.spec_from_file_location("m1_math_verification", M1_PATH)
m1 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m1
spec.loader.exec_module(m1)

DELTAS = (0.0, 1e-5, 2.5e-5, 3e-5, 3.2e-5, 1e-4, 1e-3, 1e-2, 5e-2)
MAX_BUDGET = 5
M = 16


def masks_of_size(k: int) -> list[int]:
    return [sum(1 << q for q in comb) for comb in combinations(range(M), k)]


MASKS_BY_K = {k: masks_of_size(k) for k in range(MAX_BUDGET + 1)}
MASKS_UP_TO = [mask for k in range(MAX_BUDGET + 1) for mask in MASKS_BY_K[k]]
CONDITIONING_MASKS = [mask for k in range(0, 4) for mask in MASKS_BY_K[k]]
FULL_CONTEXT_MASK = (1 << M) - 1


def bits(mask: int) -> list[int]:
    return [q for q in range(M) if mask & (1 << q)]


def panel_strings(mask: int) -> list[str]:
    return [f"{q:04b}" for q in bits(mask)]


def permute_mask_xor(mask: int, state: int) -> int:
    out = 0
    for q in bits(mask):
        out |= 1 << (q ^ state)
    return out


def add_edge(adj: list[int], a: int, b: int) -> None:
    adj[a] |= 1 << b
    adj[b] |= 1 << a


def build_law_clique_x_q4(bundle):
    n = len(bundle.worlds)
    adj = [0] * n
    index = {w: i for i, w in enumerate(bundle.worlds)}
    for law in bundle.laws:
        for s in range(16):
            a = index[(law, s)]
            for bit in range(4):
                t = s ^ (1 << bit)
                if s < t:
                    add_edge(adj, a, index[(law, t)])
    for s in range(16):
        for i, j in combinations(range(len(bundle.laws)), 2):
            add_edge(adj, index[(bundle.laws[i], s)], index[(bundle.laws[j], s)])
    allv = (1 << n) - 1
    assert m1.component_mask(allv, 0, adj) == allv
    return adj, index


def build_topologies(bundle):
    m1_adj, law_edges, index = m1.build_source_graph(bundle)
    clique_adj, index2 = build_law_clique_x_q4(bundle)
    assert index == index2
    return {
        "complete_survivor": {
            "adj": None,
            "description": "Complete graph on all 128 worlds; truth component equals the full survivor set (pure version-space coverage control).",
        },
        "law_mst_x_q4": {
            "adj": m1_adj,
            "description": "M1 topology: Q4 state cube within each law, with same-state cross-law links along the gain-vector law MST.",
            "law_mst_edges": [[bundle.laws[i], bundle.laws[j], float(d)] for i, j, d in law_edges],
        },
        "law_clique_x_q4": {
            "adj": clique_adj,
            "description": "Denser sensitivity topology: Q4 within each law, plus same-state links between every pair of laws (K8 across law dimension).",
        },
    }, index


def utility_table(bundle, truth: int, delta: float, adj):
    n = len(bundle.worlds)
    allv = (1 << n) - 1
    d_qw = m1.source_truth_distances(bundle, truth)
    surv_q = m1.survivor_bits_from_dist(d_qw, delta)
    survivor = [None] * (1 << M)
    survivor[0] = allv
    util = np.full(1 << M, -1, dtype=np.int16)
    util[0] = 0
    for k in range(1, MAX_BUDGET + 1):
        for mask in MASKS_BY_K[k]:
            b = mask & -mask
            q = b.bit_length() - 1
            prev = mask ^ b
            s = survivor[prev] & surv_q[q]
            survivor[mask] = s
            if adj is None:
                c = s
            else:
                c = m1.component_mask(s, truth, adj)
            util[mask] = n - m1.popcount(c)
    return util, surv_q


def best_masks_by_budget(util: np.ndarray):
    out = {}
    for k in range(1, MAX_BUDGET + 1):
        best_val = -1
        best_mask = None
        for mask in MASKS_BY_K[k]:
            val = int(util[mask])
            if val > best_val or (val == best_val and (best_mask is None or mask < best_mask)):
                best_val, best_mask = val, mask
        out[k] = (best_val, int(best_mask))
    return out


def greedy_for_truth_state(util_canonical: np.ndarray, truth_state: int):
    chosen = 0
    rows = {}
    for k in range(1, MAX_BUDGET + 1):
        best = None
        for q in range(M):
            if chosen & (1 << q):
                continue
            cand_actual = chosen | (1 << q)
            cand_canon = permute_mask_xor(cand_actual, truth_state)
            val = int(util_canonical[cand_canon])
            key = (val, -q)
            if best is None or key > best[0]:
                best = (key, q, val)
        chosen |= 1 << best[1]
        rows[k] = (best[2], chosen)
    return rows


def restricted_diagnostics(util: np.ndarray):
    max_gap = 0
    dr_witness = None
    min_gamma_raw = math.inf
    gamma_witness = None
    max_joint_synergy = 0
    synergy_witness = None
    comparisons = 0
    positive_dr = 0
    for L in CONDITIONING_MASKS:
        base = int(util[L])
        missing = [q for q in range(M) if not (L & (1 << q))]
        for a_i in range(len(missing)):
            q = missing[a_i]
            fq = int(util[L | (1 << q)])
            mq = fq - base
            for r in missing[a_i + 1:]:
                fr = int(util[L | (1 << r)])
                mr = fr - base
                fqr = int(util[L | (1 << q) | (1 << r)])
                joint = fqr - base
                comparisons += 2
                # Two oriented diminishing-returns checks.
                gap_q_after_r = (fqr - fr) - mq
                gap_r_after_q = (fqr - fq) - mr
                for gap, added, conditioned_on, lhs, rhs in (
                    (gap_q_after_r, q, r, mq, fqr - fr),
                    (gap_r_after_q, r, q, mr, fqr - fq),
                ):
                    if gap > 0:
                        positive_dr += 1
                    if gap > max_gap:
                        max_gap = gap
                        dr_witness = {
                            "conditioning_panel": panel_strings(L),
                            "added_context": f"{added:04b}",
                            "extra_conditioning_context": f"{conditioned_on:04b}",
                            "marginal_before": lhs,
                            "marginal_after": rhs,
                            "gap": gap,
                        }
                if joint > 0:
                    raw = (mq + mr) / joint
                    if raw < min_gamma_raw:
                        min_gamma_raw = raw
                        gamma_witness = {
                            "conditioning_panel": panel_strings(L),
                            "pair": [f"{q:04b}", f"{r:04b}"],
                            "sum_singleton_marginals": mq + mr,
                            "joint_marginal": joint,
                            "raw_ratio": raw,
                        }
                synergy = joint - mq - mr
                if synergy > max_joint_synergy:
                    max_joint_synergy = synergy
                    synergy_witness = {
                        "conditioning_panel": panel_strings(L),
                        "pair": [f"{q:04b}", f"{r:04b}"],
                        "joint_minus_sum_marginals": synergy,
                    }
    if not math.isfinite(min_gamma_raw):
        min_gamma_raw = 1.0
    return {
        "conditioning_size_limit": 3,
        "augmentation_pair_size": 2,
        "relevant_total_budget_limit": 5,
        "diminishing_returns_comparisons": comparisons,
        "positive_diminishing_returns_violations": positive_dr,
        "worst_diminishing_returns_gap": max_gap,
        "worst_diminishing_returns_witness": dr_witness,
        "restricted_submodularity_ratio_raw": min_gamma_raw,
        "restricted_submodularity_ratio_capped_at_1": min(1.0, min_gamma_raw),
        "restricted_submodularity_ratio_witness": gamma_witness,
        "max_pair_joint_synergy": max_joint_synergy,
        "max_pair_joint_synergy_witness": synergy_witness,
    }


def complete_coverage_curvature(surv_q: list[int], n: int):
    allv = (1 << n) - 1
    def f(mask: int) -> int:
        s = allv
        for q in bits(mask):
            s &= surv_q[q]
        return n - m1.popcount(s)
    f_full = f(FULL_CONTEXT_MASK)
    ratios = []
    for q in range(M):
        singleton = f(1 << q)
        if singleton <= 0:
            continue
        last = f_full - f(FULL_CONTEXT_MASK ^ (1 << q))
        ratios.append(last / singleton)
    return 0.0 if not ratios else 1.0 - min(ratios)


def pair_coverage_rows(bundle):
    _, _, d_by_q, _ = m1.pair_data(bundle)
    pair_count = d_by_q.shape[1]
    all_pairs = (1 << pair_count) - 1
    rows = []
    summaries = []
    for delta in DELTAS:
        covers = [m1.bits_from_bool(d_by_q[q] > delta) for q in range(M)]
        union = [0] * (1 << M)
        util = np.full(1 << M, -1, dtype=np.int32)
        util[0] = 0
        for k in range(1, MAX_BUDGET + 1):
            for mask in MASKS_BY_K[k]:
                b = mask & -mask
                q = b.bit_length() - 1
                prev = mask ^ b
                u = union[prev] | covers[q]
                union[mask] = u
                util[mask] = m1.popcount(u)
        full_union = 0
        for c in covers:
            full_union |= c
        full_unresolved = pair_count - m1.popcount(full_union)
        best = best_masks_by_budget(util)
        chosen = 0
        for k in range(1, MAX_BUDGET + 1):
            base = int(util[chosen])
            cand = max(
                ((int(util[chosen | (1 << q)]) - base, -q, q) for q in range(M) if not (chosen & (1 << q))),
                key=lambda x: (x[0], x[1]),
            )
            chosen |= 1 << cand[2]
            opt_val, opt_mask = best[k]
            g = int(util[chosen])
            rows.append({
                "delta": delta,
                "budget": k,
                "objective": "global_pair_coverage",
                "greedy_utility": g,
                "optimal_utility": opt_val,
                "greedy_over_optimal": g / opt_val if opt_val else 1.0,
                "greedy_panel": " ".join(panel_strings(chosen)),
                "optimal_panel": " ".join(panel_strings(opt_mask)),
                "total_world_pairs": pair_count,
                "full_library_unresolved_pairs": full_unresolved,
            })
        summaries.append({"delta": delta, "pair_count": pair_count, "full_library_unresolved_pairs": full_unresolved})
    return rows, summaries


def exact_entropy_rows(bundle):
    n = len(bundle.worlds)
    response_codes = np.zeros((M, n), dtype=np.int16)
    for q in range(M):
        mapping = {}
        nxt = 0
        for w in range(n):
            key = bundle.responses[w, q].tobytes()
            if key not in mapping:
                mapping[key] = nxt
                nxt += 1
            response_codes[q, w] = mapping[key]
    labels = [None] * (1 << M)
    labels[0] = np.zeros(n, dtype=np.int16)
    entropy = np.full(1 << M, np.nan, dtype=float)
    entropy[0] = 0.0
    for k in range(1, MAX_BUDGET + 1):
        for mask in MASKS_BY_K[k]:
            b = mask & -mask
            q = b.bit_length() - 1
            prev = mask ^ b
            pairs = list(zip(labels[prev].tolist(), response_codes[q].tolist()))
            mp = {}
            lab = np.empty(n, dtype=np.int16)
            nxt = 0
            for i, pair in enumerate(pairs):
                if pair not in mp:
                    mp[pair] = nxt
                    nxt += 1
                lab[i] = mp[pair]
            labels[mask] = lab
            counts = np.bincount(lab.astype(int))
            probs = counts[counts > 0] / n
            entropy[mask] = float(-(probs * np.log2(probs)).sum())
    rows = []
    chosen = 0
    for k in range(1, MAX_BUDGET + 1):
        best_mask = max(MASKS_BY_K[k], key=lambda mask: (entropy[mask], -mask))
        best_val = float(entropy[best_mask])
        cand_q = max(
            (q for q in range(M) if not chosen & (1 << q)),
            key=lambda q: (entropy[chosen | (1 << q)], -q),
        )
        chosen |= 1 << cand_q
        g = float(entropy[chosen])
        rows.append({
            "delta": 0.0,
            "budget": k,
            "objective": "uniform_prior_exact_signature_shannon_entropy_bits",
            "greedy_utility": g,
            "optimal_utility": best_val,
            "greedy_over_optimal": g / best_val if best_val > 0 else 1.0,
            "greedy_panel": " ".join(panel_strings(chosen)),
            "optimal_panel": " ".join(panel_strings(best_mask)),
            "maximum_possible_entropy_bits": math.log2(n),
        })
    return rows


def cycle4_counterexample():
    adj = [0] * 4
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
        add_edge(adj, a, b)
    allv = (1 << 4) - 1
    deletions = [1 << 1, 1 << 3]
    def f(mask: int):
        d = 0
        for q in range(2):
            if mask & (1 << q):
                d |= deletions[q]
        c = m1.component_mask(allv & ~d, 0, adj)
        return 4 - m1.popcount(c)
    vals = {"empty": f(0), "delete_v1": f(1), "delete_v3": f(2), "both": f(3)}
    vals["submodularity_gap"] = vals["both"] - vals["delete_v1"] - vals["delete_v3"] + vals["empty"]
    assert vals == {"empty": 0, "delete_v1": 1, "delete_v3": 1, "both": 3, "submodularity_gap": 1}
    return vals


def block_sparse_cycle_safe_audit():
    # A tree backbone with two attached triangles. Potentially deletable vertices
    # A={1,2,6}; each cyclic biconnected block contains at most one A vertex.
    n = 8
    adj = [0] * n
    edges = ((0, 1), (1, 2), (2, 3), (1, 4), (4, 5), (5, 1), (3, 6), (6, 7), (7, 3))
    for a, b in edges:
        add_edge(adj, a, b)
    allv = (1 << n) - 1
    deletable = [1, 2, 6]
    atomic_loss = {}
    for x in deletable:
        c = m1.component_mask(allv & ~(1 << x), 0, adj)
        atomic_loss[x] = allv & ~c
    rows = []
    for sel in range(1 << len(deletable)):
        d = 0
        predicted = 0
        chosen = []
        for i, x in enumerate(deletable):
            if sel & (1 << i):
                d |= 1 << x
                predicted |= atomic_loss[x]
                chosen.append(x)
        c = m1.component_mask(allv & ~d, 0, adj)
        actual = allv & ~c
        rows.append({"deleted_vertices": chosen, "actual_lost": bits(actual), "coverage_prediction": bits(predicted), "match": actual == predicted})
        assert actual == predicted
    return {"graph_edges": [list(e) for e in edges], "deletable_vertices": deletable, "all_8_deletion_subsets_match_fixed_coverage": True, "rows": rows}


def git_text(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    bundle = m1.load_source_bundle()
    topologies, index = build_topologies(bundle)
    exact_rows = []
    diagnostics = []
    worst = {}

    for law in bundle.laws:
        canonical_truth = index[(law, 0)]
        for delta in DELTAS:
            for topo_name, topo in topologies.items():
                util, surv_q = utility_table(bundle, canonical_truth, delta, topo["adj"])
                best = best_masks_by_budget(util)
                diag = restricted_diagnostics(util)
                diag.update({"truth_law": law, "canonical_truth_state": "0000", "delta": delta, "topology": topo_name})
                if topo_name == "complete_survivor":
                    diag["standard_total_curvature"] = complete_coverage_curvature(surv_q, len(bundle.worlds))
                    diag["standard_total_curvature_applicable"] = True
                else:
                    diag["standard_total_curvature"] = None
                    diag["standard_total_curvature_applicable"] = False
                diagnostics.append(diag)

                for truth_state in range(16):
                    greedy = greedy_for_truth_state(util, truth_state)
                    truth_idx = index[(law, truth_state)]
                    for k in range(1, MAX_BUDGET + 1):
                        opt_val, opt_mask_canon = best[k]
                        opt_mask_actual = permute_mask_xor(opt_mask_canon, truth_state)
                        g_val, g_mask_actual = greedy[k]
                        ratio = g_val / opt_val if opt_val > 0 else 1.0
                        exact_rows.append({
                            "truth_index": truth_idx,
                            "truth_law": law,
                            "truth_state": f"{truth_state:04b}",
                            "delta": delta,
                            "topology": topo_name,
                            "budget": k,
                            "greedy_utility": g_val,
                            "optimal_utility": opt_val,
                            "greedy_over_optimal": ratio,
                            "additive_gap": opt_val - g_val,
                            "greedy_panel": " ".join(panel_strings(g_mask_actual)),
                            "one_optimal_panel": " ".join(panel_strings(opt_mask_actual)),
                        })
                        key = (topo_name, delta, k)
                        cand = (ratio, -(opt_val - g_val), truth_idx)
                        if key not in worst or cand < worst[key][0]:
                            worst[key] = (cand, exact_rows[-1].copy())

    pair_rows, pair_summary = pair_coverage_rows(bundle)
    entropy_rows = exact_entropy_rows(bundle)
    grid_rows = m1.grid_counterexample_audit()
    cycle = cycle4_counterexample()
    block_safe = block_sparse_cycle_safe_audit()

    write_csv(OUT / "exact_vs_greedy_all_truths.csv", exact_rows)
    write_csv(OUT / "pair_coverage_exact_vs_greedy.csv", pair_rows)
    write_csv(OUT / "exact_entropy_exact_vs_greedy.csv", entropy_rows)

    # Machine-readable compact summaries.
    topo_summary = {}
    for topo_name in topologies:
        rs = [r for r in exact_rows if r["topology"] == topo_name]
        topo_summary[topo_name] = {
            "rows": len(rs),
            "minimum_greedy_over_optimal": min(r["greedy_over_optimal"] for r in rs),
            "maximum_additive_gap": max(r["additive_gap"] for r in rs),
            "greedy_suboptimal_rows": sum(r["additive_gap"] > 0 for r in rs),
            "exact_match_rows": sum(r["additive_gap"] == 0 for r in rs),
        }
    diag_summary = {}
    for topo_name in topologies:
        ds = [d for d in diagnostics if d["topology"] == topo_name]
        diag_summary[topo_name] = {
            "canonical_instances": len(ds),
            "instances_with_restricted_dr_violation": sum(d["worst_diminishing_returns_gap"] > 0 for d in ds),
            "largest_restricted_dr_gap": max(d["worst_diminishing_returns_gap"] for d in ds),
            "minimum_restricted_submodularity_ratio_capped_at_1": min(d["restricted_submodularity_ratio_capped_at_1"] for d in ds),
            "maximum_pair_joint_synergy": max(d["max_pair_joint_synergy"] for d in ds),
        }
        if topo_name == "complete_survivor":
            diag_summary[topo_name]["standard_total_curvature_range"] = [
                min(d["standard_total_curvature"] for d in ds),
                max(d["standard_total_curvature"] for d in ds),
            ]

    results = {
        "schema": "m2_optimization_results_v1",
        "source_commit": git_text("rev-parse", "HEAD"),
        "branch": git_text("branch", "--show-current"),
        "bundle": {
            "worlds": len(bundle.worlds),
            "laws": bundle.laws,
            "contexts": 16,
            "phenotype_coordinates_per_context": int(bundle.responses.shape[2]),
            "source_path": str((ROOT / "source_validation" / "two_context_2026-08-26").relative_to(ROOT)),
            "truth_coverage": "all 128 truths; exact XOR symmetry reduces computation to eight law-specific canonical state-0000 utilities, then every state is evaluated with state-specific greedy tie-breaking through q->q xor state",
        },
        "deltas": list(DELTAS),
        "budgets": list(range(1, MAX_BUDGET + 1)),
        "topologies": {k: {kk: vv for kk, vv in v.items() if kk != "adj"} for k, v in topologies.items()},
        "exact_vs_greedy_summary": topo_summary,
        "restricted_submodularity_diagnostic_summary": diag_summary,
        "worst_rows_by_topology_delta_budget": [v[1] for _, v in sorted(worst.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2]))],
        "pair_coverage_full_library_summary": pair_summary,
        "pair_coverage_budget_rows": pair_rows,
        "exact_signature_entropy_budget_rows": entropy_rows,
        "synthetic_counterexamples_and_safe_regimes": {
            "c4_two_vertex_cycle_counterexample": cycle,
            "m1_grid_arbitrarily_bad_greedy": grid_rows,
            "cycle_block_sparse_deletion_safe_audit": block_safe,
        },
    }
    (OUT / "m2_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (OUT / "submodularity_diagnostics.json").write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")

    print("M2 exact optimization PASS")
    print("rows exact-vs-greedy:", len(exact_rows))
    for name, s in topo_summary.items():
        print(name, s)
    for name, s in diag_summary.items():
        print("diagnostics", name, s)
    print("cycle C4 gap:", cycle["submodularity_gap"])
    print("grid ratios:", [r["ratio"] for r in grid_rows])
    print("pair rows:", len(pair_rows), "entropy rows:", len(entropy_rows))
    print("wrote", OUT / "m2_results.json")


if __name__ == "__main__":
    main()
