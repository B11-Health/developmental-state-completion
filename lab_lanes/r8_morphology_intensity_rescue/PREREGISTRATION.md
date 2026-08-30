# R8 Morphology/Intensity Present-State Rescue — Preregistration

Frozen before any R8 predictive fitting on 2026-08-30.

## Question
R7 found that a 46–49 feature relational centroid/volume/kinematic present representation still failed absolute reciprocal cross-acquisition prediction in both Drosophila and Tribolium. R8 tests whether adding materially richer release-native mask geometry and raw-image intensity available at or before anchor frame 25 can rescue that prerequisite.

## Frozen organisms, cohort, split, and outcomes
R8 preserves the R7 cohorts and tasks without horizon or outcome search:
- organisms: CTC `Fluo-N3DL-DRO` and `Fluo-N3DL-TRIC`;
- focal cohorts: exactly the R7 labels used in its committed analysis tables;
- recent frames: 23, 24, 25; anchor = 25;
- future frame used only for outcomes: 40;
- outcomes: `future_radial_velocity` and `future_speed` exactly as committed by R7;
- primary split: reciprocal whole-acquisition holdout, train sequence 01/test 02 and train 02/test 01;
- estimators: Ridge(alpha=1) with train-only standardization, Random Forest(300 trees, min_leaf=4, max_features=.8), Extra Trees(300 trees, min_leaf=3, max_features=.9), random seed 20260830.

No frame after 25 enters S. Frames 15/20 are forbidden until Gate 1 passes for a specific organism/outcome.

## Annotation availability constraint discovered before fitting
The public training ZIP central directories were range-read before modeling. Dense CTC `GT/SEG` masks are not available for the required cohort/time window:
- Drosophila: `GT/SEG` contains sparse single-object exemplars; at frame 24 there is only `01_GT/SEG/man_seg_024_043.tif` and `02_GT/SEG/man_seg_024_108.tif`, with no dense cohort segmentation at 23/25.
- Tribolium: no `GT/SEG` entry exists at frames 23, 24, or 25.

Therefore R8 must not call the dense `GT/TRA/man_trackNNN.tif` volumes segmentation truth. They are used only as **release-native tracking-mask geometry proxies**. This limits biological interpretation of any shape feature, especially in Tribolium where the tracking labels are very small cartographic-projection markers.

## Selective raw-image recovery
The raw entries `01/t023.tif` … `02/t025.tif` are individually ZIP-range-addressable. Compressed entry sizes are about 61–63 MB/frame for Drosophila and 77–85 MB/frame for Tribolium. R8 will retrieve only these 12 raw frames plus the 12 corresponding dense `GT/TRA` tracking-label frames, verify ZIP uncompressed size + CRC, derive features in memory, record SHA-256 provenance, and not download either full 6.22 GB / 22.09 GB archive.

## Added present-only features
### Tracking-mask geometry proxy
At frames 23/24/25:
- covariance eigenvalues/fractions and principal axis ratios;
- bounding-box extents and aspect ratios;
- Drosophila physical-voxel proxy volume, exposed-face surface area, and sphericity using the published voxel calibration;
- Tribolium projected 2D occupied area, 4-neighbor perimeter, and roundness; z is not assigned physical scale;
- recent changes 23→25 and 24→25 for prespecified shape summaries;
- frame-25 within-acquisition percentile ranks;
- frame-25 k=5 neighbor shape mean/dispersion/focal-minus-neighbor context.

### Raw intensity, using only <=25
Within each release-native tracking label:
- mean, variance, q25/median/q75 intensity;
- in-plane gradient magnitude summaries;
- in-plane boundary-vs-adjacent-outside contrast;
- intensity-weighted centroid displacement (polarity magnitude) and absolute principal-axis displacement;
- recent 23→25 and 24→25 changes for prespecified intensity summaries;
- frame-25 within-acquisition percentile ranks and k=5 local neighbor intensity context.

Raw intensities are not treated as calibrated molecular measurements. Cross-acquisition ranks are current-acquisition transforms that use no held-out outcomes.

## Primary representation and descriptive ablation
Primary Gate-1 representation = committed R7 present-only S_R + all prespecified R8 geometry-proxy + intensity features (`S_R8_full`). A geometry-only augmentation (`S_R8_mask`) will be reported as a descriptive ablation but cannot replace the primary gate once raw retrieval is successful.

## Mandatory Gate 1
For a fixed organism/outcome to pass, at least 2 of Ridge, Random Forest, Extra Trees must satisfy **in both reciprocal held-out acquisitions**:
1. held-out R² > 0; and
2. RMSE strictly below the train-fold outcome-mean naive baseline.

Gate 1 is evaluated on `S_R8_full` only. If it fails, R8 stops for that organism/outcome: no frames 15/20 are fetched for new features, no older H fit is run, and no permutation/calibration result is produced.

## Conditional history test
Only if Gate 1 passes for a fixed organism/outcome, append the same four older-history columns already frozen in R7 (`old_speed_relcentroid`, `old_radial_relcentroid`, `old_tangential_relcentroid`, `old_log_volume_change_rate`) and report reciprocal-fold ΔR². Only then may a deterministic within-training-acquisition 200-permutation H null be run. This remains predictive sensitivity, not a mechanistic-memory test.

## Interpretation boundary
A Gate-1 failure means the tested release-native representation still does not transfer adequately across acquisitions for the frozen task. It is **representation/acquisition-transfer failure**, not evidence for biological memory. Even a Gate-1 pass would show only task-specific predictive adequacy of the declared measured state, not complete biological state, Markovian mechanism, or causal memory.
