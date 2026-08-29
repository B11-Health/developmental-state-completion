# LAB LANE N1 — Novelty & Literature Red-Team

**Date:** 2026-08-29  
**Scope:** developmental-state-completion public repo at `b9f21bb`; current claim ledger, mathematics checkpoint, FM1 replication checkpoint, preprint, README, and prior novelty-lane source trace.  
**Operating rule:** adversarial. Similarity is treated as evidence *against* novelty unless a precise residual difference survives.

## Executive verdict

The project should **not** claim novelty for any of the following ideas in isolation:

- defining state by predictions of future observations or intervention-conditioned tests;
- grouping histories that have the same predictive future;
- screening off older history with a sufficient present state;
- inferring latent state and unknown parameters jointly from input-output experiments;
- using connected components of fibers / level sets as a topological object;
- using perturbations to reveal hidden mechanistic differences masked at baseline;
- selecting interventions adaptively for causal or perturbational learning;
- predicting cell fate from present molecular state;
- mapping high-dimensional perturbation responses;
- cryptic genetic/developmental variation hidden under a conserved phenotype.

Those are all strongly precedented.

The narrowest defensible candidate contribution is a **specific developmental-biology synthesis and test protocol**:

> For a predefined developmental task and intervention family, test whether a physically measurable current state makes older measured history predictively redundant under calibrated held-out scoring; represent the residual *joint state-law* ambiguity as a connected finite-resolution inverse-fiber component; and choose follow-up perturbations specifically to split that residual component, with prospective blinded validation against baseline-only and equal-cost/random perturbation comparators.

Even this must currently be described as a **candidate synthesis / research program**, not as “the first” or “unprecedented.” I did not find, in this pass, a single prior paper that combines all three pieces in this exact developmental setting, but each piece has close established ancestors.

The strongest genuinely project-specific scientific outputs today are **evidence and falsifications**, not a new universal theory: (i) direct-source FM1 task-specific screening behavior with a strong late-L1 case but estimator-dependent middle window; (ii) an external Weinreb/Klein incompleteness control; (iii) a frozen prospective source-simulator perturbation result; and (iv) a counterexample showing the project's connected-component reduction objective can make greedy selection arbitrarily bad. These should be reported as results, not as proof of a new biological law.

---

## Closest-precedent table

