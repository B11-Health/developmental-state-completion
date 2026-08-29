# Preregistration draft: prospective developmental-state completion in Arabidopsis RCOg-V suppressors

Status: **design draft, not yet registered and not yet approved by a collaborating wet lab.**

This document deliberately separates published materials from proposed experimental choices. No dose, crossing scheme, sample size, or physiological-safety threshold is treated as established until verified prospectively.

## Scientific question

Can a biologically measurable present developmental state, enriched by a small controlled intervention, predict a specified developmental future and hidden regulatory background better than baseline morphology alone, while making older measured history add little calibrated predictive information?

This is an empirical test of state completion. It is **not** a test of whether the organism is globally Markovian.

## Verified biological substrate

The strongest currently verified substrate is **Arabidopsis thaliana carrying the Cardamine hirsuta RCO transgene** `pChRCO::ChRCOg-VENUS` (`RCOg-V`). Wang et al. (2025) performed an EMS suppressor screen in this background and identified simplified-leaf suppressors affecting distinct mechanisms:

- `cuc2-4;RCOg-V` and `cuc2-5;RCOg-V` — CUC2 / margin-patterning lesions;
- `pin1-12;RCOg-V` — PIN1 / auxin transport lesion;
- `cyp71-3;RCOg-V` — CYP71 lesion;
- `nop2a-5;RCOg-V` and `nop2a-6;RCOg-V` — NOP2A / ribosome-biogenesis lesions;
- `rpl34-2;RCOg-V` — ribosomal protein lesion;
- `pgy1-5;RCOg-V` — ribosomal protein / polarity-associated lesion.

The 2025 paper reports 10-20 mature leaves per genotype for its leaf-shape comparison and shows that these distinct lesions all reduce RCO-driven lobe formation.

Primary source: Wang et al., The Plant Journal (2025), PMCID PMC12165315.

## Verified intervention interface

Hu et al. (2024) constructed a dexamethasone-inducible `ChCUC1` system in **A. thaliana**:

`ChCUC1p::LhG4:GR; Op6::ChCUC1:tdTomato; PIN1p::PIN1:GFP`

After dexamethasone versus mock treatment of developing leaves, they characterized PIN1:GFP polarity 24 hours later. ChCUC1 induction shifted the position/direction of PIN1 polarity reversals and altered margin-patterning behavior. The same study also used time-lapse imaging and ChCUC1 genetic mosaics to follow polarity and growth responses.

Primary source: Hu et al., PNAS (2024), DOI 10.1073/pnas.2321877121.

**Important:** the published ChCUC1 inducible line is not, by itself, evidence that the exact same perturbation has already been crossed into or validated in each RCOg-V suppressor background. That is a required feasibility step.

## Candidate panel

### Minimum feasibility panel

Use three mechanistically distinct simplified RCOg-V suppressor backgrounds that do not mutate PIN1 itself, for example:

1. `cuc2-4;RCOg-V` — pattern-initiation module;
2. `cyp71-3;RCOg-V` — transcription/chromatin-associated regulator affecting RCO function;
3. `nop2a-5;RCOg-V` — ribosome-biogenesis mechanism.

Keep unsuppressed `RCOg-V` as a positive morphology/control background.

The specific three-line choice is a **design proposal**, not a published optimal panel.

### Cross-allele replication

If the pilot succeeds, repeat on the independent alleles `cuc2-5` and `nop2a-6`. Cross-allele transfer is a strong guard against memorizing allele-specific quirks.

## Phase 0: feasibility before confirmatory testing

A collaborating plant lab should first establish:

1. material availability and MTA requirements;
2. whether the ChCUC1 inducible construct and required reporters can be introduced into the selected RCOg-V suppressor backgrounds without confounding complementation;
3. development-stage matching and imaging feasibility;
4. dex-versus-mock dose response and physiological burden in each background;
5. which reporter/readout set is technically robust enough for blinded acquisition.

No confirmatory classification claim should be made from Phase 0.

