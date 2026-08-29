# Prospective two-context developmental tomography — source-simulator checkpoint

Date: 2026-08-29
Original prospective freeze/render date: 2026-08-26

## Status

**Prospective post-hypothesis validation in the restricted developmental source simulator.**

This checkpoint upgrades an earlier retrospective simulator observation because the hidden laws/states, decoder, predictions and pass/fail thresholds were frozen **before** the 64 source phenotypes in the parent cohort were rendered. The frozen commitment has now been independently recovered, its canonical pre-render hash recomputed exactly, the source TSVs and frozen estimators migrated into this repository, and the preregistered results rechecked by an independent verification script.

This is **not living-plant evidence** and it is not evidence that real morphogenesis obeys a four-channel rectified architecture.

---

## 1. Novelty boundary: the latent algebra is established

In the restricted model, a signed hidden state is `s in R^n`. Context `q` acts as a coordinate reflection `R_q`, followed by rectification

`u_q(s) = [-R_q s]_+`.

For complementary contexts `q` and `qbar`,

`u_q = [-R_q s]_+`

and

`u_qbar = [R_q s]_+`.

Therefore, coordinatewise,

`R_q s = u_qbar - u_q`

and

`|s| = u_qbar + u_q`.

This is the same positive/negative-part information-preservation principle used by **Concatenated ReLU (CReLU)** and related rectifier representations. The algebra itself is **not claimed as novel**. See Shang et al., *Understanding and Improving Convolutional Neural Networks via Concatenated Rectified Linear Units*, arXiv:1603.05201.

The developmental question is different: can two **phenotypes generated under complementary biological contexts** be inverted accurately enough to recover the hidden signed causal state after a nonlinear morphogenetic decoder?

---

## 2. Exact restricted-model tomography

Let baseline context be `q=0` so that `u0=[-s]_+`.

### Full complement

If the second context flips every coordinate, `q=11...1`, then

`u_q=[s]_+`

and exactly

`boxed(s = u_q - u0)`.

Thus two exact latent views recover the complete signed state.

### Fixed-budget n−1-flip masks

The simulator also constrains the total gain budget

`||s||_1 = G`.

If the second context flips `n−1` coordinates, each flipped coordinate is recovered from the difference `u_q-u0`. The magnitude of the sole unflipped coordinate is the remaining L1 budget, and its sign is determined by whether that common rectified coordinate is active or inactive (away from the zero seam).

For `n=4`, the five universal second masks are

`0111, 1011, 1101, 1110, 1111`.

The public script `analysis/two_context_tomography_algebra.py` verifies exact reconstruction on 5,000 random four-channel worlds for all five masks.

---

## 3. Deterministic latent noise margins

Suppose each decoded latent view has coordinatewise error at most `e`.

### Full complement

Each recovered coordinate has error at most

`2e`,

so

`||s_hat-s||_2 <= 2 e sqrt(n)`.

A sufficient sign margin for coordinate `j` is

`|s_j| > 2e`.

### n−1 fixed-budget mask

For each flipped coordinate, error is again at most `2e`. The remaining magnitude is computed from the known L1 budget, so its magnitude error is at most

`2e(n−1)`.

If the unflipped sign is correctly selected,

`||s_hat-s||_2 <= 2 e sqrt(n(n−1))`.

A simple sufficient condition for the sole unflipped sign is

`|s_k| > 2 n e`,

while flipped coordinates retain the `|s_j|>2e` condition.

The public script stress-tests these sufficient bounds on 20,000 noisy random worlds.

---

## 4. Conditional phenotype-level lift

Let `F:U->Y` be the downstream phenotype map from the rectified latent signal to a phenotype representation. The archived theorem note proves the following conditional stability statement.

If, on the feasible latent domain,

`||F(u)-F(v)|| >= m ||u-v||`

for some `m>0`, and an observed phenotype `y` is within `eta` of `F(u)`, while the constrained inverse `u_hat` also fits `y` within `eta`, then

`||u_hat-u|| <= 2 eta / m`.

