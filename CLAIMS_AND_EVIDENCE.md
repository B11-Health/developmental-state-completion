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

## C2 — A compact molecular representation can be task-sufficient, but its effective dimension is decoder-dependent

**Class:** observed-data reanalysis
**Status:** directly reproduced on the released FM1 atlas; post-hoc dimensionality audit.

In the predefined late-L1 `96→120→132 h` cohort (`n=256`, 86 ancestor groups), current geometry plus the released 25-channel binary atlas state predicts subsequent lineage-volume expansion substantially better than geometry alone. PCA was fit only on training folds under ancestor-grouped cross-validation.

A single current PC is sufficient for the two flexible nonlinear decoders tested: across 30 shuffled lineage partitions, ExtraTrees averaged R² **0.654** with PC1 versus **0.638** with all 25 channels, and PC1 matched or exceeded all 25 in 30/30 partitions. HistGradientBoosting averaged **0.674** with PC1 versus **0.671** with all 25, with PC1 at least as good in 21/30 partitions.

The same one-PC claim does **not** hold for linear Ridge: on the fixed grouped split, geometry was R² 0.307, +PC1 0.451, +PC2 0.551, +PC4 0.598, and +all25 0.599. Thus roughly four PCs were needed to recover essentially all linear predictive gain.

**Finite-state caveat:** the late-L1 cohort contains only 8 distinct 25-channel atlas patterns, and PC1 assigns all eight unique scalar codes. All 30 tested target-independent random scalar projections were also injective, which is expected mathematically for a finite set. PC1 predicts better than a typical random code, but exact one-dimensional separability itself is not evidence of a one-dimensional biological manifold.

**Interpretation allowed:** for this late-L1 atlas-derived task, one dominant current atlas coordinate can carry nearly all nonlinear predictive value given current geometry.

**Interpretation not allowed:** the plant has a one-dimensional molecular state; one PC is universally sufficient; PCA dimension is an intrinsic biological state dimension.

**Critical measurement caveat:** the 25 channels are binary atlas annotations integrated onto the FM1 reference from literature, RNA in-situ hybridization and some live imaging, not repeated simultaneous molecular assays of the exact same living cells.

**Legacy provenance correction:** the exact early public prose values `0.272 -> 0.643`, `all25 ~0.633`, and old-history `+0.0095` entered the repository before an executable cohort/split/target artifact existed. Independent R1 audit can reproduce nearby ~0.64 nonlinear late-L1 performance, but cannot regenerate that exact historical tuple. The exact legacy numbers are therefore **not independently reproduced / provenance-incomplete** and must not be cited as replicated results.

See `REPRESENTATION_DIMENSION_CHECKPOINT_FM1_2026-08-29.md` and `lab_lanes/replication/R1_REFAHI_REPLICATION_CHECKPOINT_2026-08-29.md`.

## C3 — Fixed history-gain thresholds can falsely imply memory

**Class:** calibration result
**Status:** strong computational falsification of an earlier criterion.

A known-Markov ABA–GA simulator nevertheless produced a finite-sample boosted-tree history gain of roughly +0.0299 R². Therefore a rule such as “history gain above +0.02 proves non-Markov memory” is invalid.

**Consequence:** future screening-off claims must be calibrated against estimator bias, sample size, dimensionality, and known generative controls.

## C4 — Germination percentages should be modeled as finite binomial observations

**Class:** observed-data reanalysis / statistical correction
**Status:** methodologically well motivated; downstream numerical claims require repository migration.

Reported germination assays used about 75 seeds. Treating 0% or 100% as zero-noise continuous measurements creates pathological information geometry. The corrected model uses finite binomial counts with a logistic latent factor structure, so boundary observations contribute finite evidence.

## C5 — Historical 224-world counterfactual-collapse result

**Class:** historical synthetic-model report
**Status:** **provenance-incomplete / not independently reproduced from the current workspace.**

