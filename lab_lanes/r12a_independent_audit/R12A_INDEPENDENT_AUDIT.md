# R12A Independent Adversarial Audit — R12 Domain-Balanced Calibration

Date: 2026-08-30
Base audited: local main `7b3537c8fa48b85373bd6a93644972b15292a3ee`
Audit branch: `lab-r12a-independent-audit-2026-08-30`
Overall verdict: **NEEDS QUALIFICATION**

## Executive verdict

The numerical R12 claims are reproducible and the frozen computational settings are implemented as stated: the documented seed family is exactly `20260830 + r` for 30 unique replicates; the injection is `+0.30 * np.std(original Y)`; R12 imports the unchanged R10 RF/ExtraTrees models, reciprocal acquisition folds, and Gate-2 rule; the primary geometry gives 16/30 joint successes with exactly the R10B success set; and the secondary domainwise residualizer gives 30/30 S-only adequacy, 18/30 Gate-2 detections, and 18/30 joint successes. Independent spot refits reproduce committed metrics to machine precision.

Two qualifications prevent an unqualified PASS. First, Git cannot independently verify the claimed preregistration chronology: `PREREGISTRATION.md`, implementation, all results, tests, and the R12 checkpoint were first added together in commit `7b3537c`. The design text may in fact have been frozen before runs, but the repository history does not establish that fact. Second, the checkpoint overstates what Ridge residualization guarantees when it describes directions as globally or domainwise “S-unpredictable.” Ridge residuals are not conditional-mean residuals and are not even exactly linearly orthogonal under penalization. The safe description is “Ridge-residualized against S,” with the secondary geometry additionally using acquisition-specific unlabeled S/H and acquisition labels.

The headline **“domainwise residualization removes adequacy collapse but detection remains insufficient”** is supported only as a finite, task/model/seed-grid description: under the secondary geometry, S-only adequacy is 30/30 while Gate 2 and joint success are 18/30, below the frozen 24/30 criterion. Stronger causal language about what *caused* R10B failure is not supported.

## 1. Preregistration chronology — NEEDS QUALIFICATION

R12 states `Status: FROZEN BEFORE R12 OUTCOME EVALUATION`. The audited commit has parent `f3908cf328b15644477d8f4bc1264001938da7e7` (the corrected T8 commit), so R12 is chronologically downstream of R10B, R11/R11A, and T8/T8A. However, `git log -- lab_lanes/r12_domain_balanced_calibration` contains only one commit, `7b3537c`, and `git show --name-status 7b3537c` shows that the preregistration, implementation, result chunks, summaries, tests, provenance, and checkpoint were all added in that same commit.

Therefore:

- **Supported:** R12 was committed after the referenced R10B/R11/T8 evidence.
- **Not independently established:** that the R12 design file was version-frozen before any R12 outcome was evaluated, or that no geometry was tried and discarded before the committed two geometries.
- **Exact correction:** replace any audit-level assertion that preregistration chronology is verified with: “The committed R12 design declares itself frozen before evaluation, but Git history does not independently timestamp the design before the result artifacts.”

This is a provenance limitation, not evidence that post-hoc geometry changes actually occurred.

## 2. Seed family, replicate uniqueness, scale, models, folds, and Gate 2 — PASS

Independent reconstruction from the committed decision chunks found for both R12 geometries:

- exactly 30 records;
- exactly 30 unique replicate IDs, `0..29`;
- exact direction seeds `20260830 + replicate`;
- no duplicate or missing replicate IDs;
- injection scale fixed at `0.30` times the pooled original outcome SD;
- original outcome SD under the frozen table: `0.0013937937146818124` using NumPy population SD (`ddof=0`).

`r12_domain_balanced.py` dynamically imports `r10_history_calibration.py`. That R10 implementation has not changed since commit `a34f7aa8736c4db91921c5790524cf4a50bc8d3e`. Thus R12 uses the exact same:

- Random Forest: 300 trees, `min_samples_leaf=4`, `max_features=0.8`, seed 20260830;
- Extra Trees: 300 trees, `min_samples_leaf=3`, `max_features=0.9`, seed 20260830;
- reciprocal whole-acquisition 01/02 holdouts;
- S-only and S+H fit structure;
- S-only adequacy definition;
- Gate-2 requirement: both RF and ET have positive delta-R2 in both folds, mean delta-R2 >= 0.02, and S+H remains adequate.

No scale, seed, model, fold, or gate mismatch was found.

## 3. R10B reference provenance — PASS

R10B was committed earlier at `7db8d78b1d703bd6a85324b1180d855b64921da9` and records 23/30 adequacy, 19/30 Gate-2 detection, and 16/30 joint successes under the documented `20260830+r` seed family.

