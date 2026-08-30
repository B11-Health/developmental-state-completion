# M3 robust, cost-aware perturbation design

Preregistration-oriented design lane for the preserved 128-world developmental-state-completion simulator bundle.

Key separation:
- **Prospective design** treats truth as unknown and optimizes over all 128 candidate truths.
- **Retrospective scoring** may condition on a known truth only as a diagnostic and is never used to choose the living-pilot panel.

The executable audit includes exact enumeration over feasible panels, subset-DP state construction, a HiGHS MILP cross-check for costed pair coverage, tolerance/noise stress scenarios, independent experiment-failure probabilities, burden/cost budgets, and minimax robustification.

Current planning-proxy recommendation under `pilot_tight`: `0010 0100 1000`. This is **not** a biological protocol recommendation until proxy costs, burden units, failure probabilities, and phenotype tolerance/noise are replaced by preregistered protocol-derived values.

Reproduce from repository root:

`python lab_lanes/m3_robust_design/m3_robust_design.py`

Artifacts:
- `m3_robust_design.py` — executable optimizer/audit
- `m3_results.json` — machine-readable summary
- `m3_selector_comparison.csv` — objective-specific exact robust winners
- `m3_panel_shortlist.csv` — top exact prospective panels under each budget
- `M3_PREREGISTRATION_POLICY.md` — recommended preregistration algorithm/policy
- `THEOREM_COUNTEREXAMPLE_CHECKPOINT_M3_2026-08-30.md` — theory boundary and counterexamples
- `literature_map.json` — precedent/overlap ledger; no priority claim
- `artifact_manifest.json` — hashes and provenance
