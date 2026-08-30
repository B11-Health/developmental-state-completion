# T7 Empirical Implications: Robust Multi-Channel Biomarkers

Date: 2026-08-30
Status: experimental interpretation, not a biological claim.

## 1. The practical change from T6
T6 said that a binary latent branch need not admit a one-scalar continuous global biomarker. T7 adds two operational quantities:

- **predictive tolerance:** how much future error remains unavoidable at a given continuous channel count;
- **sensor margin:** once branches are continuously separated, how far apart their sensor representations remain compared with measurement noise.

A candidate biomarker panel should therefore be judged by both predictive adequacy and branch-separation margin, not only by whether a classifier can separate training labels.

## 2. Sphere benchmark
For the benchmark `S^n->RP^n`, if the future target is the unit vector `x`, then every continuous panel with at most `n` real channels has minimax Euclidean future error exactly `1`. This is a worst-case representational floor, not an estimation artifact.

At `n+1` channels the canonical panel `B=x` has:

- zero noiseless future error;
- antipodal sensor margin `2` in normalized units.

Thus the dimension threshold is abrupt under worst-case Euclidean loss: allowing error `0.99` still needs `n+1` channels, while allowing error `1` needs none.

## 3. Biomarker interpretation
A biological branch may be binary in a set-theoretic sense yet globally twisted across the measured-state manifold. In that situation:

- local one-marker rules can work in restricted regions;
- a globally continuous single marker can still be impossible;
- multiple channels may be required to avoid branch collisions;
- a discontinuous threshold/chart can conceal rather than remove the topology;
- sufficient channel count alone is not enough if the achieved separation margin is comparable to assay noise.

The empirical implication is therefore stronger than "measure more markers": **measure enough jointly continuous coordinates, and verify a prospective margin-to-noise ratio on future-distinct states.**

## 4. Suggested prospective diagnostic
For a frozen candidate panel `B_hat`:

1. Define the future metric/loss before fitting the panel.
2. Identify pairs or neighborhoods with nearly identical current base measurement `h` but materially distinct future outcomes.
3. Estimate the minimum cross-branch sensor separation on held-out data, with uncertainty.
4. Compare that separation with repeatability/noise from technical replicates.
5. Test whether the augmented present predicts future adequately without older history.
6. Stress the panel across the declared intervention family; added interventions can split previously equivalent branches.
7. Report failures and near-collisions, not only average classification accuracy.

## 5. Noise criterion for a finite branch model
If a finite-sheet approximation is scientifically defensible and the estimated normalized sensor margin is `Delta`, then bounded augmentation noise below `Delta/2` is the natural deterministic robustness target. This should not be applied blindly to Gaussian noise: for stochastic noise, report misclassification probability or predictive risk as a function of the full noise distribution.

Because `Delta` scales when biomarkers are rescaled, a meaningful report must state channel normalization and assay noise in the same units. Arbitrary numerical rescaling cannot create physical robustness.

## 6. Probabilistic outcomes
If two hidden branches produce future distributions `P` and `Q` rather than deterministic outcomes, a forced measurement collision imposes at least half their separation under any proper metric used here:

- total variation: lower bound `TV(P,Q)/2`;
- `W_1`: lower bound `W_1(P,Q)/2`.

This gives a direct experimental target: estimate how different the branch-conditioned future laws are. If they are almost identical, a topological branch collision may be irrelevant for the declared task even if the latent states are biologically distinct.

## 7. What would falsify the topological-completion interpretation
Evidence against the proposed interpretation includes:

- a validated globally continuous low-dimensional panel that separates the supposedly obstructed branch states;
- residual history disappearing after ordinary present-state feature enrichment without any branch-like geometry;
- branch-conditioned future laws being indistinguishable under the declared task metric;
- observed failure being explained by acquisition shift, calibration, leakage, or decoder misspecification rather than representational collision;
- no stable margin after technical noise is accounted for.

## 8. Safe empirical conclusion
A binary latent branch does not imply one continuous biomarker is globally adequate. Topology can force multiple channels; approximation can retain a nonzero minimax error floor; and even a topologically sufficient panel can be experimentally useless if its branch-separation margin is swallowed by noise.