| Project idea / phrase | Closest precedent(s) | Exact overlap | Residual difference that may survive | N1 verdict |
|---|---|---|---|---|
| **Developmental state completion** as “present state screens off older history for specified futures” | Shalizi & Crutchfield, *Computational Mechanics: Pattern and Prediction, Structure and Simplicity* (2001); predictive-state representations (Littman, Sutton & Singh 2001/2002; Singh, James & Rudary 2004); input-output computational mechanics (Barnett & Crutchfield 2015) | Causal states identify histories by identical future distributions; PSRs represent state using predictions of action-conditioned future tests; epsilon-transducers extend predictive equivalence to input-output processes. | Biological operationalization: demand a **physically measurable** present developmental state, calibrate residual history value statistically, and deliberately add future biological challenges to expose missing state directions. | **Broad novelty rejected. Narrow biological synthesis survives.** |
| **Counterfactual developmental tomography** | Classical system identification / observability; Hermann & Krener (1977); Villaverde's structural identifiability/observability work in nonlinear biological systems; Perturb-seq (Dixit et al. 2016); CPA and modern perturbation-response prediction | Inputs/perturbations are used to infer hidden state, dynamics, parameters, or responses that static observations cannot identify. | Emphasis on *baseline-similar developmental backgrounds* and on using a small designed perturbation panel to discriminate joint state-law worlds from morphology-level readouts. The label “tomography” is branding, not a new mathematical principle. | **Conceptual novelty weak; experimental packaging potentially useful.** |
| **Joint state-law world** `w=(theta,x)` | Augmented-state observability / structural identifiability in nonlinear systems; parameter-as-state formulations; system identification | Unknown dynamical parameters and state are inferred together from measured outputs under inputs. | Developmental-biology interpretation and coupling to finite-resolution inverse-fiber topology. | **Mathematical novelty rejected.** |
| **Connected causal fiber** `C_Q^delta(w*)` | Reeb spaces / Stein factorization; Basu, Cox & Percival (2018) on Reeb spaces of definable maps; broad level-set / inverse-image topology | Reeb/Stein constructions collapse or organize connected components of fibers of a map; connected preimage structure is classical. | Here the map is an experiment-indexed counterfactual phenotype signature on a joint state-law space, and the project follows the *target component under finite tolerance* rather than constructing the complete Reeb quotient. | **Topological object not new; application and target-relative finite-resolution use may be distinctive.** |
| **Accommodation vs accessibility / cryptic mechanism islands** | Neutral networks/genotype networks; Ciliberti, Martin & Wagner 2007; Wagner 2008; developmental-system drift (True & Haag 2001; McColgan et al. 2024 review) | Same or similar phenotype can be produced by different genotypes/mechanisms; neutral sets can have nontrivial connectivity and access different neighboring phenotypes. | Explicitly measuring phenotype-error accommodation separately from the tolerance needed to continuously connect mechanisms in a developmental state-law model. | **Analogy/metric may be useful, but broad idea strongly precedented.** |
| **Topology-aware experiment selection** | Hauser & Bühlmann 2014 active intervention design; Li et al. 2020 active learning for homology; IterPert (Huang et al. 2024) for sequential perturbation design; BRAL (Wang & Medina-Mardones 2026) topology-aware acquisition; Sharifian et al. 2025/2026 connected-component rewards in causal experiment design | Experiments are adaptively chosen to reduce uncertainty, identify causal structure, explore perturbation space, or recover topology; some recent work uses connected-component/topological rewards directly. | The project's objective is specifically the size/shape of the **target-connected inverse-fiber ambiguity in joint state-law space**, not graph SCC orientation, decision-boundary homology, or rare-cell topology. | **“Topology-aware active design” is not novel. Exact objective may be project-specific, but must be stated narrowly.** |
| **Greedy connected-ambiguity selection can fail arbitrarily badly** | Classical submodular design gives guarantees only under diminishing returns; related causal-design papers establish adaptive submodularity for different graph objectives. | Prior theory already warns that greedy guarantees are objective-dependent. | The repo has a concrete counterexample for *this exact target-component reduction objective*, with ratio `3/n -> 0`. I did not locate an exact prior statement for this precise objective in this pass. | **Potentially original narrow theorem/counterexample; literature search not yet exhaustive enough to claim first.** |
| **Current molecular state predicts future fate/growth** | Jang et al. 2017; Waddington-OT (Schiebinger et al. 2019); Weinreb et al. 2020; CellRank (Lange et al. 2022); FateLimit (Sung et al. 2026 preprint) | Present cell state is used to predict future trajectories/fates; prediction horizons and fate probabilities are explicit research targets. | The FM1 question is not generic fate prediction but *incremental value of older measured history after current atlas state*, calibrated against known-complete and known-history-dependent controls. | **Prediction novelty rejected; calibrated history-redundancy test is the narrower angle.** |
| **Developmental memory / old history retains information** | Vernalization/FLC epigenetic memory in Arabidopsis; lineage-linked heritable fate bias in Weinreb et al. 2020; extensive epigenetic/developmental memory literature | Past exposures or lineage history can remain encoded and affect future behavior. | Treating residual predictive value of history as a falsifier of a proposed current-state representation, rather than claiming memory itself is new. | **Novelty rejected.** |
| **Perturbation-response mapping** | Perturb-seq (Dixit et al. 2016 and followups); CPA (Lotfollahi et al. 2023); GEARS/scGen/modern perturbation models; IterPert | High-dimensional perturbations are mapped to molecular/cellular responses and predicted counterfactually. | Restricting the goal to discrimination of baseline-similar developmental mechanism alternatives and measuring contraction of a pre-specified ambiguity set. | **Field-level novelty rejected.** |
| **Cryptic variation exposed by perturbation** | Cryptic genetic variation (Gibson & Dworkin 2004; Paaby & Rockman 2014); developmental system drift (True & Haag 2001); genotype-network robustness/evolvability literature | Hidden variation can be phenotypically silent in one condition and revealed in another; conserved phenotype can mask mechanistic divergence. | An algorithmic experimental-design loop that chooses perturbations to maximally distinguish currently compatible state-law alternatives. | **Biological premise not new; inference/design loop may be a useful synthesis.** |

