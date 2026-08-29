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

1. **A direct-source reanalysis of the released Refahi FM1 flower atlas falsifies a broad screening-off claim and reveals a narrower late-epidermis result.** In the predefined 120→132 h L1 cohort (256 cells / 86 ancestor groups), current geometry plus the released 25-channel atlas state predicts descendant growth well. Across 200 shuffled ancestor-group partitions, fixed-Ridge history gain has median **−0.015 R²**, is positive in only 4% of partitions, and never exceeds +0.05; across 100 shuffled partitions a Gaussian log-score history value is positive in only 3%. Calibration has only ~73% power for a 0.20-SD residual history effect and ~98% power around 0.30 SD, so subtle effects cannot be excluded. The middle L1 window usually retains history under a linear decoder but is strongly partition- and decoder-dependent. See `REPLICATION_CHECKPOINT_FM1_2026-08-29.md` and `STAGE_DEPENDENCE_CHECKPOINT_FM1_2026-08-29.md`.
2. **The flower molecular channels are atlas annotations, not repeated 25-gene measurements in the exact same living cells.** Expression domains were manually integrated into FM1 from literature, RNA in-situ hybridization, and some live imaging. Earlier reported multi-window/one-PC results remain legacy analyses awaiting full artifact migration and should not be described as direct longitudinal molecular measurement.
3. **A known-Markov simulator produced spurious positive history gain under finite boosted-tree estimation.** This falsified our earlier fixed-threshold criterion and motivated calibration against known generative models.
4. **In a seed dormancy reanalysis, finite-count binomial modeling avoids pathological certainty at 0% and 100% germination and supports latent response directions that become more identifiable under selected perturbations.**
5. **In a synthetic 224-world developmental model (14 architectures × 16 hidden states), baseline morphology can collapse distinct hidden worlds that separate under intervention.**
6. **The inverse image of a phenotype can contain disconnected mechanism islands.** In the sampled model, a low-cost alternative mechanism island appeared before it connected to the target, producing a measurable accommodation-versus-accessibility gap.
7. **The best intervention for destroying a specific connected ambiguity need not be the same as the best intervention for global parameter estimation.** However, greedy ambiguity splitting is not generally near-optimal; an **independently reproduced grid counterexample** shows its approximation ratio equals `3/n` and approaches zero without additional structure. Small experiment libraries should therefore be benchmarked exhaustively.

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
- `PREREGISTRATION_RCO_PILOT.md` — source-audited prospective Arabidopsis RCOg-V suppressor protocol and falsification gates
- `REPLICATION_CHECKPOINT_FM1_2026-08-29.md` — direct-source FM1 flower-atlas replication, corrections and calibrated null/power tests
- `MATH_CHECKPOINT_2026-08-29.md` — adversarial mathematics checkpoint and frozen rejections
- `MATHEMATICAL_NOTE_PREDICTIVE_SCREENING_OFF.md` — loss-aware population screening-off identities, counterexamples, and implications
- `NEGATIVE_CONTROL_WEINREB_2020_2026-08-29.md` — external state-incompleteness control from public LARRY split-well lineage data
- `STAGE_DEPENDENCE_CHECKPOINT_FM1_2026-08-29.md` — estimator- and stage-dependent FM1 history-value audit
- `LAB_OPERATING_SYSTEM.md` — claim gates and lane structure
- `FUNDING_PIPELINE.md` — verified funding routes / exclusions
- `NSF_MATHBIO_CONCEPT_2026-08-29.md` — sponsor-ready Mathematical Biology concept built from surviving theorem/counterexample and biological-control evidence
- `NSF_BIOCORE_CONCEPT_2026-08-29.md` — biology-first prospective living-plant validation concept for BIO Core / Developmental Systems
- `EVIDENCE_DESK_2026-08-29.md` — NotebookLM evidence-control synthesis
- `research_logs/` — raw lane outputs preserved for provenance
- `analysis/` — independently rerunnable mathematical checks and result tables
- `CITATION.cff` — citation metadata

## Reproducibility status

This repository is the **public checkpoint**. The greedy counterexample, state-completion CMI calibration, Refahi FM1 stage/log-score analyses, and the Weinreb/Klein incompleteness control now have rerunnable code and machine-readable results in `analysis/` and `results/`. Several older flower/seed numerical analyses still live in prior computational checkpoints and remain **reported findings awaiting verified artifact migration**; their evidentiary status is kept separate in the claims ledger.

## Invitation to the scientific community

We welcome adversarial review, replication attempts, alternative formulations, and collaboration from developmental biology, plant biology, dynamical systems, causal inference, information theory, topological data analysis, and active experimental design.

The fastest way to help is to identify a living system where two biological backgrounds are deliberately chosen to look similar at baseline but are expected to respond differently to a small, safe perturbation panel. A prospective blinded test would provide a decisive next step.
