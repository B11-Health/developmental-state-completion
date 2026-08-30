# T4 Falsification Map

Date: 2026-08-30
Purpose: distinguish observations that kill a strong version of the program from observations that merely reveal an incomplete measurement/model choice.

## Strongest defensible working thesis
A useful, falsifiable version of the program is:

> For specified developmental prediction tasks, future-relevant ambiguity can sometimes be reduced to a task/intervention-indexed predictive state that is empirically testable, and when a measured present is incomplete, carefully chosen additional measurements or perturbations can reduce that ambiguity in a way that improves calibrated out-of-sample prediction.

This thesis has three separable layers: mathematical representation, statistical diagnosis, and experimental design. A failure in one layer does not automatically falsify the others.

## 1. What would falsify a specific state-sufficiency claim
For a frozen `(H,S,Y,Pi,k)` task, a promoted sufficiency claim should be withdrawn if any of the following occurs under adequate calibration:

- older `H` adds stable held-out predictive value after `S` across prespecified estimator classes;
- the result reverses under group-safe splitting or disappears once leakage is removed;
- richer present-state representations reveal that the original `S` was a misleading coarse proxy;
- a known-incomplete matched calibration demonstrates that the pipeline would usually fail to detect the target effect;
- the claim holds observationally but fails under a prespecified intervention in `Pi`;
- the claim holds at the reported horizon but fails at a horizon that was implicitly included in the claim language.

These falsify the **specific scoped sufficiency statement**, not the entire predictive-state framework.

## 2. What would show measurement incompleteness rather than “biological memory”
Persistent residual history after `S` is consistent with missing present state if:

- adding direct present measurements reduces the history increment;
- flexible decoders extract information from `S` that simpler models miss;
- history is strongly correlated with a present latent factor that becomes directly measured later;
- intervention response reveals current-state heterogeneity aligned with the historical signal;
- known-complete simulations analyzed through the same coarse `S` also show residual history.

These patterns argue against interpreting `H` as an autonomous memory mechanism.

## 3. What evidence would be needed before a genuine path-dependence / memory claim
A stronger biological-memory interpretation would require, at minimum, a design where:

1. relevant current-state measurements are unusually rich and have demonstrated predictive sensitivity;
2. residual history remains stable across decoder classes and group-safe splits;
3. the historical variable is not merely a proxy for a current unmeasured cause;
4. interventions that specifically alter or erase the proposed memory mechanism change future behavior as predicted while matched burden controls do not;
5. the effect replicates prospectively.

Current R2/R3 evidence does not meet this standard.

## 4. What would falsify the claim that interventions can complete an incomplete predictive state
For a preregistered unknown-truth experiment-selection policy, the relevant claim fails if, with adequate power and burden controls:

- designed interventions do not improve blinded held-out future prediction over the identical baseline stack;
- random, cheap, or simple heuristic panels match or outperform the designed panel consistently;
- gains are explained by treatment injury/stress or acquisition artifacts;
- the panel improves retrospective truth-root scores but not prospective prediction;
- nominal gains vanish under realistic failure/noise/cost constraints;
- the selected interventions are not experimentally distinguishable at the available measurement resolution.

Such results would falsify the corresponding experimental-design claim and should be retained as first-class negative results.

## 5. What would falsify the finite exact-identification theory
The pair-separation theorem itself is combinatorial and cannot be empirically falsified under its definitions. What can fail is its relevance:

- real responses are too continuous/noisy to support the declared equivalence classes;
- candidate-world enumeration is badly misspecified;
- the intervention family omits mechanisms that matter for future behavior;
- cost/burden constraints make exact separating panels infeasible;
- adaptive/stochastic dynamics make static signatures an inadequate representation.

These failures would require a richer model, not a denial of the finite theorem.

## 6. What would kill the global kernel/factorization interpretation
The global factorization claim requires explicit assumptions. It fails if:

- `h` is not regular on the region of interest and singular fibers matter;
- fibers are disconnected and future response differs across components;
- the kernel inclusion fails on any material region;
- future response is stochastic in a way not represented by `F` or its distribution-valued analogue;
- the intervention family changes hidden variables not encoded by the measurement map.

T4's `h(x)=x^2, F(x)=x` branch example already kills the assumption-free global statement.

## 7. What would falsify the broader research program
The broad program should be considered substantially weakened if a well-powered, preregistered cross-system campaign repeatedly finds all of the following:

1. no reproducible task where calibrated enrichment of `S` drives the incremental value of `H` toward a stable negligible range;
2. no reproducible task where ambiguity-guided measurement/perturbation selection improves prospective prediction beyond strong simple baselines;
3. cross-system results are dominated by estimator instability, leakage, or inaccessible measurement requirements;
4. mathematical ambiguity objectives have no robust relationship to experimentally measurable prediction gains;
5. the allegedly distinctive formal objects reduce entirely to existing predictive-state/observability/Test-Cover theory with no new theorem, benchmark, or empirical consequence.

That combination would not make the mathematics false, but it would falsify the claim that the proposed synthesis is a productive new scientific program.

## 8. What would strongly strengthen the program
The strongest non-hyped evidence would be a preregistered sequence like:

1. A coarse `S0` leaves stable, calibrated residual `H` value.
2. A richer release-native `S1` reduces but does not eliminate it.
3. An intervention/measurement panel chosen before outcomes are observed targets the remaining ambiguity.
4. The resulting `S2` reduces the residual `H` increment below a calibrated threshold on held-out groups.
5. The same decision rule works in a genuinely independent system.
6. A deliberately wrong/random panel fails to achieve the same reduction.
7. Burden/stress and leakage controls remain negative.

That would not prove universal Markovity. It would demonstrate **state completion as an operational, predictive, intervention-guided phenomenon** for the declared tasks.

## 9. Current evidence classification
- **FM1:** task/representation-specific evidence that recent measured state often makes older measured history nearly redundant; not universal closure.
- **R2 C. elegans:** large nonlinear residual-history gains, but calibration power below the preregistered promotion threshold; unresolved/calibration-limited.
- **R3 LARRY:** strong sister-lineage incompleteness diagnostic after day-2 panels up to 32 genes; not literal history and not full transcriptome.
- **M2:** greedy equals exact on one fully audited 17,280-row finite bundle; general greedy guarantee is false.
- **M3:** robust/cost-aware design is feasible on finite benchmarks, but robustification does not automatically preserve submodularity and synthetic planning panels are not living prescriptions.
- **B2:** prospective living Phase-0 is conditional GO; confirmatory RCOg-V remains NO-GO today.

## 10. Decision discipline
Every future result should be assigned to one of four states:

- **PROMOTE:** preregistered rule met with adequate calibration and provenance;
- **FAIL:** prespecified prediction decisively contradicted;
- **UNRESOLVED:** calibration, power, leakage, provenance, or feasibility prevents a decision;
- **OUT-OF-SCOPE:** result addresses a different task/intervention/horizon than the claim under review.

“Interesting” is not a fifth evidentiary category.
