# Prospective Living-System Validation — Preregistration Draft

**Date:** 2026-08-29  
**Status:** Draft protocol. **Not yet preregistered, not yet funded, not yet approved by a wet-lab collaborator, and not yet a claim of biological validation.**  
**Primary substrate proposed:** *Arabidopsis thaliana* carrying the published `RCOg-V` suppressor panel.

This document replaces earlier informal living-validation sketches. It is deliberately conservative: no dose, sample size, reporter combination, material-transfer assumption, or statistical threshold is frozen unless it has been verified or can be determined prospectively from an independent feasibility cohort.

---

## 1. Scientific question

The narrowed biological hypothesis is:

> **Can a physically measurable present developmental state approximate the interventionally predictive state required for a specified future developmental task?**

The first living experiment must distinguish two related claims.

### H1 — Counterfactual discrimination

A controlled perturbation response contains held-out predictive information about hidden developmental mechanism and/or future morphology **beyond all permitted baseline measurements**.

Operational comparison:

- `M0-morph`: baseline morphology only;
- `M0-all`: every allowed pre-intervention channel;
- `M1-active`: the same baseline channels plus the time-resolved response to a frozen perturbation panel.

The active-tomography claim requires `M1-active` to improve out-of-sample prediction over **both** baseline models.

### H2 — Task-specific state completion

Let:

- `H` = permitted pre-intervention developmental history;
- `A` = intervention assignment;
- `G` = hidden genotype/mechanistic background, revealed only after predictions are frozen;
- `S` = a measured post-intervention current state;
- `Y` = a preregistered later developmental outcome.

A candidate measured state is closer to complete for this task when adding `H`, `A`, or `G` to `S` produces little reproducible held-out predictive gain for `Y`, after finite-sample calibration.

This is **not** a proof that the plant is Markovian. Failure to detect residual history at low sample size is not evidence of true conditional independence.

---

## 2. Why the `RCOg-V` suppressor system is unusually useful

Wang et al. (2025) performed an EMS suppressor screen in *A. thaliana* carrying the *Cardamine hirsuta* `RCOg-V` transgene and identified distinct genetic lesions that all reduce RCO-driven leaf lobing.

### Verified published backgrounds

| Published background | Verified lesion / pathway | Published developmental phenotype relevant to this study |
|---|---|---|
| `cuc2-4;RCOg-V` (`slb102-2`) | CUC2 | smooth primordium margin; lobe initiation defective; RCO-VENUS becomes continuous along margin |
| `cuc2-5;RCOg-V` (`slb167-3`) | CUC2, weaker allele | mostly initiation-defective, with some lobe initiation in the published sample |
| `pin1-12;RCOg-V` (`slb59-2`) | PIN1 / auxin polarity | lobe primordia initiate; later lobe development is reduced |
| `cyp71-3;RCOg-V` (`slb166-1`) | CYP71 | lobe primordia initiate; reduced RCO-VENUS intensity reported |
| `nop2a-5;RCOg-V` (`slb31-3`) | NOP2A / ribosome biogenesis | lobe primordia initiate; reduced RCO-VENUS intensity reported |
| `nop2a-6;RCOg-V` (`slb167-1`) | NOP2A / independent allele | same mechanistic class; useful for leave-allele-out validation |
| `rpl34-2;RCOg-V` (`slb212-2`, `slb215-2`) | RPL34 | lobe primordia initiate; reduced RCO-VENUS intensity reported |
| `pgy1-5;RCOg-V` (`slb119-1`) | PGY1/RPL10aB | lobe primordia initiate; reduced RCO-VENUS intensity reported |

The screen therefore supplies **verified many-to-one phenotypic convergence**: multiple lesions simplify RCO-driven leaf shape through different biological mechanisms.

### Critical caveat: baseline leakage

The backgrounds are not guaranteed to be indistinguishable at every developmental stage or molecular channel. In fact, the primary paper shows known early differences:

