# R9 Preregistration — Acquisition/Developmental Registration Rescue

Date: 2026-08-30
Status: FROZEN BEFORE R9 OUTCOME EVALUATION

## Question
R8 expanded the present-only representation to 139 features in Drosophila and 99 in Tribolium but failed reciprocal cross-acquisition absolute adequacy. R9 tests a narrower explanation: can outcome-blind registration/harmonization of the same present measurements rescue transfer without changing the biological task?

## Frozen task inherited from R8
- Organisms: Drosophila and Tribolium Cell Tracking Challenge datasets already recovered in R5-R8.
- Cohorts: exactly the R8 focal cohorts (392 Drosophila; 287 Tribolium).
- Present anchor: frame 25.
- Present data: exactly the R8 full present feature tables derived only from frames <=25.
- Future horizon: frame 40.
- Outcomes: `future_radial_velocity` and `future_speed` only.
- Outer split: reciprocal whole-acquisition holdout, sequence 01 versus sequence 02.
- Estimators: Ridge(alpha=1), RandomForest(300 trees, min_samples_leaf=4, max_features=.8), ExtraTrees(300 trees, min_samples_leaf=3, max_features=.9), same seed 20260830.
- Baseline: train-only outcome mean.
- No older H fitting unless Gate 1 passes.

## Frozen Gate 1
For one organism/outcome/registration representation to pass, at least two of the three prespecified estimators must, in BOTH reciprocal held-out acquisitions:
1. have held-out R2 > 0; and
2. have RMSE lower than the train-only mean baseline.

A one-fold success does not pass. No horizon/outcome/cohort/model hyperparameter may be changed after R9 results are seen.

## Registration tracks
### Primary inductive track: `inductive_invariant_panel`
No target-distribution adaptation. Select a semantics-defined acquisition-robust subset from the existing R8 full columns using a frozen name rule: retain present features encoding ranks, ratios, eigenvalue fractions, normalized quantities, contrasts, density, alignment, polarity/asymmetry, or motion relative to the acquisition centroid. Raw absolute intensity/size channels that do not meet this rule are excluded. The selection uses column names only, never Y.

This track is the primary deployable test because the target acquisition need not be available in advance except for the focal sample itself.

### Primary transductive track: `transductive_domain_percentile`
Use the same R8 full columns. Independently within source and unlabeled target acquisition, replace every feature by its empirical percentile rank in that acquisition. Y is never used. This explicitly assumes the unlabeled target acquisition distribution is available at deployment and must not be described as an inductive result.

### Secondary diagnostic tracks
1. `inductive_source_quantile`: fit a QuantileTransformer on source-train S only and apply it to source/test.
2. `inductive_source_pca30`: source-train StandardScaler + PCA whitening, up to 30 components, then apply to target.
3. `transductive_robust_z`: center/scale source and target separately using each domain's S-only median/IQR.
4. `transductive_coral`: regularized covariance alignment using source and unlabeled target S only; transform source into target first/second-moment space, target unchanged.

Secondary success without a primary-track success is diagnostic/exploratory and does not by itself promote a general registration rescue claim.

## Negative control
For each primary track/model/fold, after fitting normally, deterministically permute target-row feature assignments before prediction with a fixed seed. This preserves target feature marginals but breaks cell-to-present-state pairing. It is not part of Gate 1; it checks that any apparent prediction requires the correct present state rather than only target-domain marginals.

## Decision logic
1. Run all frozen S-only transforms once.
2. Evaluate the same frozen Gate 1 per representation.
3. If a primary track passes, report the exact deployment assumption (inductive or transductive) and only then permit later H/calibration work in a separate stage.
4. If only a secondary diagnostic passes, label it exploratory and do not fit H in R9.
5. If no primary track passes, stop before H/calibration/permutation-history inference and report unresolved domain-transfer/registration failure, not biological memory.

## Claim boundary
R9 cannot establish acquisition shift as the sole cause of R8 failure. A failed registration rescue leaves developmental registration, tissue identity, lineage context, missing molecular state, label geometry limits, and other representation mismatch live. A successful transductive rescue would be conditional on access to unlabeled target-domain S and would not establish organism-wide state sufficiency.
