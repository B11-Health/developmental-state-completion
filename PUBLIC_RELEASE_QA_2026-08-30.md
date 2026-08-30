# Public Science Release QA — 2026-08-30

Status: LOCAL RELEASE CANDIDATE / NOT PUSHED

Release commit under review: `9e841d6` — audited science refresh through the SLICE-1 R15 pilot.

## Scope
This release candidate updates the public preprint/claims ledger and adds audited scientific/reproducibility lanes R10B, R11/R11A, T8/T8A, R12/R12A, R13/R13A, T9/T9A, and R15/R15A. It deliberately excludes rejected/pending media artifacts, R16 in-progress validation, grant proposal packages, and newer institutional/governance working papers.

## Mechanical QA
Executed from this release worktree:
- `lab_lanes/t8_calibration_compatibility/test_t8_compatibility.py` -> T8_TESTS_PASS
- `lab_lanes/t9_fixed_predictor_margin/test_t9_margin.py` -> T9_TESTS_PASS
- `lab_lanes/r12_domain_balanced_calibration/test_r12_domain_balanced.py` -> R12_TESTS_PASS
- `lab_lanes/r13_domainwise_sensitivity_surface/test_r13_contract.py` -> R13_CONTRACT_TEST_PASS
- `lab_lanes/r13_domainwise_sensitivity_surface/test_r13_results.py` -> R13_RESULTS_TEST_PASS
- `lab_lanes/r15a_independent_audit/audit_r15a.py` -> primary/secondary gates and all reported R2/history deltas reproduced; maximum discrepancy <= 2.3e-16.
- `lab_lanes/r15b_source_replication/R15B_SOURCE_REPLICATION_AUDIT.md` -> PASS; four fresh Zenodo preview downloads match committed size/SHA-256 exactly, feature tables match with max absolute difference 0, and metric differences are <= 2.3e-16.

## Release gate
R15B source-level replication is now PASS: fresh Zenodo bytes, SHA-256, all four 49x49 feature tables, both gates, and all reported metrics reproduce. Do not push this branch until a final diff/claim-boundary review confirms no superseded statement. R16 remains in-progress and is intentionally excluded.
