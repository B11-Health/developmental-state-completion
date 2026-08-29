# LAB LANE B1 — Biological Source Audit for the RCOg-V Prospective Pilot

Status: source-audited planning document; no material requests made; no experiment performed; no eligibility/material-availability claim inferred beyond the cited papers.

## Source bundle audited

1. Wang Y et al. (2025), *The Plant Journal*, PMCID PMC12165315. Local XML snapshot: `_source_wang_PMC12165315.xml`, SHA256 `fe94c26da9f922797938141049d697b19e0a6862ccb839c8683eb3e52a61f2cf`.
2. Hu Z et al. (2024), *PNAS*, DOI 10.1073/pnas.2321877121, PMCID PMC11214078. Local XML snapshot: `_source_hu_PMC11214078.xml`, SHA256 `f43f3cc09b3e0b0b03782ea995c7b8bb082e7132a00bd5c8a2dae09bab9a7b93`.
3. Hu et al. SI Appendix. Local PDF snapshot: `_source_hu_SI.pdf`, SHA256 `0117f535f62c07cf833eea18b17dbf44d3e556062a257af25ff6bbbb657a2407`.

Labels used below:
- **VERIFIED** = directly reported in the audited primary paper/SI.
- **INFERENCE** = biologically reasonable interpretation of reported data but not itself a directly tested material/protocol claim.
- **PROPOSED** = new design choice for the developmental-state-completion pilot.
- **UNVERIFIED / BLOCKING** = cannot be assumed before collaborator/material confirmation or Phase-0 validation.

## 1. RCOg-V substrate and suppressor alleles

| Element | Audit status | What the paper actually supports | Pilot implication |
|---|---|---|---|
| `pChRCO::ChRCOg-VENUS` (`RCOg-V`) in *A. thaliana* Col-0 | VERIFIED | Wang reports a 3229-bp ChRCO promoter, 1689-bp RCO genomic sequence fused C-terminally to VENUS, transformed into Col-0; the EMS screen was performed in homozygous RCOg-V seed. | Valid core background. |
| `cuc2-4;RCOg-V` | VERIFIED | `slb102-2`; CUC2 nonsense mutation G294→A, Trp98→stop; allelism supported. | Strong candidate for an initiation-defect class. |
| `cuc2-5;RCOg-V` | VERIFIED | `slb167-3`; CUC2 missense G287→A, Gly96→Asp; allelism supported. | Independent CUC2 allele; weaker/variable lobe-initiation phenotype reported. |
| `pin1-12;RCOg-V` | VERIFIED | `slb59-2`; PIN1 start codon mutation G3→A, Met1 lost; fertile suppressor despite pin-like phenotype later. | Avoid as primary response panel if PIN1:GFP polarity is the intervention readout, because the assay directly depends on PIN1 biology. |
| `cyp71-3;RCOg-V` | VERIFIED | `slb166-1`; CYP71 missense G386→A, Cys129→Tyr; allelism supported. | Candidate post-initiation class. |
| `nop2a-5;RCOg-V` | VERIFIED | `slb31-3`; NOP2A splice-site mutation; allelic to `nop2a-6`. | Candidate ribosome-biogenesis/post-initiation class. |
| `nop2a-6;RCOg-V` | VERIFIED | `slb167-1`; NOP2A nonsense C157→T, Gln53→stop. | Independent allele replication candidate. |
| `rpl34-2;RCOg-V` | VERIFIED | `slb212-2` and `slb215-2` share the same RPL34 missense mutation G259→A, Glu99→Lys. | Not independent alleles despite two recovered suppressor names; do not treat as cross-allele replication. |
| `pgy1-5;RCOg-V` | VERIFIED | `slb119-1`; PGY1/RPL10aB nonsense G591→A, Trp197→stop. | Candidate post-initiation/ribosomal class. |

### Developmental-mechanism evidence

