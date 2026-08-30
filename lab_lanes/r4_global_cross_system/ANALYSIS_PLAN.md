# R4 Analysis Plan

Date: 2026-08-30

## Project-level rule

R4 asks a narrow predictive question: after conditioning on a declared present representation S, does an admissible auxiliary variable H materially improve held-out prediction of a declared Y? A positive gain is a representation/task incompleteness signal. A negligible gain, when the calibration shows adequate sensitivity, is a task-specific screening-off result. Neither result by itself identifies a biological mechanism or proves a true state Markov/non-Markov.

All preprocessing that uses empirical distributions (feature selection, scaling, PCA, calibration transforms) must be fitted on training data only. Splits must keep the strongest released dependency group intact. Estimator conclusions require agreement across a linear and at least one nonlinear family. Proper-score/calibration metrics are reported alongside discrimination. Nulls permute H or Y only within admissible groups. Negative and calibration-limited outcomes remain first-class results.

## Plan 1 — GSE167135 Arabidopsis stomatal lineage (EXECUTED R4 proxy)

**Scientific role:** independent plant stress test outside LARRY and *C. elegans*. The three compact Smart-seq2/FACS files are genuinely public and require no account.

**Observed units:** 621 Smart-seq2 cells, 32,834 genes after dropping the matrix `Pool` metadata row; 478 TMMp-enriched and 143 ATML1p-enriched cells. Released pool labels are TMMp_pool_1/2 and ATML1p_pool_1/2.

**Proxy construction:** H = seven same-time FACS measurements (FSC-A/W/H, SSC-A/W/H, FITC-A). S = log1p transcriptome, with top 300 variance genes selected on each training fold, train-only standardization, then train-only 20-PC PCA. Y = reporter-enrichment class TMMp versus ATML1p. This Y is **not a future outcome**, so this run is a measurement-sufficiency proxy, not developmental-state-completion evidence.

**Grouping:** pair the released sort replicates by index, `pool_1` and `pool_2`, and leave one matched pool index out. Each test fold therefore contains both reporter classes. The initial tempting split on the four literal pool labels was rejected because each label is class-specific and produced single-class test folds.

**Estimators:** L2 logistic regression, random forest, histogram gradient boosting. Metrics: ROC AUC, log loss, Brier score, accuracy. Primary incremental quantities are AUC gain and improvements in log loss/Brier for S+H versus S.

**Null:** 20 group-preserving permutations of H within matched pool index, refitting the logistic S+H model. **Sensitivity calibration:** 20 known-complete labels generated from a train-fitted S direction, and 20 known-incomplete labels generated from S plus a training-residualized H direction. Calibration is diagnostic only; it is not a biological effect-size power calculation.

**Frozen interpretation:** positive H gain -> the selected transcriptome-PC representation does not screen off these FACS measurements for reporter-class prediction. No inference about temporal memory, molecular mechanism, or exact conditional independence.

## Plan 2 — GSE106587 zebrafish embryogenesis

**Proposed task:** terminal lineage/fate classification using the author-released developmental tree, but only after obtaining a public processed object without creating/logging into an account. H = earlier sampling time and coarse branch context; S = current expression at an intermediate window; Y = terminal branch/fate assignment. Because cells are destroyed at sequencing, this is a **reconstructed-trajectory future proxy**, not observed same-cell future.

**Split:** hold out embryo/library where released metadata allow it; if only time-library batches are released, hold entire library/time replicates. Never random-split individual cells across the same embryo/library. Feature selection/PCA train-only. Estimators: multinomial elastic-net/logistic, random forest or gradient boosting, and a nearest-centroid baseline. Metrics: macro log loss, Brier/multiclass calibration, macro AUROC, balanced accuracy.

**Nulls:** permute terminal labels within stage/library-compatible strata; second null permutes earlier branch context while preserving present-state and stage distributions. **Key falsifier:** if H gains disappear when author trajectory labels are replaced by an independently defined terminal annotation, the original gain is likely trajectory-construction circularity.

**Access gate:** Farrell lab explicitly states the processed counts/URD object at the Broad portal requires login. R4 does not create an account. GEO BAMs are public but rebuilding the full processed matrix is a larger next-wave job.

## Plan 3 — E-MTAB-6967 mouse gastrulation

**Proposed task:** cross-stage lineage prediction. H = embryo identity-compatible earlier-stage context (never supplied directly to a model if it acts as a leakage key), S = intermediate-stage expression, Y = later-stage lineage class defined from a separately frozen annotation. The dataset has 116,312 cells across nine E6.5–E8.5 stages.

**Group/split:** embryo is the primary group. If embryo identifiers are incomplete, use sample/library as a stricter surrogate. Hold out entire embryos/samples. Restrict primary analysis to lineages present in both train and held-out stages so time alone cannot trivially solve Y.

**Models:** elastic-net multinomial logistic, histogram boosting, random forest; optional nearest-centroid. Train-only HVG selection and PCA. **Calibration:** simulated known-complete and residual-H-incomplete targets on the real S/group geometry. **Null:** within-stage/embryo-safe permutation. **Negative-result rule:** if calibration power is insufficient at the declared injected effect, freeze the biological result as unresolved exactly as R2 did.

## Plan 4 — GSE112294 zebrafish first-day atlas

**Proposed task:** predict later reconstructed fate from an early/intermediate expression state. H = prior sampling stage/coarse fate-map context; S = current expression; Y = later fate-map class. The public release covers >92,000 cells during the first day.

**Leakage defense:** author fate maps/graph embeddings may already be computed from the same expression. Therefore primary Y must be a frozen biological annotation not an embedding coordinate, and S must exclude genes used to define any hand-coded lineage reporter if such genes are known. Hold library/embryo groups intact. Report a time-only baseline to quantify how much prediction comes from developmental time alone.

**Controls:** multiple estimators, train-only preprocessing, group permutation, time-only baseline, annotation-swap sensitivity, injected completeness/incompleteness calibration.

## Plan 5 — GSE269784 zebrafish cell-cycle arrest

**Proposed intervention-indexed test:** H = treatment history (division-arrest method plus exposure duration) and earlier developmental stage; S = current transcriptome at a matched stage; Y = a later developmental cell-state composition or cell-state class, provided a release-native later outcome can be linked at replicate/embryo level. This is more causal-design-relevant than an atlas-only analysis because intervention is explicit, but predictive screening-off still does not identify mechanism.

**Groups:** embryo/biological replicate, not cells. Compare reference, each independent arrest method, and matched stage. Include burden/developmental-delay covariates only when measured before Y and freeze them prospectively in the analysis definition.

**Models/metrics:** regularized multinomial/logistic and nonlinear tree/boosting models; proper scores and calibration; intervention-stratified performance. **Null:** treatment-history permutation among compatible biological replicates. **Failure mode:** if later Y cannot be linked without pseudo-pairing cross-sectional cells, downgrade to a distribution-level replicate analysis rather than inventing cell-level trajectories.

## Common promotion criteria

A dataset-specific result may enter the durable evidence ledger only if: (1) split groups block the strongest known dependence; (2) all empirical preprocessing is train-only; (3) at least two materially different estimators agree in direction; (4) a proper-score metric agrees with or explains any discrimination metric; (5) a null/permutation analysis is directionally compatible; (6) a sensitivity calibration is adequate for the promoted effect size; and (7) the claim language names the exact H, S, Y, horizon/target, intervention context and representation.
