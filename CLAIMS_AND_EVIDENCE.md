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

Current direct-source results for descendant growth:

- **40→96→120 h pooled cells (n=262):** history gain is estimator-dependent. In the current nested stage sweep, Ridge adds about +0.021 R² while random forest loses about 0.039. No broad completion or memory claim is allowed.
- **40→96→120 h L1 (n=100 / 30 ancestor groups):** the linear history effect is strongly split-sensitive but usually positive. Across 200 shuffled group partitions with fixed Ridge, median ΔR² is **+0.144**, positive in 90.5% of partitions, with 2.5th–97.5th split quantiles [-0.051,+0.251]. A 15-partition ExtraTrees sensitivity run has median near zero and no partition above +0.05. **Estimator-dependent / unresolved.**
- **96→120→132 h pooled cells (n=760 / 233 groups):** current atlas state adds substantial predictive value beyond geometry, while the extra older-history block remains small and model-sensitive.
- **96→120→132 h L1 (n=256 / 86 groups):** across 200 shuffled group partitions with fixed Ridge, median history ΔR² is **-0.015**, positive in only 4% and never above +0.05. Across 100 shuffled partitions, fixed-Ridge Gaussian history value has median **-0.035 bits/cell**, positive in only 3%. Calibration has about 73% power for one 0.20-target-SD residual-history construction and about 98% around 0.30 SD, so subtle residual effects remain unresolved.

**Interpretation allowed:** for the late FM1 L1 epidermal growth task, the released present atlas state is strongly predictive and older released history has no stable material gain under the tested repeated-partition linear analyses and nonlinear sensitivities. State sufficiency is therefore a **task-, time-, compartment-, loss-, decoder-, and finite-sample-relative empirical property**.

**Interpretation not allowed:** exact conditional independence; flower development generally screens off history; the plant is Markov; all biologically relevant memory has vanished; the atlas channels are direct longitudinal molecular measurements.

**Primary artifacts:** `REPLICATION_CHECKPOINT_FM1_2026-08-29.md`, `STAGE_DEPENDENCE_CHECKPOINT_FM1_2026-08-29.md`, `MATHEMATICAL_NOTE_PREDICTIVE_SCREENING_OFF.md`, `analysis/refahi_fm1_state_completion.py`, `analysis/fm1_gaussian_logscore.py`, and `analysis/fm1_split_stability.py`. The older `REPLICATION_CHECKPOINT_2026-08-29.md` is retained as a superseded single-split provenance record.

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

The original coarse state-law grid suggested a STRETCH-related merge barrier near `0.001543`, but a later seam-consistent source-level search **rejected that value as a discretization obstruction**. In the latest recovered simulator checkpoint, the optimized static accommodation is source dIoU `a_S ≈ 0.0002686301`. The corrected CFLOW escape boundary is near `F=0, N=1, C+S=0.8`; a cubic surrogate gives `≈0.001410471`, direct source execution gives `≈0.001410939`, and an independent nearby source sweep gives `≈0.001412041`. Thus the current source-validated estimate is `m_S ≈ 0.00141094`, with isolation gap `Δ_S ≈ 0.00114231` and ratio `m_S/a_S ≈ 5.25`.

This motivates two separate quantities:

- **accommodation**: how well an alternative mechanism can imitate the target;
- **merge/access threshold**: how much phenotype deviation is needed before a continuous path from the target reaches it.

**Evidence boundary:** these values come from the archived simulator/source-render checkpoint recovered on 2026-08-29. They supersede the old coarse-grid continuum interpretation, but the exact source artifacts and a formal continuum proof have not yet been migrated into this public repository. The `0.001543` value may be cited only as a historical sampled-grid threshold, not as the continuum merge barrier. See `TOPOLOGY_CORRECTION_STRETCH_2026-08-29.md`.

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


## C13 — Independent reconstruction from the authors' released FM1 atlas

