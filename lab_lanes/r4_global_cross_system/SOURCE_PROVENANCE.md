# R4 Source Provenance

Date: 2026-08-30

## Executed public dataset

**GSE167135 — Lopez-Anido et al., Arabidopsis stomatal lineage**

- GEO record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE167135
- Primary paper: https://www.sciencedirect.com/science/article/pii/S1534580721002112
- Public GEO supplementary directory used: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE167nnn/GSE167135/suppl/`
- Files downloaded without authentication:
  - `GSE167135_ATML1p_Smartseq2_TPM.csv.gz` — SHA-256 `d948b9609117f3df84b8d84e0d7b890231cfc8dc86f01a2e6b9bdd779e2357b0`
  - `GSE167135_TMMp_Smartseq2_TPM.csv.gz` — SHA-256 `b9017242c3adafeca0f692eeed2dd8e8ee4eb1f49dfaf3261b1e9455f0886e95`
  - `GSE167135_Smartseq2_FACSmetadata.csv.gz` — SHA-256 `7c20a17caaf2375216d3322e49fd8958edd07fb9903629f1f5f87cce9b406bb2`

The public FACS metadata has 621 rows: 336 TMMp_pool_2, 142 TMMp_pool_1, 101 ATML1p_pool_2, and 42 ATML1p_pool_1. Expression matrices match all 621 metadata sample names.

## Other first-wave source checks

- Farrell zebrafish GSE106587: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE106587 ; lab data page http://farrelllab.github.io/data/ ; primary paper https://www.science.org/doi/10.1126/science.aar3131. Lab page reports 38,731 cells, 12 time points from 3.3–12 hpf and 25 reconstructed cell types. It also states that the processed counts/URD object at Broad requires login; R4 therefore did not access that processed object or create an account.
- Mouse gastrulation E-MTAB-6967: https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-6967 ; publication reports 116,312 cells from nine E6.5–E8.5 stages.
- Zebrafish GSE112294: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE112294 ; GEO summary reports >92,000 cells from the first day of development.
- Mouse organogenesis GSE119945: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE119945 ; GEO summary reports ~2 million cells from 61 embryos E9.5–E13.5.
- Zebrafish perturbation GSE269784: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269784 ; public FTP exposes a ~613 MB reference h5ad and ~1.7 GB perturbation h5ad.
- Mouse organoid GSE164638: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164638 ; local public primary-code README identifies public annotated sandwich/dome and perturbation h5ad files.
- Arabidopsis root GSE123818: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123818 ; public processed WT/SHR matrices.
- Arabidopsis root GSE123013: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE123013 ; public merged/raw matrices.
- Arabidopsis root atlas GSE152766: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE152766 ; multiple public RDS objects including spliced/unspliced counts.
- Arabidopsis root scATAC GSE173834: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE173834.
- Rice root GSE146034: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE146034 ; primary paper reports >20,000 root-tip cells from two cultivars.
- Rice atlas GSE185068: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE185068.
- Wheat root GSE270342: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE270342.

## Access and licensing boundary

All R4 source checks were made through the isolated research browser on CDP 9444 or direct reads of public repository endpoints from Authenticated Shell. No account was created, no researcher was contacted, and no unreleased/private data were used. “Public” here means publicly retrievable from the cited repository; R4 does not infer a separate redistribution/relicensing grant beyond repository and paper terms.
