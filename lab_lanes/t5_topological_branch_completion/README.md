# T5 Topological Branch Completion

T5 asks what the local condition `ker Dh subset ker DF` misses when the current measurement has disconnected fibers.

## Core result
The differential condition makes the declared future response constant on each **connected component** of a measurement fiber, but not necessarily across different components with the same measured value. The natural deterministic completion is therefore the fiber-component/Reeb quotient. If a fixed measured value has `m` future-distinct component classes, any discrete completion needs at least `m` labels, i.e. at least `ceil(log2 m)` binary bits.

This does **not** say biology contains a literal binary branch variable. It identifies a global/topological obstruction and an information lower bound for any measurement that would resolve it.

## Files
- `TOPOLOGICAL_BRANCH_COMPLETION.md` — theorem statements, proofs, counterexample, intervention refinement, approximate version, empirical interface.
- `PRIOR_ART_AND_NOVELTY_BOUNDARY.md` — known Reeb/observability/Test-Cover ingredients versus the project-specific synthesis.
- `t5_branch_tests.py` / `t5_results.json` — executable finite witnesses.
- `literature_search.py` / `literature_search_raw.json` — automated literature reconnaissance.
- `T5_CHECKPOINT_2026-08-30.md` — decision and program implications.

## Reproduce
`python lab_lanes/t5_topological_branch_completion/t5_branch_tests.py`

No priority claim. No universal Markovity claim. No biological branch has yet been measured prospectively.
