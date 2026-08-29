# Exploratory reproduction variants

This directory contains post-hoc sensitivity analyses that deliberately alter the prediction interface from the frozen primary FM1 replication. They are retained for provenance and should not be mixed with the preregistered/direct-source checkpoint.

`reproduce_fm1_grouped.py` uses a relative per-hour volume-growth target and a richer trajectory-geometry stack (including 96 h geometry, 120 h geometry, displacement, neighbor count and volume change). Under that richer geometry interface, flexible nonlinear models already explain about half the future-growth variance and current genes add little; linear Ridge still gains substantially from current genes. This reinforces the central conclusion that apparent state-completion/dimension depends on the observation interface and decoder.
