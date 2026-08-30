# Developmental State Completion: Counterfactual Tomography of Hidden Biological Mechanisms

**Working preprint — Code Gym Research — 30 August 2026**

## Abstract

Developmental systems are commonly represented by measured phenotypes, molecular profiles, or inferred trajectories, yet these observations need not uniquely determine the internal state and dynamical law that govern future response. We develop a computational framework for **developmental state completion**: experimentally enriching the present observation until older measured history contributes little additional predictive information for a declared future task and intervention family. The framework combines task-relative predictive sufficiency, calibrated residual-history tests, exact and robust perturbation design, and topology of measurement fibers. Public-data reanalyses show why aggressive falsification is necessary. In the released Arabidopsis FM1 atlas, current integrated atlas state carries substantial task-specific predictive information beyond geometry, while the value of older ancestor state can become small in selected late developmental windows; this does not establish universal Markovity. In public *C. elegans* lineage timing, large nonlinear residual-history gains were not promoted because matched known-incomplete calibration power was below the preregistered threshold. In independent *Drosophila* and *Tribolium* trajectory tests, apparent history gains as large as roughly +0.42 Delta R^2 occurred inside predictors that failed absolute cross-acquisition adequacy, motivating the mandatory order **absolute adequacy -> increment stability -> sensitivity calibration -> interpretation**. Mathematically, the local kernel condition `ker Dh subset ker DF` guarantees constancy only on connected components of measurement fibers; disconnected components can require additional branch information. Established Borsuk-Ulam and covering-space arguments then show that a one-bit set-theoretic branch ambiguity can require arbitrarily many globally continuous Euclidean measurement channels, and can impose sharp worst-case prediction-error floors under dimensional constraints. On a preserved 128-world finite simulator bundle, greedy experiment selection matched exact optimum on all 17,280 audited rows, but explicit non-submodular and `3/n` counterexamples rule out a general greedy theorem. A separate prospective source-simulator validation demonstrates accurate two-context reconstruction within a restricted model, while living-system validation remains pending. These results define a falsifiable research program rather than a new biological law: the decisive biological test is whether richer present measurements and prospectively selected perturbations improve blinded prediction in living systems under calibrated adequacy and burden controls.

## 1. Motivation

A developmental phenotype is an output of a dynamical system, not necessarily a complete description of that system. Two organisms can look similar at a chosen time while differing in hidden molecular configuration, regulatory architecture, response capacity, or dynamical law. Static similarity therefore does not imply counterfactual equivalence.

The operational question is:

> What must be measured now so that, for the future tasks we care about, older measured history no longer improves prediction?

This shifts the concept of biological state from a philosophical label to an experimentally testable object.

## 2. Task-relative state sufficiency

Let the latent biological configuration be x, an observation map be z = h(x), and a task-relevant future be y = F(x). A local necessary geometric condition for z to retain all infinitesimal directions relevant to the task is

`ker(Dh_x) subseteq ker(DF_x)`.

Equivalently, every local latent direction invisible to the measurement must also be irrelevant to the specified future. For a family of interventions Π, the required condition becomes stricter because the measurement must preserve directions relevant to every F_π.

This formulation makes state dimension explicitly conditional on the observation stack and the task. A low-dimensional molecular measurement can be sufficient once geometry is known without implying that the organism itself has a low-dimensional state.

## 3. Predictive screening-off, loss functions, and calibration

Let `H` denote measured past, `S` measured current state, and `Y` a specified future outcome. For a prediction loss `L`, define the Bayes risk from an information set `Z` by

`R*_L(Y|Z) = inf_f E[L(Y,f(Z))]`

and define the population value of older history beyond the current state as

`V_L(H->Y|S) = R*_L(Y|S) - R*_L(Y|S,H)`.

This quantity is nonnegative at population level because a predictor given `(S,H)` can ignore `H`.

Under logarithmic loss, the Bayes-optimal prediction is the true conditional distribution and

`V_log(H->Y|S) = H(Y|S) - H(Y|S,H) = I(Y;H|S)`.

Thus, under standard regularity assumptions, zero **population** log-loss gain is equivalent to conditional independence `Y independent of H | S`. This is established information/decision theory rather than a new definition introduced here.