R12 does not call the R10B fitter. The R12 run path constructs only R12 geometries; its aggregation path reads the already-existing `r10b_seed_remediation/results/results.json` as a fixed reference. The R12 unit test also loads the committed R10B decision chunks only to compare success identities. Independent R10B spot refits of replicates 0 and 20 reproduce the committed R10B metrics to <= `3.1e-16` absolute difference.

Therefore the claim that the R10B reference was **not refit as an R12 arm** is supported.

## 4. Primary domain-balanced geometry — PASS numerically; causal interpretation qualified

Independent aggregation gives:

- S-only adequacy: **22/30**;
- Gate-2 detection: **19/30**;
- joint success: **16/30**;
- four-way decomposition: 16 joint, 6 adequacy-only, 3 detection-only, 5 neither.

Primary success replicates are exactly:

`[0, 5, 6, 9, 11, 12, 13, 15, 16, 20, 22, 24, 25, 26, 28, 29]`.

That set is exactly identical to the R10B success set. Gate-2 status is identical for all 30 directions. S-only adequacy differs for exactly one replicate, replicate 2, which does not alter the joint-success set.

The primary transform does perform the stated first-two-moment balancing. Across all 30 directions, each acquisition's balanced hidden direction has mean zero and SD one to machine precision; because both groups are individually zero-mean/unit-SD, pooled SD is also one to machine precision. The original R10B pooled residual directions did have nontrivial cross-domain SD imbalance: the larger/smaller domain-SD ratio across directions ranges from about `1.0016` to `1.4269`, median `1.1220`.

**Safe inference:** equalizing acquisition-specific mean and variance of the pooled Ridge residual did not improve the R10B joint count or change which directions jointly succeeded.

**Unsafe stronger inference:** “unequal acquisition-level scaling was not primarily causal” or “variance imbalance does not explain the failure.” A post-hoc transform that leaves a finite model/gate outcome unchanged does not identify a unique causal bottleneck, and it does not test higher moments, nonlinear S-predictability, or interactions with model fitting.

## 5. Secondary domainwise residualizer — PASS numerically; estimand/deployment qualification required

Independent aggregation gives:

- S-only adequacy: **30/30**;
- Gate-2 detection: **18/30**;
- joint success: **18/30**;
- four-way decomposition: 18 joint, 12 adequacy-only, 0 detection-only, 0 neither.

Secondary success replicates are:

`[0, 3, 5, 6, 8, 9, 11, 12, 13, 15, 16, 21, 22, 24, 25, 26, 27, 29]`.

Relative to R10B, four new successes appear (`3, 8, 21, 27`) and two R10B successes are lost (`20, 28`). Independent spot refits explicitly covered replicate 3 (new success) and replicates 20/28 (lost success) and reproduce the committed metrics to <= `2.0e-16` absolute difference.

The statement **“domainwise residualization removes adequacy collapse but detection remains insufficient”** is supported with this scope:

> For these 30 documented directions, under this secondary post-hoc calibration geometry and the frozen RF/ExtraTrees/Gate-2 stack, no S-only adequacy failures occur, while Gate 2 detects 18/30 and joint success is 18/30, below the frozen 24/30 standard.

It must not be generalized to new seeds, acquisitions, estimators, or biological history.

## 6. Outcome leakage and target-domain information — NO OUTCOME LEAKAGE FOUND; TRANSDUCTIVE TARGET-DOMAIN USE PRESENT BY DESIGN

The hidden-direction transforms use only S, H, the acquisition label, and the random seed. Y is not passed into either residualizer. Y enters only in two declared places: computing the inherited pooled `np.std(y)` injection scale and fitting/evaluating the prediction models after synthetic outcome construction. No direct outcome leakage into the residualization geometry was found.

However, both R10B/R12 operate on the R9 transductive representation, and R12 constructs synthetic hidden directions on the full two-acquisition S/H table before reciprocal prediction fits. The primary residualizer is pooled across both acquisitions and the within-domain standardizer uses acquisition identity. The secondary geometry goes further: it fits a separate `S -> z` Ridge inside each acquisition using that acquisition's unlabeled S/H, including the acquisition later treated as the held-out prediction domain.

This is **not outcome leakage** under the declared transductive calibration estimand, because no held-out Y is used in the transforms. But it is target-domain covariate access and would be leakage relative to an inductive/target-free deployment claim. R12 correctly labels the work post-hoc planning; future summaries should make “outcome-blind transductive target-domain adaptation” explicit.

## 7. Residualization does not imply S-unpredictability — NEEDS CORRECTION

The checkpoint says pooled residualization asks for a “globally S-unpredictable” direction and domainwise residualization makes the direction “S-unpredictable separately inside each acquisition.” That is too strong.

The implementation uses `Ridge(alpha=1)`, not the population conditional expectation `E[Z|S]`, and Ridge penalization does not produce exact orthogonality to the design matrix. After constructing the committed residualized directions, fitting the same Ridge family back from S to the residualized hidden direction gives nonzero in-sample R2:

