# NSF Mathematical Biology concept — 2026-08-29

## Working title

**Counterfactual State Completion: Mathematics for Identifying Developmental Mechanisms from Minimal Perturbations**

## Program fit

Primary target: NSF Mathematical Biology under **NSF 26-520 MPS Mathematical Sciences Research Programs**. Proposals are accepted anytime; the Mathematical Biology program lists the second Tuesday in October as its target date (October 13, 2026). The program explicitly requires mathematical innovation, biological relevance/significance, and strong integration between mathematics and biology.

Submission-readiness gate: verify that the submitting organization and PI/AOR roles satisfy Research.gov/NSF requirements before proposal assembly.

## Central question

> Given a biological system observed only through a finite measurement stack, what is the smallest family of perturbations needed to distinguish future-relevant hidden state-law worlds at a specified resolution, and how stable is that distinction under noise, model error and finite data?

## Intellectual premise

Observed morphology or molecular state can collapse distinct hidden developmental mechanisms. Rather than attempting to reconstruct every latent variable, we define state relative to a specified family of future prediction/intervention tasks. The mathematical object is an experiment-indexed inverse fiber of hidden state-law worlds consistent with the observed counterfactual signatures. Experiments refine this ambiguity, while calibrated predictive losses determine whether older history still contains future-relevant information outside the present measurement stack.

The proposal does **not** claim that predictive screening-off, Reeb spaces, observability, Blackwell comparison, conditional mutual information or predictive-state representations are new. The proposed mathematical contribution is their integration into a robust active-tomography problem on connected inverse fibers, together with new bounds/counterexamples and biologically testable experiment-selection criteria.

## Preliminary evidence / self-correction

1. **Monotone panel refinement:** under a coordinatewise sup/product discrepancy, appending experimental coordinates can only shrink the compatible world set and target connected component.
2. **Noise stability:** uniform signature perturbations yield a tolerance-sandwich bound; topology should be reported through critical tolerance intervals rather than one arbitrary threshold.
3. **Greedy failure:** an independently implemented counterexample makes the budget-two greedy/optimal connected-ambiguity utility ratio scale as `3/n`, approaching zero. Greedy topological splitting therefore has no general approximation guarantee without extra structure.
4. **Loss-aware screening-off:** under Bayes-optimal log loss, population history value is exactly `I(Y;H|S)`; under squared loss it measures only conditional-mean refinement. An XOR counterexample falsifies monotonic decrease of residual history under added conditioning variables.
5. **Public biological contrast:** direct-source FM1 flower analysis shows a partition-stable late-L1 near-zero history gain under tested linear losses, while a middle L1 interval is partition- and decoder-dependent. A public Weinreb/Klein split-well lineage dataset serves as a positive control where present-state incompleteness is strongly detected.

## Aim 1 — Robust topology of experiment-indexed causal fibers

Formalize hidden world space `W`, intervention panel `Q`, signature map `H_Q`, tolerance-compatible set `K_Q^delta`, and target connected component `C_Q^delta(w*)`.

Deliverables:

- exact monotone refinement theorems under specified product metrics;
- stability/tolerance-sandwich bounds under bounded signature error;
- critical merge/accessibility thresholds and persistence-like summaries;
- explicit relationships and non-equivalences with Reeb-space quotients, observability and bisimulation;
- finite-domain separation criteria and lower/upper bounds for counterfactual embedding dimension.

## Aim 2 — Decision-theoretic active tomography under finite experiment budgets

Develop experiment-selection objectives that target the *current connected ambiguity* rather than global parameter estimation.

Deliverables:

- exact exhaustive baselines for finite perturbation libraries;
- sufficient conditions under which greedy/adaptive selection is near-optimal;
- counterexamples when submodularity/adaptive-submodularity fails;
- cost-aware and noise-aware objectives;
- calibration of predictive screening statistics with known-complete and known-incomplete generators.

A core methodological rule is that negative held-out gain is not negative information: it is an estimator effect. Population claims are made through Bayes-risk identities; finite-sample claims are made only after matched calibration.

## Aim 3 — Biological stress tests and prospective interface

Use two qualitatively opposed public benchmarks before prospective wet-lab work:

- **Refahi FM1 Arabidopsis atlas:** task-specific late-L1 state appears nearly sufficient for descendant-growth prediction under the tested decoder family, while earlier/middle windows expose estimator dependence.
- **Weinreb/Klein hematopoietic lineage data:** sister-lineage information remains strongly predictive beyond a reduced present-state proxy, providing a positive control for state incompleteness.

Then freeze the mathematical policy before a prospective plant experiment performed with an appropriate developmental-biology collaborator.

## What would falsify the project

- the proposed connected-fiber summaries are unstable under biologically reasonable metrics/noise;
- active topology-aware experiment selection fails to outperform exhaustive/simple baselines when evaluated fairly;
- counterfactual embedding bounds are vacuous at realistic resolution;
- calibrated state-sufficiency statistics fail known complete/incomplete controls;
- the mathematics cannot produce a prospectively testable biological decision rule.

## Expected contribution

A rigorous theory of **information-bounded counterfactual tomography**: not a universal hidden-state reconstruction, but a task-specific way to quantify which developmental worlds remain experimentally indistinguishable, how that ambiguity changes with added interventions, and which next experiment is justified by the remaining connected uncertainty.