Squared loss is weaker. If `Y` is square-integrable, the Bayes predictor is the conditional mean and

`V_2(H->Y|S) = E[(E[Y|S,H] - E[Y|S])^2]`.

Therefore zero squared-loss or R² gain means only that history fails to improve the conditional mean under the population-optimal decoder. History may still alter variance, tails, or multimodality. This distinction is important for developmental systems.

Finite estimators introduce a second qualification. Even though population Bayes value is nonnegative, held-out history gains can be negative when the larger model pays an estimation or regularization penalty. Consequently every empirical screening-off claim in this work is indexed by the future task, loss, observation stack, decoder family, developmental compartment, and finite-sample calibration.

A further monotonicity conjecture was falsified. Residual conditional mutual information need not decrease when present-state measurements are added. If independent fair bits `H,Z` generate `Y = H xor Z`, then `I(Y;H)=0` while `I(Y;H|Z)=1 bit`. Thus adding a present variable can *unmask* historical dependence. This does not contradict monotone refinement of counterfactual inverse fibers when additional experimental coordinates are appended under a fixed product/sup metric; the two objects obey different mathematics.

Finite-sample calibration is therefore mandatory. In separate known-complete and known-history-dependent simulations, positive residual-history statistics can arise under a true Markov generator, while genuine residual effects can be missed at small sample size. We report both false-positive and power calibration rather than treating an arbitrary history-gain threshold as proof of closure.

A second failure mode emerged from independent public Cell Tracking Challenge datasets. In *Drosophila* and *Tribolium*, adding older trajectory information could improve held-out R² even when the augmented predictor itself did not transfer to the held-out acquisition. In *Tribolium* an apparent nonlinear history increment reached roughly `+0.42` at a coarse present representation while absolute augmented prediction still failed the preregistered cross-acquisition gate. A richer R7 present representation with about 46–49 relational and kinematic features likewise failed adequacy in every frozen organism/outcome task. We therefore require the empirical decision order **absolute held-out adequacy against a train-only naive baseline, then history-increment stability, then matched sensitivity calibration, then scoped biological interpretation**. A positive increment inside an inadequate predictor is not evidence of biological memory.

## 4. Direct-source flower atlas reanalysis

We independently reconstructed the public FM1 Arabidopsis flower atlas from the original Refahi et al. repository at frozen upstream commit `95fde8b`. The released lineage object, cell geometry and regulatory-pattern files permit a direct task-specific screening analysis.

A critical provenance correction is that the gene channels are **integrated atlas annotations**, not 25 simultaneous molecular assays in every exact tracked cell. The primary paper states that expression patterns were manually integrated into the FM1 4-D template from published information together with RNA in-situ and live-imaging data, using binary presence/absence annotations. We therefore refer to this object as an **atlas state** rather than a directly co-measured molecular state.

For 760 eligible 120 h cells grouped into 233 distinct 96 h ancestors, the target is lineage log-volume expansion to 132 h. Grouped outer folds keep descendants of the same 96 h ancestor together. Nested Ridge prediction gives approximately:

- current geometry: R² = 0.0333;
- current geometry + 120 h atlas state: R² = 0.2846;
- current state + 96 h ancestor history: R² = 0.2928.

A random-forest sensitivity analysis gives approximately 0.300, 0.352 and 0.330 respectively. Thus the current atlas state contributes substantial future-growth information beyond geometry, whereas the older-history increment is small and model-sensitive.

The authors' repository independently defines the L1 epidermal layer. In the predefined late-L1 cohort (256 eligible 120 h cells in 86 ancestor groups), nested Ridge gives

- geometry: R² = 0.3634;
- current geometry + atlas state: R² = 0.5947;
- current + 96 h history: R² = 0.5956.

Random forest gives approximately 0.620, 0.670 and 0.666. This is the strongest reproduced task-specific screening-off pattern in the public atlas, but calibration shows that the cohort has only about 73% power for a synthetic 0.20 target-SD residual history effect and reaches roughly 98% around 0.30 SD. Small residual effects therefore remain unresolved.