- CUC2 mutants fail lobe initiation while the other suppressors generally initiate lobe primordia;
- RCO-VENUS pattern/intensity differs across several lines.

Therefore the experiment must **earn** the word “hidden.” We will not choose a cohort because the lines look similar by eye.

---

## 3. Two baseline comparators, not one

### `M0-morph` — morphology-only shadow

Uses only preregistered non-destructive shape and growth measurements available before the perturbation.

Purpose: test the simple “same-looking plant, different mechanism” idea.

### `M0-all` — full allowed baseline

Uses **all** pre-intervention channels permitted in the experiment, including any fluorescence reporter that is actually measured.

Purpose: prevent a trivial win in which the active model appears informative only because we hid a baseline molecular marker from the comparator.

**Decision rule:** if `M0-all` already classifies mechanism/background with high held-out accuracy or predicts `Y` as well as the active model, the perturbation is not adding the information our tomography claim requires.

---

## 4. Phase 0 — independent feasibility and assay-selection cohort

**No confirmatory hypothesis will be tested on Phase 0 plants.** The feasibility cohort is used only to determine what can be safely and reproducibly frozen for the confirmatory study.

### 4.1 Material verification

Before any experiment:

1. obtain the relevant lines from a verified source under any required material-transfer agreement;
2. independently genotype the lines;
3. verify `RCOg-V` status and reporter behavior;
4. define growth conditions and leaf-node/stage conventions;
5. record seed lot, generation, growth chamber and imaging metadata.

As of 2026-08-29, Code Gym does **not** possess these materials and no collaborator has yet agreed to execute the wet-lab study.

### 4.2 Reproduce the published baseline phenotype

Reproduce, in an independent cohort:

- mature leaf-shape simplification;
- developmental-stage differences in lobe initiation;
- RCO-VENUS pattern/intensity where measured.

If the published phenotypes cannot be reproduced under the participating lab's conditions, the confirmatory study does not begin.

### 4.3 Establish a morphology-matching rule

Use a pilot-only cohort to define a fixed enrollment/matching rule based on preregistered shape features. Candidate features may include the published Leaf Interrogator representation, dissection index, normalized margin-width profiles, or another reproducible shape descriptor.

The rule must be frozen **before** confirmatory genotype labels are examined.

A confirmatory individual is eligible for the “morphology-hidden” primary analysis only if it passes this fixed baseline-matching rule.

### 4.4 Select the perturbation library

The feasibility cohort must establish:

- construct/material compatibility;
- dose and exposure window;
- timing of measurable response;
- short- and longer-term physiological burden;
- imaging feasibility;
- whether the perturbation produces sufficient between-background response variance without destroying future developmental competence.

No perturbation enters the confirmatory panel merely because it is conceptually attractive.

---

## 5. Candidate perturbation A — published inducible ChCUC1 input

Hu et al. (2024) provide a real intervention system relevant to the CUC/PIN developmental axis.

### Verified in *A. thaliana*

The paper reports a dexamethasone-inducible construct:

`ChCUC1p::LhG4:GR; Op6::ChCUC1:tdTomato`

used with `PIN1p::PIN1:GFP` in *A. thaliana*. Dex and mock were compared, with PIN1 polarity characterized 24 h later. Induced ChCUC1 altered PIN1 polarity and auxin-patterning behavior.

### Verified separately in *C. hirsuta*

The same paper also reports a distinct `RCOp::LhG4:GR; Op6::ChCUC1:V` construct in *C. hirsuta*, with ChCUC1:V detectable by 2 h after induction and transcriptomic sampling at 2, 4, 6 and 8 h.

### What is **not** yet verified

We will **not** assume that the *C. hirsuta* `RCOp` construct can simply be inserted into the *A. thaliana* `RCOg-V` suppressor experiment.

We will also not assume a combined reporter stack is spectrally or genetically trivial. The suppressor panel carries RCO-VENUS, while the published *A. thaliana* polarity assay used PIN1-GFP. Reporter compatibility/material generation must be solved by the participating plant lab.

### Prospective biological prediction, not an established result

