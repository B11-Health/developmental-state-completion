# R12 Claim Boundaries

## Allowed
- Equalizing the pooled residual direction to zero mean/unit variance within each acquisition leaves corrected joint success at 16/30, with exactly the same successful replicate identities as R10B.
- Acquisition-specific Ridge residualization of the synthetic direction against S preserves S-only adequacy in 30/30 and yields 18/30 Gate-2/joint successes on the 30 documented seeds.
- Calibration geometry therefore affects the decomposition of failure, but neither tested geometry reaches the frozen 24/30 sensitivity standard.
- Future calibration must choose pooled-global versus within-domain residual-history estimands prospectively.

## Not allowed
- Do not use the 18/30 secondary result to reinterpret observed near-zero history as screening-off.
- Do not call domainwise residualization a confirmatory replacement for R10B; it is post-hoc planning.
- Do not claim residual variance imbalance was or was not the main cause of R10B failure; the primary balancing transform simply did not improve joint success in this finite test.
- Do not describe either Ridge-residualized direction as literally S-unpredictable or as satisfying the T8 oracle condition `E[Z|S]=0`.
- Do not describe the secondary geometry as inductive/target-free; it uses acquisition-specific unlabeled S/H from the held-out domain to construct the synthetic direction.
- Do not claim 30/30 adequacy means the present state is sufficient; adequacy here is only the frozen prediction gate under a synthetic calibration geometry.
- Do not change scale, models, seeds, or gate after these results to chase 24/30.
