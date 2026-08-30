# R9 Methods — Outcome-Blind Domain Registration

## Frozen inputs
R9 reads the committed R8 full present-state analysis tables without changing cohorts, anchor frame, future frame, outcomes, or estimator hyperparameters. Drosophila uses 139 R8 full-present features; Tribolium uses 99.

## Registration families
### `inductive_invariant_panel`
A column-name rule fixed before R9 evaluation retains ranks, ratios, eigenvalue fractions, normalized quantities, contrasts, density, alignment, polarity/asymmetry, and motion relative to the acquisition centroid. It yields 81 Drosophila and 62 Tribolium features. No new target-domain transform is fit. Some inherited R8 acquisition-relative coordinates are themselves contemporaneous tissue-context measurements, so this track should be understood as a deployable acquisition-relative representation rather than a single-cell-only transform.

### `transductive_domain_percentile`
For every R8 full-present feature, source and target acquisition are independently converted to empirical percentile ranks using S only. No Y is used. This requires the unlabeled target acquisition distribution at deployment and is therefore explicitly transductive.

### Secondary diagnostics
- source-only QuantileTransformer to normal scores;
- source-only StandardScaler + PCA whitening to at most 30 components;
- separate source/target median-IQR standardization using S only;
- Ledoit-Wolf CORAL: regularized source covariance is whitened and recolored to the unlabeled target covariance; target coordinates remain in their measured target space.

## Models and gate
Ridge, Random Forest, and Extra Trees exactly match R8 settings. Each representation is evaluated by reciprocal whole-sequence holdout. A representation passes Gate 1 for an organism/outcome only if at least two estimators have R2 > 0 and RMSE below the train-only mean baseline in both held-out acquisitions.

## Negative control
For each primary representation/model/fold, the fitted model is also evaluated after a deterministic permutation of target-row feature assignments. Target feature marginals remain unchanged while the cell-to-present-state pairing is broken. This control is not part of Gate 1.

## Computational note
The frozen all-at-once command exceeded the shell execution window before producing result files. The same preregistered analysis was then serialized into four organism×outcome jobs and aggregated. No representation, hyperparameter, cohort, outcome, or gate changed after any outcome result was observed.
