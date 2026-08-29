# NSF BIO Core / Developmental Systems Concept Note — Draft 2026-08-29

## Working title
**Prospective Developmental State Completion in Plants Using Minimal Counterfactual Perturbations**

## Program target
NSF 26-517 — Core Research in Biological Sciences, Developmental Systems.

## Biological question
Two organisms can converge on a similar visible phenotype while differing in the developmental machinery that generated it. The decisive experimental question is therefore not merely **what does the organism look like?**, but **which measurable present state is sufficient to predict what it can do next under controlled developmental challenges?**

We propose a prospective, blinded plant experiment that tests whether a small, biologically justified perturbation response contains information about future development and hidden mechanism beyond every allowed baseline measurement. The study is designed so that the framework can fail cleanly.

## Experimental substrate
A strong candidate is the published *Arabidopsis thaliana* `RCOg-V` suppressor collection (Wang et al., 2025). In a common RCO-expressing background, distinct lesions in **CUC2, PIN1, CYP71, NOP2A, RPL34 and PGY1** reduce RCO-driven leaf lobing. These mutations affect different developmental functions yet converge on simplified mature leaf phenotypes.

The system also exposes an important control problem: the lines are **not** identical at every baseline channel. CUC2 suppressors show an early lobe-initiation defect and altered RCO-VENUS pattern, while several other suppressors initiate lobes and fail later. Therefore we will not declare mechanisms “hidden” by eye. The experiment will compare the active perturbation model against both morphology-only baseline (`M0-morph`) and a strongest-baseline model containing every permitted pre-intervention channel (`M0-all`).

## Hypotheses

### H1 — Counterfactual discrimination
For a preregistered future developmental target `Y`, a model using the response to a frozen perturbation panel (`M1-active`) will improve held-out probabilistic prediction relative to `M0-all` on morphology-matched confirmatory plants.

### H2 — Mechanism-level generalization
Where independent alleles are available (e.g., CUC2 and NOP2A), response features learned from one allele will generalize to the other better than expected from allele-specific overfitting.

### H3 — Task-specific state completion
At a preregistered post-intervention time, a measured current state `S` will be tested for whether older measured history, intervention assignment or hidden genotype continues to add reproducible held-out information about the later outcome `Y`. Residual gain means the proposed state is incomplete. Lack of measured gain will be interpreted only after finite-sample null and power calibration; it will **not** be described as proof that the plant is Markovian.

## Study architecture

### Phase 0 — independent feasibility cohort
Before confirmatory testing:
1. obtain and independently verify genetic materials;
2. reproduce published baseline phenotypes under the participating laboratory's conditions;
3. establish a fixed morphology-matching/enrollment rule;
4. determine reporter compatibility, perturbation dose/timing, response windows and physiological burden;
5. estimate variance for a simulation-based confirmatory sample-size calculation.

No confirmatory hypothesis is tested on Phase 0 plants.

### Candidate perturbation axis 1 — inducible ChCUC1
Hu et al. (2024) provide a published dexamethasone-inducible ChCUC1 system in *A. thaliana* that changes PIN1 polarity behavior. This gives a biologically grounded way to challenge margin-patterning competence. The exact cross/reporter architecture with the `RCOg-V` suppressor panel must be solved experimentally; the current RCO-VENUS and published PIN1-GFP reporters cannot be assumed to combine trivially.

### Candidate perturbation axis 2 — RCO/cytokinin
Hajheidari et al. (2019) established that RCO regulates cytokinin homeostasis and that elevated cytokinin signaling in the RCO domain can promote leaf complexity. The exact acute implementation, dose, timing and cost in the suppressor panel remain feasibility questions rather than frozen protocol elements.

## Confirmatory blinding
- Separate feasibility, training and locked confirmatory cohorts.
- Non-descriptive sample IDs assigned by an independent person.
- No feature, dose, threshold, hyperparameter or perturbation-policy tuning on confirmatory plants.
- Freeze code commit, environment, feature schema, model, perturbation panel/policy, exclusions, primary metric, sample-size simulation and final prediction-file SHA-256 before genotype unblinding.

## Primary endpoint
Held-out probabilistic **log loss** for hidden mechanism/background prediction, comparing `M1-active` against `M0-all` on the same confirmatory plants. Balanced accuracy, macro-F1 and calibration are secondary.

A second preregistered endpoint predicts a future developmental outcome such as later margin-growth trajectory or final leaf geometry; the exact horizon is frozen after feasibility, before confirmatory data collection.

## Physiological intervention cost
The study rejects silhouette IoU as a proxy for living harm. Feasibility will select reproducible biological burden measures such as survival, rosette growth, new-leaf emergence, flowering delay and fertility/seed set, with molecular stress or cell-death assays added only if validated by the participating laboratory.

## Falsification criteria
The central claims fail or weaken if:
1. `M0-all` performs as well as `M1-active`;
2. active decoding fails on independent alleles of the same mechanistic class;
3. older history/treatment/genotype retains reproducible predictive information after conditioning on candidate state `S`;
4. a designed multi-probe policy does not outperform random/equal-cost selection from the same validated library;
5. informative probes cause unacceptable preregistered physiological burden;
6. results are fragile across prespecified developmental-stage blocks, batches or reasonable biological metrics.

## Why Developmental Systems
The project directly asks how interacting developmental processes generate phenotype, how different developmental mechanisms can converge on similar form, and whether controlled perturbations can reveal future-relevant developmental state. It uses evolutionary/developmental variation in leaf morphogenesis not as an endpoint in itself but as a rigorous system for testing what constitutes an experimentally sufficient developmental state.

## Reproducibility and open science
The current public repository already contains the claim ledger, negative results, audited preregistration draft, mathematical counterexample code and raw research-lane logs. The prospective biological study would add a public preregistration, frozen analysis code and a clear separation between pilot decisions and confirmatory tests.

## Current external-status note
A program-fit inquiry was sent to NSF Developmental Systems contact Anna K. Allen on August 29, 2026. Miltos Tsiantis was separately contacted for scientific criticism of the `RCOg-V` suppressor panel as a prospective substrate. No reply, collaboration, endorsement, material access or funding is implied until it occurs.