Prior checkpoints report a constructed 224-world system (`14 architectures × 16 hidden states`) in which baseline morphology collapsed distinct hidden worlds that separated under intervention. The original 224-world generator/source/output bundle and the named frozen checkpoint files were **not recovered** in the authenticated Windows workspace or tested WSL paths on 2026-08-29.

**Allowed wording:** this phenomenon was historically reported in the project and motivated the counterfactual-tomography program.

**Not allowed:** “the 224-world experiment is currently reproducible from this repository” or using the later 128-world/two-context bundle as if it were the missing 224-world study.

A separate, later source-validation bundle *is* public and reproducible: `source_validation/two_context_2026-08-26/` contains 128 world/context combinations across eight laws and sixteen contexts and supports the prospective two-context result described elsewhere. It is a distinct experiment.

See `lab_lanes/provenance/P1_PROVENANCE_RECOVERY.md` once promoted and `REPRODUCIBILITY.md`.

## C6 — Historical connected-fiber / cryptic-island measurements

**Class:** historical synthetic-model / topological report
**Status:** **specific historical thresholds are provenance-incomplete; general definitions remain framework objects.**

Earlier research threads reported disconnected or weakly connected mechanism regions in a sampled state-law landscape and introduced the distinction between:

- **accommodation:** how closely an alternative mechanism can imitate the target phenotype;
- **merge/access threshold:** the phenotype tolerance required before a continuous path from the target can reach that alternative region.

A later prose checkpoint reported a correction of the original coarse STRETCH threshold (`~0.001543`) to a lower seam-optimized value (`~0.00141094`) and a static accommodation near `~0.00026863`. **P1 could not recover the underlying historical simulator/source-render artifacts or the named frozen topology checkpoint**, so these numerical values are retained only as historical reported values, not as independently source-validated numbers in the present workspace.

The mathematical lesson survives independently: sampled graphs can create apparent barriers, and component claims must distinguish discretized thresholds, source-optimized thresholds, and proved continuum bounds. The exact biological/simulator magnitude does not currently have recoverable provenance.

See `TOPOLOGY_CORRECTION_STRETCH_2026-08-29.md` and the provenance recovery note.

## C7 — Experiment-selection objective matters; connected ambiguity is not generally submodular

**Class:** mathematical/computational result plus historical simulator report
**Status:** **current negative theorem reproduced; old perturbation-ranking numbers provenance-incomplete.**

Historical checkpoints reported that a topological connected-ambiguity ranking differed from a global parameter-estimation ranking (including specific 2030→114 and rank-order numbers). The original outputs supporting those exact ranking values were not recovered, so those values must be treated as historical reports rather than current reproducible evidence.

What **is** currently reproducible:

- a grid counterexample for the target-connected component-reduction objective with greedy/optimal ratio `3/n -> 0`;
- a real submodularity violation in the preserved source-derived 128-world bundle under an explicitly declared topology proxy (marginal gain 9 before versus 19 after conditioning; gap 10);
- exhaustive budgets 1–5 in that particular source-derived stress case where greedy nevertheless matches optimal utility;
- a rooted-tree known-outcome regime where the same objective reduces to ordinary coverage and recovers the classical `(1-1/e)` greedy guarantee.

**Interpretation:** experiment value is objective- and structure-dependent. Greedy connected-ambiguity splitting is a heuristic unless a safe regime is established; pairwise robust separation is a different Test-Cover/set-cover objective with its own classical guarantees.

See `MATH_VERIFICATION_M1_2026-08-29.md`.

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

## C17 — Prospective two-context source-simulator tomography

**Class:** prospective preregistered source-simulator validation + established rectifier algebra
**Status:** frozen commitments, 128 source TSV renders, estimator models, score scripts and result JSONs migrated and independently verified in this repository.