**Class:** observed-data reanalysis / independent repository reconstruction
**Status:** reproduced from the original public code/data release at upstream commit `95fde8b`.

Using 760 eligible 120h cells grouped into 233 distinct 96h ancestor lineages, current geometry alone produced nested grouped out-of-fold R² = 0.0333 for 120→132h lineage log-volume expansion. Adding the released 25-gene 120h atlas-annotation state raised R² to 0.2846. Adding the corresponding 96h ancestor geometry + 25-gene atlas state raised R² only slightly further to 0.2928 (ΔR² history|current = +0.0082). A random-forest sensitivity analysis gave 0.3002 → 0.3524 → 0.3304.

A fixed-Ridge calibration produced biological ΔR² history|current = +0.0056 with a 5,000-group-bootstrap 95% interval of approximately [-0.039, +0.054]. A known-non-Markov synthetic control with a moderate residual history term was detected with 97.6% power above the known-Markov 95th percentile.

**Interpretation allowed:** the released FM1 data independently support substantial future-growth information in the current integrated atlas state beyond current geometry, while residual predictive value from the released 96h ancestor state is small relative to that current-state gain and not robustly resolved. The primary paper says these gene patterns were manually integrated into the FM1 template from published and newly acquired expression information; they are not 25 simultaneous molecular assays in every exact live cell.

**Interpretation not allowed:** exact conditional independence; proof of Markov closure; universal state sufficiency.

A predefined upstream L1 epidermal restriction (256 eligible cells, 86 ancestor groups) strengthens the task-specific pattern: nested Ridge 0.3634 geometry → 0.5947 current atlas state → 0.5956 with 96h history; random forest 0.6197 → 0.6700 → 0.6656. Calibration indicates good power for moderate-to-large residual history effects but limited power for subtle ones.

See `REPLICATION_CHECKPOINT_FM1_2026-08-29.md`.


## C14 — External positive control for state incompleteness

**Class:** external observed-data reanalysis / methodological control
**Status:** reproduced directionally from the Weinreb et al. 2020 public split-well lineage dataset using the released metadata and clone matrix.

A release-native reconstruction identified 504 clones with mature cells in both separated day-6 well sets. Exact mature-fate-set agreement was 57.9% versus 17.4% after clone-label permutation (`p≈0.0002`). In a frozen 133-clone three-fate cohort, a day-2 state proxy (mean SPRING x/y + starting population) achieved approximately 0.618 balanced accuracy for the other well's dominant fate; adding the separated sister-well fate raised balanced accuracy to approximately 0.827 and reduced log loss by about 0.38. Conditional mutual information between separated sister fates remained approximately 0.58–0.69 bits after conditioning on multiple day-2 state-bin resolutions, far above within-state permutation nulls.

**Interpretation allowed:** our general state-sufficiency diagnostic can flag a measured state as incomplete in a published system where the original investigators independently established hidden heritable fate information.

**Interpretation not allowed:** exact reproduction of the paper's figure-specific cohort/numbers; proof that full scRNA-seq is insufficient from our reduced SPRING-coordinate analysis alone; evidence that the same hidden variables operate in plants.

See `NEGATIVE_CONTROL_WEINREB_2020_2026-08-29.md`.

## C15 — Loss-aware predictive screening-off

**Class:** established mathematical identity + reproduced application
**Status:** theorem is standard information/decision theory; FM1 application reproduced in this repository.

Define population history value under loss `L` as

`V_L(H->Y|S) = R*_L(Y|S) - R*_L(Y|S,H)`.

Under Bayes-optimal logarithmic loss, `V_log = I(Y;H|S)`, so zero population gain is equivalent to distributional conditional independence (under standard regularity conditions). Under squared loss, `V_2 = E[(E[Y|S,H]-E[Y|S])^2]`, so zero gain establishes only conditional-mean screening-off.

