# NSF Mathematical Biology Concept Note — Draft 2026-08-29

## Working title
**Counterfactual State Completion: Mathematics for Identifying Developmental Mechanisms from Minimal Perturbations**

## Program target
NSF 26-520 — Mathematical Biology.  
Target date: October 13, 2026; proposals accepted anytime.

## Overview
Biological development is commonly observed through a small set of phenotypic and molecular measurements even though future responses may depend on hidden regulatory state, developmental history, and system parameters. This creates a task-specific inverse problem: **what must be measured or perturbed now so that the system's future responses become predictable for a specified family of interventions?**

We propose a mathematical framework that treats the hidden world as a joint state-law object `w=(theta,x)` and an experiment panel `Q` as a counterfactual observation map `H_Q(w)`. At finite experimental resolution `delta`, the worlds compatible with the observed target form an inverse tolerance set; its connected component around the truth defines a **connected causal ambiguity set**. Adding interventions refines this set. In parallel, measured developmental state is evaluated against an intervention-indexed predictive equivalence relation: two histories are equivalent when they induce identical distributions over future observations for every allowed future policy.

The project does **not** claim Reeb spaces, observability, causal states, predictive-state representations, or active experimental design as new mathematics. The research question is whether their intersection yields new, useful theory for biological inverse problems in which hidden state and developmental law are jointly uncertain, observations have finite resolution, and experiments must be chosen under biological cost.

## Central mathematical questions
1. **Finite counterfactual separation.** Under what assumptions on the biological world space, intervention family, and observation map does a finite perturbation panel separate future-relevant state-law equivalence classes? What lower bounds on the required number of experiments follow from topology, dimension and finite-noise packing?
2. **Stability of causal ambiguity.** How should finite-resolution connected inverse fibers be compared under measurement error, model discrepancy and changes in experimental tolerance? Can merge thresholds/persistence replace fragile single-tolerance statements?
3. **Experiment selection under topology.** When is ambiguity-reduction submodular or approximately submodular, and when can greedy experiment selection fail? What tractable alternatives give performance guarantees under biologically realistic intervention libraries and costs?
4. **Measurable state completion.** When can a physically measured present state approximate the minimal interventionally predictive quotient, and how can approximation error be bounded or calibrated from finite data?

## Three research aims

### Aim 1 — Build a rigorous theory of intervention-indexed causal ambiguity
Formalize exact and finite-resolution quotients for joint state-law worlds; derive monotone-refinement results under explicit metrics; characterize stability through tolerance interleavings/sandwich bounds; and connect the construction precisely to Reeb spaces, observability/identifiability and predictive-state theory.

### Aim 2 — Develop experiment-selection theory beyond greedy ambiguity reduction
We have independently reproduced a counterexample showing that connected-component ambiguity reduction is not generally submodular: on an `n x n` candidate-world grid, a greedy two-experiment policy achieves utility ratio `3/n` relative to the optimal pair, tending to zero. We will characterize structural conditions that restore approximation guarantees and develop exact/near-exact algorithms for small assay libraries with cost constraints.

### Aim 3 — Test the mathematics on a real developmental system
Use published plant developmental systems as a biological test bed. The first prospective target is an *Arabidopsis thaliana* `RCOg-V` suppressor panel in which distinct lesions in CUC2, PIN1, CYP71 and ribosome-related genes converge on simplified leaf phenotypes. We will first perform public-data / published-response analyses, then—subject to collaboration and material access—preregister a blinded perturbation experiment that compares active response against the strongest available baseline.

## Preliminary results and falsifications
- **Exact refinement:** under a coordinatewise sup metric, adding experiments produces nested inverse tolerance sets and nested target connected components.
- **Noise formulation:** uniform signature error motivates a tolerance sandwich rather than a claim that a fixed-`delta` connected component is intrinsically stable.
- **Greedy failure:** independently rerunnable code reproduces a grid construction with greedy/optimal ratios `0.30, 0.15, 0.075, 0.0375, 0.01875` for `n=10,20,40,80,160`, exactly matching `3/n`.
- **Novelty correction:** predictive screening-off of history is strongly precedented by causal states and PSRs; it is treated here as an empirical biological target, not a new state theorem.
- **Statistical correction:** a known-Markov simulator produced nonzero apparent finite-sample history gain under a flexible estimator, motivating explicit null/power calibration before any biological screening-off claim.

## Falsifiability
The project will be considered mathematically weakened if: (i) the proposed finite-resolution topology adds no decision-relevant structure beyond established observability/PSR formulations; (ii) practical intervention families violate the richness assumptions needed for finite separation; or (iii) topology-aware selection fails to outperform simpler cost-aware designs on held-out biological tasks. Negative results and failed conjectures will remain part of the public record.

## Why Mathematical Biology
The central deliverable is not a plant classifier. It is mathematics for an experimentally constrained biological inverse problem, with theory and biological relevance developed together. The plant system is intended to prevent the mathematics from drifting into an unconstrained abstract construction and to expose where measurement, noise, developmental time and intervention cost break ideal assumptions.

## Broader impacts direction
All definitions, counterexamples, simulation calibrations, preregistration templates and reproducible analyses will be released openly. The project can provide an educational bridge connecting dynamical systems, topology, causal/predictive-state theory and experimental developmental biology, while demonstrating a research culture in which negative results and novelty corrections are published alongside positive findings.

## Current external-status note
A program-fit inquiry was sent to `mathbio@nsf.gov` on August 29, 2026. This draft should be revised in response to program feedback and the ongoing primary-literature novelty audit before any proposal is submitted.