If an inducible ChCUC1 perturbation is made compatible with the suppressor panel, the **prediction to test** is that initiation/polarity-related backgrounds will produce different response trajectories. We do not write “CUC2 is rescued” or “PIN1 is unresponsive” into the preregistration unless a pilot directly establishes those responses.

---

## 6. Candidate perturbation B — RCO/cytokinin axis

Hajheidari et al. (2019) established that RCO directly regulates cytokinin-homeostasis genes and that increasing cytokinin signaling in the RCO expression domain can promote leaf complexity.

This makes cytokinin signaling a biologically relevant second axis.

However, **the exact acute perturbation implementation for the suppressor panel is not frozen**. A spatially restricted cytokinin construct, exogenous treatment, timing, dose, reversibility and physiological burden must be verified in a feasibility cohort and with a plant-development collaborator.

Until that happens, cytokinin remains a **candidate second probe**, not part of the confirmatory protocol.

---

## 7. Reporter/readout architecture gate

The participating lab must choose a compatible readout stack before confirmatory registration.

Possible classes of readout, subject to feasibility:

- brightfield / confocal morphology and margin displacement;
- RCO-VENUS already present in the suppressor panel;
- inducible ChCUC1 red reporter where available;
- a compatible auxin/PIN reporter if spectral/genetic conflicts are resolved;
- cell segmentation and growth-field measurements using a validated imaging pipeline.

**Rule:** if a molecular reporter allows trivial genotype classification before perturbation, it must be included in `M0-all`; the active model receives no credit for information already present at baseline.

---

## 8. Confirmatory study — blinding and freezing

### 8.1 Independent cohorts

- **Feasibility/pilot cohort:** assay development only.
- **Training cohort:** model fitting and perturbation-selection algorithm development.
- **Locked confirmatory cohort:** no model tuning.

Plants from the confirmatory cohort must not be used to choose features, perturbations, doses, thresholds or hyperparameters.

### 8.2 Third-party coding

A person not involved in prediction assigns non-descriptive sample identifiers. The genotype key remains hidden until the prediction file, model hash and analysis outputs are timestamped/frozen.

### 8.3 Frozen artifact

Before unblinding, archive:

- code commit;
- environment specification;
- feature schema;
- perturbation panel and order/policy;
- model parameters/hyperparameters;
- missing-data rules;
- primary metric;
- exclusion rules;
- confirmatory sample-size calculation;
- SHA-256 of the final prediction file and analysis package.

---

## 9. Primary confirmatory endpoint: does active response add information?

For hidden mechanism/background classification, use **held-out probabilistic log loss** as the primary metric because it scores full predictive distributions and discourages overconfident guessing.

Secondary metrics may include:

- balanced accuracy;
- macro-F1;
- calibration error;
- confusion matrix by mechanistic class.

The primary comparison is paired on the same held-out plants:

`M1-active` vs `M0-all`.

A morphology-only comparison `M1-active` vs `M0-morph` is scientifically useful but insufficient by itself.

### Cross-allele generalization

Where independent alleles exist, perform a preplanned leave-allele-out test. For example:

- train on one CUC2 allele and test on the other;
- train on one NOP2A allele and test on the other.

A model that succeeds only on the exact allele seen during training is weaker evidence for mechanism-level tomography.

---

## 10. Future-outcome endpoint

Define `Y` before confirmatory data are collected. Candidate outcomes include:

- subsequent lobe/margin growth trajectory;
- final leaf contour/dissection index;
- number/geometry of induced or suppressed margin outgrowths;
- another developmental endpoint supported by the chosen assay.

The exact endpoint and time horizon must be chosen during feasibility and then frozen.

---

## 11. State-completion analysis

At a preregistered post-intervention time, define the measured present state `S`.

Fit and compare held-out predictive models for `Y`:

1. `P(Y | S)`;
2. `P(Y | S, H)`;
3. `P(Y | S, A)`;
4. `P(Y | S, G)` after genotype unblinding, for analysis only;
5. where justified, `P(Y | S, H, A, G)`.