A direct XOR counterexample also falsifies the conjecture that residual history information must decrease monotonically as more present variables are added: `I(Y;H)=0` but `I(Y;H|Z)=1 bit` for `Y=H xor Z` with independent fair bits `H,Z`.

Applied to the released FM1 atlas with repeated ancestor-group partitions, fixed Ridge gives a middle-L1 median history gain of **+0.144 R²** across 200 shuffled partitions (positive in 90.5%; 2.5th–97.5th split quantiles [-0.051,+0.251]), while late L1 has median **-0.015 R²** (positive in only 4%; no partition above +0.05). A fixed-Ridge Gaussian log-score stress test across 100 shuffled partitions gives middle-L1 median history value **+0.109 bits/cell** (positive in 89%) versus late-L1 median **-0.035 bits/cell** (positive in 3%). These split quantiles describe partition sensitivity, not confidence intervals.

**Interpretation allowed:** the middle L1 window usually contains residual predictive structure under a linear decoder but is strongly partition- and decoder-dependent; late L1 shows a substantially more stable near-zero residual under the tested linear loss functions.

**Interpretation not allowed:** exact conditional independence in late L1; universal monotonic loss of history with added measurements; novelty of the log-loss/CMI identity.

Artifacts: `MATHEMATICAL_NOTE_PREDICTIVE_SCREENING_OFF.md`, `analysis/screening_loss_identities.py`, `analysis/fm1_gaussian_logscore.py`, and `analysis/fm1_split_stability.py`.

## C16 — Finite-resolution global reconstruction is Test Cover

**Class:** established combinatorial reduction + project-specific finite-resolution formulation
**Status:** exact finite-library proof recorded and toy implementation reproduced; archived Source640 phase numbers not yet independently rerun.

For a finite world library, let `U_epsilon` be the pairs farther than hidden-world resolution `epsilon`. Experiment `q` covers a far pair when its responses differ by more than phenotype threshold `delta`. A panel is `(epsilon,delta)`-identifying if and only if its covered-pair sets cover all of `U_epsilon`. Thus the minimum global panel size `kappa(epsilon,delta)` is exactly a **Minimum Test Collection / set-cover problem** on structurally relevant world pairs.

**Established mathematics:** Minimum Test Collection, separating systems, logarithmic greedy set-cover guarantees, and `1-1/e` greedy maximum-coverage guarantees are not new contributions of this project.

**Project-specific consequence:** pairwise separation and connected-fiber destruction have fundamentally different optimization structure. Greedy can have a classical guarantee for pair coverage while the connected-component objective in C11 has approximation ratio `3/n -> 0`.

For the full finite experiment library, define `epsilon_floor(delta)=max{d_W(w,w'): D_full(w,w')<=delta}`. If `epsilon < epsilon_floor(delta)`, then `kappa=infinity`; no allowed subpanel can achieve that hidden-world resolution. The toy implementation also verifies the robust `2 eta` pair-distance perturbation bound.

**Artifacts:** `FINITE_RESOLUTION_TEST_COVER_NOTE.md` and `analysis/finite_resolution_test_cover.py`.

**Interpretation not allowed:** claiming Test Cover/separating systems as novel; treating archived Source640 `kappa` numbers as independently reproduced; transferring pair-coverage greedy guarantees to the connected-topology objective.

## Highest-priority falsifiers

The framework should be considered weakened if any of the following occur under rigorous replication:

1. calibrated history gains remain large after rich present-state measurement across multiple biological systems;
2. designed perturbations fail to outperform random/equal-cost perturbations in distinguishing baseline-similar biological backgrounds;
3. connected-fiber structure is unstable to reasonable biological distance metrics or discretization;
4. proposed topological experiment-selection objectives do not improve identification efficiency prospectively;
5. reported flower/seed numerical results fail independent code-level reproduction.

## Publication rule

No public communication should upgrade a claim beyond its class in this ledger without a new tagged release that contains the supporting code, data provenance, and validation report.
