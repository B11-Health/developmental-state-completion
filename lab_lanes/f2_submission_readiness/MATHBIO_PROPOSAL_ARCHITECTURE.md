# NSF 26-520 Mathematical Biology - Proposal Architecture

Date: 2026-08-29
Status: submission-ready **architecture**, not a submitted proposal.

## Working title
**MB: Intervention-Indexed Predictive State Completion in Developmental Systems**

## Project Summary
### Overview
Developmental systems are often represented by a measured present state, but whether that state is sufficient for a declared future task depends on what is measured, what interventions are allowed, and at what resolution worlds must be distinguished. This project develops a mathematical and statistical framework for asking when present measurements and finite perturbation responses screen off older measured history for prediction, and how experiments should be chosen to refine remaining ambiguity. Core deliverables are theorem/counterexample results, exact finite-world optimization benchmarks, calibrated residual-history tests, and open biological benchmarks. Public Arabidopsis data ground the problem; prospective living validation is included only if a qualified experimental collaboration becomes executable.

### Intellectual Merit
Treat each candidate hidden world as a joint state-law object and define equivalence by intervention-indexed future-response signatures. Characterize monotone refinement under added experiments; stability under bounded signature error; finite separation conditions; lower bounds on counterfactual representations; and structural conditions under which greedy experiment design is valid or can fail. Explicitly connect to observability/identifiability, predictive-state and causal-state representations, bisimulation, Test Cover/pair separation, active/information design, and Reeb/Stein-factor ideas. Calibrate statistical estimators on known-complete and known-history-dependent generators rather than treating non-significance as proof of completion.

### Broader Impacts
Release reproducible software, exact benchmark instances, negative/counterexample results, and educational material distinguishing morphology, measured state, hidden memory and intervention response. Provide reusable preregistration/analysis templates for state-sufficiency studies. Name trainee/community activities only when they are real and budgeted; do not invent participant counts or partners.

## Specific Aims
### Aim 1 - Theory of intervention-indexed predictive equivalence
Question: what object captures task-specific future equivalence under a finite intervention/measurement family, and what can be guaranteed about refinement/stability?

Deliverables:
- frozen definitions of world, experiment, response signature, tolerance, predictive equivalence and connected ambiguity;
- monotone-refinement result under explicit topology/signature assumptions;
- stability/sandwich bounds where valid;
- finite separating-set results under explicit richness/separability assumptions;
- lower bounds/impossibility results for counterfactual representation dimension;
- frozen counterexamples to failed conjectures.

Falsification: every theorem target receives executable finite tests/adversarial search; surviving counterexamples force removal or weakening rather than post-hoc rescue.

### Aim 2 - Exact and approximate experiment design
Question: when does greedy perturbation selection approximate the exact optimum, and when can it mislead?

Deliverables:
- exact subset optimization on reproducible finite-world bundles over declared budgets/tolerances/topologies;
- comparison with greedy connected-component reduction;
- submodularity-violation and ratio/curvature diagnostics when meaningful;
- comparison to Test Cover/pair coverage, entropy/information, active diagnosis and graph/interdiction objectives;
- sufficient structural conditions for safe greedy behavior if provable, otherwise explicit negative results.

Falsification: no generic greedy guarantee if the 3/n-style or stronger counterexamples survive; report full prespecified grids, not selected favorable settings.

### Aim 3 - Statistical state-sufficiency tests and biological grounding
Question: does older measured history add stable out-of-sample predictive value after a declared current state, and can controlled responses reduce remaining ambiguity?

Deliverables:
- frozen residual-history statistic/decoder stack;
- known-complete and known-history-dependent calibration matched to N, grouping, feature dimension and noise;
- lineage/group-aware evaluation, multiple estimators and leakage checks;
- public developmental-data benchmarks, including Refahi FM1 only with audited stage/task/model qualifications;
- optional prospective Arabidopsis interface only if material/collaborator feasibility is established.

Falsification: non-significance alone is never completion; material residual history, estimator disagreement, leakage sensitivity or instability is reported as failure/unresolved; no universal biological Markov claim.

