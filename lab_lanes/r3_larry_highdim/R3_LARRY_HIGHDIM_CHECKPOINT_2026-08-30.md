# R3 checkpoint — higher-dimensional LARRY incompleteness control

Date: 2026-08-30
Branch: `lab-r3-larry-highdim-2026-08-29`
Base: `origin/main` at `f06ac51`

## Question

The existing public Weinreb/Klein control conditioned on a reduced day-2 state proxy: clone-mean SPRING x/y plus starting population. R3 asks whether the residual lineage-linked sister signal remains when S uses release-native day-2 expression features rather than only the 2D visualization.

## H / S / Y definitions

- **S** is day-2 information only. `spring2d` uses mean day-2 SPRING x/y and starting population. `expr4`, `expr8`, `expr16`, and `expr32` use progressively larger prefixes of a gene panel frozen before outcome fitting, plus starting population. Expression values come from the authors' release-native normalized-expression backend; R3 applies `log1p`, then clone-averages the sampled day-2 sisters.
- **H** in this control is the dominant mature fate observed in separated day-6 sister well 1. This is deliberately labeled a **sister-lineage incompleteness diagnostic**, not literal historical state.
- **Y** is the dominant mature fate in separated day-6 well 2.

No day-4 or day-6 expression enters S. No clone ID is a predictor.

## Cohort

The strict release-native three-fate cohort remains 133 unique clones (197 sampled day-2 cells):

- Y Neutrophil: 57
- Y Monocyte: 44
- Y Baso: 32
- separated-sister dominant-fate agreement: 0.8346

Because there is exactly one modeling row per clone, all held-out rows are clone-disjoint by construction. Repeated stratified five-fold CV is therefore group-safe at the clone level.

## Preprocessing

For expression states, scaling and PCA are inside the modeling pipeline and are fit on training folds only. Up to eight PCA components are used. Starting population and, in the S+H model, sister fate are one-hot encoded inside the same training-only pipeline. Two estimators are reported: balanced multinomial logistic regression and balanced histogram gradient boosting.

## Held-out results

Primary statistic is `log loss(S) - log loss(S+H)`: positive values mean the separated-sister fate still improves future-well prediction after conditioning on measured day-2 state. Checked-in values are means over 10 held-out folds (2 repeats x 5 folds).

| S representation | Estimator | S log loss | S+H log loss | sister log-loss gain | S bal. acc. | S+H bal. acc. |
|---|---|---:|---:|---:|---:|---:|
| SPRING 2D | logistic | 0.927 | 0.555 | **+0.372** | 0.619 | 0.832 |
| SPRING 2D | histGB | 0.934 | 0.689 | **+0.245** | 0.621 | 0.825 |
| expr4 | logistic | 1.013 | 0.532 | **+0.481** | 0.478 | 0.848 |
| expr4 | histGB | 1.059 | 0.608 | **+0.451** | 0.504 | 0.819 |
| expr8 | logistic | 1.074 | 0.599 | **+0.475** | 0.421 | 0.807 |
| expr8 | histGB | 1.317 | 0.711 | **+0.606** | 0.380 | 0.795 |
| expr16 | logistic | 0.911 | 0.614 | **+0.298** | 0.596 | 0.801 |
| expr16 | histGB | 1.130 | 0.725 | **+0.405** | 0.549 | 0.764 |
| expr32 | logistic | 0.917 | 0.589 | **+0.328** | 0.563 | 0.812 |
| expr32 | histGB | 1.232 | 0.708 | **+0.523** | 0.528 | 0.775 |

### Result

The residual sister-lineage signal **survives every tested day-2 expression-panel size and both estimators**. On the richest tested 32-gene state, adding sister fate reduces held-out log loss by about 0.328 for logistic regression and 0.523 for histogram gradient boosting.

This does **not** mean the 32-gene state is globally more informative than SPRING. SPRING 2D was constructed from a much broader transcriptome, and in these small-sample fits the expression-panel-only S is not uniformly better than the SPRING baseline. The supported claim is narrower: replacing the two plotted coordinates with direct higher-dimensional measured expression does not make the residual sister signal vanish.

## Known-null / permutation control

For `expr32`, sister-fate labels were shuffled across clones while S and Y were held fixed. Across the checked-in five permutation replicates:

- logistic null gain mean: -0.0356; maximum: -0.0047
- histGB null gain mean: -0.0264; maximum: +0.0462

Both observed expr32 gains (+0.328 and +0.523) are far outside these small null samples. With only five permutations, however, the empirical p-value floor is 1/6 = 0.167. R3 therefore treats this as a **directional known-null calibration**, not precision significance testing. Larger permutation runs are a straightforward follow-up when endpoint/runtime constraints permit.

## What changed relative to the prior control

The previous caveat that S consisted only of 2D SPRING coordinates is materially narrowed. R3 now demonstrates the same failure of screening-off when S contains direct release-native day-2 expression measurements. The caveat is not eliminated completely because R3 used a fixed 32-gene panel rather than the full 25,289-gene matrix.

## What R3 does not claim

1. It does not claim full-transcriptome state is insufficient; the full 25,289-gene matrix was not analyzed here.
2. It does not claim an author-released high-dimensional PCA representation; no such artifact was found in the public `paper-data` release path used here.
3. It does not treat sister-well fate as literal older history. It is future lineage-linked information used as an established incompleteness diagnostic.
4. It does not claim the expression panel is superior to SPRING on raw predictive accuracy.
5. It does not reproduce the paper's exact figure-specific cohorts or numbers.
6. It does not transfer this hidden-state mechanism to plants or imply universal non-Markovity.

## Bottom line

R3 strengthens the Weinreb/Klein positive control: the project diagnostic still detects residual lineage-linked future information after conditioning on a direct, higher-dimensional day-2 expression state. The result is estimator-robust across the tested linear/nonlinear models and is absent under shuffled-sister controls. The remaining major caveat is transcriptome coverage, not the original 2D-only representation.

Machine-readable results: `results/results.json`, `results/summary.csv`, `results/cv_fold_metrics.csv`, `results/permutation_null_expr32.csv`.