A developmental-window sweep complicates any simple “early memory / late Markov” narrative. In predefined L1 cells, the 40->96->120 h middle window shows a large history gain under some Ridge partitions but only a small or negative gain under tree decoders. Decomposition shows that the linear gain is driven primarily by the older 40 h atlas annotation rather than older geometry. A group-preserving permutation test confirms that this old atlas block contains incremental linear predictive structure, yet nonlinear models absorb most of the same signal from the current state. We therefore label this interval **estimator-dependent / unresolved**, not intrinsically non-Markovian.

Because the middle cohort contains only 30 history-time ancestor groups, we explicitly stress-tested outer-fold assignment. Across 200 independently shuffled five-fold ancestor-group partitions with fixed Ridge, middle-L1 history gain has median **+0.144 R²**, is positive in **90.5%** of partitions, but has wide 2.5th–97.5th split quantiles **[-0.051,+0.251]**. Late L1 has median **-0.015 R²**, is positive in only **4%** of partitions, and never exceeds +0.05. A smaller repeated ExtraTrees sensitivity run does not reproduce a material middle history gain.

The same partition stress test under a Gaussian proper score gives middle-L1 median history value **+0.109 bits/cell** across 100 shuffled group partitions (positive in 89%) but with wide split sensitivity, versus late-L1 median **-0.035 bits/cell** (positive in only 3%; no partition above +0.05 bits). These partition quantiles are not confidence intervals; they quantify dependence on the lineage-group split. The strongest conclusion is therefore a **partition- and decoder-dependent middle residual contrasted with a much more partition-stable late near-zero residual**. Exact distributional conditional independence remains unproven because the decoder family is restricted and small effects remain underpowered.

### External positive control for state incompleteness

A screening-off method is not credible if it only finds examples of apparent completion. We therefore applied the same conceptual logic to the public Weinreb et al. LARRY split-well hematopoietic lineage dataset, where the original study independently established hidden heritable fate properties not resolved by measured transcriptomic state.

Using only the released metadata and clone matrix, a release-native reconstruction identifies 504 split clones with mature cells in both day-6 wells. Exact mature-fate-set agreement between separated sister wells is 57.9% versus 17.4% after clone-label permutation (`p≈0.0002`). In a frozen 133-clone neutrophil/monocyte/basophil cohort, a reduced day-2 state proxy (mean SPRING coordinates + starting population) yields about 0.618 balanced accuracy for the other well's dominant fate; adding the separated sister-well fate raises this to about 0.827 and reduces log loss by about 0.38. Conditional mutual information between sister-well fates remains approximately 0.58–0.69 bits after conditioning on several coarse day-2 state partitions, far above within-state permutation nulls.

This is not an exact reproduction of the original Figure 3 cohorts and does not test the full scRNA-seq vector. Its role is methodological: the framework can flag a measured present-state proxy as incomplete in a published system where the underlying biology is already known to contain lineage-linked hidden fate information.

Earlier internal flower analyses reported one-PC and multi-window results with stronger molecular wording. Those analyses remain legacy results until their exact code and data transforms are migrated into the public repository; the direct-source atlas reconstruction above supersedes them for current public claims.

## 5. Finite-count seed state inference

Germination assays are frequently represented as percentages, including saturated 0% and 100% values. If those percentages are treated as continuous measurements with empirical variance, saturation can create a false impression of zero measurement noise and therefore infinite information.

The corrected generative model treats observed germination as finite counts:

`K_gj ~ Binomial(n_gj, p_gj)`

with

`logit(p_gj) = alpha_j + c_g^T l_j`.

Boundary observations then provide strong but finite evidence. This preserves the correct likelihood geometry and supports held-out inference of latent dormancy/response coordinates without treating 0/100 observations as exact continuous states.

## 6. Counterfactual developmental tomography

Historical project work reported a synthetic developmental system with 14 regulatory architectures and 16 hidden states (224 joint hidden worlds) in which baseline morphology collapsed distinct hidden worlds that separated under intervention. The original 224-world generator/source/output chain has not been recovered in the current workspace, so that example is retained as historical motivation rather than reproduced evidence. A separate later 128-world source-validation bundle is reproducible and must not be conflated with it.