For a full complementary pair,

`||s_hat-s|| <= 4 eta / m`.

This is a straightforward consequence of the co-Lipschitz assumption plus the exact rectifier algebra; it is not claimed as a new general inverse-problem theorem.

The migrated original note also records a constructive **numerical** global-univalence certificate for the frozen cubic surrogate, with reported co-Lipschitz lower bound `>=0.01572598`. It is a numerical certificate for that frozen polynomial, **not** a formal interval/rational proof for the source simulator and not a theorem about living development.

Artifact:
`source_validation/two_context_2026-08-26/PHENOTYPE_FIBER_AND_TWO_VIEW_TOMOGRAPHY_THEOREM_2026-08-26.md`

---

## 5. Parent prospective freeze

Frozen file:
`source_validation/two_context_2026-08-26/metadata/TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json`

### Canonical pre-render commitment

Stored:

`b5fdc0bd257dbb57874f107b3c7a12b6c9fe5ec9f89cb48de585743846341c3a`

The freeze script hashes the canonical JSON object **before** inserting the `sha256_pre_render` field. The public verifier removes that field, canonicalizes with sorted keys and compact separators, recomputes SHA-256, and obtains the exact stored value.

### Frozen purpose

> prospective post-hypothesis source validation of two-complementary-phenotype nonlinear reconstruction through morphogenesis

### Frozen estimator

The frozen statement specifies:

> `RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz` trained new40 only; constrained nonlinear inversion; no refit after these renders

### Frozen cohort

Eight frozen laws `P00–P07`, eight selected starting states forming four complete complementary state pairs per law.

Expected source phenotypes: `64`.

### Frozen predictions

Before rendering:

1. 100% sign recovery across all 32 starting-world complementary pairs;
2. median signed-coordinate L2 error `<0.001`;
3. maximum signed-coordinate L2 error `<0.002`;
4. all signs of the deliberately weak `0.001` channels recovered correctly.

---

## 6. Parent prospective source result

Migrated source files: **64 TSV phenotypes**.

Aggregate source-manifest SHA-256 under the public verifier's sorted `filename\0sha256` convention:

`276c7e66357604d44e2ff4cddd94d7c2fd3c8f2f64873c18898389d2f22d9dbd`

Results:

- complementary pairs: **32**;
- sign accuracy: **100%**;
- signed L2 median: **0.000175175**;
- signed L2 p95: **0.000428985**;
- signed L2 maximum: **0.000514625**;
- relative-error p95: **0.000382519**;
- all `0.001` weak-channel signs correct: **yes**;
- every frozen prediction passed: **yes**.

The worst signed-state error remains roughly four times below the preregistered `0.002` maximum-error threshold.

### Phenotype-inversion audit

The later audit, using the same frozen estimator and immutable source outputs, reports:

- source phenotypes: **64**;
- complement pairs: **32**;
- decoded-u L2 median `7.75e-5`, p95 `3.32e-4`, max `4.66e-4`;
- surrogate inversion raw L2 median `8.58e-6`, max `3.29e-5`;
- surrogate reconstruction dIoU median `1.55e-7`, p95 `5.63e-7`, max `9.87e-7`;
- weak-`0.001` pairs: **16**, sign accuracy **100%**;
- every law `P00–P07`: sign accuracy **100%**.

The parent source cohort only contains complete complement pairs, so mask `1111` is the only Hamming>=3 mask that can be evaluated prospectively from the parent renders without adding new source contexts.

---

## 7. Five-mask prospective context extension

A second freeze was created before rendering the **previously unseen contexts** needed to test all five exact Hamming>=3 masks.

Frozen file:
`source_validation/two_context_2026-08-26/metadata/FIVE_MASK_PROSPECTIVE_EXTENSION_FROZEN_2026-08-26.json`

Canonical pre-render commitment:

`7d4845aa8a50da5e5d8ffd2b0bc65e02311882879a261df8c313b4557d47663f`

### Scope warning from the freeze itself

