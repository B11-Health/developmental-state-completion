# NSF BIO Core / Developmental Systems concept — 2026-08-29

## Working title

**Prospective Developmental State Completion in Plants Using Minimal Counterfactual Perturbations**

## Program fit

Primary target: **NSF 26-517 Core Research in Biological Sciences (BIO Core)**, within the Developmental Systems scope. The current Developmental Systems program explicitly supports mechanistic work on how organismal properties emerge across space and time and includes **Plant, Fungal and Microbial Developmental Mechanisms**. BIO Core proposals are accepted anytime.

This concept is intentionally biology-first. The mathematical framework is a tool for designing and falsifying a developmental experiment, not the biological claim itself.

## Central biological question

> Can two plant developmental backgrounds that are difficult to distinguish at baseline nevertheless carry different future developmental potential, and can a small, preregistered perturbation panel expose that hidden difference prospectively?

## Rationale

A phenotype is a readout of development, not necessarily a unique specification of the mechanism that generated it. Our computational work suggests a practical test: identify backgrounds that are closely matched in baseline morphology/current reporters; apply a small perturbation selected *before unblinding*; measure the resulting response; and ask whether the response reveals future-relevant developmental state that the baseline image did not.

The proposal does **not** claim that plants are Markovian, that morphology uniquely identifies mechanism, or that one molecular coordinate is a universal state. “State completion” is operational and task-specific: a present measurement stack is considered adequate only when older measured history adds little predictive value for the preregistered future task under calibrated decoder families.

## Biological system

The current source-audited pilot is centered on Arabidopsis leaf-shape backgrounds connected to the RCO/CUC developmental module, using published suppressor/genetic resources as candidate mechanistically distinct backgrounds. Final genotype choice, reporter configuration, perturbation dose and physiological-safety thresholds must be set with the executing plant-development laboratory and frozen before confirmatory acquisition.

The project will not infer a wet-lab protocol from computational convenience. Feasibility and plant health are Phase-0 gates.

## Aim 1 — Establish a baseline “developmental shadow gap” prospectively

Select at least two mechanistically distinct plant backgrounds that can be matched within preregistered baseline morphology and directly measured current reporters at a sharply defined leaf node, tissue compartment and developmental stage.

Primary baseline test:

- train a frozen baseline-only decoder `M0` on blinded background labels;
- require that baseline accuracy/information remain below a preregistered separability ceiling;
- if baseline already identifies background reliably, the shadow-gap hypothesis for that pair is falsified and the pair is not used to claim tomography.

Directly measured reporter channels must come from the same experimental specimen/time point. External atlas priors may be used only if explicitly labeled as priors rather than measurements.

## Aim 2 — Test whether a minimal perturbation reveals hidden developmental potential

Before confirmatory unblinding, freeze a small, biologically safe perturbation panel selected from mechanistic knowledge and the computational experiment-design policy. The exact intervention interface is collaborator-defined; current source-audited candidates include perturbations that interrogate the RCO/CUC/auxin/cytokinin developmental neighborhood.

Primary endpoint:

> Out-of-sample improvement of an intervention-response decoder `M1` over the baseline-only decoder `M0` for hidden-background identification and/or a preregistered future developmental outcome.

Required comparators:

- random perturbation of equal experimental cost;
- equal-cost mechanistically plausible alternatives;
- baseline morphology/reporters alone;
- sham/control handling.

A topology-aware policy succeeds only if it prospectively improves identification or future prediction relative to those comparators.

## Aim 3 — Test state completion rather than merely classification

For each specimen define:

- `H`: older measured developmental history;
- `S`: directly measured current state after/before the specified intervention stage;
- `Y`: preregistered future developmental outcome.

At least one regularized linear and one flexible nonlinear decoder are preregistered. Distributional prediction uses a proper scoring rule where feasible. “Completion” is not declared from a nonsignificant coefficient. The exact statistic is first calibrated on known-complete and known-history-dependent generators matched for planned sample size, grouping, feature dimension and noise.

The outcome is classified as:

- **state incomplete** if older history adds reproducible predictive value beyond calibrated nulls;
- **state approximately sufficient at the tested resolution** if residual history is below a preregistered effect threshold with adequate power;
- **estimator-dependent / unresolved** if prespecified decoder families disagree.

## Preliminary evidence supporting feasibility

1. A direct-source reanalysis of the public Refahi FM1 flower atlas shows that a current integrated atlas state adds substantial future-growth information beyond geometry.
2. In a predefined late-L1 cohort, repeated group partitions show no stable material gain from older history under the tested linear losses, while a middle developmental window is estimator- and partition-dependent. This motivates strict stage/layer matching in the prospective experiment.
3. The same general screening logic strongly detects incompleteness in the Weinreb/Klein split-well lineage system, where hidden heritable fate information is independently established.
4. A post-hypothesis source-simulator experiment was preregistered before rendering and passed all frozen two-context tomography predictions: 32 complementary phenotype pairs gave 100% sign recovery with maximum signed-state L2 `5.15e-4`, and a separately frozen context extension passed all five theoretically sufficient masks. This is substantially stronger than retrospective simulation, but it remains **simulator design evidence only** until a living prospective test succeeds.

## Hard falsifiers

The biological claim fails if:

1. baseline measurements already identify the hidden background;
2. the frozen perturbation panel does not improve blinded prediction relative to baseline and equal-cost/random controls;
3. the effect disappears on an independent allele/background or replication cohort;
4. intervention responses are dominated by damage/stress rather than the intended developmental mechanism;
5. older history remains materially predictive after the proposed current state;
6. conclusions depend on post-hoc stage, model, split or reporter selection.

## Expected biological contribution

A prospective test of a simple but consequential idea: **developmental potential can be experimentally interrogated rather than inferred from appearance alone**. Success would provide a calibrated method for finding when a present plant state is sufficient for a specified future task and when an apparently similar phenotype conceals mechanistically distinct developmental futures. Failure would be equally informative by identifying which measurements or perturbations do not complete the state.
