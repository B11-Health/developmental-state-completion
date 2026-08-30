# T6 Empirical Implications

Date: 2026-08-30
Status: experimental interpretation only; no biological claim is established by topology alone.

## Core implication
A binary latent branch does **not** imply that one continuous real-valued biomarker can globally complete the measured state.

T5 says that if two future-distinct connected components share the same present measurement, one set-theoretic branch bit can name them. T6 shows that a globally continuous realization of that label may be impossible in one real channel and may require several channels.

The cleanest witness is `S^n->RP^n`: every measurement fiber has only two states, yet any continuous Euclidean augmentation that separates every pair needs at least `n+1` real channels.

## What this means for biological measurement design
Suppose a measured developmental state appears locally adequate but residual history or perturbation response suggests two globally distinct branches. A tempting next step is to search for "the missing scalar biomarker." T6 says that strategy can fail for topological reasons even in a noiseless idealization.

A more defensible experimental menu is:

1. **Multi-channel completion.** Search for a vector of present measurements whose joint geometry separates the hidden branch globally.
2. **Local-chart biomarkers.** Use different scalar markers in different regions of state space, with an explicit chart/region indicator. This accepts that no single globally continuous scalar exists.
3. **Discontinuous classification.** A branch classifier can still exist as a set-theoretic or learned decision rule, but its discontinuity boundaries must be treated as a feature, not silently interpreted as smooth biology.
4. **Non-Euclidean observables.** Phase/angle/cyclic observables can sometimes encode branch information that no real scalar can. Sensor codomain matters.
5. **Perturbation-assisted disambiguation.** If passive present measurements cannot globally separate branches at low dimension, interventions can act as additional response coordinates.

## Falsifiable experimental pattern
A topology-motivated completion claim should predeclare:

- the present representation `S`;
- the branch ambiguity to be resolved;
- the candidate measurement codomain (`R`, `R^2`, fluorescence panel, cyclic phase, local chart, etc.);
- a held-out criterion that requires the candidate to distinguish branch states prospectively;
- whether continuity/smoothness is a scientific assumption or merely a model convenience;
- stress tests near chart boundaries or branch-switching regions.

Evidence compatible with a topological obstruction would look like:

- every scalar candidate fails somewhere along a closed loop or symmetric family of states;
- two or more channels jointly resolve the ambiguity;
- local scalar markers work in patches but require branch-dependent relabeling after transport around a loop;
- a learned scalar classifier develops an unavoidable discontinuity/cut even when prediction is otherwise strong.

This pattern would motivate topology as an explanation, but it would not by itself identify the exact latent manifold or covering.

## Negative controls and alternative explanations
Before invoking topology, rule out easier explanations:

- poor absolute predictive adequacy;
- batch/acquisition confounding;
- model misspecification;
- measurement noise causing apparent collisions;
- insufficient temporal resolution;
- unmeasured continuous variables rather than branch topology;
- label leakage or post-outcome feature construction.

T6 is an obstruction theorem in an idealized mathematical model, not a shortcut around empirical validation.

## Design heuristic for the living-study program
If a candidate branch completion is binary by outcome labeling, do **not** assume a one-marker assay is the natural target. Instead compare:

- best scalar present marker;
- best two-channel present marker;
- a small predeclared multi-channel panel;
- local/charted scalar models;
- history-augmented baseline.

The decisive question is whether a present-only completion can achieve adequate held-out future prediction and collapse residual history across the declared perturbation family.

## Safe one-sentence takeaway
> A branch can be binary as information yet intrinsically multi-channel as a globally continuous measurement.
