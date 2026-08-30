# R7 Source Provenance

R7 introduces no new data source. It reuses only committed public-derived files already provenance-checked in R5 and R6.

## Drosophila (`Fluo-N3DL-DRO`)
Source lane: `lab_lanes/r5_drosophila_trajectory`.

Committed derived centroid files and R5 SHA-256 values:
- `dro_centroids_01_15_20_23.csv` — `5334ece1abf2979b18498d8cab09cd170c8c81dc7d74173c43fe3e22c7fa7f8a`
- `dro_centroids_01_24_25_40.csv` — `b2dcf3db20a873814d0a8af043cbf29590723e4a17313f02205093ddc7015db6`
- `dro_centroids_02_15_20_23.csv` — `3fc0702a00b32e718ab98535591c7a79ed93885cc144c6a25e1453d64832a9a0`
- `dro_centroids_02_24_25_40.csv` — `321567c806c6c3b0af82a823801bc7903891ab50914f0d38c5a76c7e8d9f6375`

R5 attributes the public CTC training dataset to developing *Drosophila melanogaster* nervous-system tracking, Dr. P. Keller / HHMI Janelia, SIMView light-sheet, 30 s time step. R7 uses only centroid coordinates and gold-mask voxel counts already recovered there.

## Tribolium (`Fluo-N3DL-TRIC`)
Source lane: `lab_lanes/r6_tribolium_trajectory`.

Committed derived files and R6 SHA-256 values:
- `tric_selected_centroids.csv` — `84bb18a9e8e79d84e90630b8d3778153a18b15aef569a0c08099e852222e98a6`
- `01_man_track.txt` — `aae4bbd2b660a96de8683c64327a3b2e6171802121e935c4ae0a92bbf04a35d1`
- `02_man_track.txt` — `ae2681b418f669ec4609f5d98274efdc33b1ba52a7860657c5b9aabbad325747`

R6 attributes the public CTC dataset to developing *Tribolium castaneum*, Dr. A. Jain / MPI-CBG Dresden, cartographic projection, 1.5 min time step. R7 uses projected x/y centroid geometry and gold-mask voxel counts; it does not interpret projected coordinates as micrometers.

## Leakage boundary
Features use frames <=25 only. Outcomes alone use frame 40. Sequence-local anchor centering, RMS scaling, and ranks are computed from released frame-25 measurements of that acquisition and are explicitly part of the measured present representation. No held-out future outcome is used in feature construction, estimator fitting, hyperparameter tuning, or naive-baseline fitting.