In the restricted four-channel simulator, context reflection followed by rectification gives `u_q=[-R_q s]_+`. Complementary contexts reveal the positive and negative parts of the signed latent state, so `R_q s = u_qbar-u_q`. This positive/negative-part identity is **CReLU-like established rectifier algebra**, not a new mathematical discovery. With known fixed L1 budget, masks flipping `n-1` of `n` coordinates are also exactly sufficient at the latent level away from the zero seam.

The parent prospective cohort was frozen before 64 new source phenotypes were rendered. Canonical pre-render commitment: `b5fdc0bd257dbb57874f107b3c7a12b6c9fe5ec9f89cb48de585743846341c3a`. Across 32 complementary source pairs, the frozen nonlinear phenotype decoder achieved **100% sign recovery**, median signed L2 `1.75175e-4`, p95 `4.28985e-4`, max `5.14625e-4`, and recovered every deliberately weak `0.001` channel sign. All preregistered thresholds passed.

A separately frozen context/mask extension (`7d4845aa8a50da5e5d8ffd2b0bc65e02311882879a261df8c313b4557d47663f`) rendered 64 previously unseen contexts for the already partially observed P00-P07 laws. All five Hamming>=3 masks `0111,1011,1101,1110,1111` achieved 100% sign accuracy and stayed below the frozen median `<0.001` and maximum `<0.002` L2 thresholds. This extension is prospective **with respect to new contexts/masks, not new laws**.

The public verifier recomputes both canonical freeze hashes, the frozen estimator hashes, two 64-render aggregate manifests, and every frozen pass/fail condition. The public algebra script verifies exact reconstruction on 5,000 random worlds and deterministic noise margins on 20,000 noisy trials.

**Interpretation allowed:** within this restricted developmental source simulator, two source-rendered phenotype contexts prospectively recovered the hidden signed state with the preregistered accuracy using a frozen decoder, and previously unseen contexts generalized across all five theoretically sufficient masks.

**Interpretation not allowed:** living-plant validation; universal two-perturbation sufficiency; novelty of CReLU/positive-negative decomposition; formal global injectivity of the source simulator; new-law generalization for the five-mask extension.

Artifacts: `PROSPECTIVE_TWO_CONTEXT_TOMOGRAPHY_2026-08-29.md`, `source_validation/two_context_2026-08-26/`, `analysis/verify_two_context_source_bundle.py`, and `analysis/two_context_tomography_algebra.py`.

## C18 — Absolute predictive adequacy must precede residual-history interpretation

**Class:** cross-system methodological negative result / promotion rule  
**Status:** reproduced across independent public *Drosophila* and *Tribolium* trajectory benchmarks; consistent with the earlier R2 calibration failure mode.

R5 and R6 expose a failure mode that is invisible if analysis reports only `Score(S+H)-Score(S)`. In whole-acquisition holdout, older-history features sometimes produced large positive increments while the augmented predictor itself failed to transfer. In *Tribolium*, apparent nonlinear gains reached about **+0.42 ΔR²** at the coarsest tested present representation, yet the augmented predictors still failed the preregistered absolute adequacy gate in both acquisitions. In *Drosophila*, positive radial-velocity history increments likewise occurred inside models whose held-out absolute R² remained below a train-only naive baseline.

R7 then expanded the present representation to roughly 46–49 acquisition-robust relational/kinematic features per task. None of the four frozen organism/outcome tasks passed the strict gate requiring positive held-out R² and lower RMSE than the train-only mean in both reciprocal acquisition folds for at least two of Ridge, Random Forest, and Extra Trees.

**Promotion order now required:**
1. absolute held-out adequacy against a train-only naive baseline;
2. stability/materiality of the incremental history value across prespecified estimators/groups;
3. matched known-complete/known-incomplete sensitivity calibration;
4. only then a scoped biological interpretation.

**Interpretation allowed:** a positive residual-history increment inside an inadequate predictor is not evidence of biological memory. R5/R6/R7 diagnose cross-acquisition representation/transfer failure for the tested tasks.

