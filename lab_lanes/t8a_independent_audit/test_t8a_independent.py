import importlib.util
from pathlib import Path

HERE = Path(__file__).parent
sp = importlib.util.spec_from_file_location("audit_t8a", HERE / "audit_t8a.py")
audit = importlib.util.module_from_spec(sp)
sp.loader.exec_module(audit)


def test_stated_assumptions_admit_counterexample():
    r = audit.exact_counterexample()
    assert all(r["assumptions"].values())
    assert r["R2_S_actual"] == r["R2_S_T8"]
    assert r["R2_SH_actual_oracle"] != r["R2_SH_T8_claim"]
    assert r["Delta_actual"] != r["Delta_T8_claim"]
    assert r["T8_iff_says_compatible"] is False
    assert r["actual_nonzero_amplitude_witness_passes"] is True


def test_generalized_q_term_repairs_counterexample():
    r = audit.exact_counterexample()
    assert r["Delta_actual"] == r["Delta_generalized"]
    assert r["q=Var(E[E|S,H])/B"] == "1/5"


def test_strengthened_conditional_mean_assumption_recovers_curves():
    r = audit.corrected_q0_example()
    assert r["E[E|S,H]=0"] is True
    assert r["R2_S"] == "1/3"
    assert r["R2_SH"] == "2/3"
    assert r["Delta"] == "1/3"


def test_repaired_envelope_exact_rational_grid():
    r = audit.exact_envelope_grid()
    assert r["triples_checked"] == 64
    assert r["mismatches"] == []


if __name__ == "__main__":
    test_stated_assumptions_admit_counterexample()
    test_generalized_q_term_repairs_counterexample()
    test_strengthened_conditional_mean_assumption_recovers_curves()
    test_repaired_envelope_exact_rational_grid()
    print("T8A_INDEPENDENT_TESTS_PASS")
