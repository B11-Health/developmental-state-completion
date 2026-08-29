# Reproducibility Manifest

## Current checkpoint state

This public repository was created on 2026-08-29 from a research program developed across multiple computational workspaces and conversation checkpoints. The immediate priority is to **preserve provenance before migration**.

### Frozen checkpoint identifiers recovered from the research log

- `INNOVATION_CLOSURE_STATE_COMPLETION_CHECKPOINT_2026-08-28.md`
  - reported SHA-256: `be709de7b39f2c6a4470ed7409e8ba7ef50c39cea075f5674f33b774f5cd72e8`
- `STRATIFIED_CAUSAL_FIBER_AND_MECHANISM_PERSISTENCE_CHECKPOINT_2026-08-26.md`
  - reported location in the original workspace: `/root/plant_m2_deep/`

The second file's hash was not recovered in the current authenticated workspace and must be recomputed from the original artifact before it is treated as frozen evidence.

## Required artifact migration

A result moves from “reported computational finding” to “reproduced in this repository” only when all of the following are committed:

1. raw or source-referenced input data;
2. dataset license and canonical citation;
3. exact preprocessing code;
4. analysis code;
5. environment lockfile/container recipe;
6. random seeds;
7. machine-readable output tables;
8. figure-generation code;
9. hashes of generated artifacts;
10. a clean-run transcript from a fresh environment.

## Minimum reproducible test suite

### Test A — known-Markov calibration

Re-run the Abley-style ABA–GA stochastic model with a complete Markov state and verify that the chosen finite estimator can still show nonzero apparent history gain. Quantify the null distribution across sample sizes and model classes.

### Test B — flower screening-off

For each eligible lineage window:

- fit past-only, current-only, and current+past models under nested cross-validation;
- report uncertainty, not only point estimates;
- compare against shuffled-history and known-Markov calibration distributions;
- repeat across flowers with discovery/validation separation fixed in advance.

### Test C — molecular state completion

Reproduce the reported FM1 trajectory-only, trajectory+PC1, and all-molecular models. Verify that PC1 is learned without leakage and that the older-history incremental value remains small after conditioning on present state.

### Test D — finite-count germination model

Reconstruct seed counts from archived percentages only when rational reconstruction is unambiguous. Fit the binomial logistic latent-factor model and compare it against continuous-percentage baselines under held-out genotype and held-out condition prediction.

### Test E — 224 hidden worlds

Recreate the full 14 architecture × 16 hidden-state grid. For every world, save baseline and intervention outputs. Verify exact hidden-world indexing and show at least one same-baseline/different-counterfactual pair.

### Test F — causal-fiber topology

Rebuild the sampled state-law complex and report:

- node and edge construction rules;
- phenotype metric;
- tolerance sweep;
- connected components;
- accommodation and merge/access thresholds;
- stability under grid refinement and alternative distance metrics.

### Test G — intervention ranking

For every candidate perturbation, compute the connected-fiber contraction at preregistered tolerances. Compare topology-aware selection against Fisher-information, global-parameter, random, and equal-cost baselines.

## Reproduction tags

We will use the following labels in releases:

- `reported` — recovered from a prior checkpoint but not yet re-run here;
- `reproduced` — cleanly re-run from committed code/data;
- `replicated` — independently reproduced by a separate analyst or lab;
- `prospective` — prediction frozen before new data collection;
- `biological-validation` — prospective living-system result.

The long-term goal is for every headline claim in the README to carry one of these tags and a direct path to its evidence bundle.
## Independent R1 audit — 2026-08-29

An isolated replication lane re-ran the direct-source FM1 pipeline against authors' commit `95fde8b3b9a0bd09d556ce765a2235093362306f`, checked lineage-group leakage, repeated middle/late L1 history tests, reran a fresh calibration smoke test, and audited repository history for the legacy molecular-gain tuple. It independently supports the narrowed late-L1 screening-off result but finds the exact historical `0.272 -> 0.643` tuple provenance-incomplete. See `lab_lanes/replication/R1_REFAHI_REPLICATION_CHECKPOINT_2026-08-29.md` and `lab_lanes/replication/r1_refahi_independent_audit.py`.
