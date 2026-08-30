from __future__ import annotations

import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def mean(states, fn):
    return sum((prob * fn(st) for prob, st in states), F(0))


def variance(states, fn):
    mu = mean(states, fn)
    return mean(states, lambda st: (fn(st) - mu) ** 2)


def covariance(states, f, g):
    mf = mean(states, f)
    mg = mean(states, g)
    return mean(states, lambda st: (f(st) - mf) * (g(st) - mg))


def conditional_means(states, key_fn, value_fn):
    mass = defaultdict(F)
    total = defaultdict(F)
    for prob, st in states:
        key = key_fn(st)
        mass[key] += prob
        total[key] += prob * value_fn(st)
    return {k: total[k] / mass[k] for k in mass}


def mse(states, actual_fn, pred_fn):
    return mean(states, lambda st: (actual_fn(st) - pred_fn(st)) ** 2)


def exact_counterexample():
    # S is independent Rademacher. Z has {-1,0,+1} with probabilities 1/4,1/2,1/4.
    # E = Z^2 - 1/2 is mean-zero and uncorrelated with Z, but is exactly revealed by Z.
    states = []
    z_probs = [(F(-1), F(1, 4)), (F(0), F(1, 2)), (F(1), F(1, 4))]
    a = F(1, 4)
    for s in (F(-1), F(1)):
        for z, pz in z_probs:
            e = z * z - F(1, 2)
            st = {"s": s, "m": s, "z": z, "h": z, "e": e}
            st["y_a"] = st["m"] + st["e"] + a * st["z"]
            states.append((F(1, 2) * pz, st))

    e_given_s = conditional_means(states, lambda st: st["s"], lambda st: st["e"])
    z_given_s = conditional_means(states, lambda st: st["s"], lambda st: st["z"])
    y_given_s = conditional_means(states, lambda st: st["s"], lambda st: st["y_a"])
    y_given_sh = conditional_means(states, lambda st: (st["s"], st["h"]), lambda st: st["y_a"])

    vm = variance(states, lambda st: st["m"])
    ve = variance(states, lambda st: st["e"])
    vz = variance(states, lambda st: st["z"])
    b = vm + ve
    r0 = vm / b
    x = a * a * vz / b
    vary = variance(states, lambda st: st["y_a"])

    mse_s = mse(states, lambda st: st["y_a"], lambda st: y_given_s[st["s"]])
    mse_sh = mse(states, lambda st: st["y_a"], lambda st: y_given_sh[(st["s"], st["h"])])
    r2_s = F(1) - mse_s / vary
    r2_sh_actual = F(1) - mse_sh / vary
    delta_actual = r2_sh_actual - r2_s

    r2_s_t8 = r0 / (F(1) + x)
    r2_sh_t8 = (r0 + x) / (F(1) + x)
    delta_t8 = x / (F(1) + x)

    # Generalized oracle correction: g=E[E|S,H], q=Var(g)/B.
    g_map = conditional_means(states, lambda st: (st["s"], st["h"]), lambda st: st["e"])
    q_var = mean(states, lambda st: g_map[(st["s"], st["h"])] ** 2)
    q = q_var / b
    r2_sh_general = (r0 + x + q) / (F(1) + x)
    delta_general = (x + q) / (F(1) + x)

    rho = F(3, 4)
    delta_required = F(1, 10)
    t8_iff = r0 >= rho / (F(1) - delta_required)
    actual_witness = r2_s >= rho and delta_actual >= delta_required

    assumptions = {
        "E[E|S]=0": all(v == 0 for v in e_given_s.values()),
        "E[Z|S]=0": all(v == 0 for v in z_given_s.values()),
        "Cov(E,Z)=0": covariance(states, lambda st: st["e"], lambda st: st["z"]) == 0,
        "H reveals Z exactly": all(st["h"] == st["z"] for _, st in states),
        "finite second moments": True,
        "Var(M)>0": vm > 0,
        "Var(Z)>0": vz > 0,
    }

    assert all(assumptions.values())
    assert r2_s == r2_s_t8
    assert r2_sh_actual != r2_sh_t8
    assert delta_actual != delta_t8
    assert r2_sh_actual == r2_sh_general
    assert delta_actual == delta_general
    assert not t8_iff and actual_witness

    return {
        "a": fstr(a),
        "Var(M)": fstr(vm),
        "Var(E)": fstr(ve),
        "Var(Z)": fstr(vz),
        "B": fstr(b),
        "r0": fstr(r0),
        "x": fstr(x),
        "q=Var(E[E|S,H])/B": fstr(q),
        "assumptions": assumptions,
        "R2_S_actual": fstr(r2_s),
        "R2_S_T8": fstr(r2_s_t8),
        "R2_SH_actual_oracle": fstr(r2_sh_actual),
        "R2_SH_T8_claim": fstr(r2_sh_t8),
        "Delta_actual": fstr(delta_actual),
        "Delta_T8_claim": fstr(delta_t8),
        "Delta_generalized": fstr(delta_general),
        "rho": fstr(rho),
        "delta_required": fstr(delta_required),
        "T8_iff_says_compatible": t8_iff,
        "actual_nonzero_amplitude_witness_passes": actual_witness,
    }


