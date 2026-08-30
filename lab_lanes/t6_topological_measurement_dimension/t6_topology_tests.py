#!/usr/bin/env python3
"""Executable witnesses for T6 topology claims.

These computations illustrate finite samples of exact theorems. They are not
numerical proofs of Borsuk-Ulam or covering-space classification.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def circle_scalar_witness(samples: int = 20000):
    """For several continuous scalar functions, search sampled antipodal gaps."""
    funcs = {
        "cos": lambda t: math.cos(t),
        "sin_plus_cos2": lambda t: math.sin(t) + 0.35 * math.cos(2*t),
        "smooth_combo": lambda t: 0.7*math.sin(t) - 0.2*math.cos(3*t) + 0.1*math.sin(4*t),
    }
    out = {}
    for name, f in funcs.items():
        vals = []
        best = (float("inf"), None, None)
        for i in range(samples):
            t = 2 * math.pi * i / samples
            d = f(t) - f(t + math.pi)
            vals.append(d)
            if abs(d) < best[0]:
                best = (abs(d), t, d)
        sign_change = any(vals[i] == 0 or vals[i] * vals[(i+1) % samples] < 0 for i in range(samples))
        out[name] = {
            "min_abs_sampled_antipodal_gap": best[0],
            "theta_at_min": best[1],
            "signed_gap": best[2],
            "sampled_sign_change": sign_change,
        }
    return out


def circle_two_channel_margin(samples: int = 20000):
    """B(z)=(cos t,sin t) has exact antipodal distance 2."""
    mind = float("inf")
    maxerr = 0.0
    for i in range(samples):
        t = 2 * math.pi * i / samples
        x = (math.cos(t), math.sin(t))
        y = (math.cos(t + math.pi), math.sin(t + math.pi))
        d = math.hypot(x[0]-y[0], x[1]-y[1])
        mind = min(mind, d)
        maxerr = max(maxerr, abs(d-2.0))
    return {"sampled_min_distance": mind, "max_abs_error_from_exact_2": maxerr}


def degree_d_circle_cover(d: int, samples: int = 1000):
    """Show planar coordinates separate all d sheets of z->z^d."""
    global_min = float("inf")
    for i in range(samples):
        phi = 2 * math.pi * i / samples
        roots = [((phi + 2*math.pi*j)/d) for j in range(d)]
        pts = [(math.cos(t), math.sin(t)) for t in roots]
        for a in range(d):
            for b in range(a+1, d):
                dist = math.hypot(pts[a][0]-pts[b][0], pts[a][1]-pts[b][1])
                global_min = min(global_min, dist)
    exact = 2 * math.sin(math.pi/d)
    return {
        "degree": d,
        "set_theoretic_bits": math.ceil(math.log2(d)),
        "continuous_real_channels_planar": 2,
        "sampled_min_sheet_distance": global_min,
        "exact_min_sheet_distance": exact,
        "abs_error": abs(global_min-exact),
    }


def local_branch_monodromy_degree2():
    """Track the two square roots through one base turn: labels swap."""
    # At base angle phi, roots use continuously lifted angles phi/2 and phi/2+pi.
    start = (0.0, math.pi)
    end = (math.pi, 2*math.pi)
    # Mod 2pi, the first endpoint is the second start point, and vice versa.
    return {
        "start_sheet_angles": start,
        "end_sheet_angles_after_one_base_loop": end,
        "endpoint_mod_2pi": (end[0] % (2*math.pi), end[1] % (2*math.pi)),
        "monodromy_permutation": [1, 0],
    }


def main():
    results = {
        "interpretation": "Finite numerical witnesses only; theorem proofs are in THEOREMS.md.",
        "circle_scalar": circle_scalar_witness(),
        "circle_two_channel": circle_two_channel_margin(),
        "degree_covers": [degree_d_circle_cover(d) for d in (2, 3, 4, 8)],
        "degree2_monodromy": local_branch_monodromy_degree2(),
    }
    out = Path(__file__).with_name("t6_results.json")
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
