#!/usr/bin/env python3
"""M3 robust, cost-aware perturbation design on the preserved 128-world bundle.

This lane explicitly separates:
  * retrospective known-truth scoring (diagnostic only), and
  * prospective unknown-truth design (eligible for pilot policy).

The candidate library has only 16 contexts, so exact enumeration is the
certification path.  Subset dynamic programming is used to construct exact
coverage states; a sparse MILP independently checks one costed maximum-cover
instance.  Robust/minimax objectives are not assumed submodular.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
M1_PATH = ROOT / "lab_lanes" / "math" / "m1_math_verification.py"
spec = importlib.util.spec_from_file_location("m1_math_verification", M1_PATH)
m1 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = m1
spec.loader.exec_module(m1)

M = 16
MAX_K = 5
N_MASK = 1 << M
SCENARIOS = [
    {"name": "nominal", "delta": 0.01, "eta": 0.0},
    {"name": "noise_stress", "delta": 0.01, "eta": 0.005},
    {"name": "tolerance_stress", "delta": 0.05, "eta": 0.0},
    {"name": "joint_stress", "delta": 0.05, "eta": 0.005},
]
for s in SCENARIOS:
    s["effective_threshold"] = s["delta"] + 2.0 * s["eta"]

# Planning proxies only.  These are deliberately dimensionless and must be
# replaced by protocol-derived burden/cost/failure estimates before a living run.
CONTEXT_COST = [10 + 2 * int(q).bit_count() for q in range(M)]
CONTEXT_BURDEN = [4 + int(q).bit_count() for q in range(M)]
FAIL_PROB = [0.08 + 0.01 * int(q).bit_count() for q in range(M)]
BUDGETS = {
    "pilot_tight": {"max_k": 3, "max_cost": 46, "max_burden": 20},
    "pilot_extended": {"max_k": 4, "max_cost": 60, "max_burden": 27},
}

MASKS = [m for m in range(N_MASK) if m.bit_count() <= MAX_K]
MASK_SET = set(MASKS)


def bits(mask: int) -> list[int]:
    return [q for q in range(M) if mask & (1 << q)]


def panel(mask: int) -> list[str]:
    return [f"{q:04b}" for q in bits(mask)]


def git_text(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def mask_cost_tables() -> tuple[np.ndarray, np.ndarray]:
    cost = np.zeros(N_MASK, dtype=np.int16)
    burden = np.zeros(N_MASK, dtype=np.int16)
    for mask in range(1, N_MASK):
        b = mask & -mask
        q = b.bit_length() - 1
        prev = mask ^ b
        cost[mask] = cost[prev] + CONTEXT_COST[q]
        burden[mask] = burden[prev] + CONTEXT_BURDEN[q]
    return cost, burden


def feasible(mask: int, budget: dict, cost: np.ndarray, burden: np.ndarray) -> bool:
    return (
        mask.bit_count() <= budget["max_k"]
        and int(cost[mask]) <= budget["max_cost"]
        and int(burden[mask]) <= budget["max_burden"]
    )


def priors(bundle) -> dict[str, np.ndarray]:
    n = len(bundle.worlds)
    uniform = np.full(n, 1.0 / n)
    # Sensitivity prior only: 30% on law P00, remaining mass law-balanced.
    # It is not asserted as a biological prior and is not the primary policy.
    skew = np.zeros(n, dtype=float)
    for i, (law, _state) in enumerate(bundle.worlds):
        law_mass = 0.30 if law == "P00" else 0.70 / 7.0
        skew[i] = law_mass / 16.0
    assert abs(skew.sum() - 1.0) < 1e-12
    return {"uniform": uniform, "sensitivity_P00_30pct": skew}


def pair_tables(bundle, threshold: float):
    ii, jj, d_by_q, _ = m1.pair_data(bundle)
    covers = [m1.bits_from_bool(d_by_q[q] > threshold) for q in range(M)]
    union = [0] * N_MASK
    score = np.zeros(N_MASK, dtype=np.int16)
    for mask in MASKS:
        if mask == 0:
            continue
        b = mask & -mask
        q = b.bit_length() - 1
        prev = mask ^ b
        u = union[prev] | covers[q]
        union[mask] = u
        score[mask] = u.bit_count()
    return ii, jj, d_by_q, covers, union, score


def ambiguity_rows(bundle, threshold: float) -> list[list[int]]:
    n = len(bundle.worlds)
    allw = (1 << n) - 1
    out = []
    for q in range(M):
        # Symmetric per-context tolerance relation.
        d = np.max(np.abs(bundle.responses[:, q, None, :] - bundle.responses[None, q, :, :]), axis=2)
        out.append([m1.bits_from_bool(d[w] <= threshold) | (1 << w) for w in range(n)])
    assert all((rows[w] & (1 << w)) for rows in out for w in range(n))
    return out


def component_partition(row_masks: list[int], selected: list[int], n: int) -> list[int]:
    allw = (1 << n) - 1
    if not selected:
        return [allw]
    rows = [allw] * n
    for w in range(n):
        r = allw
        for q in selected:
            r &= row_masks[q][w]
        rows[w] = r
    unseen = allw
    comps = []
    while unseen:
        seed = unseen & -unseen
        comp = 0
        frontier = seed
        while frontier:
            comp |= frontier
            unseen &= ~frontier
            nbrs = 0
            x = frontier
            while x:
                b = x & -x
                i = b.bit_length() - 1
                x ^= b
                nbrs |= rows[i]
            frontier = nbrs & unseen
        comps.append(comp)
    return comps


def ambiguity_metric_tables(bundle, threshold: float, prior_map: dict[str, np.ndarray]):
    n = len(bundle.worlds)
    row_masks = ambiguity_rows(bundle, threshold)
    worst_elim = np.zeros(N_MASK, dtype=np.int16)
    entropy = {name: np.zeros(N_MASK, dtype=float) for name in prior_map}
    max_mass = {name: np.ones(N_MASK, dtype=float) for name in prior_map}
    for mask in MASKS:
        comps = component_partition(row_masks, bits(mask), n)
        max_count = max(c.bit_count() for c in comps)
        worst_elim[mask] = n - max_count
        for name, p in prior_map.items():
            masses = []
            for c in comps:
                mass = 0.0
                x = c
                while x:
                    b = x & -x
                    i = b.bit_length() - 1
                    x ^= b
                    mass += float(p[i])
                masses.append(mass)
            entropy[name][mask] = -sum(x * math.log2(x) for x in masses if x > 0)
            max_mass[name][mask] = max(masses)
    return worst_elim, entropy, max_mass


def connected_tables(bundle, threshold: float, adj: list[int], prior_map: dict[str, np.ndarray]):
    n = len(bundle.worlds)
    allw = (1 << n) - 1
    worst_elim = np.full(N_MASK, n, dtype=np.int16)
    expected = {name: np.zeros(N_MASK, dtype=float) for name in prior_map}
    # Only MASKS are meaningful; initialize empty-panel score correctly.
    worst_elim[0] = 0
    for truth in range(n):
        d_qw = m1.source_truth_distances(bundle, truth)
        surv_q = m1.survivor_bits_from_dist(d_qw, threshold)
        survivor = [0] * N_MASK
        survivor[0] = allw
        for mask in MASKS:
            if mask == 0:
                elim = 0
            else:
                b = mask & -mask
                q = b.bit_length() - 1
                prev = mask ^ b
                s = survivor[prev] & surv_q[q]
                survivor[mask] = s
                c = m1.component_mask(s, truth, adj)
                elim = n - c.bit_count()
            if elim < worst_elim[mask]:
                worst_elim[mask] = elim
            for name, p in prior_map.items():
                expected[name][mask] += float(p[truth]) * elim
    return worst_elim, expected


def known_truth_connected_table(bundle, truth: int, threshold: float, adj: list[int]) -> np.ndarray:
    n = len(bundle.worlds)
    allw = (1 << n) - 1
    d_qw = m1.source_truth_distances(bundle, truth)
    surv_q = m1.survivor_bits_from_dist(d_qw, threshold)
    survivor = [0] * N_MASK
    survivor[0] = allw
    score = np.zeros(N_MASK, dtype=np.int16)
    for mask in MASKS:
        if mask == 0:
            continue
        b = mask & -mask
        q = b.bit_length() - 1
        prev = mask ^ b
        s = survivor[prev] & surv_q[q]
        survivor[mask] = s
        score[mask] = n - m1.component_mask(s, truth, adj).bit_count()
    return score


def one_failure_submasks(mask: int) -> list[int]:
    return [mask] + [mask ^ (1 << q) for q in bits(mask)]


def expected_under_independent_failure(mask: int, score: np.ndarray) -> float:
    qs = bits(mask)
    total = 0.0
    sub = mask
    while True:
        prob = 1.0
        for q in qs:
            prob *= (1.0 - FAIL_PROB[q]) if (sub & (1 << q)) else FAIL_PROB[q]
        total += prob * float(score[sub])
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return total


def robust_and_expected(mask: int, arrays: list[np.ndarray]) -> tuple[float, float]:
    robust = min(float(a[s]) for a in arrays for s in one_failure_submasks(mask))
    expected_worst_scenario = min(expected_under_independent_failure(mask, a) for a in arrays)
    return robust, expected_worst_scenario


def direct_pair_count(covers: list[int], mask: int) -> int:
    u = 0
    for q in bits(mask):
        u |= covers[q]
    return u.bit_count()


def solve_pair_milp(covers: list[int], pair_count: int, budget: dict) -> dict:
    nvar = M + pair_count
    c = np.zeros(nvar, dtype=float)
    c[M:] = -1.0
    rows = []
    cols = []
    vals = []
    # y_j <= sum_q cover[q,j] x_q  -> y_j - sum x_q <= 0
    for j in range(pair_count):
        rows.append(j); cols.append(M + j); vals.append(1.0)
        bit = 1 << j
        for q in range(M):
            if covers[q] & bit:
                rows.append(j); cols.append(q); vals.append(-1.0)
    Acover = coo_matrix((vals, (rows, cols)), shape=(pair_count, nvar)).tocsr()
    extra = np.zeros((3, nvar), dtype=float)
    extra[0, :M] = CONTEXT_COST
    extra[1, :M] = CONTEXT_BURDEN
    extra[2, :M] = 1.0
    A = vstack([Acover, coo_matrix(extra).tocsr()], format="csr")
    lb = np.full(pair_count + 3, -np.inf)
    ub = np.concatenate([np.zeros(pair_count), [budget["max_cost"], budget["max_burden"], budget["max_k"]]])
    res = milp(
        c=c,
        integrality=np.ones(nvar, dtype=int),
        bounds=Bounds(np.zeros(nvar), np.ones(nvar)),
        constraints=LinearConstraint(A, lb, ub),
        options={"time_limit": 60.0, "mip_rel_gap": 0.0},
    )
    if res.x is None:
        return {"success": False, "status": int(res.status), "message": str(res.message)}
    mask = 0
    for q in range(M):
        if res.x[q] > 0.5:
            mask |= 1 << q
    return {
        "success": bool(res.success),
        "status": int(res.status),
        "message": str(res.message),
        "panel_mask": mask,
        "panel": panel(mask),
        "objective_pair_count": int(round(-res.fun)),
    }


def robustification_counterexamples() -> dict:
    # Min over two individually modular/coverage scenarios need not be submodular.
    f1 = {0: 0, 1: 1, 2: 0, 3: 1}
    f2 = {0: 0, 1: 0, 2: 1, 3: 1}
    g = {m: min(f1[m], f2[m]) for m in range(4)}
    assert g[1] + g[2] < g[3] + g[0]

    # Worst-case one-dropout robustification of cardinality coverage f(Q)=|Q|
    # is also non-submodular on {a,b}: singleton value is forced to zero,
    # while a two-test panel retains value one after either dropout.
    f = {0: 0, 1: 1, 2: 1, 3: 2}
    h = {
        0: 0,
        1: min(f[1], f[0]),
        2: min(f[2], f[0]),
        3: min(f[3], f[1], f[2]),
    }
    assert h[1] + h[2] < h[3] + h[0]

    # Independent-thinning expectation for the same coverage remains submodular.
    p = 0.8
    e = {0: 0.0, 1: p, 2: p, 3: 2 * p}
    assert e[1] + e[2] >= e[3] + e[0] - 1e-12
    return {
        "min_of_coverage_scenarios": {"scenario_1": f1, "scenario_2": f2, "robust_min": g, "submodular": False},
        "worst_one_dropout_of_coverage": {"base": f, "robust": h, "submodular": False},
        "independent_failure_expectation_example": {"survival_probability": p, "expected": e, "submodular": True},
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    bundle = m1.load_source_bundle()
    n = len(bundle.worlds)
    assert n == 128 and bundle.responses.shape == (128, 16, 34)
    adj, law_edges, index = m1.build_source_graph(bundle)
    prior_map = priors(bundle)
    cost, burden = mask_cost_tables()

    pair_scores = {}
    pair_covers = {}
    ambiguity_scores = {}
    entropy_scores = {name: {} for name in prior_map}
    ambiguity_max_mass = {name: {} for name in prior_map}
    connected_worst = {}
    connected_expected = {name: {} for name in prior_map}
    known_truth_scores = {}
    truth = index[("P06", 0)]
    pair_count = None

    for s in SCENARIOS:
        name = s["name"]
        thr = float(s["effective_threshold"])
        ii, jj, _d, covers, _union, pscore = pair_tables(bundle, thr)
        pair_count = len(ii)
        pair_scores[name] = pscore
        pair_covers[name] = covers
        a_worst, a_entropy, a_mass = ambiguity_metric_tables(bundle, thr, prior_map)
        ambiguity_scores[name] = a_worst
        for pname in prior_map:
            entropy_scores[pname][name] = a_entropy[pname]
            ambiguity_max_mass[pname][name] = a_mass[pname]
        c_worst, c_expected = connected_tables(bundle, thr, adj, prior_map)
        connected_worst[name] = c_worst
        for pname in prior_map:
            connected_expected[pname][name] = c_expected[pname]
        known_truth_scores[name] = known_truth_connected_table(bundle, truth, thr, adj)

    assert pair_count == 8128
    scenario_names = [s["name"] for s in SCENARIOS]

    metrics_by_budget = {}
    selector_rows = []
    shortlist_rows = []
    recommendations = {}

    for budget_name, budget in BUDGETS.items():
        candidate_masks = [m for m in MASKS if m and feasible(m, budget, cost, burden)]
        panel_metrics = {}
        for mask in candidate_masks:
            amb_rob, amb_exp = robust_and_expected(mask, [ambiguity_scores[s] for s in scenario_names])
            pair_rob, pair_exp = robust_and_expected(mask, [pair_scores[s] for s in scenario_names])
            ent_rob, ent_exp = robust_and_expected(mask, [entropy_scores["uniform"][s] for s in scenario_names])
            ent_skew_rob, _ = robust_and_expected(mask, [entropy_scores["sensitivity_P00_30pct"][s] for s in scenario_names])
            conn_rob, conn_exp_fail = robust_and_expected(mask, [connected_worst[s] for s in scenario_names])
            # Expected-across-truth connected elimination, then independent experiment failure.
            conn_prior_exp_robust_scenario = min(
                expected_under_independent_failure(mask, connected_expected["uniform"][s]) for s in scenario_names
            )
            panel_metrics[mask] = {
                "robust_worstcase_ambiguity_elimination": amb_rob,
                "expected_failure_worstscenario_ambiguity_elimination": amb_exp,
                "robust_pair_separation": pair_rob,
                "expected_failure_worstscenario_pair_separation": pair_exp,
                "robust_uniform_entropy_bits": ent_rob,
                "expected_failure_worstscenario_uniform_entropy_bits": ent_exp,
                "robust_skew_entropy_bits": ent_skew_rob,
                "robust_truth_rooted_elimination": conn_rob,
                "expected_failure_worstscenario_truth_rooted_worsttruth_elimination": conn_exp_fail,
                "expected_failure_worstscenario_truth_rooted_uniformprior_elimination": conn_prior_exp_robust_scenario,
                "cost": int(cost[mask]),
                "burden": int(burden[mask]),
                "k": mask.bit_count(),
            }

        objective_keys = {
            "worst_case_residual_ambiguity": "robust_worstcase_ambiguity_elimination",
            "pair_test_cover_separation": "robust_pair_separation",
            "expected_entropy_uniform_prior": "robust_uniform_entropy_bits",
            "truth_rooted_connected_ambiguity": "robust_truth_rooted_elimination",
        }
        winners = {}
        for obj, key in objective_keys.items():
            winner = max(
                candidate_masks,
                key=lambda m: (
                    panel_metrics[m][key],
                    panel_metrics[m]["expected_failure_worstscenario_uniform_entropy_bits"],
                    panel_metrics[m]["robust_pair_separation"],
                    panel_metrics[m]["robust_truth_rooted_elimination"],
                    -panel_metrics[m]["cost"],
                    -panel_metrics[m]["burden"],
                    -m,
                ),
            )
            winners[obj] = winner
            r = {"budget": budget_name, "objective": obj, "selector": "exact_enumeration_minimax_one_failure", "panel": " ".join(panel(winner))}
            r.update(panel_metrics[winner])
            selector_rows.append(r)

        # Preregistration policy: connectivity-aware primary, then topology-free
        # worst ambiguity, pair separation, entropy, then burden/cost.
        policy_winner = max(
            candidate_masks,
            key=lambda m: (
                panel_metrics[m]["robust_truth_rooted_elimination"],
                panel_metrics[m]["robust_worstcase_ambiguity_elimination"],
                panel_metrics[m]["robust_pair_separation"],
                panel_metrics[m]["robust_uniform_entropy_bits"],
                panel_metrics[m]["expected_failure_worstscenario_truth_rooted_uniformprior_elimination"],
                -panel_metrics[m]["burden"],
                -panel_metrics[m]["cost"],
                -m,
            ),
        )
        recommendations[budget_name] = policy_winner
        ranked = sorted(
            candidate_masks,
            key=lambda m: (
                panel_metrics[m]["robust_truth_rooted_elimination"],
                panel_metrics[m]["robust_worstcase_ambiguity_elimination"],
                panel_metrics[m]["robust_pair_separation"],
                panel_metrics[m]["robust_uniform_entropy_bits"],
                -panel_metrics[m]["burden"],
                -panel_metrics[m]["cost"],
                -m,
            ),
            reverse=True,
        )[:20]
        for rank, m in enumerate(ranked, 1):
            rr = {"budget": budget_name, "rank": rank, "panel": " ".join(panel(m)), "mask": m}
            rr.update(panel_metrics[m])
            shortlist_rows.append(rr)
        metrics_by_budget[budget_name] = {
            "feasible_nonempty_panels": len(candidate_masks),
            "objective_winner_masks": {k: int(v) for k, v in winners.items()},
            "policy_winner_mask": int(policy_winner),
        }

    tight = BUDGETS["pilot_tight"]
    nominal = scenario_names[0]
    tight_candidates = [m for m in MASKS if m and feasible(m, tight, cost, burden)]
    enum_pair = max(tight_candidates, key=lambda m: (int(pair_scores[nominal][m]), -int(cost[m]), -int(burden[m]), -m))
    milp_result = solve_pair_milp(pair_covers[nominal], pair_count, tight)
    if milp_result.get("success"):
        assert int(pair_scores[nominal][milp_result["panel_mask"]]) == int(pair_scores[nominal][enum_pair])
        assert direct_pair_count(pair_covers[nominal], milp_result["panel_mask"]) == int(pair_scores[nominal][milp_result["panel_mask"]])

    # Retrospective known-truth diagnostic under the same uncertainty/failure set.
    known_best = max(
        tight_candidates,
        key=lambda m: (
            robust_and_expected(m, [known_truth_scores[s] for s in scenario_names])[0],
            robust_and_expected(m, [known_truth_scores[s] for s in scenario_names])[1],
            -int(cost[m]), -int(burden[m]), -m,
        ),
    )
    known_rob, known_exp = robust_and_expected(known_best, [known_truth_scores[s] for s in scenario_names])

    counterexamples = robustification_counterexamples()
    rec_mask = recommendations["pilot_tight"]
    result = {
        "schema": "m3_robust_design_results_v1",
        "base_commit": git_text("rev-parse", "HEAD"),
        "branch": git_text("branch", "--show-current"),
        "bundle": {"worlds": n, "contexts": M, "phenotype_coordinates_per_context": int(bundle.responses.shape[2]), "pair_count": pair_count},
        "separation_of_modes": {
            "prospective": "unknown truth; optimize worst/expected performance over all 128 candidate truths; eligible for pilot policy",
            "retrospective": "conditions on a known truth after the fact; diagnostic only; never used to choose the living-pilot panel",
        },
        "uncertainty_scenarios": SCENARIOS,
        "planning_proxies_not_biological_measurements": {
            "context_cost_units": CONTEXT_COST,
            "context_burden_units": CONTEXT_BURDEN,
            "independent_failure_probability": FAIL_PROB,
            "replacement_required_before_living_run": True,
        },
        "budgets": BUDGETS,
        "priors": {
            "primary": "uniform over 128 worlds",
            "sensitivity": "30% law mass on P00, remaining 70% equally across other laws; states uniform within law; arbitrary stress prior, not biological evidence",
        },
        "topology": {
            "name": "law_mst_x_q4",
            "role": "declared simulator topology proxy for truth-rooted connected ambiguity only",
            "law_mst_edges": [[bundle.laws[i], bundle.laws[j], float(d)] for i, j, d in law_edges],
            "not_claimed": "not asserted to be the topology of living biology",
        },
        "solver_comparison": {
            "subset_dp": "pair unions and panel resource totals are built recursively by parent mask",
            "exact_enumeration_nominal_pair_best": {"panel_mask": int(enum_pair), "panel": panel(enum_pair), "pair_count": int(pair_scores[nominal][enum_pair])},
            "milp_nominal_pair_check": milp_result,
            "milp_matches_exact_objective": bool(milp_result.get("success") and milp_result["objective_pair_count"] == int(pair_scores[nominal][enum_pair])),
        },
        "budget_summaries": metrics_by_budget,
        "recommended_policy": {
            "budget": "pilot_tight",
            "panel_mask": int(rec_mask),
            "panel": panel(rec_mask),
            "lexicographic_order": [
                "maximize minimax truth-rooted elimination over all truths, uncertainty scenarios, and <=1 experiment failure",
                "maximize topology-free worst-case ambiguity elimination",
                "maximize robust pair separation",
                "maximize robust uniform-prior ambiguity-class entropy",
                "maximize worst-scenario expected truth-rooted elimination under independent failures",
                "minimize burden, then cost",
            ],
            "gate": "replace proxy costs/burdens/failure probabilities and predeclare phenotype tolerance/noise before any living experiment; rerun exact enumeration",
        },
        "retrospective_known_truth_diagnostic": {
            "truth": ["P06", "0000"],
            "panel_mask": int(known_best),
            "panel": panel(known_best),
            "robust_truth_rooted_elimination": known_rob,
            "expected_failure_worstscenario_elimination": known_exp,
            "eligible_for_prospective_recommendation": False,
        },
        "robustification_theory_checks": counterexamples,
    }

    write_csv(OUT / "m3_selector_comparison.csv", selector_rows)
    write_csv(OUT / "m3_panel_shortlist.csv", shortlist_rows)
    (OUT / "m3_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # Manifest is finalized after all companion documents are written by the lane.
    print(json.dumps({
        "recommended_panel": panel(rec_mask),
        "recommended_mask": rec_mask,
        "known_truth_diagnostic_panel": panel(known_best),
        "milp_matches_exact": result["solver_comparison"]["milp_matches_exact_objective"],
        "tight_feasible_panels": metrics_by_budget["pilot_tight"]["feasible_nonempty_panels"],
    }, indent=2))
    print("M3 robust design PASS")


if __name__ == "__main__":
    main()
