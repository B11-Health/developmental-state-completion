# NSF 26-520 Mathematical Biology — one-page concept draft

**Working title:** Intervention-indexed predictive state completion in developmental systems

**Status:** internal concept draft; not submitted. Program-fit inquiry sent to NSF Mathematical Biology on 2026-08-29. Target panel date: **October 13, 2026**; the program also accepts proposals anytime.

## Problem

Biological systems are routinely represented by a current “state” — morphology, molecular profile, or latent embedding — without an operational test that the chosen measurement contains the information needed for a specified future task. Older history can remain predictive either because biology genuinely carries unresolved memory or because the present measurement/model is incomplete. We need mathematics that distinguishes these possibilities under interventions and finite data.

## Central mathematical object

For a measured history `h` and allowed future intervention policies `Π`, define histories to be predictively equivalent when they induce the same future-observation kernels under every `π in Π`. A measured current representation is **state-complete for the task** when its fibers refine these interventionally predictive-equivalence classes to a specified tolerance.

This predictive-sufficiency principle itself is established in causal states, predictive-state representations, observability, and controlled-system theory. The proposed work does **not** claim novelty for those foundations. The research question is their finite-resolution integration with a hidden joint state-law inverse problem, connected fiber topology, and experimentally constrained perturbation design in a developmental setting.

## Aim 1 — Finite-resolution theory of interventionally predictive quotients

Develop precise results for joint hidden state-law worlds `w=(x,theta)` observed through finite perturbation panels.

Questions:

- when does expanding a perturbation panel monotonically refine the connected ambiguity around the true world?
- how do ambiguity components move under bounded signature error and metric perturbation?
- what dimension/packing lower bounds constrain the number of counterfactual coordinates required for separation?
- under what transversality/richness assumptions does a generic finite perturbation tuple separate behaviorally distinct worlds?

Preliminary results include a monotone-refinement theorem under product/sup metrics, a finite-error tolerance sandwich, and provisional generic separation bounds; all will be rederived and independently checked before inclusion as theorems.

## Aim 2 — Calibrated experiment selection when topology defeats greedy design

Define experimental losses relative to the current ambiguity rather than generic parameter uncertainty. Establish when connected-component reduction is submodular or approximately submodular and when it is not.

A current counterexample shows that naive greedy ambiguity splitting can have approximation ratio tending to zero. We will therefore develop exact/branch-and-bound baselines for small assay libraries, structural sufficient conditions for approximation guarantees, and adaptive policies whose assumptions are explicit rather than assumed.

All finite-sample completion statistics will be calibrated on known-complete and known-history-dependent generators before biological interpretation.

## Aim 3 — Biological benchmark and prospective falsification

Use the released Arabidopsis FM1 flower atlas as a reproducible benchmark, then move to a prospective plant test.

Our direct-source FM1 audit already falsified a universal screening-off claim. The strongest surviving case is the 120→132 h L1 epidermal growth task: current geometry plus atlas expression predicts descendant growth at R² about 0.60–0.63, while older atlas state adds essentially no predictive value. A matched synthetic calibration had 99% power for a prespecified 0.20-SD direct history effect. Other windows/layers remain incomplete or estimator-sensitive.

Prospective validation will use a baseline-matched Arabidopsis `RCOg-V` suppressor panel if biological feasibility and collaboration are established. A frozen perturbation/decoder protocol must outperform baseline-only and physiologically matched controls; failure is an explicit negative result.

## Why Mathematical Biology

The project requires genuine two-way integration:

- mathematical innovation is driven by biological constraints such as partial observability, compartment-specific state, sequential developmental time, intervention cost, and finite sample size;
- biological claims are only accepted when they survive mathematical calibration, identifiability analysis, and prospective falsification.

## Deliverables

1. formal theory with clearly separated classical precedents and new results;
2. open-source algorithms for ambiguity computation and experiment selection;
3. simulator calibration suite for state-completion statistics;
4. reproducible flower-atlas benchmark;
5. preregistered prospective plant experiment with public negative as well as positive outcomes.

## Current evidence boundary

No living perturbation experiment has yet validated the full framework. The FM1 molecular channels are manually integrated atlas annotations, not repeated 25-gene measurements in the exact same cells. The RCOg-V prospective design requires a plant-development collaborator and feasibility work before a confirmatory study.

## Team/eligibility items still to close

- scientific PI/co-PI structure and demonstrated biological/mathematical expertise;
- collaborator commitment for prospective plant validation;
- NSF/Research.gov organizational and personnel registration verification;
- documentary confirmation of Code Gym's tax-exempt status before certification.