---

## Domain-by-domain red-team findings

### 1. Predictive-state representations

This is the most damaging precedent to any broad “new definition of state” claim. Littman/Sutton/Singh explicitly represent state using multi-step, action-conditional predictions of future observations. Singh/James/Rudary formalize PSRs as a theory of dynamical systems. Therefore phrases such as “we discovered that the real state is the set of future responses” are indefensible.

**Residual:** the project can ask a biological measurement question PSR theory does not answer: whether a finite *physical molecular/morphological measurement stack* approximates a predictive state for a specified developmental intervention family.

### 2. Computational mechanics / epsilon-transducers

Shalizi/Crutchfield causal states group histories by predictive equivalence. Barnett/Crutchfield's epsilon-transducer extends computational mechanics to structured input-output processes. This directly precedents “histories are equivalent if all allowed future inputs lead to the same output law.”

**Residual:** translating this into a prospectively testable developmental measurement protocol with explicit biological interventions, calibration, and falsification.

### 3. Observability / structural identifiability

Hermann-Krener observability and modern nonlinear biological identifiability already cover recovering hidden state from outputs under inputs. Villaverde and STRIKE-GOLDD/FISPO explicitly connect unknown parameters and states in nonlinear biological systems.

**Residual:** using a finite-resolution *connected ambiguity component* as a descriptive object after conventional identifiability fails, rather than only returning rank/identifiability status.

### 4. Reeb spaces / Stein factorization

Connected components of fibers are classical. The project's “connected causal fiber” cannot be marketed as a new topological construction.

**Residual:** target-relative tracking under an expanding panel of experimental coordinates, with phenotype tolerance and biological mechanism-space interpretation. That is an application choice, not ownership of Reeb topology.

### 5. Active experimental design

Active selection of interventions is established in causal discovery and modern single-cell perturbation screening. IterPert is especially close biologically: it sequentially chooses perturbations under budget to improve prediction. Recent BRAL is explicitly topology-aware, and recent causal-design work uses connected-component rewards.

**Residual:** optimize *target-connected inverse-fiber splitting* rather than prediction error, entropy, edge orientation, or rare-lineage discovery. The repo's negative result about greedy is important because it differentiates this objective mathematically from standard submodular pair-coverage objectives.

### 6. Developmental memory and fate prediction

The developmental-memory literature is enormous. Arabidopsis FLC vernalization is a canonical example where past cold is stored epigenetically. Weinreb et al. showed lineage-linked fate information hidden from measured transcriptional state. Fate-prediction methods and FateLimit already ask how far future fate can be predicted from present molecular state.

**Residual:** the project's calibrated question is comparative: *how much predictive value remains in older measured history once a candidate present state is known?* This is a narrower diagnostic than “predict fate.”

### 7. Perturbation-response mapping

Perturb-seq and successors already make interventions a systematic coordinate system for cellular response. CPA-like models explicitly forecast counterfactual perturbation responses.

**Residual:** treating perturbations as probes to identify *which hidden developmental world* is present, rather than mainly predicting expression response.

### 8. Evo-devo cryptic variation

Developmental system drift and cryptic genetic variation already establish that phenotypic similarity can hide mechanistic/genetic divergence and that perturbations/environments can expose hidden differences.

**Residual:** a formal, task-relative finite-resolution ambiguity set plus an algorithmic rule for choosing the next probe.

---

## Narrowest defensible public novelty statement

### Recommended

> **We are developing and testing a developmental-biology workflow that asks whether a physically measurable present state is sufficient for specified future interventions, using calibrated residual-history prediction as the diagnostic. When it is not sufficient, we represent the remaining joint state–law alternatives as a finite-resolution connected inverse-fiber component and choose perturbations to split that specific residual ambiguity. Each ingredient has strong precedent in predictive-state theory, observability, topology, and experimental design; the candidate contribution is their task-specific integration and prospective biological validation.**

### Even safer one-sentence version