The state is **incomplete** whenever older history, treatment assignment or hidden mechanism produces reproducible future-predictive gain after conditioning on `S`.

### Finite-sample calibration requirement

Before interpreting “no residual gain,” run the same statistic/model-comparison procedure on:

- a known-complete/Markov generative control;
- a deliberately history-dependent/non-Markov control;
- sample sizes and noise levels comparable to the biological study.

The confirmatory equivalence/noninferiority margin, if used, must be set **before unblinding** using the independent pilot, simulation calibration and a scientifically meaningful effect size. No arbitrary `R²` threshold is allowed.

---

## 12. Physiological perturbation cost

A living-system “low-disturbance” claim cannot use silhouette IoU as a proxy for biological harm.

The feasibility phase must define a preregistered cost vector using measurements the participating lab can collect reliably. Candidate components include:

- survival;
- whole-rosette growth rate;
- rate of new leaf emergence;
- delay to bolting/flowering;
- final fertility/seed set;
- local cell death or stress markers **only if a validated assay is available**.

Cost is reported as a vector or a prespecified composite whose weights are frozen before confirmatory testing.

A perturbation that is informative but causes unacceptable developmental injury is **not** a successful low-disturbance probe.

---

## 13. Random/equal-cost perturbation comparator

This comparator is required for the stronger claim that **targeted experiment selection** is better than generic perturbation.

It cannot be implemented honestly until a library of at least two biologically valid candidate probes with measured physiological costs exists.

Therefore:

- the minimum pilot may test **active response vs baseline/mock**;
- the stronger confirmatory study must compare the selected perturbation/policy against random selection from the same feasible library, matched or adjusted for measured cost.

A mechanical prick or arbitrary hormone treatment is not automatically an acceptable “random control.”

---

## 14. Sample-size rule

**No confirmatory N is specified in this draft.**

The NotebookLM synthesis suggested fixed sample sizes, but those values were not adequately grounded for this experiment and are rejected.

Instead:

1. use an independent feasibility cohort to estimate biological and measurement variance;
2. define the minimum scientifically meaningful improvement in the primary held-out metric;
3. simulate the entire frozen training/testing procedure, including class balance and replicate structure;
4. select confirmatory N to achieve a preregistered power target;
5. freeze N and the simulation code before confirmatory data collection.

If the required N is infeasible, narrow the hypothesis rather than quietly lowering the evidence standard.

---

## 15. Falsification criteria

The framework must be allowed to fail.

### F1 — No shadow gap

If `M0-all` already predicts hidden mechanism/future outcome as well as `M1-active`, the tested perturbation does not add the claimed counterfactual information.

### F2 — Perturbation response does not generalize

If active decoding works on seen alleles but fails on independent alleles of the same mechanistic class, the apparent signal may be allele-specific rather than mechanism-level.

### F3 — Candidate state remains history/mechanism dependent

If `H`, `A`, or `G` adds reproducible held-out predictive information about `Y` after conditioning on `S`, the candidate state is incomplete for that task.

### F4 — No advantage over random feasible probes

In the multi-probe study, if the designed policy does not outperform random/equal-cost selection, the claimed experimental-design advantage fails.

### F5 — Probe is physiologically unacceptable

If the selected perturbation crosses the preregistered biological-cost limit, it fails as a low-disturbance tomography probe even if it is informative.

### F6 — Result is metric/stage fragile

If the conclusion disappears under prespecified reasonable biological shape metrics, developmental-stage blocks or independent experimental batches, generalization is weakened.

---

## 16. Minimum viable pilot

The minimum pilot is **not yet the state-completion proof**. Its purpose is to establish that a prospective living perturbation can reveal hidden developmental mechanism beyond baseline measurements.

A defensible MVP would:

