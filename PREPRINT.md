# Developmental State Completion: Counterfactual Tomography of Hidden Biological Mechanisms

**Working preprint — Code Gym Research — 29 August 2026**

## Abstract

Developmental systems are commonly represented by measured phenotypes, molecular profiles, or inferred trajectories, yet these observations need not uniquely determine the internal state and dynamical law that govern future response. We develop a computational framework for **developmental state completion**: experimentally enriching the present observation until older measured history contributes little additional predictive information for a specified family of future interventions. The framework combines task-sufficient state representations, calibrated predictive screening-off, counterfactual perturbation design, and topology of inverse phenotype fibers. In reanalyses of lineage-resolved flower data, a recent measured molecular state often rendered older measured history nearly redundant for specific future growth tasks, while a known-Markov simulator demonstrated that finite-sample estimators can spuriously produce positive history gain, invalidating simple fixed thresholds. In a finite-count seed germination reanalysis, binomial latent-state modeling corrected pathological certainty associated with 0% and 100% percentage observations. In a synthetic developmental system spanning 224 hidden worlds, baseline morphology collapsed distinct state-law combinations that separated under intervention. A sampled state-law complex further exhibited disconnected mechanism islands within narrow phenotype tolerance, motivating a distinction between phenotypic accommodation and continuous mechanism accessibility. Interventions optimized for splitting the current connected ambiguity differed from those optimized for global parameter estimation, suggesting a topology-aware form of adaptive experimental design. These results do not establish a new biological law; they define a falsifiable research program whose decisive test is prospective, blinded discrimination of baseline-similar living biological backgrounds using algorithmically selected perturbations.

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

We next considered a synthetic developmental system with 14 regulatory architectures and 16 hidden states, producing 224 joint hidden worlds. Baseline morphology can map multiple hidden worlds to nearly identical outputs. A perturbation adds another counterfactual view of the same hidden system and can separate worlds that static appearance collapses.

This motivates the term **counterfactual developmental tomography**: reconstructing hidden developmental organization from a deliberately chosen set of perturbational projections rather than from a single unperturbed phenotype.

The key scientific transition is from asking

`What does the organism look like?`

to asking

`Which hidden worlds remain compatible with everything the organism has done under the questions we have asked?`

## 7. Connected causal fibers

Let W be the joint state-law space. For intervention panel Q, define the observation map H_Q. For target world w* and phenotype tolerance δ, define

`K_Q^δ(w*) = {w : max_{q in Q} d(h_q(w), h_q(w*)) <= δ}`.

Rather than only counting K, we track the connected component containing the target:

`C_Q^δ(w*) = Comp_{w*} K_Q^δ(w*)`.

This distinguishes two properties that static phenotype error conflates:

1. **Accommodation** — how closely an alternative mechanism can imitate the target phenotype.
2. **Accessibility** — how much phenotype deviation must be tolerated before a continuous path through mechanism space connects the target to that alternative.

An earlier coarse grid suggested that a STRETCH-related alternative mechanism appeared near phenotype error `0.000335` and merged with the target near `0.001543`. That continuum interpretation is now **withdrawn**: a later seam-consistent search showed that `0.001543` was a discretization obstruction. The latest recovered source-level checkpoint gives an optimized static accommodation `a_S ≈ 0.0002686301` and a corrected CFLOW escape/merge threshold `m_S ≈ 0.00141094` (cubic surrogate `≈0.001410471`; direct source `≈0.001410939`; independent nearby source sweep `≈0.001412041`). The resulting source-level isolation gap is `Δ_S ≈ 0.00114231`, with `m_S/a_S ≈ 5.25`.

The earlier sampled-grid transition from approximately 221 to 2012 candidate mechanisms remains useful as a **discretized connectivity observation**, but it is not the best estimate of the continuum merge threshold. The corrected seam value is source-validated within the archived simulator checkpoint; a formal global continuum proof and full source-artifact migration remain open.

## 8. Topology-aware experimental design

Adding an intervention refines the inverse fiber. We therefore define a working experiment objective based on contraction of the connected candidate set. A convenient discrete score is a log-volume reduction:

`I_topo(q; δ) = log2( |C_Q^δ| / |C_{Q union {q}}^δ| )`.

This is not Shannon mutual information.

At one reported ambiguity scale, intervention 0010 reduced a connected candidate set from 2030 to 114 nodes. A perturbation previously strong for global parameter recovery, 1011, ranked only 12th for this ambiguity-splitting objective. At a broader tolerance, the best intervention changed to 1010. Thus experimental value depends on the current ambiguity and the scientific objective.

This suggests an adaptive loop:

1. infer the current causal fiber;
2. identify the dominant connected ambiguity;
3. choose a perturbation that most strongly splits that ambiguity;
4. update the fiber;
5. repeat until the remaining uncertainty is below the task-relevant tolerance.

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

A comprehensive literature review is still required before any novelty claim is elevated beyond "candidate contribution."

## 11. Decisive biological experiment

The strongest next test is prospective and blinded. Select biological backgrounds that are deliberately similar at baseline but mechanistically distinct. Freeze the baseline morphology model. Allow the algorithm to choose a small perturbation panel. Apply those perturbations under randomization and predict hidden background before unblinding.

The primary comparison is:

- baseline morphology discrimination;
- random/equal-cost perturbation discrimination;
- topology-aware designed perturbation discrimination.

A successful result would demonstrate that the system extracts mechanistic information unavailable from static phenotype alone. Replication in an independent cohort or laboratory would be required before strong biological claims.

## 12. Limitations

The current work has major limitations:

- several numerical results have not yet been independently re-run from public code;
- synthetic hidden-world results may not transfer to living biology;
- topological structure depends on the chosen biological loss metric and sampling resolution;
- screening-off estimates are sensitive to finite-sample model bias;
- PCA-derived directions are representation-dependent;
- no current result establishes clinical, therapeutic, or agronomic efficacy;
- no formal theorem yet shows that a finite intervention panel reconstructs the full hidden causal topology.

## 13. Open problems

1. Define robust counterfactual embedding dimension under noise.
2. Establish stability bounds for connected causal fibers under metric perturbation and discretization.
3. Determine when topological experiment objectives outperform Fisher/Shannon objectives.
4. Develop calibrated conditional-independence tests tailored to longitudinal developmental data.
5. Identify minimal safe living systems for prospective blinded validation.
6. Characterize when state completion transfers across future-task families.

## Conclusion

The central proposal is simple to state: **do not declare the developmental state; experimentally complete it until the past stops helping for the futures you care about.** When the past still helps, treat that failure as information about what is missing. When multiple hidden mechanisms remain compatible with observation, use the topology of that ambiguity to choose the next experimental question.

Whether this becomes a useful biological theory depends on prospective replication. This repository is intended to make that test possible.
