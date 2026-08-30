# R13 Failure Anatomy at the Best Tested 0.45-SD Planning Point

Date: 2026-08-30
Status: descriptive decomposition of committed R13 results; no new biological claim.

R13 achieved 22/30 joint successes at 0.45 target SD. The eight failed directions decompose as follows:

- 5/30: S-only adequacy preserved, but Gate 2 failed (replicates 1, 10, 17, 19, 23).
- 1/30: Gate 2 passed, but S-only adequacy failed (replicate 20).
- 2/30: both S-only adequacy and Gate 2 failed (replicates 2, 18).

Among the five adequacy-preserved detection failures, replicates 1, 17, and 19 show the same qualitative pattern: the injected-history increment is negative in acquisition 01 and positive in acquisition 02 for both counted estimators. Replicate 10 is largely nonpositive in both acquisitions. Replicate 23 is positive in both acquisitions but misses the frozen RF mean-Delta threshold of +0.02.

This decomposition shows that the 22/30 near-miss is not explained by one homogeneous failure mode. Some directions fail because the history increment does not transfer with a stable sign across acquisitions; some fail because the present-only predictor becomes inadequate; and one fails only at the frozen effect-size threshold despite positive per-fold increments.

The safe design consequence is acquisition-level confirmation on genuinely new domains. It would be inappropriate to tune the amplitude, drop an acquisition, weaken the +0.02 rule, or choose only direction seeds that behave consistently on sequences 01/02.
