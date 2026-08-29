# Claims and Evidence Ledger

This file separates observations, computational results, interpretations, and hypotheses. Confidence labels are intentionally conservative.

## Evidence classes

- **Observed-data reanalysis** — derived from previously published biological datasets.
- **Synthetic-model result** — established inside a simulator or constructed hidden-world system.
- **Calibration result** — used to test whether an analysis procedure behaves correctly on known ground truth.
- **Interpretation** — explanatory synthesis consistent with current results but not itself directly measured.
- **Hypothesis** — prospective claim requiring new experiment.

## C1 — Predictive screening-off in the Arabidopsis flower atlas

**Class:** observed-data / atlas reanalysis
**Status:** **NARROWED — mixed across developmental windows and compartments; one strong late-L1 case survives.**

A new direct-source replication uses the authors' released FM1 lineage/geometry files and binary expression atlas at commit `95fde8b3b9a0bd09d556ce765a2235093362306f`. The released gene channels are manually mapped atlas annotations assembled from literature, RNA in-situ hybridization, and some live imaging; they are **not** repeated 25-gene measurements made longitudinally in the exact same cells.

Primary grouped-CV results for descendant growth:

- **40→96→120 h pooled cells (n=262):** Ridge current-state R² 0.168; adding older state raises R² to 0.239 (Δ +0.0706). The matched known-complete 95% null was +0.0152. ExtraTrees, however, gives Δ −0.011. Current representation is not demonstrably complete.
- **40→96→120 h L1 (n=100):** primary Δ ≈−0.0017, but matched power for a 0.20-SD direct history effect is only 38% and repeated split sensitivity is unstable. **Inconclusive.**
- **96→120→132 h pooled cells (n=760):** Ridge Δ +0.0132, but the sign/size is split- and estimator-sensitive; ExtraTrees Δ −0.044 and same-layer post-hoc analyses are negative.
- **96→120→132 h L1 (n=256):** Ridge current-state R² 0.599 and ExtraTrees R² 0.630; adding older state changes R² by −0.00035 and −0.0054 respectively. In a matched calibration, the known-complete 95% null was +0.0026 and power for a 0.20-SD direct history effect was 99%. Across 30 alternative lineage-group splits, Ridge history gain was positive only once.

**Interpretation allowed:** for the late FM1 L1 epidermal growth task, the released present atlas state is strongly predictive and older atlas state adds no reproducible value under the tested models. State completion can therefore be a **task-, time-, compartment-, and estimator-relative empirical property**.

**Interpretation not allowed:** flower development generally screens off history; the plant is Markov; all biologically relevant memory has vanished; the atlas channels are direct longitudinal molecular measurements.

**Artifacts:** `REPLICATION_CHECKPOINT_2026-08-29.md`, `analysis/refahi_state_completion_replication.py`, `analysis/refahi_calibrate_history_delta.py`, post-hoc sensitivity scripts, and `results/refahi_*.json`.

**Legacy note:** an earlier checkpoint reported low median history gain across 24 additional flower windows. Those numbers remain a separate legacy result until their exact code/data derivation is migrated and reconciled with this direct-source audit.

## C2 — One dominant molecular direction can complete a task-specific observation stack

**Class:** observed-data reanalysis  
**Status:** legacy reported analysis; not independently reproduced by the new direct-source FM1 audit.

For one earlier reported FM1-derived analysis, trajectory-only prediction of subsequent growth was around R² 0.272. Adding one unsupervised molecular principal component reportedly raised R² to about 0.643; using all 25 molecular variables yielded about 0.633. Older molecular history then added only about +0.0095 R².

**Interpretation allowed:** once geometry is already observed, one dominant molecular direction may fill much of the remaining predictive gap for this task.

**Interpretation not allowed:** the organism has a one-dimensional state.


**Current caution:** this result should not be described as a directly measured one-dimensional molecular state. The released FM1 gene channels are atlas-mapped binary expression domains, and the exact legacy PCA pipeline still requires artifact migration.

## C3 — Fixed history-gain thresholds can falsely imply memory

**Class:** calibration result  
**Status:** strong computational falsification of an earlier criterion.

A known-Markov ABA–GA simulator nevertheless produced a finite-sample boosted-tree history gain of roughly +0.0299 R². Therefore a rule such as “history gain above +0.02 proves non-Markov memory” is invalid.

