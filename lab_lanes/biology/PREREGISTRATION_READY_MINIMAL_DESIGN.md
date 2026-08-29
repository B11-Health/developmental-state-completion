# LAB LANE B1 — Smallest Defensible Prospective RCOg-V Experiment

Status: preregistration-ready **conditional design**. The confirmatory stage is not ready to launch until the Phase-0 material/cross/comparator gates below are passed.

## 1. Narrow confirmatory claim

Test only this claim:

> In a prospectively fixed set of *A. thaliana* RCOg-V genetic backgrounds, a standardized short ChCUC1 perturbation response contains blinded predictive information about hidden genetic background and a prespecified future leaf outcome beyond the complete pre-intervention baseline measurement stack.

A positive result does **not** establish global Markovity, a universal developmental state, or the topological theory in vivo.

## 2. Smallest biologically defensible panel

### Primary three-class panel

Use exactly three genetic backgrounds if material/cross feasibility is confirmed:

1. unsuppressed `RCOg-V`;
2. `cuc2-4;RCOg-V` — source-verified lobe-initiation defect, strong CUC2 allele;
3. one source-verified post-initiation suppressor chosen **before crossing based only on material/cross feasibility**, with preference order `cyp71-3;RCOg-V` then `nop2a-5;RCOg-V`.

Rationale: three classes are the smallest panel that tests more than a binary mutant-vs-control distinction while retaining a mechanistically distinct initiation class and a post-initiation class. `pin1-12;RCOg-V` is excluded from the primary panel because the proposed live response readout is PIN1:GFP polarity. `rpl34-2` is not used for independent-allele validation because the paper reports the same mutation in both recovered suppressors.

### Mandatory replication if the primary result is positive

The strongest available independent-allele replication is `cuc2-5;RCOg-V` for the CUC2 class and `nop2a-6;RCOg-V` if NOP2A is the chosen post-initiation class. Cross-allele replication is a separate validation stage and is not pooled into the primary test.

## 3. Required combined genotype / assay interface

The intended active-response assay requires, in each primary background:

- the existing `RCOg-V` transgene (RCO-VENUS);
- a functional `PIN1p::PIN1:GFP` reporter;
- the Hu dex-inducible `ChCUC1p::LhG4:GR; Op::ChCUC1:tdTomato` system.

This exact combination is **not published as validated in the RCOg-V suppressor backgrounds**. The collaborator must establish the cross/genotype feasibility, reporter function, and absence of obvious transgene-driven phenotype distortion before confirmatory data collection.

## 4. Phase 0 — feasibility only, no framework success claim

Phase 0 has six gates. Failure of any gate blocks the confirmatory study rather than being repaired post hoc.

### Gate A — material identity and transfer

Confirm for every required line:
- exact genotype and allele;
- source / stock status;
- current seed availability and viability;
- zygosity of the relevant locus/transgene;
- selectable markers and known linkage constraints;
- whether an MTA or other transfer agreement is required;
- whether redistribution is restricted.

### Gate B — combined-line feasibility

Generate or obtain the required combined backgrounds using the collaborator’s normal genetic workflow. Do not preregister an invented crossing scheme here. Confirm by genotyping/fluorescence that the intended loci/reporters are present and that the line can be propagated.

### Gate C — reporter interpretability

Confirm that:
- RCO-VENUS remains detectable in the combined lines;
- PIN1:GFP membrane localization is interpretable at the target stage;
- tdTomato induction can be detected;
- spectral bleed-through can be controlled under the selected acquisition settings;
- the selected suppressor does not make the primary reporter uninterpretable.

### Gate D — perturbation transfer

Start from Hu’s **published reference condition** for the Col-0 inducible/PIN1:GFP line: 10 µM dexamethasone + 0.01% Triton X-100 spray; DMSO-matched mock; treatment when leaf 3 is visible; leaf 4 assessed 24 h later.

This is a reference starting point, not a guaranteed final condition. Phase 0 must test whether the same condition yields a measurable but non-destructive response in each combined RCOg-V background. If the collaborator changes concentration, carrier, surfactant, application method, stage, or response time, the final choice and rationale must be frozen before confirmatory acquisition.

### Gate E — burden / physiological-cost measurement

The burden panel is **new protocol**, not published validation. At minimum choose a small, directly observable set that can distinguish developmental interrogation from gross injury. Candidate measures, subject to collaborator feasibility, are:
- short-window growth change versus matched mock;
- visible tissue injury / survival;
- developmental delay over a fixed follow-up interval.

Time to flowering and fertility/seed production are optional longer-term burden outcomes if the lab follows plants that long. No weighted burden score is permitted until component behavior is observed in Phase 0.

### Gate F — equal-cost/random perturbation comparator

A confirmatory claim about specifically informative intervention design requires an equal-cost/random comparator. The current papers do not supply one.

