# R7 Cross-Organism Relational Present-State Adequacy Rescue — Preregistration

Frozen before predictive fitting on 2026-08-30.

## Question
R5 (Drosophila) and R6 (Tribolium) showed that positive residual-history increments can occur while absolute cross-acquisition prediction is inadequate. R7 asks a prior question: can a richer, acquisition-robust **present-only** relational representation rescue absolute future prediction across the two released acquisitions in either organism?

## Public inputs
Only already-recovered Cell Tracking Challenge release-native centroid/label-volume/track-table data from R5 `Fluo-N3DL-DRO` and R6 `Fluo-N3DL-TRIC` are used. No raw fluorescence, unreleased data, or new biological annotation is introduced.

## Cohorts and anchor
Anchor frame = 25. Frames 23/24/25 define recent motion; 15/20 are older history; frame 40 defines future. Focal Drosophila cohort: labels present at all six selected frames (189 sequence 01, 203 sequence 02). Focal Tribolium cohort: continuous labels spanning frames 15–40 per gold track metadata (expected 93 + 194). Current neighborhood geometry may use every released gold label available at frame 25; neighbor-motion summaries use only anchor neighbors with track continuity to the required past frame(s).

## Present representation S_R
All quantities are release-native and use no frame after 25. Coordinates are centered within acquisition on frame-25 released centroids and divided by frame-25 RMS radius. Rank transforms are within the measured anchor acquisition and are treated as current-state coordinates, not cross-acquisition learned parameters.

Prespecified present-only features:
- normalized distance to acquisition centroid and within-acquisition radial rank;
- log label volume and within-acquisition volume rank;
- k-nearest-neighbor distances/densities for k=3,5,10;
- local geometric spread/anisotropy from neighbor-offset covariance eigenvalues;
- local neighbor log-volume mean/dispersion and focal-minus-local-volume contrast;
- recent focal velocity and acceleration invariants: speed, radial component, tangential magnitude;
- motion relative to acquisition-centroid translation/acceleration;
- local neighbor velocity consensus/dispersion, focal-versus-consensus alignment and relative-speed mismatch where 24→25 continuity permits.

No absolute angular orientation or raw global vector component is used in the primary representation.

## Older history H
Only if Gate 1 passes for a specific organism/outcome: older 15→20 centroid-relative focal speed, radial velocity, tangential speed, and older log-volume change/rate. H is kinematic history, not molecular memory.

## Outcomes
Two prespecified scalar future tasks, both normalized by the anchor acquisition RMS radius:
1. average future radial velocity from frame 25→40 along the frame-25 radial unit direction;
2. average future speed from frame 25→40.

No vector task is promoted because reciprocal acquisition coordinate alignment is not established.

## Split and estimators
Primary split is reciprocal whole-acquisition holdout: train on sequence 01/test 02 and train on sequence 02/test 01. Core prespecified estimators: standardized Ridge, Random Forest, Extra Trees. The naive comparator is the **training-fold outcome mean**, with no held-out outcome information. Ridge preprocessing is fit on training rows only. Tree estimators receive the fixed current-state feature map directly.

## Mandatory decision order
### Gate 1 — absolute adequacy of present-only S_R
For an organism/outcome to advance, at least **two of the three core estimators** must, in **both** held-out sequences:
- have held-out R² > 0; and
- have RMSE strictly below the train-only mean naive baseline.

This gate is evaluated on `S_R` alone. Failure means `ADEQUACY_LIMITED`; history fitting for that organism/outcome is not run.

### Gate 2 — residual-history stability/materiality
Only for Gate-1-passing tasks, fit `S_R + H`. H must improve R² in both reciprocal folds for at least two core estimators and produce mean ΔR² >= 0.02 for those estimators. Otherwise stop without calibration.

### Gate 3 — sensitivity/permutation
Only for Gate-2-passing tasks, run within-training-acquisition row permutations of H (200 deterministic permutations per fold/estimator), refitting `S_R + permuted(H)`. Report the observed ΔR² against this null distribution. This is a sensitivity/null check, not a mechanistic causal test.

## Interpretation boundary
Representation inadequacy and biological memory are distinct. Failure of S_R means these released relational/kinematic observables do not transfer adequately for the frozen task. It does not imply biological memory. A stable H increment, if reached, would only show residual predictive information in older measured kinematics beyond the declared present representation; it would not establish non-Markov biology, a molecular memory mechanism, or a complete biological state.