> Laws P00–P07 were already partially source-rendered in the complementary-pair cohort. This is prospective with respect to the missing contexts/masks, **not a new-law generalization test**.

The extension froze 64 new source contexts, completing all 16 states for each of the eight existing laws.

### Locked estimator hashes

- cubic decoder:
  `d7e4027e4ed252225b5f5db87b758df31c67d94c02af1680ce172dc9b6074340`
- linear initializer:
  `856bcc7076af37d7a548e720dfe1cebcfd7acc92f35997b683e1e7c56cffe904`
- reference algorithm:
  `bbebc27b2ec562c2d5d83b69dd2b8c45a6b43ca36adb87b91d9bd4994dfe4508`

The public verifier recomputes all three hashes from the migrated files.

### Extension source manifest

64 newly rendered TSVs; aggregate manifest:

`19c8c9e72e69fa4175ef6a15d80c897f362662f6cfa900adcc9fedf50287004a`

### Five-mask results

| Mask | Oriented tests | Unordered pairs | Sign accuracy | Median L2 | p95 L2 | Max L2 | Weak 0.001 sign accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0111 | 128 | 64 | **1.000** | 0.0001977 | 0.0008550 | 0.0012108 | **1.000** |
| 1011 | 128 | 64 | **1.000** | 0.0001920 | 0.0006886 | 0.0014386 | **1.000** |
| 1101 | 128 | 64 | **1.000** | 0.0001420 | 0.0005401 | 0.0009594 | **1.000** |
| 1110 | 128 | 64 | **1.000** | 0.0001376 | 0.0005523 | 0.0009597 | **1.000** |
| 1111 | 128 | 64 | **1.000** | 0.0001644 | 0.0004778 | 0.0008171 | **1.000** |

All five masks passed every preregistered threshold.

Again: this is **prospective context/mask generalization on already partially observed laws**, not a second independent prospective law-generalization cohort.

---

## 8. What this result establishes

Within the restricted four-channel developmental source simulator, with its fixed L1 gain budget and frozen nonlinear phenotype decoder:

1. two complementary source-rendered phenotypes were prospectively sufficient to reconstruct signed hidden state with the preregistered accuracy;
2. the result included channels with gain exactly `0.001`, which passed the frozen sign criterion;
3. after freezing the estimator, previously unseen contexts allowed all five theoretically sufficient Hamming>=3 masks to pass their preregistered context-generalization thresholds;
4. the result survived migration into the public repo and independent hash/result verification.

This is substantially stronger than a retrospective synthetic fit.

---

## 9. What it does not establish

It does **not** establish that:

- living plants obey this rectified four-channel architecture;
- two perturbations are universally sufficient in biology;
- the CReLU-like positive/negative decomposition is mathematically novel;
- the source simulator phenotype map is globally injective in the continuum by a formal source-level proof;
- the five-mask extension is a new-law prospective test;
- phenotype inversion will remain stable under realistic imaging noise, biological heterogeneity, injury/stress responses or unmodeled latent variables.

The decisive next biological test remains prospective wet-lab validation with direct measurements and preregistered perturbations.

---

## 10. Public reproducibility

Exact migrated source-validation bundle:

`source_validation/two_context_2026-08-26/`

It contains:

- 64 parent source TSV renders;
- 64 extension source TSV renders;
- both frozen preregistration JSONs;
- parent result and audit JSONs;
- extension result JSON;
- frozen cubic and linear decoder NPZ files;
- exact freeze/build/score scripts;
- frozen five-mask reference decoder;
- original phenotype-fiber/two-view theorem working note.

Run:

```bash
python analysis/verify_two_context_source_bundle.py
python analysis/two_context_tomography_algebra.py
```

The first script verifies the frozen commitments, estimator hashes, source manifests and preregistered pass/fail claims. The second verifies the exact restricted-model algebra and deterministic noise bounds independently of the simulator source outputs.

## Current evidence label

**Prospective, preregistered, source-simulator validated; not yet biologically validated.**
