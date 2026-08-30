# R9 Source Provenance

Date: 2026-08-30

R9 uses only committed R8-derived analysis tables and does not fetch new biological data.

## Exact inherited inputs
- `lab_lanes/r8_morphology_intensity_rescue/results/drosophila_analysis_table.csv` — 1,000,994 bytes — SHA-256 `cbd975f9b8042f276f4cd27ed7f7dcccfd43ae0548bae542e82466971bcceac3`.
- `lab_lanes/r8_morphology_intensity_rescue/results/tribolium_analysis_table.csv` — 626,304 bytes — SHA-256 `51a3310f88ea9a3183fd8b0235e8d76badb7c3c349822714113f8cf71cec29c8`.
- `lab_lanes/r8_morphology_intensity_rescue/results/feature_schema.json` — 13,157 bytes — SHA-256 `cc7c5b130fbe4493bbf04a589a278660ad11662460a51bc73eab0b751678c260`.

Those R8 tables inherit the public Cell Tracking Challenge provenance and R8 boundary that GT/TRA label volumes are tracking-label geometry proxies, not dense segmentation ground truth, and raw fluorescence intensity is not a calibrated molecular measurement.

R9 transformations use only present-state S. No frame after 25 and no future outcome is used to fit a registration transform.