The collaborator must nominate a biologically legitimate alternative perturbation that:
1. can be applied at the same developmental stage;
2. has a measurable response window comparable to the active probe;
3. can be burden-matched prospectively using the Phase-0 burden measures;
4. is not expected, from the same mechanistic rationale, to directly target the ChCUC1→PIN1 margin-patterning axis;
5. has an appropriate matched vehicle/mock condition.

**No mechanical prick, generic hormone, heat shock, or other treatment is inserted here without validation.** If no defensible comparator can be nominated and burden-matched, the confirmatory experiment can still test M1-vs-M0 information gain, but it cannot claim that the chosen perturbation outperforms an equal-cost/random perturbation strategy.

## 5. Confirmatory specimen definition

Freeze one tissue/stage cohort. Recommended source-grounded target is developing leaf 4 at a length-matched stage around the Hu assay, because the dex/PIN1 response was demonstrated there. The exact permitted length window must be chosen from Phase-0 distributions before test-set genotype unblinding.

Do not pool different leaf nodes or widely different primordium stages in the primary endpoint.

## 6. Pre-intervention baseline stack (M0)

Every specimen, irrespective of arm, receives the same baseline acquisition stack before intervention:

1. leaf node / developmental timing metadata;
2. leaf or primordium length;
3. preregistered margin geometry/shape features;
4. RCO-VENUS signal features if reporter quality passes Phase 0;
5. baseline PIN1:GFP features if reporter quality passes Phase 0;
6. any other reporter channel that will later appear in M1.

Nothing available at baseline may be withheld from M0 to manufacture an intervention advantage.

### Baseline-matched primary subset

Define a morphology/development-stage matching rule from Phase-0/training data only. Freeze the metric and tolerance before unlocking confirmatory labels. Report both the full confirmatory cohort and the matched subset; designate one as primary before acquisition.

## 7. Intervention arms

For each background, randomize specimens to:

- **Active probe:** final frozen ChCUC1 dex condition.
- **Matched mock:** frozen vehicle/surfactant control.
- **Equal-cost/random comparator:** only if Gate F is passed; otherwise omit this arm and explicitly narrow the claim.
- **Comparator-matched mock:** if the comparator requires a distinct vehicle/procedure.

Randomization occurs after baseline eligibility/QC and before treatment. The allocation sequence is generated independently of imaging/model fitting.

## 8. Response acquisition

### Primary response time

Use 24 h after induction if Phase 0 confirms the Hu transfer. Any alternate time must be frozen based on Phase-0 assay quality, not confirmatory separation.

### Source-supported response features eligible for preregistration

Freeze a compact response vector derived from published modalities, for example:
- distance from a margin protrusion/convergence tip to PIN1 polarity reversal;
- frequency of PIN1 polarity classes in a preregistered region of interest;
- change in PIN1 polarity features from baseline, if the same specimen can be imaged non-destructively at both times;
- ChCUC1:tdTomato induction intensity/distribution as a treatment-engagement feature;
- RCO-VENUS response features if Phase 0 shows reliable repeated measurement.

Do not add transcriptomics, DR5, cell-death reporters, or extra fluorescent reporters to the primary model unless they are prospectively introduced and validated before preregistration.

## 9. Future developmental outcome Y

Choose exactly one primary future outcome before confirmatory acquisition. The lowest-complexity choice that is source-compatible is a quantitative later leaf-shape outcome from the same leaf, such as a fixed mature margin-complexity/shape metric. The exact metric and follow-up time are selected in Phase 0 and frozen.

A second outcome may be secondary, but the primary Y cannot be selected after seeing genotype separation.

## 10. Models

### M0 — baseline-only decoder

Inputs: complete pre-intervention baseline stack.

### M1 — active-response decoder

Inputs: exactly the M0 stack plus the frozen active-response vector.

### M2 — equal-cost/random-response decoder (conditional)

Inputs: exactly the M0 stack plus the frozen response vector measured under the comparator perturbation. This model exists only if Gate F is passed.

Use one prespecified regularized linear model and one prespecified nonlinear model. The exact estimators/hyperparameter-selection rules are frozen before confirmatory unblinding. If the primary qualitative conclusion differs across the two estimators, classify the result as estimator-dependent/unresolved.

## 11. Primary endpoint

The primary statistical endpoint is **blinded out-of-sample improvement in multiclass probabilistic prediction of hidden genetic background by M1 over M0**, using a single frozen proper scoring rule selected before acquisition (recommend multiclass log loss unless the team has a documented reason to select Brier score).

Secondary endpoints:
- the other proper scoring rule (Brier or log loss);
- balanced accuracy;
- prediction error for the frozen future outcome Y;
- M1 versus M2 if the equal-cost comparator exists;
- residual-history/state-completion statistic.

