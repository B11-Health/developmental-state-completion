# R6 Claim Boundaries

## Supported
- A second independent developing-insect CTC dataset reproduces the statistical failure mode identified by R5: large positive relative history gains can occur in models that do not transfer adequately across acquisition groups.
- In the Tribolium primary task, nonlinear Delta R2 reached +0.42 while augmented cross-sequence prediction still failed the preregistered adequacy gate.
- One secondary future-speed Ridge model had positive R2 in both acquisitions, and older H reduced its performance in both; this is a useful control but not a promoted sufficiency result.
- The program-wide order “adequacy first, Delta-H second, calibration third” is empirically justified by R5 and R6.

## Not supported
- Tribolium cells possess a biological memory mechanism captured by old kinematics.
- Tribolium development is Markov or non-Markov.
- Current projected geometry/kinematics is a complete state.
- A +0.42 Delta R2 is evidence of state incompleteness when the augmented predictor itself fails group transfer.
- Two acquisition sequences establish broad replication.
- Cartographic pixel/slice coordinates are physical micrometer coordinates.

## Representation limitation
`Fluo-N3DL-TRIC` is a cartographic projection and the official CTC page reports physical voxel size as not applicable. R6 therefore uses sequence-normalized projected x/y geometry. This is a deliberately narrow prediction representation, not a claim about real 3D tissue mechanics.
