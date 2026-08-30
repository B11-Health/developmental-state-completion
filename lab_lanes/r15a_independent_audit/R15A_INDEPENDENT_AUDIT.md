# R15A Independent Audit — SLICE-1 Multi-Embryo Preview Pilot

Date: 2026-08-30
Audited branch point: `8f5c694`
Verdict: **PASS WITH QUALIFICATIONS**

## Executive decision
The committed R15 numerical results reproduce independently from the committed derived feature tables without importing the R15 analysis implementation. The primary DS0007 adequacy gate and the secondary DS0035 cross-marker gate both reproduce exactly; all reported S-only vector R2 values and all observed S+H history deltas agree to machine precision. Git history also independently verifies that the representation/protocol was committed before the validation-derived feature/result commit, that the primary model/gate implementation was committed before the validation result commit, and that the secondary stress-test script was committed before the result commit.

The result is therefore suitable for promotion as a **small preregistered cross-embryo adequacy pilot**, not as evidence of screening-off. The history question remains unresolved because the pilot has only two development embryos, one primary validation embryo plus one secondary stress-test embryo, temporally overlapping windows within embryos, and no matched known-incomplete sensitivity calibration or permutation null.

## Independent numerical reproduction
Fresh audit code reimplemented the feature-table loading, t-8/t/t+8 windows, train-only standardization, Ridge/RF/ExtraTrees models, vector SSE/R2 calculation, adequacy rule, and S+H comparison. It did not import `r15_pilot.py` or `r15_secondary.py`.

### Primary DS0007
Training embryos: DS0004 + DS0005 only.

- Ridge: R2_vector = -0.0136182576 — fail.
- Random Forest: R2_vector = +0.0306888288 — pass.
- Extra Trees: R2_vector = +0.0566599155 — pass.
- Frozen 2-of-3 Gate 1: **PASS**.

Observed S+H minus S increments:
- Ridge: -0.0539977124
- Random Forest: -0.0088336472
- Extra Trees: -0.0080864328

### Secondary DS0035 Lamin #4 stress test
- Ridge: R2_vector = +0.0370720684 — pass.
- Random Forest: R2_vector = +0.0378014692 — pass.
- Extra Trees: R2_vector = +0.0340558652 — pass.
- Gate 1: **PASS**.

Observed S+H minus S increments:
- Ridge: -0.1126941358
- Random Forest: -0.0150741032
- Extra Trees: -0.0775617681

Maximum independent-vs-committed discrepancy is <=2.3e-16. Each committed derived table has exactly 49 rows spanning time indices 1..49.

## Chronology audit
Repository chronology is unusually clean for this pilot:

1. `2c4ff42` — preregistration, extractor, and DS0004/DS0005 development-derived features committed. DS0007/DS0035 derived features are absent.
2. `3c3700d` — exact primary models/gate code frozen.
3. `f3112fb` — exact secondary DS0035 stress-test code frozen.
4. `8f5c694` — DS0007/DS0035 derived feature tables, results, checkpoint, source hashes, and claim boundaries added.

This supports the claim that the analysis choices visible in Git were fixed before the validation results were committed. It cannot prove that no uncommitted exploratory calculation occurred outside Git, so the correct term is **repository-verified preregistration chronology**, not absolute proof of zero researcher degrees of freedom.

## Provenance audit
`SOURCE_HASHES.json` records exact byte sizes and SHA-256 hashes for the four metadata workbooks and four released full-quality preview TIFFs. Raw TIFFs are intentionally excluded from Git because of size. This audit did not independently redownload all raw TIFFs from Zenodo; it therefore verifies the committed derived-feature/result chain and recorded raw-file identities, not a second-from-network image-extraction replication. That stronger source-level replication should be done in a later independent lane if R15 becomes a headline empirical result.

## Important qualifications
1. **Tiny embryo count.** Two development embryos are insufficient for a stable population-level performance estimate. DS0007 and DS0035 are valuable falsification checks, not a population sample.
2. **Overlapping temporal windows.** Nine within-embryo windows overlap in raw time. R15 correctly treats embryo as the external validation unit; row-level uncertainty or p-values would be invalid.
3. **Secondary is not a second primary confirmatory replicate.** DS0035 was predeclared as a marker-domain stress test. It strengthens robustness context but must not be pooled with DS0007 to manufacture a larger confirmatory N.
4. **No history sensitivity calibration.** Negative observed Delta R2 in both held-out embryos cannot establish screening-off or history redundancy. No matched known-incomplete power calibration or acquisition-respecting null was performed.
5. **Whole-embryo preview state only.** This does not test cell-lineage state completion or molecular state. The eight coordinates summarize four-view whole-embryo image geometry.
6. **Modest effect size.** Positive held-out vector R2 is only about 0.03–0.057. The important result is crossing the frozen train-only-naive adequacy gate in unseen embryos, not high explained variance.

## Safe scientific statement
A defensible statement is:

> In a preregistered pilot using 2025 SLICE-1 Tribolium whole-embryo preview movies, an eight-coordinate current image-geometry state achieved modest positive four-hour-future vector prediction in an unseen Cytok8 embryo for Random Forest and Extra Trees and in a predeclared Lamin-domain stress-test embryo for all three frozen models. Adding the four-hour-older image state reduced held-out R2 in both embryos, but the pilot is too small and lacks matched sensitivity calibration, so the history question remains unresolved.

## Verdict
**PASS WITH QUALIFICATIONS** for the cross-embryo adequacy pilot and its reported numerical results.

**NO PROMOTION** of screening-off/history redundancy.

R15A_COMPLETE
