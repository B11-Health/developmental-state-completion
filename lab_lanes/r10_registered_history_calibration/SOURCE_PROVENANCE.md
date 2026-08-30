# R10 Source Provenance

Date: 2026-08-30

R10 introduces no new biological data. It consumes the committed R8 Tribolium analysis table and feature schema through the R9-qualified task definition.

Controlling upstream artifacts:
- `lab_lanes/r8_morphology_intensity_rescue/results/tribolium_analysis_table.csv`
- `lab_lanes/r8_morphology_intensity_rescue/results/feature_schema.json`
- `lab_lanes/r9_domain_registration_rescue/PREREGISTRATION.md`
- `lab_lanes/r9_domain_registration_rescue/R9_CHECKPOINT_2026-08-30.md`

The R8 table inherits public Cell Tracking Challenge provenance and the explicit annotation boundary that GT/TRA masks are tracking-label geometry proxies rather than dense segmentation ground truth. R10 uses no frame after 25 to construct S or H; Y remains the frozen frame25-to-frame40 future radial velocity.

R10 does not fetch, alter, or add biological observations. Synthetic calibration changes only a copy of Y in memory for sensitivity testing and is never represented as measured biology.