> **The candidate contribution is not a new definition of state or a new topology, but a falsifiable experimental workflow for measuring when a developmental state is predictively sufficient and for choosing perturbations against the specific mechanism ambiguity that remains.**

### What we can say about current evidence

- Direct-source FM1 reanalysis supports a **task-specific late-L1 screening pattern**, not universal Markov closure.
- The middle L1 window is **estimator- and split-dependent**, which actively argues against a simple universal completion story.
- The Weinreb/Klein reanalysis is a useful **positive control for incompleteness**.
- The two-context experiment is **prospective source-simulator validation**, not living-plant validation.
- The connected-component greedy counterexample is a **narrow mathematical negative result** for the project's exact objective, not a general theorem about active learning.

---

## Phrases Alfredo must never use publicly

1. **“We discovered the true state of development.”** No. State is task- and measurement-relative here.
2. **“We invented predictive state.”** Directly contradicted by PSR and computational-mechanics literature.
3. **“We proved development is Markovian.”** The FM1 result is finite-sample, task-, compartment-, loss-, and decoder-relative; exact conditional independence is unproven.
4. **“The plant forgets its past.”** Biologically false as a general statement; plant developmental/epigenetic memory is well established.
5. **“One molecular dimension controls flower development.”** The repo itself falsifies that interpretation; the finite-state projection trap and Ridge results rule it out.
6. **“Connected causal fibers are a new topology we invented.”** Reeb/Stein fiber-component topology is established.
7. **“Counterfactual developmental tomography is a new mathematical field.”** The name may be new branding; the underlying system-identification logic is not.
8. **“No one has used perturbations to reveal hidden biological state before.”** Perturb-seq, systems identification, causal discovery, lineage/fate work, and classical genetics make that untenable.
9. **“Our algorithm finds the optimal experiment.”** The repo contains a proof that greedy can be arbitrarily bad for the connected-component objective.
10. **“Our simulations prove a new biological law.”** They do not. They establish computational properties and preregistered simulator performance.
11. **“We have validated this in living plants.”** Not yet.
12. **“We are the first to show identical phenotypes can hide different mechanisms.”** Developmental system drift, cryptic genetic variation, neutral networks, and systems biology long predate this project.
13. **“History is useless once you measure the present.”** The middle FM1 window is a direct warning against this generalization.
14. **“The current 25-gene state was measured simultaneously in the tracked FM1 cells.”** It is an integrated binary atlas annotation assembled onto the reference template.
15. **“This is Nobel-level / paradigm-shifting proof.”** Evidence is not remotely at that stage; public use would damage credibility.
16. **“First ever,” “unprecedented,” “completely new,” “rewrites biology,” or “solves development”** unless a claim-specific systematic review and independent expert review support the exact wording.

---

## Novelty ranking after attack

### Potentially strong, but not yet safe as a priority claim

**Exact connected-target-fiber experiment objective + greedy impossibility result.** The repository has a constructive counterexample with `3/n -> 0`. Related connected-component causal-design objectives exist, but I did not locate this exact target-inverse-fiber objective/counterexample. Before claiming mathematical novelty, search optimization, active diagnosis, test selection, graph interdiction, adaptive submodularity, and topology-aware design literature specifically for equivalent set functions.

### Moderate

**Integrated developmental state-completion workflow.** Strongly derivative ingredients, but the exact pipeline from calibrated residual-history sufficiency -> joint state-law connected ambiguity -> perturbation chosen against that ambiguity -> blinded living validation may be distinctive as a biological program.

### Moderate-to-weak

**Accommodation vs accessibility as a developmental ambiguity diagnostic.** Useful distinction, but it sits close to neutral networks, genotype-phenotype map topology, robustness/evolvability, and Reeb-fiber thinking.

### Weak / naming only

**Counterfactual developmental tomography.** Good communicative label, but not safe as a claim of conceptual priority.

### Rejected

Predictive-state mathematics; screening-off principle; joint state/parameter inference; Reeb/Stein topology itself; fate prediction; perturbation-response mapping; active intervention selection generically; cryptic variation under conserved phenotype; developmental memory.

---

## Closest sources verified in the existing browser during N1