**Interpretation not allowed:** history is irrelevant in these organisms; the cells are Markov; the residual-history signal is biologically meaningful; or R7's richer representation is close to a complete state.

Artifacts: `lab_lanes/r5_drosophila_trajectory/`, `lab_lanes/r6_tribolium_trajectory/`, and `lab_lanes/r7_relational_adequacy_rescue/`.

## C19 — Local kernel sufficiency factors through connected fiber components, not necessarily the raw measurement

**Class:** mathematical structural result + counterexample  
**Status:** proved and executable finite examples recorded in T5; no priority claim.

For a smooth submersion `h:X->S` and smooth future map `F`, the local condition

`ker Dh_x subset ker DF_x`

forces `F` to be constant along each **connected component** of each fiber of `h`. Thus the natural global object is the quotient that identifies points lying in the same connected measurement-fiber component. The condition does not in general imply that `F` factors through `h` itself when a fiber is disconnected.

The explicit example `X=R\{0}`, `h(x)=x^2`, `F(x)=x` has vacuous local kernel obstruction, but `h` merges `+x` and `-x` even though their futures differ. A branch/sign coordinate repairs the factorization.

For a finite set of `m` future-distinct component classes inside a measurement fiber, any exact discrete branch code needs at least `ceil(log2 m)` bits. A synthetic noisy-history witness additionally shows how older measured history can act as a proxy for a missing branch coordinate and become redundant once that coordinate is measured.

**Interpretation allowed:** local differential sufficiency can miss global disconnected-fiber ambiguity; history may proxy for omitted branch information.

**Interpretation not allowed:** biological systems literally contain discrete branch bits; every residual-history signal is topological; or the Reeb/fiber-component quotient is a new mathematical construction.

Artifacts: `lab_lanes/t5_topological_branch_completion/`.

## C20 — Set-theoretic branch complexity and continuous measurement dimension can diverge arbitrarily

**Class:** established topology applied to task-relative state completion  
**Status:** T6 passed independent adversarial audit with hypothesis/novelty qualifications applied upstream.

Define the continuous Euclidean completion dimension `cdim_R(h,F)` as the minimum number of continuous real-valued augmentation coordinates needed so that `(h,B)` separates every measurement collision whose futures differ, with `+infinity` allowed when no finite witness exists.

For the antipodal quotient `h:S^n->RP^n` with future `F(x)=x`, Borsuk–Ulam gives the exact result

`cdim_R(h,F)=n+1`.

Each measurement fiber contains only two points, so an exact discrete branch label needs one bit, yet a globally continuous Euclidean realization can require `n+1` real channels. For the double cover `z->z^2` on `S^1`, one continuous real scalar cannot separate every antipodal pair, while two real coordinates do.

T6A independently reconstructed the proofs. It strengthened the finite-cover scalar theorem by showing connectedness of the base is unnecessary for the rank-order proof, required the standard nice-base hypotheses before invoking Stiefel–Whitney classes, and identified projected-embedding / `k`-prem literature as substantial prior art for the underlying fiberwise Euclidean-lift problem.

**Interpretation allowed:** a small discrete latent branch count does not imply an equally small globally continuous biomarker panel.

**Interpretation not allowed:** the Borsuk–Ulam obstruction, projected-embedding problem, configuration-space criterion, or characteristic-class machinery is novel to this project; real-channel count can be compared directly to finite-precision bit capacity without a measurement model.

Artifacts: `lab_lanes/t6_topological_measurement_dimension/` and `lab_lanes/t6a_independent_audit/`.

## C21 — Topological collision obstructions can induce sharp minimax predictive-error floors and noise margins

**Class:** project-specific predictive-risk synthesis of established topology/metric bounds  
**Status:** T7 passed independent adversarial audit; missing Hausdorff/decoder-codomain assumptions were repaired upstream.

