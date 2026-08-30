# R6 — Tribolium Cross-Sequence Trajectory Stress Test

Date: 2026-08-30
Status: **ADEQUACY-LIMITED NEGATIVE RESULT**

## Purpose
R6 tests the absolute-predictive-adequacy rule introduced by R5 in a second independent developing insect, *Tribolium castaneum*.

Public source: Cell Tracking Challenge `Fluo-N3DL-TRIC`, a 3D cartographic projection of a developing beetle embryo from the Max Planck Institute of Molecular Cell Biology and Genetics, Dresden, Germany. Frames are 1.5 minutes apart. The challenge identifies blastoderm lineages at the embryonic/extra-embryonic tissue border for tracking evaluation.

The public training archive is about 22.1 GB. R6 uses HTTP byte ranges to read only the ZIP64 central directory, two tiny lineage tables, and 12 selected gold tracking masks. No raw fluorescence movie is downloaded.

## Frozen cohort/task
Continuous labels from frame 15 through frame 40 only:
- sequence 01: 93 cells
- sequence 02: 194 cells
- total: 287

Anchor frame 25.

- H: older projected motion 15->20, old speed/radial velocity, old label-volume change.
- S0: current normalized radial position + log volume.
- S1: S0 + recent speed/radial motion 24->25 + recent volume change.
- S2: S1 + acceleration magnitude/radial acceleration 23/24/25.
- primary Y: future radial velocity 25->40.
- secondary Y: future speed 25->40.
- split: leave one entire acquisition sequence out.
- estimators: Ridge, Random Forest, Extra Trees.

See `PREREGISTRATION.md`; it was written before predictive fitting.

## Result
The **primary radial-velocity task failed Gate 1: absolute predictive adequacy**. No estimator had positive S+H R2 in both held-out acquisitions while also beating the train-mean dummy in both.

This matters because the relative history gains looked extremely impressive for the nonlinear models:

- S0 Random Forest: Delta R2 **+0.422**
- S0 Extra Trees: **+0.291**
- S2 Random Forest: **+0.180**
- S2 Extra Trees: **+0.249**

The nonlinear gains were positive in both reciprocal folds, yet the augmented predictors remained inadequate cross-sequence. At S2, RF S+H was R2=-0.121 in sequence 01 and +0.124 in sequence 02; Extra Trees was -0.198 and +0.183. The naive train-mean baseline was R2=-0.062 and -0.094 respectively.

Therefore the spectacular-looking Delta R2 values are **not** promoted as residual-history evidence.

The secondary future-speed task contained one useful opposite pattern: Ridge predicted future speed with positive R2 in both held-out acquisitions, but adding H made it worse in both folds. RF and Extra Trees were inadequate. This is not enough for a state-sufficiency claim because the preregistered multi-estimator adequacy rule was not met, but it further argues against cherry-picking a favorable H result.

## Program impact
R5 showed that +0.05 to +0.08 history gains can live inside an inadequate model. R6 shows the problem can be much larger: **Delta R2 above +0.4 can still be scientifically disqualified by absolute transfer failure.**

That makes the adequacy gate a central result of the current program's statistical discipline.
