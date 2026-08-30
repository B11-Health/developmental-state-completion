# T7 Reviewer Red Team

Date: 2026-08-30

## Claim 1: "k<=n implies worst-case sphere error >=1"
**Attack:** Borsuk-Ulam only gives one antipodal collision, not a large bad set.

**Resolution:** one collision is sufficient for a worst-case bound. At the collided pair, the common decoder output must be at distance at least half of `||x-(-x)||=2` from one endpoint. No claim about average risk or measure of the bad set follows.

## Claim 2: "The lower bound is sharp"
**Attack:** perhaps no decoder can attain exactly 1 uniformly.

**Resolution:** the constant decoder `0 in R^(n+1)` has error exactly `||x||=1` for every sphere point. Therefore minimax risk is exactly 1 for every `k<=n`.

## Claim 3: "epsilon dimension jumps from 0 to n+1"
**Attack:** maybe intermediate dimensions achieve error 0.7 or 0.99.

**Resolution:** T7.1 rules out every error strictly below 1 for all `k<=n`; T6/T7.2 gives zero at `n+1`. Hence no intermediate dimension can cross the `<1` threshold.

## Claim 4: "n+1 gives a positive margin"
**Attack:** margin can be made arbitrary by rescaling.

**Resolution:** correct. `B=x` has normalized margin 2, but `cB` has margin `2|c|`. T7 explicitly treats raw margin as scale-dependent and requires fixed normalization/noise units before empirical comparison.

## Claim 5: "fiberwise injectivity on a compact finite cover gives positive margin"
**Attack:** a positive continuous function on a noncompact set can have infimum zero.

**Resolution:** compactness is explicitly required. T7.C1 gives a noncompact two-sheet counterexample with pointwise separation and zero infimum. The proof also checks that the off-diagonal fiber-pair set is compact for a finite cover.

## Claim 6: "noise below Delta/2 gives robust recovery"
**Attack:** exact nearest-neighbor recovery may fail if the base measurement is also noisy.

**Resolution:** the theorem assumes the base point `p(e)` is known exactly and only `B` receives bounded additive noise. No claim is made for noisy `h`; that requires a joint metric and geometry on neighboring fibers.

## Claim 7: "Delta/2 is sharp"
**Attack:** equality `2 eta=Delta` may still be decodable depending on the noise realization.

**Resolution:** the claim is worst-case uniform guarantee. At equality, the midpoint lies in both closed noise balls for a minimum-margin pair, so an adversary can make the observation identical. Some other noise realizations remain decodable.

## Claim 8: "probabilistic theorem applies to proper metrics"
**Attack:** 'proper metric' is ambiguous and TV/Wasserstein have different geometry.

**Resolution:** T7 uses genuine metrics on probability measures, specifically TV and Wasserstein under their standard domains. The collision lower bound uses only triangle inequality. Pairwise sharpness is stated separately: exact for TV via mixture midpoint and for `W_1`; no universal `W_p`, `p>1`, midpoint claim is made.

## Claim 9: "topological error floor explains empirical error"
**Attack:** model misspecification and finite data could dominate.

**Resolution:** agreed. `R_k` is a population representational infimum. Statistical/model-class/calibration errors are separate and can only be attributed after adequate controls.

## Claim 10: "quantitative Borsuk-Ulam novelty"
**Attack:** quantitative coincidence/waist literature is extensive.

**Resolution:** T7 makes no such novelty claim. Its sharp error-1 result is explicitly described as classical Borsuk-Ulam plus a triangle inequality and trivial upper bound.
