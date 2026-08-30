# R6 Tribolium Trajectory Preregistration

Frozen before predictive model fitting on 2026-08-30.

## Dataset
Cell Tracking Challenge `Fluo-N3DL-TRIC`, developing *Tribolium castaneum* embryo, Max Planck Institute of Molecular Cell Biology and Genetics (Dresden, Germany), 3D cartographic projection, 1.5-minute time step. The challenge states that gold tracking evaluation focuses on blastoderm lineages at the embryonic/extra-embryonic tissue border.

## Analysis cohort
Use only gold-track labels whose single label exists continuously from frame 15 through frame 40. A label that divides/terminates inside this window is excluded rather than stitching descendants into a synthetic trajectory. Frames used: 15,20,23,24,25,40.

Expected from metadata before fitting: 93 qualifying sequence-01 tracks and 194 sequence-02 tracks (287 total).

## Coordinate convention
TRIC is a cartographic projection and the CTC page reports physical voxel size as not applicable. No micrometer geometry is claimed. For each acquisition sequence, frame-25 x/y centroids define a current-embryo center and RMS radial scale. This whole-frame current geometry is part of S and uses no future frame. All displacements are expressed in frame-25 embryo-scale units. z-slice centroid is retained in source data but excluded from the primary task.

## Frozen H / S / Y
Anchor: frame 25.

- `H`: older normalized x/y velocity from frame 15->20 (5 frames = 7.5 min), older speed, older radial velocity relative to the frame-25 radial direction, and older log-label-volume change.
- `S0`: frame-25 normalized radial distance + log label volume.
- `S1`: S0 + recent normalized speed and radial velocity from frame 24->25 + recent log-volume change.
- `S2`: S1 + recent acceleration magnitude and radial acceleration from frames 23,24,25.
- primary `Y`: average normalized future radial velocity over frame 25->40 (22.5 min), measured along the frame-25 radial unit direction.
- secondary `Y`: average normalized future speed magnitude over frame 25->40.

This is a kinematic state-sufficiency task. H is trajectory history, not molecular memory.

## Grouping
Two reciprocal leave-one-acquisition-sequence-out folds. No label from the held-out acquisition is used to fit the predictor. Whole-embryo frame-25 center/scale for that acquisition is allowed because it is explicitly part of the measured present S and contains no future information.

## Estimators
- standardized Ridge;
- Random Forest;
- Extra Trees.

No estimator will be selected post hoc as the sole basis of a promoted claim.

## Promotion gates
### Gate 1 — absolute predictive adequacy
Before interpreting any H increment, S+H must beat a train-only mean dummy under the same held-out acquisition, and must have positive held-out R2 in both reciprocal folds for at least two of the three prespecified estimators. Failure => `ADEQUACY_LIMITED`; do not promote Delta-H, and do not manufacture significance/calibration claims around an inadequate predictor.

### Gate 2 — stable residual-history increment
If Gate 1 passes, the H increment must be positive in both held-out acquisitions and positive on average for at least two of three estimators, with a material proper-score/R2 improvement rather than only negligible numerical drift.

### Gate 3 — sensitivity calibration
Only if Gates 1-2 pass, run matched known-complete/known-incomplete calibration plus within-sequence H permutations. A residual-history promotion requires demonstrated sensitivity to the frozen known-incomplete target.

## Interpretation boundaries
Even a positive R6 result would mean only that older projected kinematics add predictive value beyond the declared current projected kinematics for the frozen future-motion task. It would not establish organism-level non-Markovity, a molecular memory mechanism, or full biological state incompleteness.
