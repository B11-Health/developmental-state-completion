# Public Research Hub

Static GitHub Pages research landing page for the Developmental State Completion project.

## Source checkpoint

The copy and commit-pinned evidence links in this W2 refresh were audited against `origin/main` at commit `f06ac518496d1f27396ae77ae9243655a5355cf5` on 2026-08-29. The site intentionally separates observed-data reanalysis, simulator evidence, mathematical results, historical/provenance-incomplete reports, readiness decisions, and prospective living hypotheses.

W2 incorporates only reviewed durable results integrated after the previous site checkpoint:

- M2 exact perturbation optimization: 17,280 audited 128-world rows; greedy equals exact on this bundle, while general non-submodularity/counterexamples remain; block-sparse deletion is recorded only as a sufficient safe structural condition.
- R2 cross-system *C. elegans* analysis: large nonlinear residual-history gains, but the preregistered stable-history decision is not met because matched incomplete-state calibration power is below the declared threshold.
- B2 living-system feasibility: Phase 0 is conditional GO; the confirmatory RCOg-V study is NO-GO today pending material/transfer, optics, and burden gates.
- F2 submission readiness: NSF 26-520 Mathematical Biology is GO to full preparation, but Research.gov organization/PI/AOR/SPO readiness remains unverified; NSF 26-517 BIO Core remains conditional on a real living experimental path.

Historical 224-world/topology provenance corrections remain unchanged, and no simulator or feasibility result is represented as living-plant validation.

## Files

- `index.html` — complete single-page research hub
- `style.css` — responsive, dependency-free styles
- `script.js` — mobile navigation and evidence-status filtering only

No analytics, trackers, external fonts, third-party JavaScript, or remote UI dependencies are included.

## Local preview

From the repository root, run:

```bash
python -m http.server 8000 --directory site
```

Then open `http://localhost:8000/`.

## Deployment status

The hub is already deployed through the repository's GitHub Pages Actions workflow. W2 does **not** push or deploy this refresh. The W2 changes must remain local until separately reviewed and intentionally published.

When a later deployment is authorized, publish the reviewed `site/` artifact through the existing Pages workflow and preserve commit-pinned evidence links unless a fresh evidence audit intentionally advances the checkpoint.

## Review checklist before any future deployment

- Re-audit `origin/main` if the repository changes after `f06ac518496d1f27396ae77ae9243655a5355cf5`.
- Preserve the historical 224-world/topology provenance-incomplete status unless original artifacts are actually recovered and audited.
- Keep FM1 wording task/stage/representation/decoder-specific; do not promote it to universal Markovity.
- Keep the R2 stable-history decision as not met unless a new preregistered calibrated analysis changes that status.
- Do not infer general greedy safety from the zero-loss M2 finite audit.
- Keep living RCOg-V validation prospective until an actual preregistered confirmatory study is executed.
- Keep Research.gov/AOR/SPO submission authority unverified until documented.
- Test desktop/mobile layout, no horizontal overflow, keyboard/mobile navigation, and every commit-pinned evidence link.
