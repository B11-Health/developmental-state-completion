# F1 — NSF 26-520 Mathematical Biology submission-ready planning

Date: 2026-08-29
Status: internal planning draft; not submitted.
Ranking: **GO — contingent on institutional submission readiness and final team structure.**

## One-page concept summary
**Working title:** `MB: Intervention-indexed predictive state completion in developmental systems`

Biological science routinely compresses a developing organism into a present “state,” yet there is rarely an operational test that the chosen measurements are sufficient for a specified future and intervention family. Older history can remain predictive either because biology retains unresolved memory or because the present measurement/interface is incomplete. This project develops a mathematical theory for deciding, at finite resolution and under controlled perturbations, when a measured present state is sufficiently predictive for a declared developmental task.

The framework treats a hidden world as a joint state-law object `w=(x, theta)` and compares worlds through their response signatures under a finite experiment set. The proposal will formalize monotone refinement of experimentally indistinguishable connected components as interventions are added; stability/sandwich bounds under bounded signature error; finite separating sets under explicit richness assumptions; lower bounds on counterfactual representation dimension; and conditions under which greedy experiment selection is safe or provably unsafe. Established connections to observability, structural identifiability, predictive-state representations, causal states, bisimulation and Reeb-space/Stein-factor ideas will be stated as precedents rather than renamed as new mathematics.

A second thrust makes the theory statistically testable. The exact residual-history statistic and decoder will be calibrated on known-complete and known-history-dependent simulators matched to biological sample size, grouping, feature dimension and noise. Existing Refahi FM1 reanalysis serves only as an observational benchmark: current 120 h geometry plus 25-channel atlas state substantially improves prediction of 132 h growth beyond geometry, while the remaining 96 h history gain is small and model-sensitive, especially in late L1. It is not evidence of universal Markovity.

A biological validation interface will use a narrowly preregistered Arabidopsis perturbation problem if a qualified wet-lab collaborator is secured. The current candidate is the RCOg-V suppressor system with a published inducible ChCUC1/PIN1 response interface. No dose, cross, material availability, sample size or physiological burden threshold will be invented. The mathematical proposal remains publishable even if the wet-lab arm is delayed: the core deliverables are theorem/counterexample results, executable finite-world tests, calibrated estimators and open benchmark code.

## Intellectual Merit
The project asks a foundational mathematical-biology question: what finite measurements and interventions are sufficient to identify the future-relevant predictive quotient of a partially observed developmental system? Merit rests on (1) a precise finite-resolution inverse problem over joint state-law worlds; (2) provable refinement and stability results; (3) explicit impossibility/lower-bound results; (4) adversarial analysis of experimental design heuristics; and (5) statistics calibrated against known complete/incomplete generators rather than equating non-significance with state completion. The work is designed to produce both positive theorems and frozen counterexamples.

## Broader Impacts
Deliver open-source simulation, calibration and analysis tools that let experimentalists test whether a proposed state representation actually screens off older measured history for a defined task. Release reproducible benchmark datasets/workflows, concise teaching material on predictive sufficiency versus biological memory, and transparent negative results. Where feasible, involve trainees at the math/biology/computation boundary and create reusable preregistration templates for intervention-based state tests. No claim is made here about specific trainee numbers or institutional programs not yet arranged.

## Specific Aims
1. **Theory:** prove or falsify finite-resolution results for intervention-indexed predictive equivalence, connected ambiguity refinement, perturbation stability and finite separation.
2. **Algorithms/statistics:** develop and benchmark experiment-selection rules and frozen residual-history tests with matched known-complete/known-incomplete calibration.
3. **Biological grounding:** test transfer on public developmental data and, contingent on collaboration/material feasibility, execute a prospective Arabidopsis perturbation benchmark with blinded decoding.

## Risk and falsification
The proposal is explicitly falsifiable. A conjecture is dropped if a finite counterexample survives audit. A greedy design rule is not promoted if it can be arbitrarily bad without additional assumptions. A biological state-completion claim fails if an active response does not improve blinded out-of-sample prediction beyond the full baseline stack, if older history remains materially predictive after calibration, if effects disappear on independent alleles, or if perturbation burden plausibly explains the response. Estimator disagreement is reported as unresolved rather than averaged away.

## Data and reproducibility plan
- Version-control all code, frozen analysis specifications and machine-readable results.
- Preserve upstream source commit hashes and provenance manifests.
- Use lineage/group-aware splits where biological relatives would otherwise leak across folds.
- Freeze decoders, feature extraction and intervention-selection rules before genotype unblinding in prospective work.
- Release simulator seeds/configurations and known-complete/known-incomplete calibration generators.
- Distinguish directly measured specimen channels from external atlas annotations.
- Archive negative/counterexample results rather than silently replacing failed conjectures.

## Collaborator gaps
- Mathematical PI/co-PI structure with demonstrable expertise in mathematical biology/dynamical systems/statistical learning.
- Developmental plant biology collaborator able to execute Arabidopsis imaging/perturbation work.
- Access to/transfer permission for candidate RCOg-V suppressor and inducible ChCUC1/PIN1 materials.
- Quantitative imaging expertise and a person independent of model fitting for specimen coding/unblinding.
- Sponsored-research/AOR support for NSF submission.

## Budget categories — no invented rates
Personnel/salary and fringe; trainee support where appropriate; computing/storage; software/cloud costs if justified; travel for collaboration/scientific dissemination; publication/data-repository costs; biological supplies and growth/imaging costs if the wet-lab aim is included; microscopy/core-facility charges; subaward to a collaborating experimental institution if used; consultant costs only if sponsor-compliant; indirect costs per the institution's verified treatment. Voluntary committed cost sharing is prohibited by the solicitation.

## Registration/certification checklist
**Verified solicitation facts:** eligible proposer categories include U.S. nonprofit non-academic research organizations directly associated with research/education; no PI restriction; LOI and preliminary proposal not required; Research.gov or Grants.gov allowed; separate collaborative proposals must use Research.gov; proposals accepted anytime, with program target dates.

**Must verify before submission:** exact legal entity name; current documentary nonprofit/tax status; active SAM registration (repo audit says active through 2027-08-19, but do not expose identifiers); Research.gov organization registration; PI account and organizational role; AOR/SPO role and authority; Grants.gov readiness if used; biosketches; current & pending support; research-security disclosures/certifications; facilities/resources; data-management and sharing plan; indirect-cost basis/rate; conflict-of-interest and other institutional policies; collaborator/subaward documents; any human/vertebrate/biosafety statements if later applicable. No application field should be guessed.
