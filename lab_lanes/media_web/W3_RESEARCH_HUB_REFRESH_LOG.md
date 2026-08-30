# W3 Research Hub Evidence Refresh Log

Date: 2026-08-30
Branch: `lab/w3-research-hub-refresh`
Worktree: `C:/Users/codeg/mcp-shell-auth/workspace/dsc-w3-refresh`
Base / reviewed evidence commit: `fe5f049` (`origin/main`)
Publication state: **LOCAL ONLY — NOT PUSHED, NOT DEPLOYED, PAGES UNCHANGED**

## Scope

Refreshed the existing static research hub only with reviewed durable R3/M3/F3 results present on `origin/main @ fe5f049`. Preserved W2 provenance corrections, the R2 calibration-limited decision, B2 confirmatory living-study NO-GO, and the prominent “What we are NOT claiming” boundaries. The quarantined NotebookLM video is not advertised or linked. No Upwork/Fiverr interaction, social publication, external send, push, or Pages mutation was performed.

## Durable evidence incorporated

### R3 higher-dimensional LARRY control
- Added a dedicated observed-data control card using direct release-native day-2 expression panels up to 32 genes.
- Reports the richest-panel held-out sister log-loss gains: +0.328 logistic and +0.523 HistGradientBoosting.
- Explicitly states H is separated-sister fate used as an incompleteness diagnostic, not literal history.
- Explicitly states the 32-gene panel is not the full 25,289-gene transcriptome and five permutations are only directional null calibration.

### M3 robust cost-aware perturbation design
- Added the prospective unknown-truth selection rule and prohibited known-truth retrospective selection for a living pilot.
- Added the exact `pilot_tight` synthetic planning panel `0010 0100 1000`.
- Identifies cost, burden, failure probability, and tolerance/noise values as synthetic planning proxies requiring replacement before any living protocol.
- Preserves the theory boundary: pointwise minimax and worst-case one-failure dropout robustification are not generally submodular.

### F3 institutional readiness
- Updated funding/readiness language to **MathBio GO to prepare / NO-GO to submit**.
- States that the controlled Research.gov session is unauthenticated.
- Keeps organization/UEI linkage, intended-PI affiliation, Institution Administrator/PI/AOR/SPO-equivalent roles, COI support, F&A basis, disclosures/common forms, and related institutional gates unresolved.
- No institutional authority, certification, submission readiness, rate, or role is inferred.

## Preserved boundaries

- R2 remains calibration-limited; its preregistered positive stable-history rule was not met.
- B2 Phase 0 remains conditional GO while confirmatory RCOg-V remains NO-GO today.
- M2 exact greedy matching on 17,280 audited rows is not a general guarantee.
- Historical 224-world/topology values remain provenance-incomplete.
- No simulator/source-validation/feasibility result is promoted to living validation.
- The “What we are NOT claiming” section now also captures the specific R3/M3/F3 non-claims.

## Commit-pin audit

All site GitHub checkpoint/evidence links were advanced to the reviewed `fe5f049` commit. Static path validation and browser QA are recorded below before commit.

## Browser QA

Used the existing research-hub Chrome tab only and navigated it to the isolated local `site/index.html`; unrelated tabs were not modified.

Desktop viewport: 1440x1000
- `readyState=complete`; title correct.
- `documentElement.clientWidth = 1425`; `scrollWidth = 1425`.
- **No horizontal overflow.**
- Rendered content spot-check: R3 32-gene boundary present; M3 `0010 0100 1000` present; F3 prepare-GO/submit-NO-GO present; no `NotebookLM` text present.

Mobile emulation: 375x812
- `documentElement.clientWidth = 360`; `scrollWidth = 360`.
- **No horizontal overflow**, including element-level bounds check (excluding the intentional off-canvas skip link).
- Mobile navigation toggle displayed; nav initially hidden with `aria-expanded=false`.
- Toggle activation changed `aria-expanded=true`, applied the open state, displayed the nav, and preserved `scrollWidth == clientWidth`.

## Files changed

- `site/index.html`
- `site/README.md`
- `lab_lanes/media_web/W3_RESEARCH_HUB_REFRESH_LOG.md`

`style.css` and `script.js` are unchanged unless QA demonstrates a responsive defect.
