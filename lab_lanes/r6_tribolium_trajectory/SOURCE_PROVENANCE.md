# R6 Source Provenance

Date: 2026-08-30

## Official public dataset
Cell Tracking Challenge `Fluo-N3DL-TRIC`.

Dataset page: `https://celltrackingchallenge.net/3d-datasets/`
Training archive: `https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-TRIC.zip`

Official page metadata used:
- developing *Tribolium castaneum* embryo, 3D cartographic projection;
- Dr. A. Jain, Max Planck Institute of Molecular Cell Biology and Genetics, Dresden, Germany;
- Zeiss LightSheet LZ.1;
- time step 1.5 minutes;
- physical voxel size marked not applicable due to cartographic projections;
- challenge evaluation tracks blastoderm lineages at the border of embryonic and extra-embryonic tissues.

HTTP HEAD observed training archive size: 22,088,481,712 bytes.

## Selective range extraction
R6 used `remote_zip_extract.py` to parse ZIP64 metadata and selectively retrieve:
- sequence 01 and 02 `GT/TRA/man_track.txt`;
- gold label masks at frames 15,20,23,24,25,40.

Each entry is checked against its ZIP CRC and uncompressed size. Derived manifest records per-mask uncompressed SHA-256.

No raw fluorescence image movie was downloaded.

## Derived source hashes
- `01_man_track.txt`: `aae4bbd2b660a96de8683c64327a3b2e6171802121e935c4ae0a92bbf04a35d1`
- `02_man_track.txt`: `ae2681b418f669ec4609f5d98274efdc33b1ba52a7860657c5b9aabbad325747`
- `tric_selected_centroids.csv`: `84bb18a9e8e79d84e90630b8d3778153a18b15aef569a0c08099e852222e98a6`
- `tric_source_manifest.json`: `f608d95af31996385f1afed505ccf9d47abe6ab8b715e0ffc576f8c9881f9387`