For the same antipodal problem `S^n->RP^n`, `F(x)=x`, with Euclidean prediction loss, every continuous augmentation with `k<=n` channels has minimax worst-case prediction error exactly **1**: Borsuk–Ulam forces one antipodal measurement collision, the two futures are distance 2 apart, and the triangle inequality forces at least unit error at one endpoint; the constant-zero decoder attains unit error everywhere. Therefore the epsilon-completion dimension jumps from 0 channels at tolerance `epsilon>=1` to `n+1` channels for every `epsilon<1`.

More generally, if a completed measurement collides two states whose future targets are distance `delta` apart in a metric prediction space, any deterministic decoder incurs worst-case error at least `delta/2` on that pair. The same pairwise bound applies to probability-law targets under metrics such as total variation and Wasserstein under their standard hypotheses.

For a compact finite cover over a Hausdorff base, a continuous fiberwise-injective Euclidean augmentation has a positive global within-fiber separation margin `Delta_B`. If only the augmentation receives adversarial additive sensor noise bounded by `eta` and the base point is known exactly, nearest-neighbor sheet recovery is guaranteed when `2 eta < Delta_B`; when a minimum-margin pair exists and `2 eta >= Delta_B`, uniform exact sheet recovery cannot be guaranteed.

**Interpretation allowed:** topological impossibility can be translated into a task-relative worst-case prediction floor, and successful exact completion still needs measurement separation large relative to assay noise.

**Interpretation not allowed:** one forced collision implies a large average-case error; empirical prediction error is caused by topology without ruling out model/data/domain-shift effects; the raw numerical margin is meaningful without fixed measurement units/normalization; or the underlying topology/robust-decoding ingredients are new.

Artifacts: `lab_lanes/t7_robust_topological_completion/` and `lab_lanes/t7a_independent_audit/`.

## C22 — The first R4 Arabidopsis execution is a same-time measurement-completeness proxy, not a future-state test

**Class:** public-data cross-system proxy analysis  
**Status:** reproduced on public GSE167135 release files with group-aware train-only preprocessing; deliberately not promoted as temporal screening-off.

In 621 public Smart-seq2 cells from the *Arabidopsis* stomatal-lineage dataset GSE167135, R4 used train-only transcriptomic PCs as `S`, seven same-time FACS measurements as added `H`-like information, and reporter-defined TMMp-vs-ATML1p class as the target. Across the tested logistic, Random Forest, and HistGradientBoosting estimators, adding the FACS measurements improved held-out AUC by about 0.05–0.062 and log loss by about 0.086–0.175 under the available matched-pool split.

This is useful evidence that release-native measurement channels contain complementary state information. It is **not** a future outcome, not literal history, and cannot establish developmental screening-off.

**Interpretation allowed:** the global registry yielded a reproducible independent plant proxy showing complementary present-state information beyond transcriptomic PCs.

**Interpretation not allowed:** FACS is biological memory; the result demonstrates future-state sufficiency; reporter class is a future fate; or the available pool IDs provide ideal biological-replicate grouping.

Artifacts: `lab_lanes/r4_global_cross_system/`.

## Highest-priority falsifiers

The framework should be considered weakened if any of the following occur under rigorous replication:

1. calibrated history gains remain large after **absolutely adequate, cross-group-transferable** rich present-state predictors across multiple biological systems;
2. designed perturbations fail to outperform random/equal-cost perturbations in distinguishing baseline-similar biological backgrounds;
3. connected-fiber structure is unstable to reasonable biological distance metrics or discretization;
4. proposed topological experiment-selection objectives do not improve identification efficiency prospectively;
5. reported flower/seed numerical results fail independent code-level reproduction.

## Publication rule

No public communication should upgrade a claim beyond its class in this ledger without a new tagged release that contains the supporting code, data provenance, and validation report.


### R8 morphology/intensity adequacy rescue
**Evidence class:** public-data predictive transfer stress test; negative adequacy result.

