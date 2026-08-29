# Scientific Communications Drafts — Evidence-Safe Only

**Do not post/send automatically.** Drafts are constrained to claims supported by the current public repo and N1 novelty audit.

## LinkedIn post 1 — What survived the red-team

We tried to disprove our own novelty claims before making them louder.

The result was useful: several ideas we had been circling are **not ours to claim**. Predictive-state representations already define state through future action-conditioned predictions. Computational mechanics already groups histories by predictive equivalence. Observability and structural-identifiability theory already address hidden state and unknown dynamics. Reeb spaces already organize connected components of fibers. Active experimental design already chooses interventions to reduce uncertainty.

So the question became narrower — and, I think, more scientific:

**Can a physically measurable developmental state become sufficient for a specific family of future interventions, such that older measured history stops adding stable predictive value? And when it is not sufficient, can we use the structure of the remaining mechanism ambiguity to choose the next perturbation?**

Our current Arabidopsis flower-atlas reanalysis does not prove a universal “memoryless” state. In one late epidermal growth task, the current atlas state carries substantial predictive information and older released history adds little stable value under the tested analyses. An earlier window is much more model- and split-dependent. That contrast is exactly why we are treating state sufficiency as task-, stage-, measurement-, loss-, and decoder-relative.

The decisive experiment is still ahead: blinded living-plant discrimination of baseline-similar backgrounds, comparing algorithmically chosen perturbations with baseline-only and equal-cost/random perturbations.

That is the claim we are willing to defend today. Smaller than the original story, but much harder to knock down.

#DevelopmentalBiology #SystemsBiology #CausalInference #MachineLearning #OpenScience

---

## LinkedIn post 2 — A negative result changed the project

One of the most important results in our developmental-state project is a failure of a tempting idea.

We wanted to choose the “best next perturbation” greedily: at each step, pick the experiment that most shrinks the connected set of mechanisms still compatible with the observations.

It sounds reasonable. It can also be arbitrarily bad.

In a reproducible grid construction now in the public repository, two perturbations are individually weak but jointly cut the ambiguity dramatically. A decoy perturbation looks slightly better on the first step, so greedy selection takes it — and with a two-experiment budget the greedy/optimal utility ratio falls like `3/n`, approaching zero as the construction grows.

Why this matters biologically: “most informative experiment” is not a universal concept. An assay that is strong for parameter estimation, prediction error, entropy reduction, or pairwise separation can be poor for breaking the *specific connected mechanism ambiguity* that matters for the current hypothesis.

This does **not** mean we invented active experimental design; that field is deep and mature. It means our particular topology-sensitive objective has different optimization behavior, so we have to benchmark greedy choices against exhaustive or stronger alternatives whenever the perturbation library is small enough.

The broader lesson for our lab is simple: a framework gets more credible when it contains the tests that can embarrass it.

#ExperimentalDesign #SystemsBiology #Optimization #ScientificMethod #OpenScience

---

## Short scientific outreach email

**Subject:** Narrowed developmental-state hypothesis and prospective Arabidopsis test

Dear Colleague,

We are developing a deliberately narrow developmental-state hypothesis and would value a critical read from someone working close to plant morphogenesis and perturbation biology.

After a literature red-team, we are **not** claiming novelty for predictive-state mathematics, observability, Reeb/fiber topology, or active experimental design. Our remaining question is operational: for a specified developmental task, can a physically measurable current state make older measured history predictively redundant under calibrated held-out tests; and, when it does not, can perturbations chosen against the remaining joint state–law ambiguity outperform baseline-only and equal-cost/random perturbations?

Our current evidence is limited to direct-source FM1 reanalysis, an external lineage-based incompleteness control, and prospective source-simulator validation. We have not yet demonstrated the claim in living plants.

If this overlaps with work you think we are missing — especially prior plant studies that explicitly combine history-screening with designed perturbations — I would be grateful for the citation or criticism. That is exactly the failure mode we are trying to identify before a biological pilot.

Best,
Alfredo
Code Gym Research
