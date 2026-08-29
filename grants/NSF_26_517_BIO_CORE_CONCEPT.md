# NSF 26-517 BIO Core / Developmental Systems — one-page concept draft

**Working title:** Prospective counterfactual decoding of hidden developmental mechanisms in Arabidopsis leaf morphogenesis

**Status:** internal concept draft; not submitted. Developmental Systems program-fit inquiry sent to Dr. Anna K. Allen on 2026-08-29; automatic reply indicates return from conference on 2026-08-31. BIO Core accepts full proposals anytime.

## Biological question

Can different regulatory lesions that converge on similar present morphology be distinguished prospectively by a small, controlled developmental perturbation panel — and can the resulting present response state predict a specified future better than morphology alone?

The proposed study tests a narrow biological hypothesis: **state completion is task- and intervention-relative.** It does not assume that a plant has one universal hidden state or that development is globally Markovian.

## Rationale and tractable system

Wang et al. (2025) generated an unusually useful Arabidopsis substrate by screening suppressors of the `pChRCO::ChRCOg-VENUS` (`RCOg-V`) lobed-leaf phenotype. Distinct lesions in CUC2, PIN1, CYP71, NOP2A, RPL34 and PGY1 reduce RCO-driven leaf complexity through different developmental mechanisms.

A minimum feasibility panel would compare mechanistically distinct backgrounds such as:

- `cuc2-4;RCOg-V` — margin-patterning module;
- `cyp71-3;RCOg-V` — CYP71-dependent regulation;
- `nop2a-5;RCOg-V` — ribosome-biogenesis mechanism;
- unsuppressed `RCOg-V` — positive morphology/control background.

The exact material panel is provisional and depends on collaborator availability/MTA feasibility.

## Aim 1 — Establish a morphology-matched hidden-mechanism cohort

Quantify baseline developmental stage, leaf/primordium size, margin geometry and every reporter channel that will be available to the active model. Define the matched test cohort using a frozen baseline distance rule before genotype unblinding.

**Falsifier:** if baseline measurements already classify the hidden backgrounds at ceiling, there is no useful cryptic-mechanism test in this panel.

## Aim 2 — Measure a controlled present response state

Hu et al. (2024) established a dexamethasone-inducible ChCUC1 system in Arabidopsis and measured PIN1 polarity 24 h after induction versus mock treatment. We propose this as a candidate developmental probe because it interrogates margin-patterning competence rather than merely damaging tissue.

The exact crossing scheme, dose, application and reporter configuration must be validated with the originating/qualified plant lab before confirmatory registration. Cytokinin biology is mechanistically relevant to RCO but is **not** treated as a ready-to-use second probe until a real protocol is validated.

Record physiological burden separately from morphology: growth delay, visible injury/survival, developmental timing, and reproductive effects when applicable.

## Aim 3 — Blinded prospective prediction and state-completion test

Before unblinding:

1. freeze feature extraction;
2. freeze baseline-only model M0;
3. freeze intervention-response model M1;
4. freeze perturbation-selection rule;
5. hash and timestamp all predictions.

Primary comparison: does M1 improve blinded hidden-background/future-outcome prediction over M0, mock treatment, and a biologically validated equal-cost comparator?

Secondary completion test: after conditioning on the measured present response state `S`, does older measured history `H` add calibrated predictive information about the preregistered future `Y`?

Every finite-sample statistic will be calibrated against a known-complete null and a known-history-dependent alternative at the same effective sample size/model complexity.

## Existing benchmark that constrains the proposal

A new reanalysis of the released Refahi FM1 Arabidopsis flower atlas shows why this experiment must be compartment- and stage-specific. In a late L1 epidermal window, current atlas state predicts descendant growth well and older atlas history adds no reproducible value. Other windows/layers are incomplete or model-sensitive. That result **rejects** a universal state-completion claim and motivates a prospective test whose biological interface is explicitly defined.

## Outcomes that would weaken the framework

- active responses do not beat baseline-only prediction;
- results fail on independent alleles of the same pathway;
- apparent information gain is explained by stress/damage;
- history remains predictive after a richer present-state measurement under adequate calibrated power;
- the selected perturbation is not better than a physiologically matched non-targeted control.

## Collaboration status

Miltos Tsiantis's group has been contacted for scientific critique/collaboration because it developed the RCOg-V system and has the relevant genetics/imaging expertise. **No commitment is claimed.**

## Evidence boundary

This is a prospective proposal. The RCOg-V suppressor biology and ChCUC1 inducible system are published; their combination into this exact blinded tomography experiment is not. No prospective living validation has yet been completed.
