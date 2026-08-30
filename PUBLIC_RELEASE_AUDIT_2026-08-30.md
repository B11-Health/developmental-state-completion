# P1A Public Release Audit — 2026-08-30

Status: **READY_LOCAL**

Audited starting release candidate: `698784ecb1f6926256dfdcbc5a678b2c6d46f015` on `public-science-wave4-2026-08-30`.
Public baseline: `origin/main` = `d39aade` at audit start.
Scope reviewed: full new diff `origin/main..698784e`, plus P1A release-only corrections below. No push, publication, email, or marketplace-browser action was performed.

## Release-diff decision

The candidate is three commits ahead of the public baseline before this audit:
- `9e841d6` — audited science refresh through R15/R15A;
- `37704ec` — public release QA record;
- `698784e` — R15B independent source-level replication.

The diff adds public scientific/reproducibility material through R15B plus `PUBLIC_RELEASE_QA_2026-08-30.md`. No new grant proposal package, governance/compliance evidence, corporate-resolution material, rejected/pending media artifact, private audit video, or R16 validation artifact is present in the new filenames.

A scan of added lines in the new diff found no email addresses, SSN/EIN patterns, credential/token patterns, or other sensitive identifiers. One environment-specific internal path was found and corrected before release: `lab_lanes/r15b_source_replication/range_fetch_all.js` hard-coded a private absolute Windows workspace path; it now resolves `raw` relative to `__dirname`.

Mentions of excluded material in `PUBLIC_RELEASE_QA_2026-08-30.md` are exclusion statements only; no such artifacts are included.

## Scientific boundary review

### R10B / stale 10-of-30 wording

**Issue found and fixed.** The body of `PREPRINT.md` and `CLAIMS_AND_EVIDENCE.md` already correctly distinguished the original implemented-seed result (10/30) from the documented-preregistration-seed remediation (16/30, 53.3%), still below 24/30. The preprint abstract still stated only the superseded 10/30 figure. P1A corrected the abstract to state that 10/30 was the mismatched-seed result and that R10B obtained 16/30 under `20260830+r`, still below 24/30. Remaining 10/30 mentions are explicitly historical/provenance-qualified, not controlling sensitivity estimates.

### R11 / R11A

The public text keeps R11 as a planning diagnostic tied to the original implemented-seed directions, states only aggregate grid behavior, and does not claim replicate-wise monotonicity or universal plateau behavior. It does not replace the corrected R10B result. This matches the R11A **NEEDS QUALIFICATION** boundary.

### T8 / T8A

The public text includes the repaired condition `E[E|S,H]=0`, identifies the generalized `q` term when that condition fails, and explicitly limits the result to idealized calibration-design algebra rather than finite-sample RF/ExtraTrees gates or biology. This matches the T8A qualification boundary.

### R12 / R12A

The public text reports primary 16/30 joint success and secondary 30/30 S adequacy with 18/30 detection/joint success, calls the secondary transductive/acquisition-conditioned, avoids equating Ridge residualization with `E[Z|S]=0`, and states that Git does not independently establish the claimed pre-outcome R12 freeze. No causal upgrade is made. This matches R12A.

### R13 / R13A

The public text reports the frozen-grid joint counts 1/30, 18/30, 22/30, 20/30 and preserves the 24/30 reference. It does not promote 0.45 SD as a confirmatory threshold or claim a universal non-monotone law. R13A is described only as mechanical reproducibility/chronology support, not an independent-model scientific audit.

### R15 / R15A / R15B

The public text preserves the small-N, whole-embryo, present-state-adequacy scope and does not claim screening-off, history redundancy, Markovity, cell-lineage completion, or population-wide SLICE-1 generalization. P1A added explicit R15B provenance to `PREPRINT.md` and `CLAIMS_AND_EVIDENCE.md`: four exact released preview TIFFs were independently redownloaded, byte-size/SHA-256 identities matched, all four 49x49 feature tables regenerated exactly, and both adequacy gates plus all primary/secondary metrics reproduced to machine precision. The R15/R15A scientific qualifications remain unchanged.

## Artifact/reference review

Top-level public references in `PREPRINT.md`, `CLAIMS_AND_EVIDENCE.md`, and `PUBLIC_RELEASE_QA_2026-08-30.md` were checked against the tree: 31 unique lab-lane artifact references resolved; no broken referenced artifact path was found. The QA file was updated to identify the audited starting candidate as `698784e` and to include R15B in scope.

## Lightweight release checks rerun

- `t8_calibration_compatibility/test_t8_compatibility.py` -> **T8_TESTS_PASS**
- `t9_fixed_predictor_margin/test_t9_margin.py` -> **T9_TESTS_PASS**
- `r12_domain_balanced_calibration/test_r12_domain_balanced.py` -> **R12_TESTS_PASS**
- `r13_domainwise_sensitivity_surface/test_r13_contract.py` -> **R13_CONTRACT_TEST_PASS**
- `r13_domainwise_sensitivity_surface/test_r13_results.py` -> **R13_RESULTS_TEST_PASS**
- `r15a_independent_audit/audit_r15a.py` -> both gates reproduce; reported R2/history deltas match with maximum discrepancy <= 2.3e-16.

The R15A rerun rewrote only last-bit floating-point serialization in `RECOMPUTED.json`; P1A restored that generated file to the committed release-candidate version because the numerical result and audit decision are unchanged.

## P1A corrections

1. Corrected stale abstract wording from controlling 10/30 to the R10B documented-seed 16/30 result while preserving 10/30 as provenance.
2. Removed the private absolute Windows workspace path from R15B `range_fetch_all.js`.
3. Added explicit R15B source-level replication language and artifact reference to the public preprint/claims ledger.
4. Updated `PUBLIC_RELEASE_QA_2026-08-30.md` to identify `698784e` as the P1A starting candidate and include R15B in scope.
5. Removed one trailing-whitespace defect in the newly added T8A audit text so the full public diff passes `git diff --check`.

## Final gate

**READY_LOCAL.** After the corrections above, the local release candidate is scoped to audited public science through R15B plus release QA, contains no newly introduced sensitive identifiers or excluded institutional/media/R16 packages in the new diff, and its public scientific wording respects the audited R10B/R11A/T8A/R12A/R13A/R15A/R15B boundaries.

No push was performed.

P1A_COMPLETE
