# Source provenance — R2 C. elegans cross-system replication

## Public dataset
- Cell Tracking Challenge 3D datasets page: `https://celltrackingchallenge.net/3d-datasets/`
- Dataset: `Fluo-N3DH-CE`, described as a developing *C. elegans* embryo from the Waterston Lab, University of Washington.
- Training archive: `https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DH-CE.zip`
- Server-reported archive size used for byte-range extraction: 3,428,322,151 bytes.
- The CTC page links the biological source paper: Murray JI et al. (2008), *Nature Methods*, DOI `10.1038/nmeth.1228`, “Automated analysis of embryonic gene expression with cellular resolution in C. elegans.”

## Recovery method
The full microscopy archive is ~3.4 GB and was not required for this predefined lineage-timing task. The public server advertises byte-range support. `fetch_ctc_lineage_metadata.py` reads the ZIP end-of-central-directory record, finds the two `TRA/man_track.txt` entries, and downloads/decompresses only those exact byte ranges. No lineage links are inferred from images.

Recovered ground-truth lineage tables:
- `Fluo-N3DH-CE/01_GT/TRA/man_track.txt` -> `source_data/01_man_track.txt`; SHA-256 `5d9e918af772cdef76bee457178f798e9c244586a3157aa5f241354fb5ca4bdb`; 11,724 bytes.
- `Fluo-N3DH-CE/02_GT/TRA/man_track.txt` -> `source_data/02_man_track.txt`; SHA-256 `0dd47996b54da449cb5c9e55f6688eb77c2769710f970d06898e49ca8ee2457a`; 11,785 bytes.

Each row has the CTC lineage format used here: track label, start frame, end frame, parent label. Sequence 01 contains 720 tracks and four initial roots; sequence 02 contains 724 tracks and two initial roots. Biological parents are binary in both sequences.

## Local source snapshots
- `source_data/crossref_nmeth1228.json`, SHA-256 `d8aca04d37dc2a075350fddd0d1c7f5fdb6235f432da2c25757dbfff12d46eab`.
- `source_data/manifest.json` records archive paths, local paths, offsets, compressed/uncompressed sizes, and lineage-table hashes.

## Provenance limitation
This analysis uses the public Cell Tracking Challenge repackaging of lineage ground truth rather than claiming that the CTC ZIP is the original Murray laboratory release. The biological source paper and Waterston Lab attribution are those explicitly linked by the CTC dataset page.
