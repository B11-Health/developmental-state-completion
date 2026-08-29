# F1 — NSF 26-517 BIO Core / Developmental Systems submission-ready planning

Date: 2026-08-29
Status: internal planning draft; not submitted.
Ranking: **CONDITIONAL — strong scientific fit, but do not submit until wet-lab execution and material feasibility are real.**

## One-page concept summary
**Working title:** `Prospective developmental-state completion in plants using minimal counterfactual perturbations`

Developmental phenotypes can look similar while hiding different regulatory mechanisms. The biological question is whether a small, controlled perturbation can expose a present response state that predicts a defined developmental future and hidden regulatory background better than morphology and baseline reporters alone. The project does not test whether an organism is globally Markovian; it tests task-specific state sufficiency in a fixed tissue, developmental window, measurement interface, intervention family and future endpoint.

The candidate system is Arabidopsis carrying the Cardamine hirsuta RCO transgene `pChRCO::ChRCOg-VENUS` (RCOg-V), for which Wang et al. reported multiple mechanistically distinct simplified-leaf suppressors. Hu et al. reported a dexamethasone-inducible ChCUC1 system with PIN1:GFP and demonstrated altered PIN1 polarity 24 h after induction in developing leaves. The exact combination of that inducible construct with each RCOg-V suppressor has not been established by the current audit, so crossing strategy, material availability, dose and burden are Phase-0 feasibility questions rather than proposal “facts.”

The confirmatory experiment will compare a full baseline-only model with a model receiving the identical baseline stack plus preregistered perturbation-response features. Genotype/background keys will remain blinded until feature extraction, decoder, intervention rule and prediction files are frozen. A biologically legitimate equal-cost/random comparator is desirable but will only be included if the collaborating lab can validate one with comparable physiological burden. Sample size will not be borrowed from prior papers: a pilot will estimate variance/acquisition failure, and confirmatory N will be selected by simulation before unblinding.

Primary success requires reproducible out-of-sample improvement of intervention response over baseline for hidden-background prediction and a declared continuous future developmental endpoint, while physiological disruption remains within prespecified collaborator-validated bounds. A secondary state-completion analysis asks whether older measured trajectory adds predictive value after the current response state, using matched known-complete/known-incomplete calibration.

## Intellectual Merit
The study directly tests whether distinct developmental mechanisms can be interrogated through controlled, low-dimensional perturbation responses rather than inferred from endpoint morphology alone. It combines causal developmental biology, live quantitative imaging and rigorous predictive falsification. The innovation is not “plants are Markov”; it is a prospective, blinded assay of whether a measurable intervention-response state is sufficient for a declared developmental task, with explicit failure criteria and finite-sample calibration.

## Broader Impacts
Produce reusable experimental and computational protocols for separating hidden developmental mechanisms with fewer perturbations; open analysis code and preregistration templates; share negative results and calibration workflows; and create accessible educational material showing the difference between morphology, internal developmental state and response-based mechanism identification. Broader-impact activities requiring specific partners or participant counts remain to be negotiated and should not be invented.

## Specific Aims
1. **Feasibility and assay validation:** verify material availability, construct compatibility, developmental staging, imaging, dose/mock response and physiological burden in selected backgrounds.
2. **Prospective blinded mechanism prediction:** test whether preregistered intervention-response features improve held-out prediction of hidden suppressor background and future leaf development beyond the full baseline stack.
3. **State sufficiency:** test whether older history retains calibrated predictive value after the current response state and whether success transfers to independent alleles/mechanistic backgrounds.

## Risk and falsification
Hard failures include: baseline measurements already erase the intended ambiguity; intervention response fails to improve blinded prediction; an effect does not replicate across an independent allele; perturbation causes stress/damage sufficient to explain discrimination; older history remains materially predictive after the proposed state; conclusions depend on post-hoc stage/layer pooling or a favored estimator. Phase-0 data cannot be used as confirmatory evidence. If construct introgression or material access proves impractical, narrow the biological aim rather than inventing a substitute system.

## Data and reproducibility plan
- Frozen preregistration before confirmatory acquisition.
- Non-descriptive specimen IDs and withheld genotype key.
- Same baseline channels for baseline and active models.
- Direct specimen measurements for any channel used to claim state completion; external atlases labeled as priors.
- Prespecified linear and nonlinear estimators; disagreement = unresolved.
- Calibration on known-complete and known-history-dependent generators matched to planned N/group structure/noise.
- Timestamp/hash predictions before unblinding.
- Release code, metadata schema, exclusions/QC rules and de-identified imaging-derived measurements when permitted by material/data agreements.

## Collaborator gaps
- Arabidopsis developmental lab with RCO/CUC/PIN expertise and controlled growth/imaging capacity.
- Exact material holder(s) and MTA/transfer path for RCOg-V suppressors and inducible ChCUC1/PIN1 lines.
- Expertise in crossing/genotyping and live confocal imaging.
- Independent specimen-coding/blinding function.
- Statistical/power analysis support for simulation-based confirmatory N.

## Budget categories — no invented rates
Personnel/fringe; plant growth and genotyping supplies; crossing/seed propagation; microscopy/core-facility time; imaging storage and compute; software/data infrastructure; travel/collaboration; publication/repository costs; subaward to experimental collaborator; shipping/material-transfer costs if allowable; indirect costs per verified institutional treatment. Voluntary committed cost sharing is prohibited by the solicitation.

## Registration/certification checklist
**Verified solicitation facts:** eligible proposer categories include U.S. nonprofit non-academic research organizations directly associated with research/education; no PI restriction; Research.gov or Grants.gov submission permitted; separate collaborative proposals must use Research.gov; proposals accepted anytime.

**Must verify before submission:** exact legal entity and documentary nonprofit status; SAM status; Research.gov organization and PI/AOR/SPO roles; Grants.gov if used; biosketch/current-pending support; research-security disclosures; facilities/resources; data-management plan; indirect-cost basis; organizational COI and required sponsor policies; subaward/consultant documents; material-transfer permissions; plant/biosafety compliance statements if applicable to the final protocol; all certifications generated by the active PAPPG/system at submission time.
