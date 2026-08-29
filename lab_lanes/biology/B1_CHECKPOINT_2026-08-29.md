# B1 Biology Lane Checkpoint — 2026-08-29

## Outcome

**Phase-0 GO; confirmatory CONDITIONAL.** The biological substrate and perturbation/readout interface are source-supported, but the decisive combined genotypes have not been shown in the audited papers. Material availability, cross feasibility, reporter compatibility, perturbation burden, and the equal-cost/random comparator remain explicit gates.

## Strongest source-supported facts

- Wang et al. directly support the RCOg-V suppressor alleles, including `cuc2-4/5`, `pin1-12`, `cyp71-3`, `nop2a-5/6`, `rpl34-2`, and `pgy1-5`, plus live RCO-VENUS imaging and mature-leaf shape quantification.
- Wang distinguishes CUC2 suppressors as lobe-initiation defects and the other tested suppressors as primarily post-initiation at the analyzed stage.
- Hu et al. directly support an *A. thaliana* dex-inducible ChCUC1/PIN1:GFP assay with a 24-h polarity response.
- Hu SI supplies a reproducible reference condition: 10 µM dexamethasone + 0.01% Triton X-100 spray, DMSO-matched mock, treatment when leaf 3 is visible, leaf 4 imaging 24 h later.
- The exact Hu inducible/PIN1 material is not published as crossed into RCOg-V suppressors.
- Neither target paper establishes public seed-stock availability or a physiological-cost calibration for this combined pilot.

## Design reduction

The smallest defensible primary panel is three classes: `RCOg-V`, `cuc2-4;RCOg-V`, and one post-initiation suppressor selected strictly on material/cross feasibility (`cyp71-3` preferred, `nop2a-5` fallback). `pin1-12` is excluded from the primary panel because PIN1 polarity is the proposed response assay.

The primary endpoint is frozen as blinded out-of-sample proper-score improvement of an active-response decoder (M1) over a complete baseline-only decoder (M0). An equal-cost/random comparator decoder (M2) is permitted only if a real plant lab validates a biologically legitimate burden-matched alternative perturbation before confirmatory acquisition.

## Files

- `BIOLOGICAL_SOURCE_AUDIT.md` — direct source audit and corrections.
- `PREREGISTRATION_READY_MINIMAL_DESIGN.md` — conditional preregistration-ready design with M0/M1/M2, blinding, falsifiers, and variance-gated power plan.
- `TSIANTIS_COLLABORATOR_QUESTIONS.md` — exact material, transfer, crossing, assay, comparator, and burden questions; no contact made.
- `_source_wang_PMC12165315.xml` — audited Wang source snapshot.
- `_source_hu_PMC11214078.xml` — audited Hu source snapshot.
- `_source_hu_SI.pdf` / `_source_hu_SI.txt` — audited Hu supplementary methods snapshot/extraction.

## Frozen cautions

1. Do not call CYP71 a demonstrated direct RCO regulator; the paper allows indirect effects.
2. Do not treat Wang/Hu original sample sizes as power justification for the decoder experiment.
3. Do not call survival, flowering, fertility, or whole-plant growth established dex-cost measures in these lines.
4. Do not claim the Hu dex condition is validated in RCOg-V suppressors until Phase 0 demonstrates transfer.
5. Do not imply seed/material availability from publication.
6. Do not claim perturbation-selection superiority unless an equal-cost/random comparator is validated prospectively.
7. Do not call a non-significant history term “state completion” without calibrated false-positive behavior and power on matched simulators.

B1_COMPLETE