- Frozen cohorts/tasks/splits remain the R7 Drosophila and Tribolium frame25->40 tasks with reciprocal whole-acquisition holdout.
- Present-only S was expanded from 49 to **139 features** in Drosophila and from 46 to **99 features** in Tribolium using release-native GT/TRA tracking-mask geometry proxies plus raw-image intensity from frames 23/24/25. GT/TRA is not called segmentation ground truth, and raw intensity is not called a molecular assay.
- **Gate 1 failed in all four organism x outcome tasks:** zero of three prespecified estimators passed both reciprocal acquisitions.
- Tribolium radial prediction showed a one-fold improvement (RF/Extra Trees R2 about +0.30 in sequence02) but remained negative in sequence01; this is not promoted as adequacy.
- Because Gate 1 failed, R8 did **not** fit older H, run H permutation tests, or run sensitivity calibration.

**Allowed claim:** adding substantially richer release-native morphology/intensity did not rescue cross-acquisition adequacy for the frozen tasks, strengthening the evidence for a representation/domain-transfer limitation.

**Prohibited upgrade:** R8 does not establish biological memory, non-Markov development, exhaustion of the present state, or irrelevance of richer molecular/tissue/registration variables.

### R9 acquisition/developmental registration rescue
**Evidence class:** preregistered public-data domain-transfer rescue; one conditional positive adequacy result.

- Frozen R8 cohorts, frame25 anchor, frame40 outcomes, reciprocal whole-acquisition split and model hyperparameters were unchanged.
- The primary `transductive_domain_percentile` representation uses only S but requires the unlabeled target acquisition distribution; it is **not** an inductive/target-free result.
- For Tribolium future radial velocity, Random Forest passed both reciprocal folds at R2 about **+0.081 / +0.114** and Extra Trees at **+0.115 / +0.224**, each beating the train-only mean RMSE. Thus 2/3 prespecified estimators passed both folds.
- Robust domain scaling and CORAL also passed as secondary transductive diagnostics, while the target-free/invariant panel did not. Drosophila outcomes and Tribolium future speed remained inadequate.
- Target-row permutation controls were negative in all primary-model folds.

**Allowed claim:** outcome-blind target-distribution registration materially rescues reciprocal absolute prediction for one narrow Tribolium radial task, showing that acquisition/domain mismatch contributed to the earlier one-sided failure.

**Prohibited upgrade:** do not call the result inductive, mechanism, universal state sufficiency, Markovity, or evidence about older history.

Artifacts: `lab_lanes/r9_domain_registration_rescue/`.

### R10 registered-history calibration
**Evidence class:** preregistered residual-history test inside the single R9-qualified task; calibration-limited result.

- R10 tested only Tribolium future radial velocity under the passing transductive percentile present representation and counted only Random Forest/Extra Trees, the Gate-1-qualified estimators.
- Observed history increments were near zero and not stable: mean Delta R2 **-0.0030** (RF) and **-0.0054** (Extra Trees).
- The S and S+H predictors remained absolutely adequate, but the history Gate 2 failed.
- **0/100** matched H-permutation replicates passed the full two-model history gate.
- The original +0.30 target-SD calibration implementation used a seed family that did not match the written preregistration and yielded **10/30 (33.3%)** joint successes. R10B reran only the documented seed rule (`20260830+r`) and obtained **16/30 (53.3%)**, still below the frozen **24/30 (80%)** requirement.

**Allowed claim:** after solving the absolute-transfer prerequisite for one task, the observed history increment is very small, but the current sample/model stack still lacks demonstrated sensitivity for a screening-off conclusion. The exact calibration percentage is seed-family sensitive; the documented-seed remediation still fails the preregistered threshold. Status: **calibration-limited / unresolved**.

