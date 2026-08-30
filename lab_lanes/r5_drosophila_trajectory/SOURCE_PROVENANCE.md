# R5 Source Provenance

Date: 2026-08-30

## Dataset
Cell Tracking Challenge `Fluo-N3DL-DRO` training dataset.

Official dataset page: `https://celltrackingchallenge.net/3d-datasets/`
Training archive: `https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-DRO.zip`

Official page metadata observed in R5:
- organism/context: developing *Drosophila melanogaster* embryo;
- source attribution: Dr. P. Keller, Howard Hughes Medical Institute / Janelia Farms Research Campus, USA;
- microscope: SIMView light-sheet;
- voxel size: 0.406 x 0.406 x 2.03 micrometers;
- time step: 30 seconds;
- challenge note: evaluation tracking uses cells forming the developing nervous system, identifiable from the gold tracking annotation.

HTTP HEAD on the public training archive returned content length 6,222,579,236 bytes and `Accept-Ranges: bytes`.

## Selective extraction
R5 implemented a ZIP64 central-directory/HTTP-range reader. It fetched only:
- both public gold `TRA/man_track.txt` files;
- selected gold `TRA/man_trackNNN.tif` label volumes at frames 15,20,23,24,25,40 for sequences 01 and 02.

Each ZIP entry is checked against its recorded uncompressed size and CRC before use. The derived centroid JSON sidecars additionally record the SHA-256 of each fetched uncompressed TIFF entry.

No raw fluorescence movie volume was downloaded or analyzed.

## Derived source hashes
- `dro_centroids_01_15_20_23.csv`: `5334ece1abf2979b18498d8cab09cd170c8c81dc7d74173c43fe3e22c7fa7f8a`
- `dro_centroids_01_24_25_40.csv`: `b2dcf3db20a873814d0a8af043cbf29590723e4a17313f02205093ddc7015db6`
- `dro_centroids_02_15_20_23.csv`: `3fc0702a00b32e718ab98535591c7a79ed93885cc144c6a25e1453d64832a9a0`
- `dro_centroids_02_24_25_40.csv`: `321567c806c6c3b0af82a823801bc7903891ab50914f0d38c5a76c7e8d9f6375`

The matching JSON sidecars contain per-entry archive names, CRCs, dimensions and uncompressed hashes.
