# R8 Morphology/Intensity Present-State Rescue Checkpoint

Date: 2026-08-30
Decision: **ADEQUACY-LIMITED / STOP BEFORE HISTORY INTERPRETATION**

## Question
R8 tested whether materially richer release-native present measurements could rescue the absolute cross-acquisition prediction prerequisite that failed in R5-R7. The frozen task, cohorts, reciprocal whole-acquisition split, anchor frame 25, future frame 40, outcomes, and estimator family were unchanged from the preregistration.

## Data recovered without full-archive download
Using the existing ZIP64 range reader and a serialized chunk cache, R8 recovered only raw image frames 23/24/25 and corresponding GT/TRA tracking-label frames for both sequences of `Fluo-N3DL-DRO` and `Fluo-N3DL-TRIC`. Each completed raw entry was reconstructed from bounded chunks and checked against ZIP uncompressed size and CRC before feature extraction.

Dense GT/SEG segmentation is not available for the required full cohort/time window. Therefore GT/TRA masks are explicitly treated as **tracking-label geometry proxies, not segmentation ground truth**. Raw pixel intensities are release-native image intensity, not calibrated molecular measurements.

## Present representation
The primary present-only representation combined R7 relational/kinematic features with prespecified morphology and intensity features from frames 23/24/25 only.

- Drosophila: R7 present 49 features; mask-augmented 91; full morphology+intensity present **139 features**.
- Tribolium: R7 present 46 features; mask-augmented 51; full morphology+intensity present **99 features**.

Added measurements include covariance/eigenvalue shape summaries, axis and bounding-box ratios, Drosophila proxy surface/sphericity, Tribolium projected area/perimeter/roundness, recent shape changes, within-acquisition ranks, local neighbor shape context, focal intensity distribution, gradients, boundary contrast, intensity polarity/asymmetry, recent intensity changes, and local intensity context. No frame after 25 enters S.

## Frozen Gate 1
A fixed organism/outcome could advance only if at least two of Ridge, Random Forest, and Extra Trees achieved both positive held-out R2 and lower RMSE than the train-only mean baseline in **both** reciprocal held-out acquisitions.

### Drosophila future radial velocity - FAIL
Full-primary held-out R2:
- Ridge: sequence01 catastrophic extrapolation / numerically extreme negative R2; sequence02 -1.622.
- Random Forest: sequence01 -0.186; sequence02 -0.455.
- Extra Trees: sequence01 -0.197; sequence02 -0.420.

Passing estimators in both folds: **0/3**.

### Drosophila future speed - FAIL
Full-primary nonlinear held-out R2 remained strongly negative:
- Random Forest: -4.866 / -15.663.
- Extra Trees: -4.718 / -16.971.
Ridge also failed, including catastrophic sequence01 extrapolation.

Passing estimators in both folds: **0/3**.

### Tribolium future radial velocity - FAIL with one-fold improvement
Full-primary held-out R2:
- Ridge: -0.271 / -0.544.
- Random Forest: -0.180 / **+0.295**.
- Extra Trees: -0.078 / **+0.299**.

RF and Extra Trees pass sequence02 but fail sequence01. No estimator passes both reciprocal acquisitions. Passing estimators in both folds: **0/3**. The one-fold improvement is not promoted because the gate was explicitly cross-acquisition.

### Tribolium future speed - FAIL
All full-primary held-out R2 values were negative in both acquisitions. Some models beat the naive RMSE in one fold, but positive R2 and reciprocal-fold success were both required.

Passing estimators in both folds: **0/3**.

## Mandatory stop
Gate 1 failed for all four organism x outcome tasks. Therefore, exactly as preregistered:
- older H was **not fit**;
- no history increment was interpreted;
- no H permutation null was run;
- no known-complete/known-incomplete calibration was run.

## Interpretation
R8 does **not** support biological-memory or non-Markov claims. It shows that even a much richer release-native present representation based on centroid/kinematics, local relations, tracking-mask geometry proxies, and raw-image intensity does not transfer adequately between the two acquisitions for the frozen frame25->40 tasks.

The asymmetric Tribolium radial result is especially informative: morphology/intensity can improve prediction in one acquisition without producing a representation that generalizes to the other. This points toward acquisition/domain shift, developmental registration, tissue identity, lineage context, or other missing present coordinates as live explanations. R8 cannot identify which explanation is correct.

## Program consequence
R5-R8 now establish a hard empirical discipline: **absolute present-state adequacy must precede residual-history inference**. Adding features until one fold looks good is not sufficient. A future rescue needs either stronger acquisition harmonization/registration, genuinely richer biological state measurements, more independent acquisitions, or a redesigned outcome/horizon chosen prospectively rather than after inspecting these failures.

R8_COMPLETE
