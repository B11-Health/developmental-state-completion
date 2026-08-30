# R10 Preregistration — Registered History Increment and Calibration

Date: 2026-08-30
Status: FROZEN BEFORE R10 HISTORY EVALUATION

## Eligibility inherited from R9
R9 produced exactly one primary Gate-1 pass: Tribolium `future_radial_velocity` under `transductive_domain_percentile`, with Random Forest and Extra Trees positive and better than the train-only mean baseline in both reciprocal held-out acquisitions. R10 is restricted to that task/representation. No Drosophila task, future-speed task, alternate horizon, or secondary registration method is eligible.

## Frozen data and representation
- Use the committed R8 Tribolium analysis table and R8 full 99-feature present schema.
- S: all 99 full-present columns, transformed independently within source and target acquisition to empirical percentile ranks exactly as R9 primary transductive registration.
- H: the four pre-existing R7/R8 older-history columns only: `old_speed_relcentroid`, `old_radial_relcentroid`, `old_tangential_relcentroid`, `old_log_volume_change_rate`.
- For S+H, H is independently converted to empirical percentile ranks within source and target acquisition, using no Y.
- Outcome: `future_radial_velocity` only.
- Split: reciprocal whole-acquisition holdout 01/02 only.
- Models counted for inference: Random Forest and Extra Trees with exactly the R8/R9 hyperparameters and seed 20260830. Ridge may be reported descriptively but cannot determine Gate 2 because it failed Gate 1.

## Observed Gate 2
For each adequate estimator, compute held-out R2 for S and S+H in both folds and `delta_R2 = R2(S+H)-R2(S)`.

Gate 2 passes only if BOTH Random Forest and Extra Trees satisfy:
1. delta_R2 > 0 in both reciprocal folds; and
2. mean delta_R2 across the two folds >= +0.02.

S+H must also retain positive R2 and beat the train-only mean baseline in both folds. A one-fold gain does not pass.

## Matched no-increment permutation calibration
Run 100 deterministic replicates. Within each fold and domain, independently permute H row assignments in training and held-out data, preserving H marginals but breaking cell-level H pairing. S and Y remain unchanged. Fit S+H_permuted using the same RF/ET models. For each replicate apply the same Gate-2 decision rule. The fraction of null replicates that pass Gate 2 is the matched finite-sample false-positive rate. Per-model/fold null delta-R2 distributions are also retained. Resolution is 1/100.

## Known-incomplete +0.30-SD calibration
Run 30 deterministic synthetic-effect replicates. For each replicate:
1. build a random unit-norm linear combination of the four domain-percentile H columns using seed 20260830+r;
2. residualize that H combination against registered S with Ridge(alpha=1) on the pooled S/H calibration table using no Y;
3. standardize the residual to unit SD;
4. define `Y* = Y + 0.30 * SD(Y) * H_residual`;
5. refit the same RF/ET S and S+H models under reciprocal acquisition holdout and apply the same Gate-2 rule.

Record whether the original S-only absolute-adequacy rule remains satisfied for both RF/ET in each synthetic replicate. Calibration is considered adequate to interpret a null/weak observed history result only if at least 24/30 (80%) replicates both preserve S-only adequacy and pass Gate 2 for the injected +0.30-SD residual-history effect.

This calibration is a matched sensitivity stress test, not a biological effect-size claim.

## Decision logic
- If observed Gate 2 passes and the 100-permutation false-positive rate is small, report stable residual-history value beyond the registered present for this one task. Do not call it mechanism or memory.
- If observed Gate 2 fails but +0.30-SD calibration power is >=80%, support a bounded near-zero/weak-history conclusion at that sensitivity scale.
- If observed Gate 2 fails and calibration power is <80%, label the history question calibration-limited/unresolved.
- If observed Gate 2 passes but permutation null frequently passes, label the increment unstable/unresolved.

## Prohibited inferences
No universal Markovity/non-Markovity, no organism-wide memory claim, no causal mechanism, no generalization beyond Tribolium radial velocity, no target-free deployment claim, and no re-use of the R5/R6 history increments computed inside inadequate unregistered predictors.
