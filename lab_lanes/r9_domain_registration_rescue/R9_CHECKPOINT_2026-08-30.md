# R9 Acquisition/Developmental Registration Rescue Checkpoint

Date: 2026-08-30
Decision: **CONDITIONAL TRANSDUCTIVE ADEQUACY RESCUE FOR TRIBOLIUM RADIAL VELOCITY / OTHER TASKS FAIL**

## Objective
R9 asked whether R8's asymmetric cross-acquisition failure could be substantially reduced by outcome-blind registration of the same measured present, without changing cohort, anchor, future horizon, outcomes, models, or adequacy gate.

## Primary result
The preregistered **transductive domain-percentile** representation passes Gate 1 for *Tribolium* future radial velocity. Random Forest and Extra Trees have positive held-out R2 and beat the train-only mean RMSE in both reciprocal acquisition holds:

| Estimator | Held-out seq01 R2 | Seq01 RMSE | Held-out seq02 R2 | Seq02 RMSE |
|---|---:|---:|---:|---:|
| Random Forest | +0.081 | 0.001511 | +0.114 | 0.001203 |
| Extra Trees | +0.115 | 0.001483 | +0.224 | 0.001126 |
| Ridge | -0.193 | 0.001721 | -1.068 | 0.001838 |

Train-only naive RMSE is 0.001624 for held-out sequence01 and 0.001337 for held-out sequence02. Thus 2/3 estimators satisfy the frozen rule in both acquisitions.

This is the first trajectory-series representation from R5-R9 to pass the reciprocal absolute-adequacy prerequisite for one frozen organism/outcome task.

## Why this is conditional
The successful primary transform is **transductive**: each held-out acquisition's unlabeled present-state feature distribution is available and used to convert features to within-domain empirical percentiles. It is not a target-free inductive deployment result and must never be described as such.

The preregistered inductive invariant panel still fails, so R9 does not show that the same model transfers to a new acquisition without access to that acquisition's present-state distribution.

## Secondary convergence
Two independently prespecified S-only transductive diagnostics also pass the same Gate 1 for Tribolium radial velocity:
- separate source/target robust median-IQR standardization: RF +0.085/+0.112; Extra Trees +0.163/+0.177 R2 across seq01/seq02;
- CORAL covariance alignment: RF +0.177/+0.285; Extra Trees +0.297/+0.332 R2 across seq01/seq02.

These secondary passes strengthen the interpretation that acquisition-scale/distribution mismatch is materially involved. They do not prove it is the only missing factor.

## Negative control
For the passing primary percentile representation, deterministic target-row feature permutation makes every estimator/fold negative. RF control R2 is -0.237/-0.714 and Extra Trees is -0.072/-0.551 for held-out seq01/seq02. Thus the positive result requires the correct cell-to-present-state pairing; target marginal normalization alone is insufficient.

## Failures preserved
- Drosophila radial velocity: no preregistered representation passes Gate 1.
- Drosophila future speed: no representation passes.
- Tribolium future speed: no representation passes.
- Tribolium inductive invariant panel: fails reciprocal radial adequacy despite retaining the favorable seq02 direction.
- Ridge fails the rescued Tribolium radial task under the passing transductive representations.

## History boundary
R9 does **not** fit older H, run history permutations, or perform known-complete/known-incomplete calibration. The preregistration permits that work only after a primary adequacy pass and places it in a later stage. R9 establishes the prerequisite for exactly one task; it does not establish screening-off or residual history.

## Interpretation
The R5-R8 failure cannot be treated simply as evidence that more raw present features were missing. For Tribolium radial velocity, outcome-blind acquisition distribution registration converts the previously one-sided R8 result into reciprocal positive held-out prediction for two nonlinear estimators. This is evidence that domain/acquisition mismatch materially contributed to the earlier inadequacy.

The result remains task-, organism-, estimator-, feature-, and deployment-assumption-specific. It does not establish biological memory, non-Markov development, universal state sufficiency, or a mechanism for the acquisition shift.

## Next gate
A separate preregistered history/calibration lane may now test, **only for Tribolium future radial velocity under the frozen passing transductive percentile representation**, whether older H has stable incremental value beyond the registered present and whether the analysis has adequate sensitivity to interpret a near-zero increment.

R9_COMPLETE
