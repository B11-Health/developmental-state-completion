# T6A Source Verification Notes

Date: 2026-08-30
Method: isolated research browser on CDP 9444 only.

## Verified / located sources

1. **Borsuk--Ulam**
   - Karol Borsuk (1933), *Drei Saetze ueber die n-dimensionale euklidische Sphaere*, Fundamenta Mathematicae 20, 177--190.
   - DOI: `10.4064/fm-20-1-177-190`.
   - Used only for the classical statement: every continuous `S^n->R^n` identifies an antipodal pair.

2. **Configuration spaces**
   - Edward Fadell and Lee Neuwirth (1962), *Configuration Spaces*, Mathematica Scandinavica 10, 111--118.
   - DOI: `10.7146/math.scand.a-10517`.
   - Journal/publisher result located at `https://journals.msp.org/mscand/article/view/2674` and the journal archive at `https://tidsskrift.dk/math/article/view/10517`.

3. **Projected embeddings / k-prems**
   - P. M. Akhmetiev and S. A. Melikhov, *Projected and near-projected embeddings*, arXiv:1711.03520.
   - Search record states the standard definition: `f:N->M` is a `k`-prem if there exists `g:N->R^k` such that `f x g:N->M x R^k` is an embedding.
   - S. A. Melikhov, *Transverse fundamental group and projected embeddings*, arXiv:1505.00505; search record notes covering maps as a case of the theory.
   - This is the most important novelty-boundary source for T6.

4. **Covering spaces / monodromy**
   - Allen Hatcher, *Algebraic Topology*, standard covering-space treatment.
   - T6A's proof of scalar trivialization deliberately does not require monodromy classification and instead uses only evenly-covered neighborhoods.

5. **Characteristic classes**
   - John Milnor and James Stasheff, *Characteristic Classes* (1974).
   - Allen Hatcher, *Vector Bundles and K-Theory* (public PDF located via search).
   - Used for associated line bundles, Whitney product formula, and the top Stiefel--Whitney obstruction to a nowhere-zero section.

6. **Equivariant Borsuk--Ulam machinery**
   - Edward Fadell and Sufian Husseini (1988), *An ideal-valued cohomological index theory with applications to Borsuk-Ulam and Bourgin-Yang theorems*, Ergodic Theory and Dynamical Systems 8.

## Evidence-quality boundary

The mathematical audit does not rely on search-engine summaries as proof. Source searches were used to verify bibliographic existence, terminology, and novelty overlap. Proofs in `AUDIT.md` were independently reconstructed from definitions and standard theorems.
