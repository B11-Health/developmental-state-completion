# T9 Fixed-Predictor Adequacy-Margin Checkpoint

Date: 2026-08-30
Decision: **EXACT FINITE-SAMPLE MSE-MARGIN IDENTITY / DESIGN USE ONLY**

For any fixed finite-sample outcome `y`, predictor `p`, baseline `b`, injection direction `z`, and amplitude `a`, the predictor's squared-error advantage over the baseline after `y_a=y+az` is exactly

`G(a)=G(0)+2a<z,p-b>`.

The common quadratic `a^2||z||^2` term cancels. If `z` is orthogonal to `p-b`, the fixed-predictor baseline-relative MSE margin is invariant to injection amplitude.

An exact add-and-subtract decomposition extends this to changed predictor/baseline choices and isolates baseline movement and refitting/generalization terms. The result clarifies why finite-sample adequacy collapse in R10–R12 cannot be attributed to synthetic variance alone.

`test_t9_margin.py` verifies the identity on random vectors, orthogonal invariance, the refit/baseline decomposition, and the audited R2 crossing counterexample. The R2 corollary is one-sided under nonzero alignment and requires positive target variance; exact orthogonality gives sign invariance wherever R2 is defined.

This is elementary algebra, not a novelty claim and not a direct theorem about the refitted cross-acquisition RF/ExtraTrees pipeline.

T9_COMPLETE
