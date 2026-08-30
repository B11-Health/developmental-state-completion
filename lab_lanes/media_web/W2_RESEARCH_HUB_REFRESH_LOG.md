# W2 Research Hub Evidence Refresh Log

Date: 2026-08-29
Branch: `lab-media-w2-refresh-2026-08-29`
Worktree: `C:/Users/codeg/mcp-shell-auth/workspace/dsc-w2-refresh`
Base / reviewed evidence commit: `f06ac518496d1f27396ae77ae9243655a5355cf5` (`origin/main`; durable scientific results through `5753a64`)
Publication state: **LOCAL ONLY — NOT PUSHED, NOT DEPLOYED**

## Scope

Refreshed the existing W1/D1 static research hub only with reviewed durable results already integrated into `origin/main` at the base commit. The final base advanced from `5753a64` to editorial-only `f06ac51` during W2; that newer commit adds no scientific result, so public evidence content remains limited to the requested M2/B2/F2/R2 durable results. No Upwork/Fiverr interaction, social publication, push, Pages deployment, external send, or scientific-artifact rewrite was performed.

## Durable evidence incorporated

### M2 exact perturbation optimization
- Public copy now states the exact finite audit size: 128 truths × 9 tolerances × 3 topologies × 5 budgets = **17,280 rows**.
- Greedy matched exact optimum on every audited row: 0 suboptimal rows, minimum ratio 1.0, maximum additive gap 0.
- The page explicitly prevents extrapolation: concrete non-submodularity remains and the 3/n → 0 general counterexample remains controlling outside safe structure.
- Added the M2 block-sparse deletion condition only as a **sufficient** regime under which truth-rooted disconnection reduces to monotone submodular fixed-set coverage.
- Pinned evidence: `lab_lanes/m2_optimization/THEOREM_COUNTEREXAMPLE_CHECKPOINT_M2_2026-08-29.md`, all-row CSV, executable audit, plus M1 counterexample.

### R2 cross-system *C. elegans* result
- Added a dedicated observed-data result card for 701 eligible dividing tracks from two embryos.
- Reports median nonlinear history gains of +0.171 R² (HistGradientBoosting) and +0.134 R² (random forest), with the primary grouped-split stability percentages.
- Freezes the preregistered interpretation: the positive stable-history rule was **not met** because matched +0.30 target-SD incomplete-state calibration power was only 17.5–39%, below the required ≥80% for at least two estimators.
- Explicitly disallows true-state non-Markovity and molecular-memory claims.
- Pinned evidence: R2 checkpoint, preregistration, and results directory.

### B2 living-system feasibility
- Living-validation status changed from generic prospective readiness to the reviewed B2 decision: **Phase-0 conditional GO; confirmatory RCOg-V NO-GO today**.
- Names the unresolved gates without inventing availability: exact material/transfer path, three-class genetics, reporter optical separation, induction transfer, perturbation burden, and future-outcome feasibility.
- Preserves the fallback boundary: Hu-system-only access supports method-transfer feasibility, not an RCO hidden-genotype confirmatory claim.
- Pinned evidence: B2 GO/NO-GO decision, Phase-0 matrix, source ledger.

### F2 NSF submission readiness
- Funding card now states NSF 26-520 Mathematical Biology is **GO TO FULL PREPARATION**, not submission.
- Research.gov organization registration, intended-PI affiliation, AOR authority, and SPO/equivalent routing remain explicitly unverified/hard gates.
- NSF 26-517 BIO Core / Developmental Systems remains conditional on a real living experimental path.
- No submission/account/role/certification/rate/commitment is implied.
- Pinned evidence: F2 checkpoint.

## Preserved corrections / boundaries

- FM1 remains task-, stage-, representation-, decoder-, and finite-sample-specific predictive screening-off; no universal Markovity.
- No one-dimensional biology claim.
- Causal states, PSRs, observability, Reeb/Stein topology, active/information design, and related concepts are not claimed as mathematical priority.
- Historical 224-world generator/topology/ranking chain remains provenance-incomplete.
- Exact legacy 0.272→0.643 tuple remains unreproduced and is not promoted as current evidence.
- Later 128-world source-validation bundle remains simulator evidence only.
- Phase-0 feasibility is not living-plant validation.

## Commit-pin audit

All prior site evidence links were advanced from the old frozen hash to `f06ac518496d1f27396ae77ae9243655a5355cf5`.

Static repository validation:
- 22 unique commit-pinned GitHub evidence URLs extracted from the refreshed HTML.
- `git cat-file -e <commit>:<path>` succeeded for all 22 pinned paths.
- 0 pinned evidence paths missing at the reviewed commit.
- 0 references to the prior `2c914784...` checkpoint remain in `site/index.html`.

## Browser QA

Used the existing authenticated Windows Chrome CDP session at port 9222 and a local HTTP preview of `site/`; no unrelated tabs were modified.

Desktop viewport: 1440×1000
- Page title correct.
- `readyState=complete`.
- `documentElement.clientWidth = 1425`; `scrollWidth = 1425`.
- **No horizontal overflow.**

Mobile viewport: 375×812
- In a single emulation session, `documentElement.clientWidth = 375`; `scrollWidth = 375`.
- **No horizontal overflow.**
- Mobile nav toggle is visible while nav is initially hidden.
- Activating the menu changes `aria-expanded` to `true`, adds the open state, and displays the navigation.
- No ordinary body element exceeded the mobile viewport; the deliberately off-canvas accessibility skip link was excluded from this overflow diagnostic.

DOM/content spot-checks confirmed the refreshed M2, R2, B2, and F2 material is present.

## Files changed

- `site/index.html`
- `site/README.md`
- `lab_lanes/media_web/W2_RESEARCH_HUB_REFRESH_LOG.md`

`style.css` and `script.js` required no change for this evidence-only refresh.