1. use a small subset of verified `RCOg-V` suppressor backgrounds selected by a pilot-only morphology-matching rule;
2. include an unsuppressed `RCOg-V` positive-control line but not count it as a “hidden” class if baseline morphology trivially differs;
3. implement **one** verified perturbation plus mock;
4. record baseline and time-resolved post-perturbation measurements;
5. freeze a classifier before genotype unblinding;
6. compare `M1-active` against both `M0-morph` and `M0-all`;
7. report physiological cost;
8. use the result only to justify or reject expansion to the full state-completion study.

---

## 17. Gold-standard living study

The stronger study adds:

- multiple mechanistic classes;
- independent alleles for mechanism-level generalization;
- at least two validated perturbations or a broader feasible library;
- random/equal-cost experiment-selection comparator;
- post-intervention state `S` followed by a frozen future outcome `Y`;
- explicit residual-history/genotype screening-off analysis;
- multi-batch replication;
- known-complete and known-history-dependent simulation calibration at matched N/noise;
- external preregistration before confirmatory unblinding.

Success would **not** mean “plants are Markov.” It would support the narrower statement that, for the specified measurement interface and future task, the measured state approximates an interventionally sufficient predictive representation.

---

## 18. Sources verified during this audit

### Suppressor panel

Wang Y. et al. (2025), *The Plant Journal*.  
**A suppressor screen of an Arabidopsis thaliana REDUCED COMPLEXITY (RCO)-expressing strain provides insight into the genetics of leaf margin complexity.**  
PMC full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC12165315/

### Inducible CUC1 / PIN polarity

Hu Z. et al. (2024), *PNAS* 121:e2321877121.  
**A CUC1/auxin genetic module links cell polarity to patterned tissue growth and leaf shape diversity in crucifer plants.**  
https://www.pnas.org/doi/10.1073/pnas.2321877121

### RCO / cytokinin mechanism

Hajheidari M. et al. (2019).  
**Autoregulation of RCO by Low-Affinity Binding Modulates Cytokinin Action and Shapes Leaf Diversity.**  
PubMed: https://pubmed.ncbi.nlm.nih.gov/31761704/

### Growth-based quantitative leaf framework

Kierzkowski D. et al. (2019), *Cell* 177:1405-1418.  
**A Growth-Based Framework for Leaf Shape Development and Diversity.**  
DOI: https://doi.org/10.1016/j.cell.2019.05.011

### CUC2/RCO spatial interaction

Bhatia N. et al. (2023), *Current Biology* 33:2977-2987.  
**Interspersed expression of CUP-SHAPED COTYLEDON2 and REDUCED COMPLEXITY shapes Cardamine hirsuta complex leaf form.**  
DOI: https://doi.org/10.1016/j.cub.2023.06.037

### Lab/system capability context

Max Planck Institute for Plant Breeding Research — Department of Comparative Development and Genetics (Miltos Tsiantis):  
https://www.mpipz.mpg.de/226344/tsiantis-dpt

---

## 19. Current collaboration status

As of 2026-08-29:

- NSF Mathematical Biology has been contacted for program-fit guidance;
- NSF BIO/Developmental Systems program contact Anna K. Allen has been contacted for program-fit guidance;
- Michael Levin has been contacted for conceptual/novelty criticism;
- Miltos Tsiantis has been contacted specifically about the suitability of the `RCOg-V` suppressor panel and biologically defensible perturbations/readouts.

**No reply, collaboration, material access, endorsement or funding should be implied until it actually occurs.**

---

## 20. What must be frozen in the final preregistration

The final registered protocol cannot be released until all of the following are concrete:

- participating laboratory and investigator roles;
- material availability / MTA status;
- exact genotype panel;
- growth and developmental-stage protocol;
- baseline-matching rule;
- perturbation library, dose, timing and mock conditions;
- reporter/imaging architecture;
- physiological-cost metric;
- outcome `Y` and time horizon;
- definition of current state `S`;
- model family / tuning policy;
- sample-size/power simulation;
- primary metric and statistical test;
- missing-data/exclusion rules;
- unblinding procedure;
- code/data timestamp and hashes.

Until then, this file is a **design checkpoint**, not a preregistered study.