**Prohibited upgrade:** do not say history is redundant/useless, Tribolium is Markov or memoryless, or 0/100 permutation passes proves conditional independence. The +0.30-SD effect is synthetic calibration, not a measured biological effect.

Artifacts: `lab_lanes/r10_registered_history_calibration/`.

Seed-remediation artifact: `lab_lanes/r10b_seed_remediation/`.

### R11 calibration-failure decomposition
**Evidence class:** post-R10 planning diagnostic; not a new biological test and not a replacement for the preregistered R10 decision.

- Using the same first 20 **original implemented-seed** residual-history directions (not the later R10B documented-seed family), S-only adequacy preservation was **85%, 70%, 55%, 45%** at injected scales 0.15, 0.30, 0.45, 0.60 target SD.
- Gate-2 detection was **0%, 45%, 60%, 75%** across the same scales.
- The strict joint success rate was **0%, 30%, 30%, 30%**.
- The opposing trends match the idealized fact that adding an S-unpredictable target component can make H easier to detect while degrading the absolute predictive adequacy of S alone.

**Allowed claim:** in the original implemented-seed planning surface, the calibration bottleneck has two components—under-detection and adequacy collapse—and larger synthetic injection did not increase the aggregate strict joint rate on the tested grid. Future calibration should report adequacy and detection axes separately as well as any joint success rule. This planning surface does not replace R10B's corrected documented-seed calibration.

**Prohibited upgrade:** do not choose a favorable post-hoc scale, call any scale a biological effect size, reinterpret R10 as screening-off, or claim the 30% plateau is universal.

Artifacts: `lab_lanes/r11_sensitivity_design/`.

### T8/T8A calibration compatibility envelope
**Evidence class:** independently audited idealized mathematical design result; not a biological test.

- In the corrected simple population-oracle model, `(S,H)` must reveal the injected direction `Z` **and** satisfy `E[E|S,H]=0`; exact revelation of `Z` alone is insufficient.
- With `r0` the unperturbed present-only oracle R2, present threshold `rho`, and required incremental R2 `delta`, a compatible injection exists iff **`r0 >= rho/(1-delta)`**.
- When `r0>=rho`, the largest simple-model incremental R2 compatible with the present threshold is **`1-rho/r0`**.
- T8A constructed a finite counterexample to the original weaker assumption set. In the generalized case, `q=Var(E[E|S,H])/B` enters the augmented curve: `R2_{S+H}=(r0+x+q)/(1+x)` and `Delta=(x+q)/(1+x)`.

**Allowed claim:** calibration adequacy and detection thresholds can be mathematically incompatible in a declared oracle model when the base predictor lacks enough adequacy headroom; the simple envelope is exact only under the audited conditional-mean assumptions.

**Prohibited upgrade:** do not present T8 as a theorem about R10/R11 finite-sample RF/ExtraTrees gates, omit the `E[E|S,H]=0` condition, claim the empirical calibration plateau is mathematically forced, infer biology, or claim mathematical priority.

Artifacts: `lab_lanes/t8_calibration_compatibility/` and `lab_lanes/t8a_independent_audit/`.

### R12/R12A domain-balanced calibration geometry
**Evidence class:** post-R10B planning diagnostic with independent adversarial audit; not a new biological test.

- Primary: centering/scaling the pooled Ridge-residualized synthetic direction within each acquisition gives **22/30 S adequacy, 19/30 Gate-2 detection, 16/30 joint**, with exactly the R10B joint-success set.
- Secondary: acquisition-specific Ridge residualization against S gives **30/30 S adequacy and 18/30 Gate-2/joint success**, still below the frozen **24/30** standard.
- Both transforms are outcome-blind but transductive with respect to target-domain covariates; the secondary explicitly uses acquisition-specific unlabeled S/H in the held-out domain.
- Ridge residualization does **not** imply `E[Z|S]=0` or literal S-unpredictability.
- R12A reproduced the committed metrics to machine precision. Git history does not independently prove the declared pre-outcome R12 freeze because design and result artifacts first appear in the same commit.

