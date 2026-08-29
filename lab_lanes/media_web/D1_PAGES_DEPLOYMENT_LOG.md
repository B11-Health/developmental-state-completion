# D1 GitHub Pages Deployment Log

Date: 2026-08-29

## Deployment

- Repository: B11-Health/developmental-state-completion
- Published source: `site/` only
- Pages workflow: `.github/workflows/pages.yml`
- Deployment commit: `93b89893e6381a25d2131c49990467e444a0c3cf` (`93b8989`)
- Successful workflow run: `Deploy public research hub #2`, run `33278008111`
- Live URL: https://b11-health.github.io/developmental-state-completion/
- Artifact: `github-pages`, 13 KB, SHA-256 `3bfb8fdead4b08dce58ea0458780b7e6f67f25093e484b972d31e7ec92b4e035`

The repository already contained the smallest appropriate official GitHub Pages Actions configuration when deployment was checked. It uses `actions/checkout@v4`, `actions/configure-pages@v5` with `enablement: true`, `actions/upload-pages-artifact@v3` with `path: site`, and `actions/deploy-pages@v4`. No custom domain, DNS, analytics, trackers, paid services, or unrelated settings were configured.

## Deployment history

- Run #1 for commit `93b8989` failed during initial Pages setup.
- Run #2 was manually dispatched against the same commit and completed successfully in 19 seconds.
- GitHub reported the deployment URL above from the successful `github-pages` environment deployment.

## Live QA

- Desktop viewport: 1440x1000. Document `scrollWidth == clientWidth` (1425 px), so no horizontal overflow was detected.
- Mobile viewport: 375x812. Document `scrollWidth == clientWidth` (360 px), so no horizontal overflow was detected.
- Mobile navigation control is present.
- Internal anchors: all same-page `#...` links resolve to existing targets.
- Evidence links: 19 unique GitHub evidence URLs extracted from the deployed HTML were checked; none returned HTTP 4xx/5xx responses.
- Live document title verified as `Developmental State Completion — Public Research Hub`.
- Page loaded to `readyState=complete` at the public URL.

## Notes

GitHub emitted a non-blocking Actions warning that Node.js 20-targeting action versions are currently forced onto Node.js 24. Deployment nevertheless completed successfully. No unverifiable organization/security approval was encountered.