- **VERIFIED:** In 600–1200 µm leaf primordia, `cuc2-4;RCOg-V` and `cuc2-5;RCOg-V` show smooth margins / impaired lobe initiation; 5/17 `cuc2-5` samples nevertheless formed lobe primordia. Wang therefore interprets `cuc2-5` as potentially weaker than `cuc2-4`.
- **VERIFIED:** PIN1, CYP71, NOP2A, RPL34, and PGY1 suppressors showed lobe primordium initiation similar to RCOg-V in the analyzed stage, consistent with defects after initiation.
- **VERIFIED:** RCO-VENUS fluorescence intensity was lower in `cyp71-3`, `nop2a-5`, `nop2a-6`, `rpl34-2`, and `pgy1-5` than in RCOg-V.
- **INFERENCE:** Calling CYP71 a “transcription/chromatin-associated regulator affecting RCO function” is too strong for the pilot label. The paper says CYP71 is a WD40-domain cyclophilin associated with chromatin and that reduced RCO levels may contribute to the phenotype; it also explicitly allows indirect growth/proliferation effects. Use “CYP71-associated post-initiation suppressor” unless a more specific mechanistic claim is independently demonstrated.

## 2. Published baseline/readout modalities in Wang et al.

### Macroscopic leaf shape

**VERIFIED:** Mature leaves were flattened under transparent adhesive film on white paper and scanned at 800 dpi. Leaf Interrogator was used for shape-space PCA. Leaf dissection index was `(perimeter^2)/(4*pi*area)`. Figure 2 analyzed the 10th rosette leaf of one-month-old plants, `n=10–20` leaves/genotype for the original biological comparison.

**Important:** those `n` values are not a justified confirmatory sample size for blinded genotype decoding.

### Confocal RCO/PIN imaging

**VERIFIED:** Wang used a Leica TCS-SP8 upright confocal. For GFP/VENUS imaging, a 25× water objective, 1024×1024 pixel format, 0.7–1 µm z-spacing, sequential frame scanning, GFP 488 nm excitation/493–510 nm collection and VENUS 514 nm excitation/520–550 nm collection are reported. Dye separation was used to mitigate GFP/VENUS crosstalk.

**VERIFIED:** For RCO-VENUS quantification, leaf primordia were imaged at identical settings and nuclear fluorescence was measured in Fiji; approximately 10 intact nuclei in the central RCO domain were selected per sample before averaging.

**VERIFIED:** Wang’s transgenic imaging material included `pChRCO::ChRCOg-VENUS` and `pAtPIN1::AtPIN1-GFP`.

## 3. ChCUC1/PIN1 perturbation interface from Hu et al.

### Inducible construct and genetic background

**VERIFIED:** Hu generated dex-inducible `ChCUC1p::LhG4:GR; Op::ChCUC1:tdTomato` and transformed it into an *A. thaliana* Col-0 `PIN1p::PIN1:GFP` background. Twenty independent T2 lines were isolated; two representative lines were selected for experiments after expression/phenotype comparison.

**VERIFIED:** Hu also used a separate heat-shock Cre-lox mosaic system (`HSp::dBox:Cre; 35Sp::lox-spacer-lox::ChCUC1:Venus`) in `PIN1p::PIN1:GFP`. This is a distinct intervention system and should not be conflated with the dex spray experiment.

### Published dex/mock protocol for confocal imaging

**VERIFIED reference conditions from Hu SI:**
- dexamethasone stock: 50 mM in DMSO;
- working induction solution: 10 µM dexamethasone + 0.01% Triton X-100;
- mock: same solution with DMSO replacing dex stock;
- seedlings grown in soil until leaf 3 was visible;
- dex or mock applied by spraying;
- cultivated another 24 h;
- dissected to expose leaf 4 at target developmental stage;
- mounted on 1.5% agar containing 1/2 MS, 1% sucrose, and 1 ml/L PPM for imaging;
- compared leaves of closely matched length to reduce developmental-stage variation.

**Critical transfer caveat:** these exact conditions are **VERIFIED in the Hu Col-0 inducible/PIN1:GFP material**, but **UNVERIFIED in RCOg-V suppressor backgrounds**. They are a reference starting protocol, not a dose/safety claim for the proposed crosses.

### Published acute endpoint

