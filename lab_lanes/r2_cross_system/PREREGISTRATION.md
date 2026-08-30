# R2 preregistration — C. elegans lineage-timing state sufficiency

Frozen before biological model fitting on 2026-08-29.

## Dataset
Cell Tracking Challenge `Fluo-N3DH-CE` training data: developing *C. elegans* embryos, Waterston Lab. Public page links Murray et al. (2008), Nature Methods, DOI 10.1038/nmeth.1228. Only the lineage ground-truth tables are required; microscopy volumes are not downloaded. Two sequences (`01`, `02`) are treated as distinct embryos.

## Predefined task
For each lineage track that ends in an observed binary division before the movie boundary and has sufficient ancestry:
- **Y (future):** current cell-cycle duration in frames, `end - start + 1`.
- **S (candidate present state):** birth/start frame, lineage depth, and embryo indicator. These are coarse state coordinates available at birth and do not use future frames.
- **H (older measured history):** parent cycle duration, grandparent cycle duration, and parent-minus-grandparent duration difference; all are completed before the focal cell is born.

The scientific question is deliberately narrow: does ancestral division timing add stable held-out predictive value for focal division timing after this candidate present state? This is not a test of molecular Markovity or full biological state completion.

## Inclusion/exclusion
- Include focal tracks with exactly two children (observed division), nonzero parent and grandparent, and complete parent/grandparent durations.
- Exclude terminal tracks censored at the movie boundary and non-dividing tracks.
- Never use descendants, focal end frame, child timing, image features measured after birth, or track IDs as predictors.

## Leakage-safe groups and splits
Assign each focal track to its embryo plus its depth-2 ancestor (or earliest available ancestor if shallower). All descendants of that early clade stay in one group. Use repeated GroupShuffleSplit (100 seeds; 25% groups test) and report group overlap checks. A stricter depth-1 grouping sensitivity is also required.

## Estimators
Predefined regressors: standardized Ridge, RandomForestRegressor, and HistGradientBoostingRegressor. Hyperparameters are fixed in code; no test-set tuning. Evaluate S versus S+H on identical splits. Primary metric is held-out R^2; also report MAE.

## Primary history-gain statistic
For each split/estimator, `delta_R2 = R2(S+H) - R2(S)`.

## Falsification / decision rule
Call **stable residual history value** only if all of the following hold:
1. At least two of three estimators have median delta_R2 > +0.02.
2. Those same estimators have positive delta_R2 on at least 80% of valid grouped splits.
3. Their observed median delta_R2 exceeds the estimator-specific 95th percentile of a matched known-complete synthetic control.
4. The corresponding known-incomplete calibration (history term = 0.30 target-SD after S) has >=80% power to exceed the known-complete 95th-percentile cutoff.

If these conditions fail, the result is not evidence of stable residual history value. Failure also does not prove exact conditional independence; it only bounds detectable gain for this task/representation/model/sample.

## Calibration
Construct matched synthetic outcomes on the same rows/groups/features. Known-complete outcomes depend on S plus Gaussian noise. Known-incomplete outcomes use the same S signal/noise plus a standardized parent-duration residual term at 0.30 target-SD. Repeat 200 simulations with the same grouped split seeds and estimator definitions.

## Sensitivities
- depth-1 clade grouping;
- remove embryo indicator from S;
- permutation/leakage sanity checks;
- report sample/group counts and split-level train/test group intersections.