**Allowed claim:** calibration geometry changes the finite adequacy/detection decomposition, but neither audited geometry reaches the frozen sensitivity standard; the remaining detection failure cannot be converted into a screening-off conclusion.

**Prohibited upgrade:** do not infer a unique causal reason for R10B failure, describe the secondary as target-free/inductive, equate Ridge residualization with oracle conditional independence, or reinterpret observed near-zero history as redundancy.

Artifacts: `lab_lanes/r12_domain_balanced_calibration/` and `lab_lanes/r12a_independent_audit/`.

### R13 domainwise sensitivity surface
**Evidence class:** prospectively committed post-R12 planning surface with mechanical reproducibility audit; not a biological test.

- Same documented 30 seeds, R9-qualified Tribolium radial task, RF/ExtraTrees, reciprocal acquisition folds, R10 Gate 2, and acquisition-specific Ridge-residualized R12 secondary geometry.
- Scale 0.15: **30/30 S adequacy, 1/30 detection/joint**.
- Scale 0.30: **30/30 S adequacy, 18/30 detection/joint**, inherited from R12 and not refit.
- Scale 0.45: **27/30 S adequacy, 23/30 detection, 22/30 joint (73.3%)**.
- Scale 0.60: **27/30 S adequacy, 22/30 detection, 20/30 joint (66.7%)**.
- The preregistration was committed before implementation/results. Exact reruns preserve every decision identity; observed numeric rerun drift is <=5e-16.

**Allowed claim:** the domainwise geometry materially improves the planning sensitivity surface, peaking at 22/30 on the frozen grid, but still does not reach the historical 24/30 criterion; stronger injection beyond 0.45 SD does not improve aggregate joint success on this task/grid.

**Prohibited upgrade:** do not adopt 0.45 SD as a post-hoc confirmatory threshold, generalize the non-monotone surface, infer screening-off/Markovity/biological memory, or treat this same-data planning surface as independent biological validation.

Artifacts: `lab_lanes/r13_domainwise_sensitivity_surface/` and `lab_lanes/r13a_mechanical_audit/`.



### R15 SLICE-1 cross-embryo preview pilot
**Evidence class:** repository-preregistered independent public-resource pilot with independent numerical/chronology audit; small-N adequacy evidence only.

- Resource: 2025 SLICE-1 Tribolium whole-embryo four-view preview movies; DS0004/DS0005 were development-only.
- Primary predeclared unseen embryo DS0007: Ridge R2_vector **-0.0136**; Random Forest **+0.0307**; Extra Trees **+0.0567**. The frozen 2-of-3 absolute-adequacy gate passes.
- Predeclared cross-marker Lamin #4 stress test DS0035: Ridge **+0.0371**, Random Forest **+0.0378**, Extra Trees **+0.0341**; all three beat the train-only mean baseline.
- Four-hour-older image history reduced held-out R2 for every estimator in both embryos: DS0007 deltas **-0.0540/-0.0088/-0.0081**; DS0035 **-0.1127/-0.0151/-0.0776** for Ridge/RF/ET respectively.
- R15A reimplemented the analysis without importing R15 model code; all gates and metrics reproduce to machine precision. Repository history verifies preregistration/model-freeze commits before the validation-result commit.

**Allowed claim:** a compact eight-coordinate current whole-embryo image-geometry state achieved modest positive four-hour-future vector prediction in two untouched embryos, including a predeclared marker-domain stress test.

**Prohibited upgrade:** do not claim history redundancy, screening-off, Markovity, cell-lineage state completion, causal or molecular memory, or generalization to the full SLICE-1 collection. Negative observed history deltas are unresolved because the pilot lacks matched sensitivity calibration and has only two development embryos.

Artifacts: `lab_lanes/r15_slice1_multiacquisition/` and `lab_lanes/r15a_independent_audit/`.