**Consequence:** future screening-off claims must be calibrated against estimator bias, sample size, dimensionality, and known generative controls.

## C4 — Germination percentages should be modeled as finite binomial observations

**Class:** observed-data reanalysis / statistical correction  
**Status:** methodologically well motivated; downstream numerical claims require repository migration.

Reported germination assays used about 75 seeds. Treating 0% or 100% as zero-noise continuous measurements creates pathological information geometry. The corrected model uses finite binomial counts with a logistic latent factor structure, so boundary observations contribute finite evidence.

## C5 — Baseline morphology can collapse distinct hidden developmental worlds

**Class:** synthetic-model result  
**Status:** demonstrated in a constructed 224-world system (14 architectures × 16 hidden states).

The archived simulator study contains hidden worlds that are visually or numerically indistinguishable at baseline but diverge under intervention. This is the core proof-of-principle for **counterfactual developmental tomography**.

**Interpretation allowed:** perturbations can identify distinctions that static morphology cannot in the model.

**Interpretation not allowed:** the same discrimination performance has been demonstrated prospectively in living plants.

## C6 — Connected causal fibers can contain cryptic mechanism islands

**Class:** synthetic-model / topological analysis  
**Status:** supported on a sampled finite state-law complex; continuum theorem not established.

For a phenotype tolerance around δ = 0.00155, the sampled target connected component reportedly contained about 2030 candidate mechanisms spanning four hidden states. A dominant alternative mechanism island appeared at lower phenotype error but remained disconnected until a higher tolerance saddle was crossed.

This motivates two separate quantities:

- **accommodation**: how well an alternative mechanism can imitate the target;
- **merge/access threshold**: how much phenotype deviation is needed before a continuous path from the target reaches it.

Their difference measures sampled topological isolation under the chosen phenotype metric.

## C7 — Experimental value is objective-dependent

**Class:** synthetic-model result  
**Status:** supported in the sampled ambiguity landscape.

At one ambiguity scale, intervention 0010 reportedly reduced the connected candidate set from 2030 to 114, while a previously strong global parameter-estimation assay (1011) ranked only 12th for this topological objective. At a broader tolerance the best intervention changed to 1010.

**Interpretation:** “most informative experiment” is not universal. The optimal assay depends on the scientific loss function and the structure of the current ambiguity.

**New correction (2026-08-29):** connected-component reduction is not generally submodular. A grid counterexample from the mathematics lane makes a greedy topological selection rule arbitrarily worse than the optimal size-k subset. Therefore greedy selection is a heuristic unless additional structure is established; exhaustive subset benchmarking is mandatory for tractable assay libraries.

## C8 — Developmental state completion

**Class:** hypothesis / framework  
**Status:** proposed biological/computational application; the underlying predictive-sufficiency mathematics is established.

**Novelty correction (2026-08-29):** grouping histories by identical future distributions is strongly precedented by causal states; action/intervention-conditioned predictive representations are strongly precedented by predictive-state representations (PSRs) and input-output computational mechanics. We therefore do **not** claim that screening off older history or representing state by counterfactual future predictions is mathematically new.

A candidate present state S should satisfy, for preregistered future interventions π:

1. an intervention can move S;
2. S predicts Yπ;
3. older history and treatment assignment add little predictive information once S is known, within calibrated uncertainty.

If a newly introduced future intervention restores predictive value to old history, the current state representation is incomplete. The next experiment should target the newly exposed missing direction.


## C9 — Experiment-panel refinement under a sup/monotone metric

**Class:** mathematical structural result  
**Status:** provisional proof recorded; formal independent check pending.

Under the current definition

`K_Q^delta(w*) = {w : max_{q in Q} d(h_q(w), h_q(w*)) <= delta}`,

if `Q subset Q'` then `K_Q'^delta subset K_Q^delta`, and the target connected components inherit the same inclusion. This is the exact sense in which adding experimental coordinates refines ambiguity.

**Restriction:** the result depends on keeping a coordinatewise monotone/product metric. It should not be stated for arbitrary renormalized distances.

## C10 — Fixed-tolerance topology is not robust; a tolerance sandwich is

**Class:** mathematical robustness result  
**Status:** provisional proof recorded; formal independent check pending.

If counterfactual signatures have uniform world-wise error at most `epsilon`, target-relative sup distances can shift by at most `2 epsilon`. The corresponding target components are bounded between lower- and higher-tolerance components.

