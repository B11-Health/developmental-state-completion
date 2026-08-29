# Replication checkpoint — Refahi Arabidopsis flower atlas

Date: 2026-08-29  
Status: **exploratory observed-data reanalysis; not prospective; not peer reviewed**

## Why this checkpoint exists

We returned to the primary Arabidopsis flower-atlas publication and ran a new state-completion diagnostic directly from the authors' released code/data representation rather than relying on earlier derived summaries.

Primary source:

- Refahi et al., *Developmental Cell* (2021), “A multiscale analysis of early flower development in Arabidopsis provides an integrated view of molecular regulation and growth control.”
- Data DOI: `10.17863/CAM.61991`
- Authors' GitLab repository: `slcu/teamHJ/publications/refahi_etal_2020`
- Source commit used here: `95fde8b3b9a0bd09d556ce765a2235093362306f`

## Critical measurement caveat

The flower geometry and lineages in FM1 are time-lapse measurements, but the 25 released gene-expression channels used here are **binary atlas annotations**. The paper states that expression information from published work, RNA in-situ hybridization, and some live imaging was manually mapped onto individual cells of the FM1 reference series in MorphoNet at five developmental stages.

Therefore this analysis does **not** constitute repeated 25-gene molecular measurement of the exact same living cells through time. The appropriate language is “atlas-derived current expression state,” not “longitudinal molecular state.”

## Frozen primary analysis

Before the first successful run, the analysis was frozen as follows:

- windows: 40→96→120 h and 96→120→132 h;
- future target: `log(total descendant volume at future / current cell volume)`;
- M0: current geometry — log volume and 3-D center;
- M1: M0 + current 25-channel binary atlas expression state;
- M2: M1 + older geometry + older 25-channel atlas state;
- 5-fold grouped CV, with groups defined by the older ancestor cell so descendants cannot split across train/test folds;
- primary estimator: Ridge (`alpha=10`);
- primary finite-sample placebo: 100 permutations shuffling complete older-state vectors between lineage groups;
- nonlinear robustness estimator: ExtraTrees with fixed hyperparameters;
- analyses repeated for all eligible cells and the released L1 epidermal subset.

The initial monolithic execution exceeded the shell runtime before producing any results. It was then split into one case per process; model specification, folds, features and null remained unchanged.

## Primary results

| Window | Subset | n / lineage groups | Current R² Ridge | +History R² Ridge | ΔR² history | ExtraTrees ΔR² history | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| 40→96→120 | all | 262 / 84 | 0.168 | 0.239 | **+0.071** | −0.011 | pooled linear representation is incomplete; nonlinear result conflicts |
| 40→96→120 | L1 | 100 / 30 | 0.062 | 0.061 | −0.0017 | −0.021 | low predictive power; cannot establish completion |
| 96→120→132 | all | 760 / 233 | 0.269 | 0.282 | **+0.013** | −0.044 | small estimator-/mixture-sensitive residual history |
| 96→120→132 | L1 | 256 / 86 | **0.599** | **0.599** | **−0.00035** | −0.0054 | strongest state-completion-like case |

For late L1, ExtraTrees current-state R² is 0.630 and falls slightly to 0.624 after history is added.

## Matched known-complete / known-incomplete calibration

The exact Ridge ΔR² statistic was calibrated using the real current/history feature correlation and lineage-group structure.

**Known-complete/null generator:** future outcome is generated from current-state features plus independent noise; older features remain correlated with current state but have no direct effect.

**Known-incomplete generator:** adds a direct history direction residualized against current features with amplitude 0.20 target standard deviations.

| Window | Subset | Real ΔR² | 95% known-complete null | Power for 0.20-SD history effect |
|---|---|---:|---:|---:|
| 40→96→120 | all | +0.0706 | +0.0152 | 0.75 |
| 40→96→120 | L1 | −0.0017 | +0.0132 | **0.38** |
| 96→120→132 | all | +0.0132 | −0.0023 | 1.00 |
| 96→120→132 | L1 | −0.00035 | +0.0026 | **0.99** |

The late-L1 null result is therefore qualitatively different from the early-L1 null result. In late L1, this diagnostic had high simulated power for the prespecified 0.20-SD history effect yet observed essentially no gain. Early L1 is underpowered and is classified as **inconclusive**, not complete.

## Repeated lineage-split sensitivity

Thirty alternative shuffled GroupKFold partitions were run post hoc with Ridge.

- **40→96→120 all:** mean ΔR² +0.0506; 30/30 positive; 5–95% range +0.0195 to +0.0748.
- **40→96→120 L1:** unstable; mean +0.1365, range −0.061 to +0.307; current prediction itself is weak. This reinforces the **inconclusive** label.
- **96→120→132 all:** mean +0.0071, range −0.043 to +0.032; only 70% positive. The pooled late effect is not split-stable.
- **96→120→132 L1:** mean −0.0154; history positive in only 1/30 splits; 5–95% range −0.0337 to −0.00335. This strengthens the late-L1 result.

