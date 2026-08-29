# Developmental State Completion

**An open research program on counterfactual developmental tomography, connected causal fibers, and experimentally completing predictive biological state.**

Code Gym research checkpoint — 2026-08-29

> Status: **preprint-stage computational research. Not peer reviewed.** Several results are simulation- or reanalysis-based and require independent biological replication.

## The central question

What must we know about a living system **right now** so that its older measured history becomes unnecessary for predicting what it can do next?

We call the experimental program for answering that question **developmental state completion**.

Rather than assuming that morphology, transcriptomics, lineage history, or any other measurement is "the state," we treat state as a task-relative empirical object. Given old history `H`, a candidate current measurement `S`, and future outcome `Y`, a candidate state is useful when it predicts the future and older history adds little conditional information once `S` is known.

The stronger intervention-aware version asks for a current representation that screens off older history across a preregistered family of future challenges.

## Working mathematical objects

### 1. Task-sufficient measurements

Let the hidden developmental state be `x`, observation map `z = h(x)`, and future task `y = F(x)`. Locally, a measurement can be sufficient for that future when hidden directions invisible to the sensor are also irrelevant to the task:

`ker(Dh_x) subseteq ker(DF_x)`.

### 2. Predictive state replacement

Let `H` = measured past, `S` = measured current state, and `Y` = future. Define `J = I(Y; S | H)` and `M = I(Y; H | S)`. The regime of interest is `J > 0` while `M` is small under a specified estimator and uncertainty model. This is a predictive diagnostic, **not proof that an organism is Markov**.

### 3. Connected causal fibers

Let `W` be a joint hidden state-law space and let `H_Q(w)` be the vector of phenotypes produced under an experimental panel `Q`. For a target world `w*` and tolerance `δ`, define the experimentally indistinguishable set

`K_Q^δ(w*) = {w : max_q d(h_q(w), h_q(w*)) <= δ}`.

The object we care about is not only this inverse image, but the connected component containing the target:

`C_Q^δ(w*) = Comp_{w*} K_Q^δ(w*)`.

This distinguishes hidden mechanisms that merely imitate the same phenotype from mechanisms continuously accessible within the permitted phenotype tolerance.

## Main computational findings so far

1. **A recent measured molecular state often screens off older measured history for specific future growth tasks in multiple flower lineage windows.** This is predictive screening-off under finite estimators, not a proof of biological Markovity.
2. **One dominant molecular direction can recover much of the missing predictive power for a particular future once geometry is already measured.** This is conditional on the observation stack and should not be interpreted as a one-dimensional organismal state.
3. **A known-Markov simulator produced spurious positive history gain under finite boosted-tree estimation.** This falsified our earlier fixed-threshold criterion and motivated calibration against known generative models.
4. **In a seed dormancy reanalysis, finite-count binomial modeling avoids pathological certainty at 0% and 100% germination and supports latent response directions that become more identifiable under selected perturbations.**
5. **In a synthetic 224-world developmental model (14 architectures × 16 hidden states), baseline morphology can collapse distinct hidden worlds that separate under intervention.**
6. **The inverse image of a phenotype can contain disconnected mechanism islands.** In the sampled model, a low-cost alternative mechanism island appeared before it connected to the target, producing a measurable accommodation-versus-accessibility gap.
7. **The best intervention for destroying a specific connected ambiguity need not be the same as the best intervention for global parameter estimation.** However, greedy ambiguity splitting is not generally near-optimal; a counterexample shows its approximation ratio can approach zero without additional structure. Small experiment libraries should therefore be benchmarked exhaustively.

See [CLAIMS_AND_EVIDENCE.md](CLAIMS_AND_EVIDENCE.md) for claim-level status, caveats, and reproduction requirements.

## What we are not claiming

We are not claiming that plants are Markov systems; morphology uniquely determines mechanism; one molecular principal component is the universal developmental state; the topology language itself is novel; computational simulation establishes a new biological law; or any result here currently justifies a medical, agricultural, or clinical intervention.

## Novelty boundary

Several neighboring ideas are established: predictive cell states, causal states, predictive-state representations (PSRs), lineage/fate prediction, perturbation-response mapping, augmented-state observability/identifiability, neutral networks, Reeb spaces, active experimental design, and topological summaries of biological data. In particular, **predictive screening-off is not a new mathematical definition of state**. The candidate contribution being tested here is narrower:

> **Can we experimentally complete a present developmental state until older measured history becomes predictively redundant across a specified family of future interventions, while using the topology of the remaining connected causal fiber to choose the next experiment?**

That statement is a research hypothesis and framework, not a settled discovery.

## Repository map

- `README.md` — accessible overview
- `CLAIMS_AND_EVIDENCE.md` — claim ledger with confidence labels
- `PREPRINT.md` — technical manuscript draft
- `REPRODUCIBILITY.md` — provenance and what is still needed for full reproduction
- `ROADMAP.md` — prospective biological validation program
- `MATH_CHECKPOINT_2026-08-29.md` — adversarial mathematics checkpoint and frozen rejections
- `LAB_OPERATING_SYSTEM.md` — claim gates and lane structure
- `FUNDING_PIPELINE.md` — verified funding routes / exclusions
- `EVIDENCE_DESK_2026-08-29.md` — NotebookLM evidence-control synthesis
- `research_logs/` — raw lane outputs preserved for provenance
- `CITATION.cff` — citation metadata

## Reproducibility status

This repository is the **public checkpoint**. Some original analysis artifacts currently live outside this repository in prior computational workspaces and conversation-generated checkpoints. They are being migrated only after provenance is verified. Until raw code, data hashes, and execution environments are attached, numerical results should be treated as **reported computational findings awaiting independent reproduction**.

## Invitation to the scientific community

We welcome adversarial review, replication attempts, alternative formulations, and collaboration from developmental biology, plant biology, dynamical systems, causal inference, information theory, topological data analysis, and active experimental design.

The fastest way to help is to identify a living system where two biological backgrounds are deliberately chosen to look similar at baseline but are expected to respond differently to a small, safe perturbation panel. A prospective blinded test would provide a decisive next step.