**VERIFIED:** At 24 h after dex vs mock, Hu measured PIN1:GFP polarity behavior in developing *A. thaliana* leaf 4. The reported endpoint included distance from a margin protrusion tip to PIN1 polarity reversal; ChCUC1 induction changed reversal position.

**VERIFIED:** For Figure 2A–C, the reversal distance per leaf was based on the first five cells with clear reversed polarity; `n=3` leaves/treatment in that original demonstration. This `n` is not a pilot power estimate for our decoder.

### Imaging/analysis modality

**VERIFIED:** Leica SP8 upright, long-working-distance water-immersion 25×/0.95 objective. GFP 488/493–510 nm; Venus 514/520–550 nm; tdTomato 561/575–600 nm; chlorophyll 650–700 nm. Typical XY pixel size 0.3–0.5 µm and z-step 0.7–1 µm. HyD detectors were used except chlorophyll (PMT).

**VERIFIED:** MorphographX 2.0 was used to make curved 2D meshes and cell segmentations. PIN1 planar polarity was scored from membrane signal; two researchers independently assessed polarity and compared results. Cells could be assigned apical, basal, bipolar, lateral, non-polar, or unknown classes.

**VERIFIED:** Hu also quantified reporter signal, cell/tissue area change, growth anisotropy and proliferation from time-lapse meshes in separate experiments.

## 4. What is and is not a published “physiological cost” measure

### Published biological response measurements

- **VERIFIED:** local growth repression and changes in growth anisotropy/area extension were quantified in the heat-shock mosaic experiments.
- **VERIFIED:** final leaf morphology was recorded after some mosaic inductions.

### Not published as burden calibration for the dex assay

The target papers do **not** establish, for the proposed RCOg-V suppressor crosses:
- survival injury threshold;
- whole-plant relative growth-rate cost of dex induction;
- developmental delay threshold;
- time-to-flowering cost;
- fertility/seed-production cost;
- stress-reporter threshold;
- a composite “physiological cost” score.

All of those are **PROPOSED Phase-0 burden/QC measurements** if the collaborator regards them as technically appropriate. They must not be described as reported by Wang or Hu.

## 5. Material availability audit

- **VERIFIED:** Wang’s data-availability statement says supporting data are available on request from the corresponding author; it does not establish public stock availability of the suppressor seed lines.
- **VERIFIED:** Hu’s data/material/software statement lists supplementary information and GEO accessions for sequencing datasets; it does not state that the inducible line, suppressor material, or combined crosses are deposited in a public stock center.
- **UNVERIFIED / BLOCKING:** current possession, distributability, stock-center accession, MTA terms, seed viability, zygosity, selectable markers, and permission to redistribute any of the required lines.

Therefore the pilot must explicitly wait for the originating lab/collaborator to confirm material status.

## 6. Corrections to the existing preregistration draft

1. Replace “CYP71 = transcription/chromatin-associated regulator affecting RCO function” with the narrower source-grounded wording above.
2. Add the published Hu dex/mock conditions as **reference conditions**, while stating transfer to RCOg-V backgrounds is a Phase-0 feasibility question.
3. Do not imply material availability from publication alone.
4. Do not call growth delay/survival/flowering/fertility published perturbation-cost measures; label them proposed burden outcomes.
5. Do not treat the two recovered `rpl34-2` suppressors as independent alleles.
6. Keep `pin1-12;RCOg-V` out of the primary panel when PIN1:GFP polarity is the intended response feature unless the collaborator has a specific rationale and assay redesign.
7. Distinguish Hu’s dex inducible line from the separate heat-shock mosaic system.

## Audit conclusion

The source-supported biological core is real and unusually usable for a prospective test: RCOg-V suppressor genetics, a live RCO-VENUS readout, published PIN1:GFP imaging, and a reproducible ChCUC1 dex/mock response at 24 h all exist. The missing bridge is not conceptual; it is **material/cross feasibility and burden validation in the combined RCOg-V suppressor backgrounds**. No confirmatory experiment should begin until that bridge is experimentally cleared.