## Post-hoc layer localization

To understand pooled-cell heterogeneity, we required both the current cell and its older ancestor to remain within the same released layer category.

### Late window 96→120→132

History **reduced** predictive R² in every same-layer subset tested:

- L1: Ridge ≈0; ExtraTrees −0.005;
- L2: Ridge −0.026; ExtraTrees −0.049;
- deeper/other: Ridge −0.061; ExtraTrees −0.028.

Thus the small positive pooled Ridge history term is not reproduced inside stable layer strata.

### Early window 40→96→120

- L2 showed modest positive history gain: Ridge +0.040, ExtraTrees +0.021.
- deeper/other did not show a consistent positive signal.
- L1 is too unstable/weakly predicted to classify.

This suggests that the useful state representation itself changes with developmental stage and compartment.

## Post-hoc model/encoding checks

1. **Ridge penalty:** pooled positive history gains persist across `alpha=0.1…1000`, so they are not a single regularization accident.
2. **Nonlinear ExtraTrees:** history never improves the two primary L1 cases and decreases late pooled performance, showing estimator dependence.
3. **Combinatorial cell-state encoding:** replacing 25 additive binary genes with a categorical one-hot expression pattern does not produce a universal answer. History remains positive in pooled Ridge and small/negative or unstable in L1.
4. **Current layer identity:** adding L1/L2/other indicators improves early pooled current-state R² but does not fully eliminate the Ridge history term.

## Falsification / correction

### Rejected broad statement

> “A recent present state generally screens off older history across early Arabidopsis flower development.”

The released atlas does **not** support this as a universal statement. Screening-off depends on developmental window, tissue compartment, estimator, and state encoding.

### Strongest surviving observed-data statement

> In the late FM1 L1 epidermal window (120 h current state predicting 132 h descendant growth), current geometry plus the released atlas expression state predicts future growth well (R² ≈0.60–0.63), and older 96 h atlas state adds no reproducible predictive value under the tested Ridge and ExtraTrees models. A matched synthetic calibration had 99% power to detect a direct history effect of 0.20 target SD.

Even this statement is **task-specific and atlas-specific**. It does not establish a universal state variable or biological Markovity.

## Scientific interpretation

The result is more interesting after narrowing:

1. **State completion can be local.** A measurement may be sufficient for one tissue layer, developmental window and future target while remaining incomplete elsewhere.
2. **Residual history can diagnose a missing state representation rather than intrinsic non-Markov biology.** Pooled cells and early L2 retain history signal, while later same-layer strata do not.
3. **Estimator dependence is itself a falsification gate.** A history effect that exists only under one restricted predictor should not be promoted to biological memory without testing richer current-state models.
4. **The next biological test must be prospective.** The atlas annotation is an invaluable benchmark, but the decisive experiment requires real current-state reporters/measurements and a frozen future/intervention protocol in living plants.

## What this changes in the larger framework

The framework should no longer seek one universal “completed developmental state.” The operational object is indexed by at least:

- biological compartment / measurement interface;
- developmental time;
- future prediction/intervention family;
- measurement resolution;
- estimator class and finite-sample calibration.

A more honest notation is therefore something like `S*(I, t, Π, Y, ε)`: a minimal or near-minimal measured present state relative to an experimental interface `I`, developmental time `t`, allowed future intervention family `Π`, target `Y`, and tolerated predictive error `ε`.

## Files

Primary analysis:

- `analysis/refahi_state_completion_replication.py`

Finite-sample calibration:

- `analysis/refahi_calibrate_history_delta.py`

Post-hoc diagnostics:

- `analysis/refahi_posthoc_layer_sensitivity.py`
- `analysis/refahi_posthoc_layer_subsets.py`
- `analysis/refahi_posthoc_ridge_sensitivity.py`
- `analysis/refahi_posthoc_combinatorial_state.py`
- `analysis/refahi_posthoc_split_sensitivity.py`

Machine-readable outputs are in `results/`.

## Next acceptance tests

1. Repeat the late-L1 analysis on an independent flower with directly measured reporter state rather than manually mapped multi-source atlas annotation.
2. Predefine a richer current-state model class before looking at history gain.
3. Calibrate all completion statistics at the actual biological sample size and group structure.
4. Prospectively perturb an RCOg-V suppressor system and ask whether a frozen response state improves prediction beyond every baseline current-state channel.
5. Treat any reappearance of history after a new intervention as evidence that the state representation is incomplete for the enlarged future family—not as a failure of the entire framework.