- Littman, M. L., Sutton, R. S., Singh, S. **Predictive Representations of State.** NIPS 2001 / published proceedings 2002.
- Singh, S., James, M. R., Rudary, M. **Predictive State Representations: A New Theory for Modeling Dynamical Systems.** UAI 2004; arXiv:1207.4167.
- Shalizi, C. R., Crutchfield, J. P. **Computational Mechanics: Pattern and Prediction, Structure and Simplicity.** J. Stat. Phys. 104 (2001), 817–879.
- Barnett, N., Crutchfield, J. P. **Computational Mechanics of Input-Output Processes: Structured Transformations and the epsilon-Transducer.** J. Stat. Phys. 161 (2015), 404–451; arXiv:1412.2690.
- Hermann, R., Krener, A. J. **Nonlinear Controllability and Observability.** IEEE TAC (1977).
- Villaverde, A. F. **Observability and Structural Identifiability of Nonlinear Biological Systems.** Complexity (2019); arXiv:1812.04525.
- Basu, S., Cox, N., Percival, S. **On the Reeb spaces of definable maps.** arXiv:1804.00605.
- Hauser, A., Bühlmann, P. **Two Optimal Strategies for Active Learning of Causal Models from Interventional Data.** IJAR 2014; arXiv:1205.4174.
- Li, W., Dasarathy, G., Ramamurthy, K. N., Berisha, V. **Finding the Homology of Decision Boundaries with Active Learning.** NeurIPS 2020.
- Huang, K., Lopez, R., Hütter, J.-C., Kudo, T., Rios, A., Regev, A. **Sequential Optimal Experimental Design of Perturbation Screens Guided by Multi-modal Priors (IterPert).** RECOMB 2024 / bioRxiv 2023.
- Wang, W., Medina-Mardones, A. M. **Bayesian Rips Active Learning: Topology-Aware Acquisition for Rare Lineages.** ICLR 2026 MLGenX workshop.
- Dixit, A. et al. **Perturb-Seq: Dissecting Molecular Circuits with Scalable Single-Cell RNA Profiling of Pooled Genetic Screens.** Cell 2016.
- Lotfollahi, M. et al. **Predicting cellular responses to complex perturbations in high-throughput screens.** Mol. Syst. Biol. 2023.
- Jang, S. et al. **Dynamics of embryonic stem cell differentiation inferred from single-cell transcriptomics show a series of transitions through discrete cell states.** eLife 2017.
- Schiebinger, G. et al. **Optimal-Transport Analysis of Single-Cell Gene Expression Identifies Developmental Trajectories in Reprogramming.** Cell 2019.
- Weinreb, C., Rodriguez-Fraticelli, A. E., Camargo, F. D., Klein, A. M. **Lineage tracing on transcriptional landscapes links state to fate during differentiation.** Science 2020; PMID 31974159; PMCID PMC7608074.
- Lange, M. et al. **CellRank for directed single-cell fate mapping.** Nature Methods 2022.
- Sung, J. Y. et al. **FateLimit quantifies the prediction horizon of cell fate.** bioRxiv 2026 preprint.
- Berry, S. et al. **Environmental perception and epigenetic memory: mechanistic insight through FLC.** Plant Journal / review literature around 2015; Arabidopsis FLC is a canonical counterexample to any blanket “plants forget history” language.
- True, J. R., Haag, E. S. **Developmental system drift and flexibility in evolutionary trajectories.** Evolution & Development 2001.
- Gibson, G., Dworkin, I. **Uncovering cryptic genetic variation.** Nature Reviews Genetics 2004.
- Ciliberti, S., Martin, O. C., Wagner, A. **Innovation and robustness in complex regulatory gene networks.** PNAS 2007.
- Wagner, A. **Robustness and evolvability: a paradox resolved.** Proc. R. Soc. B 2008.
- McColgan, Á. et al. **Understanding developmental system drift.** Development 2024 review.

## Audit limits

This was a strong adversarial pass using the current repository plus targeted browser literature searches. It is **not** a formal systematic review, citation-network search, patent search, or priority opinion. Any future “first” claim requires a claim-specific search protocol, forward/backward citation chaining, domain-expert review, and preprint/patent checking immediately before publication.
