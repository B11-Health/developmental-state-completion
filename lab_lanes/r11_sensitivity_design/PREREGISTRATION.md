# R11 Preregistration — Calibration-Failure Decomposition and Sensitivity Surface

Date: 2026-08-30
Status: FROZEN BEFORE NEW R11 SCALE EVALUATION

## Purpose
R10 observed a near-zero older-history increment in the one R9-adequate Tribolium radial task, but its +0.30 target-SD known-incomplete calibration achieved only 10/30 joint successes versus 24/30 required. R11 does **not** reinterpret that near-zero result. It asks why the calibration failed and what a future adequately powered design would need.

## Frozen decomposition
R10's existing 30 decisions are partitioned into four mutually exclusive categories: (A) S-only adequacy preserved and Gate 2 detects H; (B) S-only adequacy preserved but Gate 2 fails; (C) Gate 2 detects H but S-only adequacy is lost; (D) neither. This decomposition is descriptive of already-frozen R10 results.

## Planning-only sensitivity surface
Use the exact R10 task, percentile registration, cohorts, RF/ExtraTrees models, history columns, seeds, residual-history construction, folds, and Gate-2 rule. Evaluate the same first 20 residual-history directions at injected scales 0.15, 0.30, 0.45, and 0.60 times the original target SD. The 0.30 results are inherited from R10 and must not be refit. New fits are only 0.15, 0.45, and 0.60.

For each scale report separately:
1. A(scale): fraction preserving the original two-model S-only absolute-adequacy prerequisite;
2. D(scale): fraction satisfying Gate 2 regardless of S-only adequacy;
3. J(scale): fraction satisfying both;
4. D|A(scale): Gate-2 detection conditional on S-only adequacy.

This is a prospective **design diagnostic**, not a new biological test and not a replacement for R10's preregistered 0.30 decision.

## Hypothesis under test
Because a known-incomplete injected component is deliberately unpredictable from S, increasing its amplitude can improve H detectability while simultaneously degrading absolute S-only prediction. Therefore J(scale) need not be monotone in effect size. R11 will preserve both axes instead of collapsing them into a single generic 'power' label.

## Stop/claim rules
- No screening-off, Markovity, memorylessness, or biological-history claim can be upgraded from R11.
- Do not choose a favorable scale after results and call it the new threshold.
- Do not change models, folds, features, history coordinates, outcome, registration, or seed family.
- Any future confirmatory calibration threshold must be chosen prospectively using this planning surface, not retrospectively applied to R10.

## Post-audit provenance addendum (added after R11 execution; does not alter the frozen design)
Independent R11A audit established that the phrase "exact R10 ... seeds" above refers to the **implemented** R10 calibration seed family, `20260830 + 500000 + r`. The literal R10 preregistration had instead written `20260830 + r`. R11 paired its scales correctly to the implemented R10 first-20 directions, but those directions were not literal-seed-formula compliant with R10's preregistration.

R10B subsequently executed the documented R10 seed family and obtained 16/30 joint calibration successes versus the frozen 24/30 requirement, so the calibration-limited decision survived. R11 remains a planning surface for the original implemented-seed directions and does not replace R10B.
