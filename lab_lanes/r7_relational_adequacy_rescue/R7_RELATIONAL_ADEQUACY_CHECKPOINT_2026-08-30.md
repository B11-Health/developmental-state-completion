# R7 Cross-Organism Relational Present-State Adequacy Rescue Checkpoint

Date: 2026-08-30
Decision: **ADEQUACY-LIMITED / STOP BEFORE HISTORY INTERPRETATION**

## Objective
R7 tested whether substantially richer release-native, acquisition-robust present-state representations could rescue absolute future prediction in the same two-organism public trajectory setting where R5 and R6 showed misleading positive residual-history increments inside inadequate predictors.

## Data and split
No new biological data were fetched. R7 reused the public-derived CTC centroid/label-volume/track-table files already committed and provenance-checked by R5 and R6.

- Drosophila: 392 focal tracks, reciprocal acquisition holdout (189 / 203).
- Tribolium: 287 continuous focal tracks, reciprocal acquisition holdout (93 / 194).
- Anchor frame: 25; recent-state frames: 23/24/25; future frame: 40.
- Primary split: hold out an entire acquisition sequence reciprocally.

## Present-only representation tested
The preregistered `S_R` representation used no future frame and included approximately 46–49 scalar invariant features depending on dimensionality:
- acquisition-centered RMS-scale-normalized radius and rank;
- current label-volume value/rank;
- kNN distance/density features for k=3,5,10;
- local covariance/eigenvalue shape fractions;
- neighbor volume mean/dispersion/contrast;
- recent focal velocity and acceleration invariants;
- focal motion relative to acquisition-centroid translation/acceleration;
- neighbor recent-velocity consensus, dispersion, alignment and relative-speed mismatch.

No raw absolute angle or cross-acquisition global vector alignment was used. Tribolium remained in normalized cartographic-projection coordinates.

## Gate 1 — absolute adequacy of present-only S_R
Frozen rule: for an organism/outcome to advance, at least two of Ridge, Random Forest, and Extra Trees must have positive held-out R² **and** beat the train-only outcome-mean baseline in RMSE in **both** reciprocal held-out acquisitions.

### Drosophila — future radial velocity
| Estimator | Seq01 R² | Seq02 R² | Seq01 RMSE | Seq02 RMSE |
|---|---:|---:|---:|---:|
| Train-mean naive | -0.014 | -0.015 | 0.004809 | 0.004762 |
| Ridge | -0.382 | -1.586 | 0.005613 | 0.007602 |
| Random Forest | -0.252 | -0.522 | 0.005344 | 0.005831 |
| Extra Trees | -0.302 | -0.532 | 0.005449 | 0.005851 |

Passing estimators in both folds: **0 / 3**.

### Drosophila — future speed
| Estimator | Seq01 R² | Seq02 R² | Seq01 RMSE | Seq02 RMSE |
|---|---:|---:|---:|---:|
| Train-mean naive | -4.016 | -15.372 | 0.008377 | 0.007735 |
| Ridge | -5.344 | -28.944 | 0.009421 | 0.010461 |
| Random Forest | -4.478 | -18.057 | 0.008754 | 0.008346 |
| Extra Trees | -4.377 | -18.579 | 0.008674 | 0.008459 |

Passing estimators in both folds: **0 / 3**.

### Tribolium — future radial velocity
| Estimator | Seq01 R² | Seq02 R² | Seq01 RMSE | Seq02 RMSE |
|---|---:|---:|---:|---:|
| Train-mean naive | -0.062 | -0.094 | 0.001624 | 0.001337 |
| Ridge | -0.754 | -0.846 | 0.002088 | 0.001736 |
| Random Forest | -0.529 | -1.006 | 0.001949 | 0.001810 |
| Extra Trees | -0.641 | -0.869 | 0.002019 | 0.001747 |

Passing estimators in both folds: **0 / 3**.

### Tribolium — future speed
| Estimator | Seq01 R² | Seq02 R² | Seq01 RMSE | Seq02 RMSE |
|---|---:|---:|---:|---:|
| Train-mean naive | -0.115 | -0.069 | 0.000924 | 0.001171 |
| Ridge | -0.730 | -0.017 | 0.001151 | 0.001142 |
| Random Forest | -0.481 | -0.192 | 0.001065 | 0.001236 |
| Extra Trees | -0.177 | -0.127 | 0.000949 | 0.001202 |

Passing estimators in both folds: **0 / 3**. Ridge narrowly beats the naive RMSE in sequence 02, but still has negative R² and fails sequence 01; this is not adequate under the frozen rule.

## Mandatory stop
All four organism × outcome tasks fail Gate 1. Therefore:
- Gate 2 older-history increment fitting was **not run**;
- Gate 3 permutation/sensitivity calibration was **not run**;
- no residual-history effect is interpreted or promoted.

This follows the preregistered decision order rather than mining a positive ΔR² from inadequate predictors.

## Scientific interpretation
The negative result is stronger than R5/R6 in one specific way: adding local relational geometry, anchor ranks, local density/shape statistics, and neighbor-motion consensus still did not make the released centroid/volume/kinematic present representation transfer adequately across acquisitions for the frozen horizons.

That is evidence of **representation/task transfer inadequacy**, not evidence of biological memory. Possible missing present-state information includes developmental registration, richer morphology, intensity/polarity, tissue identity, lineage context, molecular state, or other acquisition-robust coordinates unavailable in the current release-native tables. R7 does not identify which missing variable matters.

## Cross-lane conclusion
R5/R6 warned that a large positive history increment can be meaningless when absolute prediction is bad. R7 attempted the direct rescue and still failed the earlier prerequisite. Thus the defensible program-level lesson remains:

**absolute present-state adequacy -> residual-history increment -> sensitivity/calibration -> scoped interpretation.**

R7 stops at the first arrow.

R7_COMPLETE
