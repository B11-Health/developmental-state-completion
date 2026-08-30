# T6 Topological Measurement-Dimension Obstructions

This lane extends T4/T5 from set-theoretic fiber-component completion to **continuous measurement realizability**.

## Main result
For the antipodal quotient `h:S^n->RP^n` with future `F(x)=x`, every fiber contains only two future-distinct states, but any globally continuous Euclidean augmentation needs exactly `n+1` real channels. One set-theoretic branch bit is therefore not the same thing as one continuous biomarker.

## Files
- `THEOREMS.md` — definitions, exact theorems, proofs, edge cases, finite-cover and characteristic-class generalizations.
- `PRIOR_ART.md` — established mathematics versus project-specific synthesis.
- `EMPIRICAL_IMPLICATIONS.md` — consequences for measurement and perturbation design.
- `REVIEWER_RED_TEAM.md` — adversarial claim checks and overstatement traps.
- `t6_topology_tests.py` — executable numerical/topological witnesses.
- `test_t6_topology.py` — regression tests.
- `t6_results.json` — generated witness output.
- `T6_CHECKPOINT_2026-08-30.md` — completion checkpoint.

## Reproduce
Run:

`python lab_lanes/t6_topological_measurement_dimension/test_t6_topology.py`

The tests are illustrations and regression checks, not substitutes for the exact topology proofs.

## Claim boundary
No priority claim is made for Borsuk-Ulam, covering-space monodromy, configuration spaces, equivariant topology, characteristic classes, Reeb spaces, or nonlinear observability. T6 uses these established ideas to expose a hidden assumption in continuous developmental-state completion.