**Interpretation:** report critical-tolerance intervals and persistence/merge thresholds; do not present one fixed `delta` component as intrinsically stable.

## C11 — Greedy connected-ambiguity splitting has no general approximation guarantee

**Class:** mathematical counterexample / negative result  
**Status:** **REPRODUCED COMPUTATIONALLY**. The construction is recorded in `MATH_CHECKPOINT_2026-08-29.md` and independently implemented in `analysis/greedy_component_counterexample.py`. The generated CSV verifies the predicted ratio `3/n` through `n=160`.

A complementary-wall grid construction makes the marginal value of an experiment increase dramatically after another experiment, violating submodularity. Adding a decoy experiment causes the budget-two greedy/optimal utility ratio to scale like `O(1/n)` and approach zero.

**Consequence:** no claim of near-optimal greedy topological experiment design without additional assumptions such as submodularity/adaptive submodularity or direct optimal-subset comparison.


## C12 — Finite-sample screening-off statistics require calibrated null and power controls

**Class:** statistical calibration / negative-control result  
**Status:** **REPRODUCED COMPUTATIONALLY**.

The project independently reconstructed a known first-order Markov binary process and a deliberately history-dependent alternative, then estimated plug-in conditional mutual information `I(Y;H | S,A)` over 1,000 Monte Carlo trajectories per sample size.

| N | Markov mean CMI | empirical 95% Markov cutoff | history-dependent mean CMI | power |
|---:|---:|---:|---:|---:|
| 250 | 0.01238 | 0.02877 | 0.01988 | 0.203 |
| 500 | 0.00577 | 0.01356 | 0.01456 | 0.475 |
| 1,000 | 0.00306 | 0.00738 | 0.01168 | 0.778 |
| 2,000 | 0.00145 | 0.00343 | 0.01035 | 0.989 |

**Interpretation:** a truly Markov process can yield positive estimated residual-history information at finite `N`, while a genuine history effect may have weak detection power in small samples. Therefore “history did not improve prediction” is not evidence of state completion unless the chosen statistic/model is calibrated against both known-complete and known-history-dependent controls at comparable sample size/noise.

**Artifacts:** `analysis/state_completion_cmi_calibration.py` and `analysis/state_completion_cmi_calibration_results.csv`.


## C9 — Independent reconstruction from the authors' released FM1 atlas

**Class:** observed-data reanalysis / independent repository reconstruction  
**Status:** reproduced from the original public code/data release at upstream commit `95fde8b`.

Using 760 eligible 120h cells grouped into 233 distinct 96h ancestor lineages, current geometry alone produced nested grouped out-of-fold R² = 0.0333 for 120→132h lineage log-volume expansion. Adding the released 25-gene 120h state raised R² to 0.2846. Adding the corresponding 96h ancestor geometry + 25-gene state raised R² only slightly further to 0.2928 (ΔR² history|current = +0.0082). A random-forest sensitivity analysis gave 0.3002 → 0.3524 → 0.3304.

A fixed-Ridge calibration produced biological ΔR² history|current = +0.0056 with a 5,000-group-bootstrap 95% interval of approximately [-0.039, +0.054]. A known-non-Markov synthetic control with a moderate residual history term was detected with 97.6% power above the known-Markov 95th percentile.

**Interpretation allowed:** the released FM1 data independently support substantial future-growth information in the current molecular state beyond current geometry, while residual predictive value from the measured 96h ancestor state is small relative to that current-state gain and not robustly resolved.

**Interpretation not allowed:** exact conditional independence; proof of Markov closure; universal state sufficiency.

See `REPLICATION_CHECKPOINT_FM1_2026-08-29.md`.

## Highest-priority falsifiers

The framework should be considered weakened if any of the following occur under rigorous replication:

1. calibrated history gains remain large after rich present-state measurement across multiple biological systems;
2. designed perturbations fail to outperform random/equal-cost perturbations in distinguishing baseline-similar biological backgrounds;
3. connected-fiber structure is unstable to reasonable biological distance metrics or discretization;
4. proposed topological experiment-selection objectives do not improve identification efficiency prospectively;
5. reported flower/seed numerical results fail independent code-level reproduction.

## Publication rule

No public communication should upgrade a claim beyond its class in this ledger without a new tagged release that contains the supporting code, data provenance, and validation report.
