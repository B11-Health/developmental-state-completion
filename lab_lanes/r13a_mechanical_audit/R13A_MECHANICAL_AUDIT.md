# R13A Mechanical Reproducibility Audit

Date: 2026-08-30
Status: **MECHANICAL PASS / INDEPENDENT-MODEL AUDIT STILL DISTINCT**

R13 has a verifiable preregistration chronology: `9487bf4` committed the scale grid and inheritance rules before implementation `aff852a` and before the first result commit `953bbe5`.

The first completed R13 result and the later exact reruns have identical aggregate summaries and identical decision booleans/replicate identities. Re-running some chunks changed only floating-point last bits: maximum absolute drift in stored per-model decision metrics was `2.220e-16` and maximum numeric drift in rerun metric CSVs was `4.996e-16`. No Gate-2, adequacy, or joint-success decision changed.

Frozen surface:
- 0.15 SD: 30/30 adequacy, 1/30 detection/joint.
- 0.30 SD: 30/30 adequacy, 18/30 detection/joint (inherited R12 arm, not refit).
- 0.45 SD: 27/30 adequacy, 23/30 detection, 22/30 joint.
- 0.60 SD: 27/30 adequacy, 22/30 detection, 20/30 joint.

The best tested point is 22/30 at 0.45 SD, still below the frozen 24/30 planning reference. This audit supports computational reproducibility and preregistration chronology; it is not a substitute for a separate independent scientific/model audit if one is required for publication-level promotion.