The motivating idea is **counterfactual developmental tomography**: reconstructing hidden developmental organization from a deliberately chosen set of perturbational projections rather than from a single unperturbed phenotype. The current evidence for this idea therefore comes from the separately preserved finite optimization and prospective source-simulator artifacts described below, not from treating the historical 224-world numbers as revalidated.

### Prospective two-context source-simulator validation

A later post-hypothesis source-simulator experiment tests a much sharper claim than the original 224-world discrimination example. In the restricted four-channel model, context `q` reflects selected signed coordinates before a rectifying gate,

`u_q(s)=[-R_q s]_+`.

For complementary contexts `q` and `qbar`, the two rectified signals satisfy

`R_q s = u_qbar-u_q`.

This positive/negative-part identity is the same information-preserving principle used by Concatenated ReLU (CReLU); we do **not** claim the rectifier algebra as novel. The scientific test is whether the hidden signed state remains recoverable when only the downstream source-rendered phenotypes are observed and must be inverted through a frozen nonlinear morphogenetic decoder.

The parent experiment was frozen before 64 new source phenotypes were rendered. Its canonical pre-render SHA-256 commitment is

`b5fdc0bd257dbb57874f107b3c7a12b6c9fe5ec9f89cb48de585743846341c3a`.

The frozen predictions required 100% sign recovery across 32 complementary pairs, median signed-state L2 below `0.001`, maximum below `0.002`, and correct sign recovery of deliberately weak `0.001` coordinates. With the frozen decoder and no post-render refit, all predictions passed:

- sign accuracy: **100%**;
- median signed L2: `1.75175e-4`;
- p95: `4.28985e-4`;
- maximum: `5.14625e-4`;
- every `0.001` weak-channel sign correct.

A separately frozen context-generalization extension rendered 64 previously unseen contexts for the same eight partially observed laws. It evaluated the five masks `0111,1011,1101,1110,1111`, which are exactly sufficient at the latent level in the fixed-budget four-channel model. Every mask achieved 100% sign recovery and satisfied the frozen median `<0.001` and maximum `<0.002` error thresholds. The extension is prospective with respect to **new contexts/masks, not new laws**.

The public repository now contains all 128 source TSV renders, both frozen preregistrations, frozen decoder models, exact score/build scripts and independent hash-verification code. This upgrades the result from an archived retrospective report to a verifiable prospective **source-simulator** validation. It remains computational evidence only; no living biological system has yet passed this test.

The key scientific transition is from asking

`What does the organism look like?`

to asking

`Which hidden worlds remain compatible with everything the organism has done under the questions we have asked?`

## 7. Connected causal fibers and global branch completion

Let W be the joint state-law space. For intervention panel Q, define the observation map H_Q. For target world w* and phenotype tolerance δ, define

`K_Q^δ(w*) = {w : max_{q in Q} d(h_q(w), h_q(w*)) <= δ}`.

Rather than only counting K, we track the connected component containing the target:

`C_Q^δ(w*) = Comp_{w*} K_Q^δ(w*)`.

This distinguishes **accommodation**—how closely an alternative mechanism can imitate the target phenotype—from **accessibility**—whether a continuous path through admissible mechanism space connects the target to that alternative at the declared tolerance. Earlier project notes reported specific 224-world and seam/merge thresholds, but the original historical generator/source/topology chain was not recovered in the current provenance audit. Those numerical thresholds are therefore retained only as historical motivation, not as current reproduced evidence. The reproducible topology claims below use separately preserved artifacts.

A more general mathematical issue arises even before a tolerance graph is chosen. Let `h:X->S` be a smooth submersion and `F:X->Y` smooth. If

`ker Dh_x subset ker DF_x`

for every x, then F is constant on each **connected component of each measurement fiber**. Thus F factors through the quotient that identifies points lying in the same connected fiber component. It need not factor through h itself when a fiber is disconnected. The elementary example `X=R\{0}`, `h(x)=x^2`, `F(x)=x` satisfies the local kernel condition but merges positive and negative branches with different futures; a branch/sign coordinate repairs the factorization.

