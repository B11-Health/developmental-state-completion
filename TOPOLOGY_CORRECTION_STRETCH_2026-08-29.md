# Topology correction — STRETCH cryptic island

Date: 2026-08-29

## Status

Recovered archived simulator/source-render checkpoint. The exact source artifacts still need migration into this public repository; this is not a new continuum theorem reproduced from scratch here.

## Frozen rejection

The old statement `m_S ≈ 0.001543` as a continuum STRETCH merge barrier is **rejected**. The later checkpoint identifies it as a coarse-grid discretization obstruction. It may be retained only as a historical sampled-graph connectivity threshold.

## Corrected source-level estimate

Optimized state-1011 static mimic:

- approximate gains: `(0.67447, 0.52739, 0.04224, 0.55589)`;
- source accommodation: `a_S = 0.0002686300765` dIoU.

Corrected CFLOW escape seam:

- boundary near `F=0`, `N=1`, `C+S=0.8`;
- seam-consistent cubic optimum near `(0.743911, 0.056089, 0, 1)`;
- surrogate target dIoU `≈0.001410471`;
- direct source target dIoU `≈0.001410939`;
- independent nearby source sweep `(0.744,0.056,0,1)` gives `≈0.001412041`.

Therefore the current archived source estimate is

`m_S ≈ 0.00141094`,

with isolation gap

`Δ_S = m_S-a_S ≈ 0.00114231`

and ratio

`m_S/a_S ≈ 5.25`.

## Scientific interpretation

The qualitative phenomenon survives: an alternative hidden mechanism can imitate the target much more cheaply than it can be reached continuously from the target while remaining phenotypically close. What changed is the estimated bottleneck height.

The correction exposes a general failure mode: sampled graphs can create false barriers when a thin low-cost seam lies between grid points. Future topology claims must distinguish sampled-grid thresholds, seam-optimized source thresholds, and proved continuum bounds.

## Remaining proof gap

The later seam-consistent cubic phenotype decoder had very small source discrepancies on large sampled validation sets and no sampled local rank collapse, but no rigorous uniform continuum error bound or global injectivity proof was established.
