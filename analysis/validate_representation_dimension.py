#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'results'
def j(n): return json.loads((R/n).read_text())
def close(a,b,t=1e-9):
    if abs(a-b)>t: raise AssertionError((a,b))
r=j('refahi_pc_completion_L1_ridge.json')['rows']; close(r['geom']['r2_oof'],0.30661368572262404); close(r['geom+PC1']['r2_oof'],0.45149781988470905); close(r['geom+PC4']['r2_oof'],0.5977757631689217); close(r['geom+all25']['r2_oof'],0.5990869276144117)
e=j('refahi_pc_completion_L1_extra_trees.json')['rows']; close(e['geom+PC1']['r2_oof'],0.6360923008238175); close(e['geom+all25']['r2_oof'],0.6299763366476829)
h=j('refahi_pc_completion_L1_histgb.json')['rows']; close(h['geom+PC1']['r2_oof'],0.6602142905578487); close(h['geom+all25']['r2_oof'],0.6501422161125148)
es=j('refahi_pc_split_stability_extra_trees_30.json'); close(es['summary']['pc1']['mean'],0.6535538114718805); close(es['summary']['all25']['mean'],0.6379639611230237); close(es['fraction_pc1_ge_all25'],1.0)
hs=j('refahi_pc_split_stability_histgb_30.json'); close(hs['summary']['pc1']['mean'],0.6744265468418057); close(hs['summary']['all25']['mean'],0.6710083898169008); close(hs['fraction_pc1_ge_all25'],0.7)

sc=j('refahi_pc1_state_code_audit.json'); close(sc['pc1_explained_variance'],0.5820176211735517); close(sc['n_unique_pc1_state_means'],8); close(sc['min_state_pc1_separation'],0.01567075845018895)
rp=j('refahi_random_projection_extra_trees.json'); close(rp['random_projection']['fraction_injective'],1.0); close(rp['random_projection']['median'],0.5996336954194558)
rph=j('refahi_random_projection_histgb.json'); close(rph['random_projection']['fraction_injective'],1.0); close(rph['random_projection']['median'],0.6302397351680256)
ra=j('refahi_pc1_robustness_alignment_audit.json'); close(ra['random_10000']['pc1_margin_percentile'],0.4988); close(ra['random_10000']['pc1_standardized_margin_percentile'],0.1443); close(ra['random_10000']['pc1_abs_spearman_percentile'],0.7439)

print('REPRESENTATION_DIMENSION_VALIDATED')
