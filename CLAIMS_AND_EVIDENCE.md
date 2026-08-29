# Claims and Evidence Ledger

This file separates observations, computational results, interpretations, and hypotheses. Confidence labels are intentionally conservative.

## Evidence classes

- **Observed-data reanalysis** — derived from previously published biological datasets.
- **Synthetic-model result** — established inside a simulator or constructed hidden-world system.
- **Calibration result** — used to test whether an analysis procedure behaves correctly on known ground truth.
- **Interpretation** — explanatory synthesis consistent with current results but not itself directly measured.
- **Hypothesis** — prospective claim requiring new experiment.

## C1 — Predictive screening-off in flower lineages

**Class:** observed-data reanalysis  
**Status:** supported in the current checkpoint, pending independent reproduction.

Across 24 eligible four-timepoint lineage windows in five WT flowers outside the original discovery flower, the reported median gain from older history after conditioning on a recent measured state was approximately 0.0033 in cross-validated R², and 22/24 windows showed history gain below +0.05.

**Interpretation allowed:** a sufficiently recent *measured* state can make older *measured* history nearly redundant for a specified prediction task.

**Interpretation not allowed:** the plant is proven Markov; all biologically relevant memory has vanished.

## C2 — One dominant molecular direction can complete a task-specific observation stack

**Class:** observed-data reanalysis  
**Status:** supported in one key flower analysis; generalization unknown.

For one reported FM1 analysis, trajectory-only prediction of subsequent growth was around R² 0.272. Adding one unsupervised molecular principal component reportedly raised R² to about 0.643; using all 25 molecular variables yielded about 0.633. Older molecular history then added only about +0.0095 R².

**Interpretation allowed:** once geometry is already observed, one dominant molecular direction may fill much of the remaining predictive gap for this task.

**Interpretation not allowed:** the organism has a one-dimensional state.

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

## Highest-priority falsifiers

The framework should be considered weakened if any of the following occur under rigorous replication:

1. calibrated history gains remain large after rich present-state measurement across multiple biological systems;
2. designed perturbations fail to outperform random/equal-cost perturbations in distinguishing baseline-similar biological backgrounds;
3. connected-fiber structure is unstable to reasonable biological distance metrics or discretization;
4. proposed topological experiment-selection objectives do not improve identification efficiency prospectively;
5. reported flower/seed numerical results fail independent code-level reproduction.

## Publication rule

No public communication should upgrade a claim beyond its class in this ledger without a new tagged release that contains the supporting code, data provenance, and validation report.
