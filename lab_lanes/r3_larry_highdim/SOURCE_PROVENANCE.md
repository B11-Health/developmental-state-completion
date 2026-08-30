# R3 LARRY high-dimensional source provenance

## Primary publication and release

- Weinreb, Rodriguez-Fraticelli, Camargo & Klein, *Lineage tracing on transcriptional landscapes links state to fate during differentiation*, Science 2020. PMID 31974159; PMCID PMC7608074.
- Klein Lab public `paper-data` repository, commit `b8658b78c1c288019dfa60b6f50aace270528a29`.
- Release directory: `Lineage_tracing_on_transcriptional_landscapes_links_state_to_fate_during_differentiation`.

The release README states that the in-vitro experiment contains day-2, day-4 and day-6 single-cell transcriptomes, clone membership, starting population, cell-type annotations and SPRING coordinates. It documents a normalized counts matrix with rows=cells and columns=genes, plus metadata and clone-matrix files.

## Files/endpoints used

Small direct-release files:

- `stateFate_inVitro_metadata.txt.gz`
- `stateFate_inVitro_clone_matrix.mtx.gz`
- `stateFate_inVitro_gene_names.txt.gz` (used to verify the released gene universe)

The release-native SPRING viewer for `SF_all/all_combined` exposes the same normalized expression matrix through its public `grab_one_gene.py` endpoint. R3 verified that the viewer gene menu contains 25,289 genes, exactly matching the released gene-name list, and that each queried gene returns 130,887 expression values, exactly matching the metadata row count and clone-matrix row count.

R3 used that endpoint to retrieve a fixed 32-gene day-2 expression panel without downloading the approximately 2.07 GB compressed whole matrix. The panel order was frozen before outcome-model fitting; hashes of every downloaded input are in `results/input_hashes.json`.

## Cell-order verification

- metadata rows: 130,887
- clone matrix shape: 130,887 x 5,864
- released gene list: 25,289
- SPRING gene menu: 25,289
- each queried expression vector: 130,887 values

This row-count identity is the release-native alignment basis used by the analysis.

## Cohort reconstruction

Using the same strict three-fate reconstruction as the prior control gives 133 clone-level units with a sampled day-2 sister and day-6 descendants in both well sets, restricted to dominant `Neutrophil`, `Monocyte`, or `Baso` fate in each separated well. Those 133 units contain 197 sampled day-2 cells.

## Important provenance limitation

R3 did not download the complete 25,289-gene sparse matrix and therefore does **not** claim a full-transcriptome replication of the paper's fate-prediction figures. It is a release-native higher-dimensional expression control using 32 measured genes, not an author-released PCA artifact and not a reconstruction of every preprocessing step used in the paper.
