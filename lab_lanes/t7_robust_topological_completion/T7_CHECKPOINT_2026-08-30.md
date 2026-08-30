# T7 Checkpoint — Robust/Approximate Topological Completion

Date: 2026-08-30
Branch: `lab-t7-robust-topological-completion-2026-08-30`
Base: local main `d14951c` (contains T6 at/after `f8eeaec`)

## Completed mathematical results

1. Defined a fiberwise continuous sensor margin `Delta_B` and an epsilon/minimax predictive-completion dimension.
2. Proved the sharp sphere statement for `h:S^n->RP^n`, `F(x)=x`:
   - every continuous `B:S^n->R^k`, `k<=n`, forces a common antipodal completed measurement;
   - every decoder, even discontinuous, then has worst-case Euclidean future error at least `1`;
   - the constant-zero decoder attains error exactly `1`;
   - therefore minimax risk is exactly `1` for all `k<=n`;
   - for every `epsilon<1`, the minimum continuous Euclidean completion dimension is exactly `n+1`;
   - for `epsilon>=1`, zero augmentation channels suffice.
3. Verified the `n=0` edge case separately.
4. Showed `B(x)=x in R^(n+1)` gives zero error and normalized antipodal margin `2`.
5. Proved a generic collision-to-metric-risk lower bound `delta/2`.
6. Extended that bound to future probability laws under any metric on laws, explicitly TV and Wasserstein.
7. Proved pairwise sharpness for TV via the mixture midpoint and for `W_1`; avoided an unsupported universal midpoint claim for `W_p`, `p>1`.
8. Proved that on a compact finite cover over a Hausdorff base, continuous fiberwise injectivity gives a strictly positive global separation margin.
9. Gave a noncompact two-sheet counterexample showing compactness is essential.
10. Proved the bounded additive sensor-noise threshold: exact uniform sheet recovery is guaranteed when `2 eta < Delta_B`, while at `2 eta >= Delta_B` a minimum-margin pair has intersecting closed noise balls and uniform exact recovery cannot be guaranteed.
11. Distinguished exact topology, approximate minimax prediction, decoder continuity, sensor noise, model-class error, and finite-sample/statistical error.

## Prior-art search
Using only the isolated browser on CDP 9444, searched and recorded literature around:
- Borsuk 1933 antipodal theorem;
- Yang/Bourgin-Yang coincidence results;
- Fadell-Husseini equivariant cohomological index;
- Gromov sphere waist and Memarian's proof;
- projected/fiberwise embedding literature including Melikhov;
- robust/noisy sensor placement context.

No mathematical priority claim is made. The sharp error-1 theorem is explicitly framed as classical Borsuk-Ulam plus a two-point triangle inequality and a trivial matching decoder.

## Executable witnesses
`test_t7_robust.py` passes seven checks:
- constant sphere decoder error exactly 1;
- identity antipodal margin approximately 2;
- sampled scalar circle witness detects an antipodal collision/sign change;
- compact 3-sheet example has positive margin 3;
- TV midpoint distances `(1, .5, .5)`;
- W1 midpoint distances `(2, 1, 1)`;
- noncompact margin decays below `1e-4` by `t=100000`.

Frozen values are in `t7_results.json`.

## Claim boundary
T7 does not prove average-case lower bounds from one Borsuk-Ulam collision, does not handle noisy base measurement `h`, does not equate rescaled numerical margin with physical robustness, and does not attribute empirical excess error to topology without statistical/model controls.

## Empirical implication
A binary latent branch does **not** imply one continuous biomarker can robustly complete state. Topology may force multiple channels; even below exact completion, it can impose a nonzero worst-case predictive error floor; and after exact separation is topologically possible, the panel still needs a branch-separation margin large relative to assay noise.