## Baseline matching

Before intervention, each plant must be measured with the same preregistered baseline stack:

- leaf node and chronological/developmental age;
- leaf/primordium size;
- quantitative margin geometry / shape descriptor;
- RCO-VENUS signal if available in the selected line;
- any reporter channel used later in the active arm.

The baseline-only comparator receives **all** of these channels. Active-intervention benefit must come from the response, not from withholding a baseline marker from the control model.

A morphology-matched evaluation subset should be defined by a preregistered distance/tolerance chosen before genotype unblinding in the held-out test cohort.

## Intervention arms

### Verified candidate: ChCUC1 induction

- treatment: dexamethasone induction of the published ChCUC1 system;
- control: matched mock treatment;
- first verified response time: 24 h for PIN1 polarity, based on Hu et al. (2024).

Exact dose/application method must be copied from the original materials/methods or agreed with the originating lab; it is **not frozen here**.

### Cytokinin-based perturbation

Hajheidari et al. (2019) established that local cytokinin signaling mediates part of RCO function and that elevated cytokinin signaling in the RCO domain can increase leaf complexity. This supports cytokinin biology as a mechanistic axis.

However, the current evidence audit does **not** justify a ready-to-use acute cytokinin probe for the suppressor-classification experiment. Any cytokinin intervention remains **Phase-0 exploratory** until the exact construct/treatment, timing, burden, and interpretation are validated.

Primary source: Hajheidari et al. (2019), PubMed 31761704.

## Blinding

A party not involved in model fitting assigns non-descriptive specimen IDs. The test-set genotype key remains inaccessible until:

1. the feature extraction code is frozen;
2. the decoder is frozen;
3. the intervention-selection rule is frozen;
4. all predictions are written to a timestamped file;
5. the file hash is committed to the public repository or another immutable registry.

Only then is the genotype key released.

## Models and primary endpoint

### M0 — baseline-only

Predict hidden background and future developmental outcome from the full pre-intervention measurement stack.

### M1 — intervention-response

Use the same baseline stack plus preregistered response features from the perturbation window.

### Primary endpoint

Out-of-sample improvement of M1 over M0 on the blinded test cohort, measured by:

- multiclass log loss / Brier score for hidden-background prediction;
- balanced accuracy as an interpretable secondary classification metric;
- a preregistered continuous error metric for the selected future developmental outcome.

The framework fails this first prospective test if M1 does not reproducibly outperform M0 after uncertainty correction.

## State-completion endpoint

Define:

- H = older measured trajectory before the current assay window;
- S = current baseline plus intervention-response state;
- Y = preregistered future developmental outcome.

Estimate whether H retains predictive information for Y after conditioning on S.

This statistic must first be calibrated on known-Markov and known-non-Markov simulators at the **same effective sample size and model complexity**. A positive finite-sample history gain is expected even under a true Markov null; failure to reject history dependence is not proof of completion.

## Physiological intervention cost

Do not use silhouette change as a proxy for biological harm.

At minimum, record:

- short-term relative growth-rate change versus mock;
- developmental delay;
- survival / visible tissue injury;
- time to flowering if the assay spans that interval;
- fertility/seed production if plants are followed to reproduction.

If the collaborating lab has validated cell-death or stress reporters, those may be added prospectively. No arbitrary weighted cost function is frozen before empirical calibration.

## Random/equal-cost comparator

A random/equal-cost perturbation comparator is scientifically desirable, but it must be a **biologically legitimate** treatment whose physiological burden can be matched to the designed probe. The current evidence does not justify inventing a mechanical prick or nonspecific hormone treatment. The collaborator must nominate and validate this arm before confirmatory preregistration.

## Sample size

No confirmatory N is claimed from the existing papers. Their reported n values were designed for their original biological questions, not blinded mechanism classification.

Recommended two-stage plan:

