# R15 SLICE-1 Multi-Embryo Preview Pilot Preregistration

Date: 2026-08-30
Status: FROZEN BEFORE DS0007/DS0035 PREVIEW DOWNLOAD OR VALIDATION ANALYSIS

## Scientific purpose
Test whether a compact current whole-embryo image geometry state can predict a future image geometry state across independent Tribolium embryos in the 2025 SLICE-1 collection, and only if absolute cross-embryo adequacy succeeds ask whether a substantially older image state adds stable predictive value. This is an image-level developmental-state pilot, not a cell-lineage or mechanistic-memory test.

## Data partition fixed before validation
- Development-only: DS0004 and DS0005, both Cytok8 nanobody subline #2. They were used only to verify preview format and freeze the representation. They can never count as validation wins.
- Primary unseen validation: DS0007, Cytok8 nanobody subline #3.
- Secondary domain stress test: DS0035, Lamin nanobody subline #4.
- No additional SLICE-1 preview will be selected based on R15 results. Scaling beyond this pilot requires a separate preregistration over a larger fixed subset or the full collection.

## Preview representation
Use the released full-quality preview multipage TIFF (`Movie-FQ.TIF`). Each time point is split into four equal-width acquisition-view panels. For each panel, subtract the 5th-percentile background, cap at the 99.5th-percentile signal, and compute normalized intensity-weighted geometry.

The frozen present/future state vector contains only the eight across-view means:
1. `mean_cx` normalized x centroid;
2. `mean_cy` normalized y centroid;
3. `mean_sx` normalized x spread;
4. `mean_sy` normalized y spread;
5. `mean_covxy` normalized xy covariance;
6. `mean_entropy` coarse 8x8 spatial entropy;
7. `mean_occupancy` normalized signal occupancy;
8. `mean_edge` normalized edge energy.

Across-view standard-deviation features are excluded from validation because the development embryos showed substantially weaker same-subline reproducibility; this choice is frozen before validation data are downloaded.

## H / S / Y construction
All available pilot datasets have 49 time points at 30-minute intervals over 24 hours. Use nine non-overlapping-center windows with present indices
`T = {9,13,17,21,25,29,33,37,41}`.

For each present index t:
- H = eight-feature image state at t-8 (4 hours older);
- S = eight-feature image state at t;
- Y = eight-feature image state at t+8 (4 hours future).

This produces nine rows per embryo. Windows overlap in raw time, so embryo—not row—is the unit of external validation.

## Models and preprocessing
Fit Ridge, Random Forest, and Extra Trees multi-output regressors. Standardize each S/H/Y coordinate using training embryos only. Hyperparameters must be fixed in code before DS0007/DS0035 outcomes are scored. Do not tune on validation embryos.

## Vector adequacy score
For held-out embryo e, define vector SSE by summing squared error over all nine windows and eight standardized Y coordinates. The train-only naive predictor is the training-embryo mean Y vector. Define
`R2_vector = 1 - SSE_model/SSE_naive`.
Also report vector RMSE.

Gate 1 passes an embryo for an estimator only if `R2_vector > 0` and model RMSE is below the train-only naive RMSE. Primary adequacy requires at least two of the three estimators to pass on DS0007. DS0035 is reported separately as a marker-domain stress test and cannot rescue a failed DS0007 primary gate.

## History rule
Only if primary Gate 1 passes, refit S+H with the identical training/validation split and model settings. For each estimator report `Delta R2_vector = R2_vector(S+H)-R2_vector(S)`. No biological-history interpretation is allowed in this two-embryo-training/one-embryo-validation pilot; the result is only a direction for a larger SLICE-1 preregistration.

## Stop rules
- If DS0007 primary Gate 1 fails, stop history interpretation and classify current image state as cross-embryo inadequate at this representation/horizon.
- Do not change horizon, feature set, panel split, model family, or validation embryo after seeing results.
- Do not substitute DS0035 for DS0007 if DS0007 fails.
- No claim of Markovity, non-Markovity, molecular memory, causality, or universal state sufficiency is allowed.
