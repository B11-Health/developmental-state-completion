# R6 Tribolium Trajectory Checkpoint

Date: 2026-08-30
Decision: **ADEQUACY-LIMITED — DO NOT PROMOTE RESIDUAL-HISTORY CLAIM**

## Source
Cell Tracking Challenge `Fluo-N3DL-TRIC`, developing *Tribolium castaneum* embryo, Dr. A. Jain / Max Planck Institute of Molecular Cell Biology and Genetics, Dresden, Germany. Cartographic projection; 1.5-minute time step; physical voxel size is explicitly not applicable on the CTC page due to the projection.

Gold annotations cover blastoderm lineages near the embryonic/extra-embryonic border. R6 does not generalize to all embryonic cells.

## Data acquisition
The 22,088,481,712-byte public ZIP accepts HTTP range requests. R6 selectively recovered the gold lineage tables and frames 15,20,23,24,25,40 for both training sequences. Compressed gold-mask payload for each selected frame is only about 53-55 kB, so the analysis avoids downloading the raw 22 GB movie.

Cohort restriction was frozen before fitting: a label must exist continuously from frame 15 through frame 40. Resulting N=287 (93 + 194).

## Preregistered primary task
Primary outcome = normalized future radial velocity from frame 25 to 40.

Absolute adequacy gate required S+H to:
1. beat a train-only mean dummy in both held-out sequences; and
2. have positive held-out R2 in both sequences for at least two of three estimators.

Only after this could Delta-H be interpreted.

## Primary findings
### Richest present S2
| Estimator | Mean R2(S) | Mean R2(S+H) | Delta R2 | Delta positive in both folds? | Gate-1 adequate? |
|---|---:|---:|---:|---|---|
| Extra Trees | -0.256 | -0.008 | **+0.249** | yes | no |
| Random Forest | -0.179 | +0.001 | **+0.180** | yes | no |
| Ridge | -0.092 | -0.622 | -0.530 | no | no |

The mean values hide the critical fold asymmetry. S2 RF S+H: sequence01 R2=-0.121, sequence02 +0.124. S2 Extra Trees S+H: -0.198, +0.183. Neither is adequate in both acquisitions.

At the coarsest S0, the apparent nonlinear history rescue was even larger: RF +0.422 and Extra Trees +0.291, positive in both folds, while mean augmented R2 remained around -0.013 and -0.043.

### Why the result is negative
The exact scientific question is not “can H make a bad model less bad?” It is whether H adds stable information inside a predictor that actually transfers to a new acquisition. R6 fails that prerequisite.

Gate 1 = FAIL.
Gate 2 = not evaluated for promotion.
Gate 3 calibration/permutation = not run because Gate 1 failed.

## Secondary future-speed task
Ridge produced positive absolute R2 in both folds at all S levels. At S2:
- sequence01 R2(S)=+0.277, R2(S+H)=+0.092;
- sequence02 R2(S)=+0.090, R2(S+H)=+0.040.

Thus, for the one estimator that transferred well, adding older H **hurt prediction in both acquisitions**. The nonlinear estimators showed positive H increments but remained inadequate.

No “history irrelevant” claim is promoted because the preregistered multi-estimator adequacy/calibration standard was not met.

## Cross-lane synthesis
R2 blocked promotion because sensitivity/calibration power was inadequate despite large H gains.
R5 blocked promotion because absolute cross-group prediction was inadequate despite positive H gains in a secondary task.
R6 reproduces the R5 failure mode in a different organism and makes it quantitatively stronger: even +0.42 Delta R2 can be a false-positive narrative if absolute transfer is ignored.

## Next implication
Future state-sufficiency protocols should treat the decision order as mandatory:

**absolute adequacy -> increment stability -> sensitivity calibration -> scoped biological interpretation.**

R6_COMPLETE
