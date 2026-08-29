# Public Research Hub

Static GitHub Pages-ready research landing page for the Developmental State Completion project.

## Source checkpoint

The copy and commit-pinned evidence links in this site were audited against `origin/main` at commit `2c9147841810dd5734996b6db8faca33fad5029c` on 2026-08-29. The site intentionally distinguishes reproduced results, historical/provenance-incomplete reports, and prospective hypotheses.

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

## GitHub Pages deployment

This lane did **not** push changes or enable GitHub Pages. After review, two simple deployment options are available:

1. Publish from a branch/folder by moving or copying the site to the Pages-configured source directory (for example `/docs` if that is the chosen repository setting).
2. Add a GitHub Actions Pages workflow that uploads `site/` as the Pages artifact.

Whichever method is chosen, keep claim links commit-pinned or intentionally update the audited checkpoint hash after a fresh evidence review. Do not silently point corrected claims at a moving branch.

## Review checklist before public deployment

- Re-audit `origin/main` if the repository changed after `2c914784...`.
- Confirm the historical 224-world/topology status has not changed through recovered artifacts.
- Confirm the FM1 replication wording still matches the latest claim ledger.
- Confirm any living-plant pilot status remains prospective unless actual preregistered data exist.
- Test desktop/mobile layout and keyboard navigation in the deployment environment.
- Verify every GitHub evidence link resolves to the intended frozen commit.