For a finite fiber containing m future-distinct connected-component classes, any exact discrete branch code needs at least `ceil(log2 m)` bits. This is a set-theoretic label bound, not a statement about physical sensor precision. A synthetic noisy-history example shows the statistical consequence: older history can carry residual predictive information only because it proxies for an omitted branch coordinate, and become redundant once that coordinate is measured. This gives one concrete mechanism by which residual history may indicate present-state incompleteness without implying a distinct biological memory variable.

## 8. Topology-aware experimental design and continuous measurement obstructions

Adding an intervention refines the set of candidate worlds that remain observationally compatible. Several objectives are useful, but they must not be conflated. Pairwise separation of a finite world library is a Minimum Test Collection / coverage problem with classical set-cover structure. By contrast, shrinking the connected component containing a target world can be non-submodular.

On the preserved **128-world** simulator bundle, exhaustive enumeration across 128 truths, nine tolerances, three topology settings, and budgets 1–5 produced 17,280 audited rows; ordinary greedy selection matched the exact optimum on every one of those rows. This is an instance certificate, not a theorem. Explicit four-cycle and grid constructions show that the connected truth-rooted objective is non-submodular in general and that a greedy/optimal utility ratio can scale as `3/n -> 0`. Robustification does not automatically restore structure: pointwise minimax and one-failure objectives can also destroy submodularity. These counterexamples make exact optimization or proved structural assumptions mandatory when feasible.

The T5 branch quotient introduces a second design question: how many **continuous measurement channels** are required to realize a missing branch coordinate globally? Define `cdim_R(h,F)` as the minimum k such that a continuous augmentation `B:X->R^k` separates every collision of h whose futures differ. For the antipodal quotient `h:S^n->RP^n` with `F(x)=x`, Borsuk-Ulam gives the exact dimension

`cdim_R(h,F)=n+1`.

Each fiber contains only two states—one exact discrete branch bit—yet a globally continuous Euclidean completion may need n+1 channels. For `z->z^2` on `S^1`, one real scalar cannot separate every antipodal pair whereas two real coordinates suffice. This is an application of established Borsuk-Ulam, covering-space, configuration-space and projected-embedding (`k`-prem) ideas, not a claim of new topology.

The obstruction has a sharp task-relative approximate form. With Euclidean future loss on `S^n`, every continuous augmentation with `k<=n` forces minimax worst-case error exactly 1; the lower bound follows from one forced antipodal collision and the triangle inequality, and the zero decoder attains it. Thus no dimensional reduction permits worst-case error below the sphere radius. Conversely `B(x)=x` in n+1 channels gives exact decoding and antipodal sensor margin 2 in normalized units.

For a compact finite cover over a Hausdorff base, any continuous fiberwise-injective Euclidean augmentation has a positive global within-fiber separation margin `Delta_B`. If the base measurement is known exactly and only the augmentation receives adversarial additive noise of norm at most η, exact sheet recovery is guaranteed when

`2 η < Delta_B`.

At or above the attained minimum-margin threshold, uniform exact recovery cannot be guaranteed. The raw margin is scale-dependent and therefore only meaningful relative to fixed sensor units/noise normalization. These results motivate a practical distinction between **topological possibility** (enough channels exist), **robust realization** (branches are separated by a useful margin), and **statistical learnability** (finite data and model class can exploit the measurement).

## 9. Developmental state completion

The ideas above combine into a recursive experimental criterion. Randomize an intervention T, measure old history H, measure a candidate current state S after perturbation, and then apply preregistered future challenges π with outcomes Y_π.

A strong candidate state should satisfy approximately:

- T moves S;
- S predicts Y_π;
- older history H and original treatment T add little predictive information about Y_π once S is known, within calibrated estimator uncertainty.

Then introduce a new future challenge. If old history becomes useful again, the present state representation is incomplete. The newly exposed residual points toward the next missing measurement or perturbation.

## 10. Relationship to existing work

The framework overlaps with established fields including predictive cell-state modeling, lineage tracing, fate forecasting, perturbation-response mapping, active experimental design, neutral networks, and topological data analysis. Recent work such as FateLimit explicitly quantifies prediction horizons from present molecular states, and high-throughput perturbational platforms map developmental phenotypes under controlled interventions.