- feasibility/pilot: fixed small balanced cohorts used only to estimate acquisition failure rates and response variance, not to declare the framework successful;
- confirmatory study: choose N by simulation before unblinding, targeting at least 90% power for the preregistered M1-vs-M0 effect size deemed biologically meaningful, with multiplicity control for secondary endpoints.

The final N and effect-size threshold must be frozen before confirmatory data acquisition.

## Lessons imported from the Refahi FM1 replication

The 2026-08-29 direct-source flower-atlas audit changed this prospective design in four ways. These are design constraints, not claims that the leaf system will behave like the flower atlas.

### 1. Compartment and developmental time are part of the state definition

The confirmatory analysis must not pool biologically heterogeneous layers, leaf nodes, or developmental epochs into one primary completion statistic. The primary cohort must be defined prospectively by tissue compartment and developmental stage. Cross-compartment/generalization analyses are secondary and reported separately.

### 2. Primary current-state channels must be measured in the same living specimen

The Refahi gene channels are atlas annotations mapped from multiple sources. That is useful for benchmarking but can spatially smooth/regularize state. For the RCOg-V experiment, any molecular channel used to claim state completion must be directly acquired from the experimental specimen at the stated current time, or explicitly labeled as an external atlas prior rather than a measurement.

### 3. Estimator disagreement is a result, not something to average away

At least one prespecified regularized linear model and one prespecified nonlinear model should be evaluated. If the qualitative conclusion about residual history differs between them, the state is labeled **estimator-dependent / unresolved**, not complete or incomplete. No post-hoc choice of the model giving the preferred conclusion.

### 4. Completion requires both false-positive and power calibration

Before biological unblinding, the exact history-gain statistic/model must be run on matched known-complete and known-history-dependent generators using the planned sample size, group structure, feature dimension and noise scale. A non-significant history term is only interpretable when the test has adequate power for a preregistered biologically meaningful residual-history effect.

## Hard falsifiers

1. Baseline morphology/reporters already predict hidden background as well as the active response, eliminating the proposed shadow gap.
2. Intervention responses fail to improve blinded prediction beyond M0.
3. Performance disappears on independent alleles of the same gene/pathway.
4. The selected probe causes enough physiological disruption that the response can be explained as damage/stress rather than developmental interrogation.
5. Older history remains materially predictive after the proposed S, beyond the calibrated nonzero finite-sample null.
6. Results are not robust to reasonable preregistered baseline-matching tolerances or train/test splits.

## What success would mean

A successful study would support a narrow claim:

> In this specified Arabidopsis developmental system and intervention family, a measurable present response state carries future-relevant information that baseline morphology alone misses and can approximate an interventionally predictive state for the chosen task.

It would **not** establish a universal biological state variable, prove organismal Markovity, or validate all connected-fiber/topological claims in vivo.

## Required collaborator decisions before registration

- exact suppressor backgrounds/material availability;
- crossing strategy for inducible ChCUC1 and reporters;
- dose and application protocol;
- developmental stage and imaging schedule;
- physiologically matched comparator perturbation;
- acquisition QC and exclusion rules;
- target future outcome;
- confirmatory effect-size threshold and power simulation.

## Primary literature

- Wang Y et al. (2025). A suppressor screen of an Arabidopsis thaliana REDUCED COMPLEXITY (RCO)-expressing strain provides insight into the genetics of leaf margin complexity. The Plant Journal. PMCID: PMC12165315.
- Hu Z et al. (2024). A CUC1/auxin genetic module links cell polarity to patterned tissue growth and leaf shape diversity in crucifer plants. PNAS. DOI: 10.1073/pnas.2321877121.
- Bhatia N et al. (2023). Interspersed expression of CUP-SHAPED COTYLEDON2 and REDUCED COMPLEXITY shapes Cardamine hirsuta complex leaf form. Current Biology. DOI: 10.1016/j.cub.2023.06.037.
- Hajheidari M et al. (2019). Autoregulation of RCO by low-affinity binding modulates cytokinin action and shapes leaf diversity. PubMed: 31761704.
