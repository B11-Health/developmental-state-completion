import json,hashlib
from pathlib import Path
R=Path('/root/plant_m2_reeb_global')
base=json.load(open(R/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json'))
seen=set(base['states']); allstates=[f'{i:04b}' for i in range(16)]; missing=[s for s in allstates if s not in seen]
fr={
 'date':'2026-08-26',
 'purpose':'prospective context-generalization extension: render only previously unseen states for the already-frozen P00-P07 laws, then evaluate all five exact Hamming>=3 two-context panels',
 'scope_warning':'Laws P00-P07 were already partially source-rendered in the complementary-pair cohort. This is prospective with respect to the missing contexts/masks, not a new-law generalization test.',
 'parent_freeze_sha':base['sha256_pre_render'],
 'laws':base['laws'],
 'already_rendered_states':base['states'],
 'new_states_to_render':missing,
 'masks':['0111','1011','1101','1110','1111'],
 'estimator':{
   'cubic':'RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz',
   'cubic_sha256':'d7e4027e4ed252225b5f5db87b758df31c67d94c02af1680ce172dc9b6074340',
   'linear_initializer':'TWO_PHENOTYPE_LINEAR_U_DECODER_FROZEN_2026-08-26.npz',
   'linear_initializer_sha256':'856bcc7076af37d7a548e720dfe1cebcfd7acc92f35997b683e1e7c56cffe904',
   'reference_algorithm':'five_two_context_nonlinear_decoder.py',
   'reference_algorithm_sha256':'bbebc27b2ec562c2d5d83b69dd2b8c45a6b43ca36adb87b91d9bd4994dfe4508',
   'rule':'Use the same constrained nonlinear u decoder and fixed-budget reconstruct function; no refit, retuning, new starts, threshold changes, or source-informed estimator modification.'
 },
 'predictions':[
   'Each of the five masks has 100% sign accuracy over all 8 laws x 16 starting states.',
   'Each mask has median signed-coordinate L2 error <0.001.',
   'Each mask has maximum signed-coordinate L2 error <0.002.',
   'For P00-P03, every pair involving the 0.001 channel recovers that channel sign correctly under every mask.'
 ],
 'evaluation':'After completing only new_states_to_render, combine those immutable outputs with the parent cohort TSVs to form the 16-state source table. Evaluate every starting state for each mask; report duplicate-oriented 128 tests/mask and also 64 unordered state-pairs/mask where appropriate.'
}
raw=json.dumps(fr,sort_keys=True,separators=(',',':')).encode(); fr['sha256_pre_render']=hashlib.sha256(raw).hexdigest()
out=R/'FIVE_MASK_PROSPECTIVE_EXTENSION_FROZEN_2026-08-26.json';json.dump(fr,open(out,'w'),indent=2)
print(fr['sha256_pre_render']);print('missing',missing,'jobs',len(missing)*len(fr['laws']))
