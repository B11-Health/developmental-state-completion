# R13 Failure Decomposition

Date: 2026-08-30
Status: descriptive analysis of the preregistered completed surface; no new fits or scales.

## Why 0.45 does not reach 24/30
At 0.45 target SD, S-only adequacy is 27/30 and Gate-2 detection is 23/30, but their overlap is 22/30. The failures are not one homogeneous low-power mode.

Estimator-level Gate-2 components at 0.45:
- Extra Trees sign failure in at least one reciprocal fold: reps 1, 10, 17, 19.
- Extra Trees positive in both folds but mean delta-R2 < 0.02: rep 2.
- Random Forest sign failure in at least one reciprocal fold: reps 1, 10, 17, 19.
- Random Forest positive in both folds but mean delta-R2 < 0.02: reps 2, 18, 23.
- S+H absolute-adequacy failures: none.

Thus the residual detection bottleneck at 0.45 is almost entirely cross-fold sign stability and the frozen mean-delta threshold, not S+H inadequacy.

## Why 0.60 gets worse
At 0.60, adequacy stays 27/30 but Gate-2 detection falls from 23/30 to 22/30 and joint success falls from 22/30 to 20/30.

Paired 0.45 -> 0.60 transitions:
- joint true -> true: 19
- joint true -> false: 3 (reps 3, 7, 14)
- joint false -> true: 1 (rep 23)
- joint false -> false: 7

For reps 3, 7, and 14, Extra Trees remains strongly positive at 0.60 and Random Forest retains a positive mean delta-R2, but one RF reciprocal fold becomes negative. Therefore the larger injection does not simply weaken the signal; the nonlinear refit changes cross-domain fold behavior.

Rep 23 moves the other direction: at 0.45 both estimators are positive in both folds but RF mean delta-R2 is only ~0.0167 (<0.02); at 0.60 both estimators are comfortably positive and the replicate passes.

Estimator-level Gate-2 components at 0.60:
- Extra Trees sign failures: reps 1, 17, 19.
- Random Forest sign failures: reps 3, 7, 14, 17, 19.
- Random Forest positive in both folds but mean delta-R2 < 0.02: rep 10.
- S+H absolute-adequacy failure: rep 18.

## Design implication
The preregistered grid does not justify searching for a finely tuned amplitude between 0.45 and 0.60. The relevant remaining issue is stability of incremental prediction across independent domains/estimators. A future confirmatory design should increase independent acquisition/session structure and choose its calibration geometry/amplitude prospectively, rather than optimize amplitude on these same 30 directions.

This analysis is descriptive of the frozen surface and cannot upgrade R13 into biological evidence.