def corrected_q0_example():
    # S, E, Z independent Rademacher; H=Z. Then E[E|S,H]=0 exactly.
    states = []
    a = F(1)
    for s in (F(-1), F(1)):
        for z in (F(-1), F(1)):
            for e in (F(-1), F(1)):
                st = {"s": s, "m": s, "z": z, "h": z, "e": e}
                st["y_a"] = s + e + a * z
                states.append((F(1, 8), st))

    y_given_s = conditional_means(states, lambda st: st["s"], lambda st: st["y_a"])
    y_given_sh = conditional_means(states, lambda st: (st["s"], st["h"]), lambda st: st["y_a"])
    e_given_sh = conditional_means(states, lambda st: (st["s"], st["h"]), lambda st: st["e"])

    vm = variance(states, lambda st: st["m"])
    ve = variance(states, lambda st: st["e"])
    vz = variance(states, lambda st: st["z"])
    b = vm + ve
    r0 = vm / b
    x = a * a * vz / b
    vary = variance(states, lambda st: st["y_a"])
    r2_s = F(1) - mse(states, lambda st: st["y_a"], lambda st: y_given_s[st["s"]]) / vary
    r2_sh = F(1) - mse(states, lambda st: st["y_a"], lambda st: y_given_sh[(st["s"], st["h"])]) / vary
    delta = r2_sh - r2_s

    assert all(v == 0 for v in e_given_sh.values())
    assert r2_s == r0 / (F(1) + x)
    assert r2_sh == (r0 + x) / (F(1) + x)
    assert delta == x / (F(1) + x)

    return {
        "E[E|S,H]=0": True,
        "r0": fstr(r0),
        "x": fstr(x),
        "R2_S": fstr(r2_s),
        "R2_SH": fstr(r2_sh),
        "Delta": fstr(delta),
    }


def exact_envelope_grid():
    # Exact-rational, implementation-independent check of the repaired q=0 envelope.
    r0s = [F(1, 5), F(1, 2), F(4, 5), F(1)]
    rhos = [F(1, 5), F(2, 5), F(3, 5), F(4, 5)]
    deltas = [F(1, 10), F(1, 4), F(1, 2), F(3, 4)]
    checked = 0
    mismatches = []
    for r0 in r0s:
        for rho in rhos:
            for delta in deltas:
                lo = delta / (F(1) - delta)
                hi = r0 / rho - F(1)
                interval_nonempty = hi >= 0 and lo <= hi
                theorem = r0 >= rho / (F(1) - delta)
                checked += 1
                if interval_nonempty != theorem:
                    mismatches.append({"r0": fstr(r0), "rho": fstr(rho), "delta": fstr(delta)})
    assert not mismatches
    return {"triples_checked": checked, "mismatches": mismatches}


def boundary_checks():
    # These are exact endpoint/limit sanity checks for the repaired q=0 theorem.
    # VE=0 => r0=1 and compatibility iff rho + delta <= 1.
    ve0_pairs = [(F(3, 5), F(1, 4)), (F(4, 5), F(1, 4)), (F(1, 2), F(1, 2))]
    ve0 = []
    for rho, delta in ve0_pairs:
        theorem = F(1) >= rho / (F(1) - delta)
        sum_rule = rho + delta <= 1
        assert theorem == sum_rule
        ve0.append({"rho": fstr(rho), "delta": fstr(delta), "compatible": theorem})

    return {
        "r0_below_rho": "no feasible x because R2_S(x)<=r0 for x>=0",
        "VE_zero": ve0,
        "delta_to_0": "lower x -> 0; compatibility -> r0>=rho",
        "delta_to_1": "lower x -> infinity; no finite compatible amplitude for rho>0",
        "rho_to_0": "upper x -> infinity; Delta_max -> 1 as a supremum at rho=0, not a finite-amplitude maximum",
        "rho_to_1": "for any fixed delta>0 compatibility becomes impossible; at rho=1, positive delta is impossible",
    }


def main():
    out = {
        "verdict": "NEEDS QUALIFICATION",
        "counterexample_under_stated_T8_assumptions": exact_counterexample(),
        "repaired_q0_example": corrected_q0_example(),
        "exact_repaired_envelope_grid": exact_envelope_grid(),
        "boundary_checks": boundary_checks(),
        "core_correction": "For oracle S+H R2, add E[E|S,H]=0 a.s. (with Z measurable from S,H), or replace the claimed curve by the generalized q-term curve.",
    }
    out_path = Path(__file__).with_name("audit_results.json")
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