The primary claim fails if the preregistered uncertainty interval/test does not support an M1-over-M0 improvement of at least the frozen biologically meaningful threshold.

## 12. State-completion endpoint

Define before analysis:
- `H`: older measured trajectory available before the current assay window;
- `S`: the frozen current-state representation consisting of baseline + active response;
- `Y`: the frozen future leaf outcome.

Test whether adding H to a predictor already given S materially improves out-of-sample prediction of Y. Calibrate the exact history-gain statistic on known-complete and known-history-dependent simulated generators matched to the planned group structure, feature dimension, noise level and confirmatory sample size.

A non-significant H term alone is **not** evidence of completion. The test must show acceptable false-positive behavior under the complete generator and prespecified power for a biologically meaningful residual-history effect under the non-complete generator.

## 13. Blinding and information barriers

1. A person not fitting the decoder assigns non-descriptive specimen IDs and treatment codes.
2. The analysis team receives images/features without genotype labels for the confirmatory test set.
3. The genotype key remains inaccessible until all of the following are frozen:
   - eligibility/exclusion decisions made from blinded QC;
   - feature extraction code/version;
   - ROI rules;
   - decoder code and hyperparameter rule;
   - primary scoring rule and uncertainty procedure;
   - active/comparator response definitions;
   - all test-set predictions written to disk.
4. Hash the prediction file and analysis configuration before key release.
5. Only then unlock genotype/treatment identities required for final scoring.

Manual PIN1 polarity scoring, if retained, is performed by readers blinded to genotype and treatment code. Hu’s paper used two independent readers for polarity assessment; the pilot should preserve independent blinded scoring or replace it with a frozen automated rule validated before unblinding.

## 14. Exclusion and QC rules

Freeze after Phase 0 and before confirmatory acquisition:
- developmental-stage/leaf-length eligibility window;
- reporter-detection minimums;
- focus/segmentation failure criteria;
- treatment-engagement criteria, if any;
- visible injury exclusion rule, if injury makes the developmental response uninterpretable;
- specimen loss handling;
- whether exclusion is specimen-level or channel-level.

No exclusion rule may reference genotype-separation performance.

## 15. Power and sample-size plan

### No invented N

Neither Wang’s `n=10–20` mature leaves/genotype nor Hu’s `n=3` leaves/treatment for the acute polarity demonstration is a power basis for this blinded decoding endpoint.

### Phase-0 outputs required for power calculation

Estimate, without claiming success:
- acquisition/segmentation failure rate;
- within-background variance/covariance of the frozen baseline and response features;
- response variance under dex and mock;
- between-specimen correlation if repeated imaging is used;
- class-conditional score distributions for M0 and M1 under cross-validation confined to Phase 0/training data;
- burden/comparator variance if M2 is planned.

### Confirmatory N selection

Before confirmatory acquisition, run simulation/resampling using the Phase-0 variance structure and a **predeclared minimum biologically meaningful M1–M0 improvement**, not the most favorable observed pilot effect. Select N to achieve at least 90% power for that threshold at the prespecified type-I error level, incorporating expected acquisition failures and the group-aware train/test structure.

If the pilot is too small to estimate variance stably, widen the variance range in sensitivity simulations or collect more feasibility data. Do not substitute an arbitrary N.

## 16. Hard falsification criteria

The primary hypothesis is falsified or materially weakened if any of the following occurs:

1. **No shadow gap:** M0 already predicts background/future outcome at essentially the same level as M1 within the frozen meaningful-effect threshold.
2. **No intervention information gain:** M1 does not improve blinded out-of-sample proper score over M0.
3. **Generic perturbation explanation:** when M2 is available, the active probe does not outperform the burden-matched comparator to the preregistered threshold.
4. **Damage/stress confound:** active-probe burden exceeds the frozen interpretability limit or response tracks nonspecific injury rather than the developmental readout.
5. **No allele transfer:** a positive class effect disappears on the independent allele replication planned for that pathway.
6. **Residual history remains:** H produces a materially positive calibrated gain after conditioning on S with adequate power to detect the prespecified residual-history effect.
7. **Estimator dependence:** prespecified linear and nonlinear estimators yield opposing primary conclusions.
8. **Stage fragility:** the result exists only under a post-hoc stage/matching tolerance and fails the frozen tolerance analysis.

## 17. Decision gates

- **GO to Phase 0:** yes. The papers support a concrete biological substrate and acute perturbation/readout.
- **GO to confirmatory study:** conditional on Gates A–F and frozen power analysis.
- **GO to an “optimal intervention” claim:** only if the equal-cost/random comparator is validated and M1 prospectively exceeds M2.
- **GO to a state-completion claim:** only if the history-gain test is calibrated for both false positives and power and survives blinded confirmatory analysis.