## Project Description section map
1. Motivation and central mathematical-biology question: task-specific sufficiency, not global completion.
2. Prior work and novelty boundary: observability, identifiability, PSRs/causal states, bisimulation, Reeb/Stein, Test Cover, information design, developmental memory/fate prediction.
3. Preliminary foundation: reproducible simulator results, M1 theorem/counterexample checkpoint, audited R1 Refahi result. Historical 224-world claims only if provenance is independently recovered.
4. Aim 1 methods: formal setup, theorem targets, counterexample generation, executable theorem QA.
5. Aim 2 methods: objective family, exhaustive optimum, greedy/alternatives, approximation diagnostics.
6. Aim 3 methods: H/S/Y task, grouped splitting, model classes, matched calibration, predefined stability/effect criteria, leakage sensitivity.
7. Biological interface: public-data grounding mandatory; prospective living work contingent unless collaboration/material path is real before submission.
8. Evaluation/falsification: theorem, algorithm, statistical and biological failure rules; negative results frozen.
9. Reproducibility/data stewardship: commits, manifests, checksums, configs/seeds, provenance tiers, release plan.
10. Broader Impacts: open tools/benchmarks, negative-result practice, educational/preregistration resources tied to real activities.
11. Management/roles/timeline: mathematical, computational/statistical, biological and data-integrity roles; AOR/admin outside scientific workplan.

## Work packages
**WP1 Formalization/theorem QA:** definitions frozen; surviving theorem statements have adversarial finite tests; counterexample catalog is a valid deliverable.

**WP2 Exact perturbation design:** optimum vs greedy and alternate objectives across a prespecified grid; approximation claims require analytical/empirical support under declared assumptions.

**WP3 Statistical calibration:** matched known-complete/incomplete generators; estimator disagreement/poor calibration becomes a limitation, not averaged away.

**WP4 Public biological benchmark:** one or more frozen H/S/Y longitudinal developmental analyses with group-aware splits and leakage controls; no positive result required.

**WP5 Optional living-system interface:** enter only with actual collaborator, material/transfer path, construct compatibility, growth/imaging feasibility and pilot plan. Otherwise present as future validation/design guidance, not a funded dependency.

## Evaluation matrix
| Claim type | Success | Failure |
|---|---|---|
| Theorem | proof with explicit assumptions + adversarial finite tests | counterexample/hidden assumption invalidates statement |
| Experiment design | exact optimum comparison + justified approximation conditions | heuristic unstable/arbitrarily poor outside narrow conditions |
| State sufficiency | older H adds negligible/stable calibrated value after S for predefined task | H remains materially predictive or result flips by estimator/split |
| Biological grounding | mathematical variables map to real measurements/interventions | critical variables/perturbations unavailable or confounded |
| Prospective response test | active response improves blinded held-out prediction beyond identical baseline stack and burden controls | no improvement, stress/burden explanation, or failed replication |

## Reproducibility architecture
- Git-tracked code and immutable release commits for submitted preliminary results.
- Upstream dataset/repository hashes and provenance manifests.
- Checksums for downloaded/derived artifacts.
- Machine-readable configs/results for every benchmark.
- Frozen grouping/split rules before final analysis.
- Simulator seeds and full configuration disclosure.
- Known-complete/incomplete calibration generators released.
- Specimen-measured variables clearly separated from external atlas annotations.
- Negative/counterexample results retained.
- Prospective predictions timestamped/hashed before unblinding if living work occurs.

## Timeline / milestones
Use phase ordering until project period/personnel are finalized:
1. Formal freeze: definitions, novelty map, theorem targets, exact objectives.
2. Counterexample/optimization campaign.
3. Statistical calibration.
4. Public biological replication.
5. Integration: theory/software release and manuscripts.
6. Conditional prospective experiment only after collaboration/material/admin entry criteria clear.

## Collaborator-role architecture
Do not assign names until commitments exist:
- PI/mathematical lead;
- computational/optimization senior lead;
- statistics/ML senior person or collaborator;
- developmental-biology collaborator;
- experimental subaward lead if applicable;
- independent coding/unblinding role for prospective work.

## Document checklist
### Scientific
- [ ] Project Summary with Overview/Intellectual Merit/Broader Impacts.
- [ ] Project Description against this map.
- [ ] Specific Aims frozen.
- [ ] closest-precedent/novelty map incorporated.
- [ ] preliminary-result provenance checked.
- [ ] M1 failed conjectures excluded.
- [ ] R1 claims phrased stage/task/model-specifically.
- [ ] biological interface only describes real or explicitly contingent resources.
- [ ] falsification table included.
- [ ] broader impacts correspond to real activities.

### Administrative
- [ ] Research.gov organization registration verified.
- [ ] PI account + organization affiliation verified.
- [ ] AOR and SPO/equivalent verified.
- [ ] SAM active and reps/certs reviewed by authorized owner.
- [ ] documentary legal/nonprofit records available.
- [ ] current biosketch/current-pending/COA/personnel docs.
- [ ] Facilities/Equipment/Other Resources.
- [ ] Data Management and Sharing Plan.
- [ ] verified budget/justification including F&A treatment.
- [ ] subaward/collaboration package if applicable.
- [ ] COI policy/certification support.
- [ ] final current-PAPPG + NSF 26-520 compliance pass.
