# Frozen analysis plan — LARRY cytokine perturbation state-completion stress test

Date frozen: 2026-08-29, before downloading or analyzing the normalized gene-count matrix.

## Source

Weinreb et al., Science 2020, `Lineage tracing on transcriptional landscapes links state to fate during differentiation`.

- PubMed PMID: 31974159
- PMCID: PMC7608074
- GEO: GSE140802
- Klein Lab processed-data repository commit: `b8658b78c1c288019dfa60b6f50aace270528a29`
- Cytokine processed files documented at the Klein Lab public `paper-data` README.

## Why this dataset is adversarial

The paper reports stable fate biases revealed by lineage relationships that are not detectable from single-cell RNA sequencing alone. Therefore the analysis begins from a system in which a current molecular snapshot is already known to be incomplete for some fate questions.

## Experimental unit and interpretation

This is **not** longitudinal measurement of the same single cell. Destructive scRNA-seq samples different sisters from the same genetically barcoded clone at successive times.

The operational state is therefore a **clonal-population state**:

- `H_c`: mean day-2 pre-intervention transcriptome of sampled cells from clone `c`;
- `S_cq`: mean day-4 transcriptome of sampled cells from clone `c` after cytokine condition `q`;
- `Y_cq`: day-6 fate labels of descendants from clone `c` under condition `q`.

The question is: after observing the post-intervention day-4 clone state, does the pre-intervention day-2 clone state still improve prediction of day-6 descendant fate?

## Eligibility

Primary clone-condition units must have:

1. at least one barcoded cell at day 2;
2. at least one barcoded cell at day 4 in condition `q`;
3. at least one barcoded cell at day 6 in the same condition `q`.

Conditions with day-6 data: full cocktail, M-CSF, G-CSF, EPO. SCF is excluded from the primary future test because the released metadata contains no day-6 SCF cells.

All eligible day-6 descendant cells are prediction rows, but **all rows from a clone are assigned to the same CV fold**.

## Outcome

Primary endpoint: multiclass day-6 cell-type annotation.

Classes with very low representation after the eligible-clone filter may be collapsed into `other` using a rule frozen before model fitting: retain a named class only if it has at least 100 eligible day-6 cells and occurs in at least 20 distinct clones; otherwise map it to `other`.

Secondary endpoints:

- macro-averaged log loss / multiclass Brier score;
- macro-F1 / balanced accuracy for interpretability;
- condition-stratified performance, reported descriptively rather than selected post hoc.

## Predictors

### Q0 — intervention only

One-hot cytokine condition. This is the trivial experimental-environment baseline.

### S — current state

One-hot cytokine condition + day-4 clone-average transcriptomic representation.

### S+H — current state plus older state

Same as `S` + day-2 clone-average transcriptomic representation.

No clone barcode/ID is ever used as a predictor.

## Transcriptome preprocessing

- Use the released total-count-normalized sparse matrix.
- Validate matrix orientation against the 65,075-cell metadata before analysis.
- Remove genes expressed in fewer than 1% of eligible day-2/day-4 cells.
- Apply `log1p`.
- Within each training fold only, select the 2,000 genes with highest variance across the clone-average day-2/day-4 training states.
- Standardize selected features using training-fold statistics.
- Reduce day-4 and day-2 transcriptomes separately to at most 30 PCA components each, fitted only on training clones. Component count is `min(30, n_training_clones - 2, n_selected_genes)`.

The same training-derived transforms are applied to test clones.

## Models

Primary estimator: multinomial logistic regression with L2 penalty, fixed `C=1`, maximum iterations 5000.

Nonlinear robustness estimator: HistGradientBoostingClassifier on the PCA representation, fixed hyperparameters (`max_iter=300`, `max_leaf_nodes=15`, `learning_rate=0.05`, random seed 20260829).

Estimator disagreement is classified as **unresolved / model-dependent**, not averaged away.

## Cross-validation

- 5-fold GroupKFold, shuffled with fixed seed 20260829.
- Group = clone ID.
- Stratification by condition is not allowed to split a clone; condition balance will be reported per fold.
- All preprocessing is fitted inside each training fold.

## Primary statistic

For each estimator:

`Delta_history = LogLoss(S) - LogLoss(S+H)`

Positive values mean older day-2 state improves future-fate prediction after conditioning on day-4 state.

Also report `Delta_current = LogLoss(Q0) - LogLoss(S)`.

## Finite-sample calibration

The exact history statistic will be calibrated on the real design matrix/group structure.

### Known-complete null

Within each cytokine condition, permute day-2 history vectors between training clones while leaving day-4 current state and day-6 outcomes intact. This destroys clone-specific history information while preserving marginal history structure. Repeat 100 times using the frozen folds. The 95th percentile of `Delta_history` is the empirical false-positive threshold.

### Known-incomplete positive control

Construct a synthetic target perturbation on top of the observed multiclass outcome probabilities in which a held-out direction of day-2 history residualized against day-4 state changes class logits. Calibrate two effect levels corresponding to mean absolute logit shifts of 0.25 and 0.50. Report detection power versus the known-complete 95th percentile.

This calibration is a sensitivity analysis for the statistic, not a biological model of hematopoiesis.

## Predefined robustness checks

1. restrict to clones with at least 2 day-2 and 2 day-4 cells;
2. condition-specific analyses for G-CSF, EPO and full cocktail if each retains at least 30 eligible clones after class filtering; M-CSF will be reported but not used alone as proof because its fate distribution is strongly monocyte-dominated;
3. compare clone-mean transcriptome with median-PC aggregation if technically feasible without altering outcome labels;
4. repeat with 20 versus 30 PCA components.

These are robustness checks, not alternative primary analyses to choose among after seeing results.

## Falsification logic

- If `S` strongly beats `Q0` but `S+H` still improves beyond the calibrated null in both estimator classes, day-4 transcriptomic state is incomplete for this future/intervention family.
- If `S` strongly beats `Q0` and history does not improve beyond the null **with adequate positive-control power**, the result supports a bounded clonal state-completion claim.
- If estimators disagree qualitatively, label the result model-dependent/unresolved.
- If day-4 state does not beat intervention-only baseline, the released transcriptomic representation is not useful enough for a state-completion claim in this task.

## Claims explicitly forbidden

This analysis cannot prove that hematopoiesis is Markovian, that lineage history is biologically erased, or that a clone-average transcriptome is a universal cell state. It tests only whether the specified older sampled clonal state adds predictive information beyond the specified post-intervention clonal state for day-6 fate under the released cytokine conditions.
