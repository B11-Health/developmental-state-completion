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

## 3. Predictive screening-off and its calibration

Let H denote measured past, S measured current state, and Y a future outcome. Two conditional information quantities organize the problem:

`J = I(Y; S | H)`

and

`M = I(Y; H | S)`.

J measures future-predictive information present in current state beyond measured history. M measures predictive history the candidate current state failed to absorb. The experimental regime of interest is positive J with small M.

However, finite predictive estimators do not provide an exact conditional-independence test. In our calibration, a known-Markov ABA–GA simulator generated a positive old-history R² gain near +0.03 under a boosted-tree procedure even though the full simulator state is Markov by construction. Consequently, fixed history-gain thresholds cannot prove Markov closure. All screening-off statements in this program are therefore estimator- and uncertainty-qualified.

## 4. Flower lineage reanalysis

In a lineage-resolved flower dataset, the original discovery analysis suggested that recent molecular measurements add substantial predictive power for subsequent growth beyond geometry and prior trajectory. The strongest reported FM1 result was approximately:

- trajectory/geometry prediction: R² ≈ 0.272;
- plus one unsupervised molecular PC: R² ≈ 0.643;
- all 25 molecular measurements: R² ≈ 0.633;
- additional older molecular history after current state: approximately +0.0095 R².

The appropriate interpretation is not that the biological state is one-dimensional. Rather, conditional on the geometry already observed, one dominant molecular direction may fill much of the remaining task-relevant information gap.

A separate validation sweep across 24 eligible lineage windows in five other WT flowers reported a median older-history gain of approximately 0.0033 R² after conditioning on recent state, with 22 of 24 windows below +0.05. These values require code-level reproduction in this repository and should presently be treated as reported reanalysis results.

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

In the sampled complex, an alternative mechanism family reportedly appeared at phenotype error near 0.000335 but did not merge with the target component until roughly 0.001543, creating a persistent topological gap. At a narrow transition near the main saddle, the target component reportedly expanded from approximately 221 to 2012 sampled mechanisms and from one hidden-state chamber to four.

These are finite-grid computational observations, not continuum theorems.

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
