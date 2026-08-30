# R3 — Higher-dimensional LARRY incompleteness control

This lane tests whether the residual separated-sister fate signal from the prior Weinreb/Klein control survives when the present-state representation uses release-native day-2 expression rather than only a 2D SPRING position.

## State definitions

- **S**: information observed at day 2 only. Baseline `S_2D` is clone-mean SPRING x/y plus starting population. Higher-dimensional `S_expr-k` is clone-mean log1p normalized expression for the first k genes in the frozen panel plus starting population, with k in {4, 8, 16, 32}.
- **H / sister diagnostic**: dominant mature fate in separated day-6 well 1. This is **not** an older measurement and is never described as such. It is lineage-linked future information used only as a known state-incompleteness diagnostic.
- **Y**: dominant mature fate in separated day-6 well 2.

No day-4 or day-6 transcript expression enters S. No clone ID is used as a predictor.

## Leakage controls

Each row is one clone, so every held-out row is automatically a held-out clone. Repeated stratified five-fold splits are therefore clone-disjoint. For expression states, standardization and PCA are inside the sklearn pipeline and fit only on the training folds. The nonlinear and linear estimators use identical fold assignments and state definitions.

## Outputs

- `r3_larry_highdim.py` — acquisition + cohort reconstruction + held-out analysis
- `FEATURE_PANEL_PREDECLARED.txt` — panel frozen before R3 outcome fitting
- `SOURCE_PROVENANCE.md` — release and alignment provenance
- `results/summary.csv` — primary held-out summaries
- `results/cv_fold_metrics.csv` — fold-level results
- `results/permutation_null_expr32.csv` — shuffled-sister known-null calibration
- `results/results.json` — machine-readable checkpoint summary
- `R3_LARRY_HIGHDIM_CHECKPOINT_2026-08-30.md` — interpretation and limits

## Reproduction

From repository root:

```text
python lab_lanes/r3_larry_highdim/r3_larry_highdim.py --data-dir <local-data-dir> --out-dir lab_lanes/r3_larry_highdim/results --repeats 2 --permutations 10
```

The checked-in machine-readable results use two repeats of five-fold clone-held-out CV. The 32-gene shuffled-sister calibration checked in separately uses five permutations because authenticated endpoint/shell runtime limits made larger endpoint-driven reruns unreliable; that small permutation count is treated only as a coarse calibration, not a precise p-value.