- primary pooled geometry: approximately `0.0140` to `0.0235`, median `0.0203` across 30 directions;
- secondary domainwise geometry: approximately `0.0294` to `0.2078`, median `0.0765` across the 60 direction-domain combinations.

These numbers are not a new inference target; they are a countercheck showing that “unpredictable from S” is not a property guaranteed by the code.

**Exact correction:** use “pooled Ridge-residualized against S” and “acquisition-specific Ridge-residualized against S,” not “S-unpredictable.” Do not equate either construction with the T8 oracle assumption `E[Z|S]=0`.

## 8. Relation to T8 — PASS if kept as analogy only

The corrected T8 theorem explicitly states that its conditional-expectation assumptions are idealized oracle conditions and do not establish why R10/R11/R12 finite-sample RF/ExtraTrees gates pass or fail. R12 does not satisfy or test those oracle assumptions merely by applying Ridge residualization.

Therefore T8 can motivate an adequacy/detectability compatibility concern, but cannot causally explain R12's 30/30 secondary adequacy or 18/30 detection, and cannot turn the finite empirical result into a theorem.

## 9. Aggregation and normalization bugs — PASS

Independent decision reconstruction from the committed per-fold metric CSVs yielded zero mismatches with the committed per-replicate decision JSON for both geometries. The aggregation code also explicitly rejects anything other than the exact unique replicate set `0..29`.

No evidence was found for:

- duplicate or missing replicates;
- wrong seed mapping;
- incorrect scale;
- RF/ExtraTrees hyperparameter drift;
- fold drift;
- Gate-2 drift;
- decision/metric aggregation mismatch;
- within-acquisition mean/SD normalization error.

## 10. Independent spot refits

`audit_r12a.py` independently reconstructs the R8 table, percentile S/H representation, random directions, Ridge residualization geometries, RF/ExtraTrees fits, adequacy rule, and Gate 2 without calling the R12 fitting functions. Spot refits cover:

- primary reps 0 and 3;
- secondary reps 3, 20, and 28;
- R10B reference reps 0 and 20.

Maximum absolute difference versus committed numeric metrics is <= `4.1e-16`. Results are recorded in `audit_results.json`.

## 11. Exact corrections to R12 wording

1. **Preregistration provenance**
   - Current implication: chronology is independently verified.
   - Corrected: “The committed R12 preregistration declares itself frozen before evaluation, but Git history adds design and results in the same commit, so the pre-outcome freeze is not independently auditable from repository chronology.”

2. **Primary causal wording**
   - Avoid: “the original failure is not primarily caused by unequal acquisition-level scaling.”
   - Use: “within-acquisition centering/scaling of the pooled Ridge residual did not improve the 16/30 joint result or alter the R10B joint-success identities.”

3. **S-unpredictability wording**
   - Avoid: “globally S-unpredictable” / “S-unpredictable within each acquisition.”
   - Use: “pooled Ridge-residualized against S” / “acquisition-specific Ridge-residualized against S.”

4. **Secondary interpretation**
   - Keep only with finite-grid scope: “the secondary domainwise Ridge-residualized geometry eliminates S-only adequacy failures among these 30 documented directions, but Gate-2/joint detection is 18/30, below the frozen 24/30 criterion.”

5. **Deployment scope**
   - Add: “both geometries are outcome-blind but transductive with respect to target-domain covariates; the secondary geometry additionally uses acquisition-specific S/H to construct the synthetic direction and is not an inductive target-free procedure.”

## 12. Safe methodological statement

**Safe statement:**

> In the frozen Tribolium radial-velocity calibration task, using the documented `20260830+r` directions and the same RF/ExtraTrees reciprocal-acquisition Gate-2 pipeline, acquisition-wise centering/scaling of the pooled Ridge-residualized hidden direction leaves joint success at 16/30 with exactly the R10B success set. A secondary post-hoc geometry that Ridge-residualizes the direction separately within each acquisition yields 30/30 S-only adequacy and 18/30 Gate-2/joint successes, still below the frozen 24/30 sensitivity standard. This shows that the observed failure decomposition is sensitive to calibration geometry, but it does not identify a causal biological mechanism, prove S-screening-off, or establish an oracle `E[Z|S]=0` condition. The secondary geometry is a transductive, acquisition-conditioned planning diagnostic whose estimand must be chosen prospectively in any future confirmatory calibration.

## Final decision

**NEEDS QUALIFICATION.** Numerical and implementation claims pass independent reproduction. Qualification is required for (a) unverified pre-outcome preregistration chronology in Git, (b) overstatement of Ridge residuals as literally S-unpredictable, (c) causal language about what primarily caused the calibration failure, and (d) explicit recognition of the secondary geometry's stronger transductive/domain-conditioned estimand.

R12A_COMPLETE