The candidate novelty here is therefore not "predictive cell state" or "topology in biology". It is the combined operational program of:

- completing a present state until older measured history is screened off for specified future interventions;
- representing residual uncertainty as a connected causal fiber in joint state-law space;
- selecting new perturbations to split the topology of that residual ambiguity.

The mathematical prior-art boundary is now sharper. Predictive screening-off and future-equivalence quotients overlap causal states, predictive-state representations, observability/identifiability and bisimulation; finite pair separation overlaps Test Cover/separating systems; continuous fiberwise Euclidean completion overlaps projected-embedding / `k`-prem problems; and the antipodal lower bounds are direct applications of Borsuk-Ulam/equivariant topology. The project-specific contribution sought is the integration of these established ideas into one task- and intervention-indexed workflow with explicit adequacy, calibration, topology, robustness and falsification gates. No mathematical priority claim is made for the underlying ingredients.

## 11. Decisive biological experiment

The strongest next test is prospective and blinded. Select biological backgrounds that are deliberately similar at baseline but mechanistically distinct. Freeze the baseline morphology model. Allow the algorithm to choose a small perturbation panel. Apply those perturbations under randomization and predict hidden background before unblinding.

The primary comparison is:

- baseline morphology discrimination;
- random/equal-cost perturbation discrimination;
- topology-aware designed perturbation discrimination.

A successful result would demonstrate that the system extracts mechanistic information unavailable from static phenotype alone. Replication in an independent cohort or laboratory would be required before strong biological claims.

## 12. Limitations

The current work has major limitations:

- the strongest biological evidence remains computational reanalysis of released data; no living-system state-completion claim has been validated prospectively;
- the original historical 224-world generator/source/topology chain and exact legacy FM1 `0.272 -> 0.643` tuple remain provenance-incomplete and are excluded from current reproduced evidence;
- R2 *C. elegans* is calibration-limited despite large observed nonlinear history increments;
- R5/R6/R7 show that cross-acquisition predictive adequacy can fail even when residual-history increments look large, so those datasets currently diagnose representation/transfer failure rather than memory or closure;
- R3 LARRY uses separated sister-well fate as a lineage-linked incompleteness diagnostic, not literal older history, and the tested 32-gene present panel is not the full transcriptome;
- the R4 GSE167135 execution is a same-time measurement-completeness proxy, not a future-outcome test;
- morphology and topology depend on the declared observation map, future task, metric, intervention family, tolerance and admissible state-law space;
- the T5–T7 topological results are established-mathematics applications/syntheses and do not by themselves show that a living developmental system has a nontrivial cover, branch coordinate or topological measurement obstruction;
- continuous-channel lower bounds assume globally continuous Euclidean measurements; discontinuous/local-chart, non-Euclidean, intervention-assisted or otherwise structured observations can obey different constraints;
- robust sensor margins require fixed units/noise models, and the compact-cover guarantee uses standard separation hypotheses such as a Hausdorff base;
- screening-off estimates remain sensitive to finite-sample bias, decoder choice, calibration power and group/domain shift;
- synthetic hidden-world and source-simulator results may not transfer to living biology;
- no current result establishes clinical, therapeutic or agronomic efficacy.

## 13. Open problems

1. Define robust, admissible-measurement counterfactual embedding dimension under noise; bare exact dimension on finite libraries is not informative because generic scalar projections are injective.
2. Establish stability bounds for connected causal fibers under metric perturbation and discretization.
3. Determine when topological experiment objectives outperform Fisher/Shannon objectives.
4. Develop calibrated conditional-independence tests tailored to longitudinal developmental data.
5. Identify minimal safe living systems for prospective blinded validation.
6. Characterize when state completion transfers across future-task families.

## Conclusion

The central proposal is simple to state: **do not declare the developmental state; experimentally complete it until the past stops helping for the futures you care about.** When the past still helps, treat that failure as information about what is missing. When multiple hidden mechanisms remain compatible with observation, use the topology of that ambiguity to choose the next experimental question.

Whether this becomes a useful biological theory depends on prospective replication. This repository is intended to make that test possible.
