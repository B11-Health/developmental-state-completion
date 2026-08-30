#!/usr/bin/env python3
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_witness():
    subprocess.run([sys.executable, str(HERE / "t6_topology_tests.py")], check=True, capture_output=True, text=True)
    return json.loads((HERE / "t6_results.json").read_text(encoding="utf-8"))


def test_circle_scalar_sign_change():
    r = run_witness()
    assert all(v["sampled_sign_change"] for v in r["circle_scalar"].values())


def test_circle_two_channel_exact_margin():
    r = run_witness()
    assert abs(r["circle_two_channel"]["sampled_min_distance"] - 2.0) < 1e-12


def test_degree8_bits_vs_channels():
    r = run_witness()
    d8 = next(x for x in r["degree_covers"] if x["degree"] == 8)
    assert d8["set_theoretic_bits"] == 3
    assert d8["continuous_real_channels_planar"] == 2
    assert abs(d8["sampled_min_sheet_distance"] - 2*math.sin(math.pi/8)) < 1e-12


def test_degree2_monodromy_swaps():
    r = run_witness()
    assert r["degree2_monodromy"]["monodromy_permutation"] == [1, 0]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print("PASS", t.__name__)
