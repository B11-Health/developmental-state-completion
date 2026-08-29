import json,hashlib
from pathlib import Path
R=Path('/root/plant_m2_reeb_global')
laws={
'P00':[.001,.5996666666666667,.5996666666666667,.5996666666666667],
'P01':[.5996666666666667,.001,.5996666666666667,.5996666666666667],
'P02':[.5996666666666667,.5996666666666667,.001,.5996666666666667],
'P03':[.5996666666666667,.5996666666666667,.5996666666666667,.001],
'P04':[.005,.005,.895,.895],
'P05':[.895,.895,.005,.005],
'P06':[.05,.9,.35,.5],
'P07':[.95,.1,.65,.1],
}
states=['0000','0011','0101','0110','1111','1100','1010','1001']
fr={'date':'2026-08-26','purpose':'prospective post-hypothesis source validation of two-complementary-phenotype nonlinear reconstruction through morphogenesis','decoder':'RECTIFIED_GLOBAL_DEG3_FROZEN_2026-08-26.npz trained new40 only; constrained nonlinear inversion; no refit after these renders','contexts':'for each selected starting state s, use source phenotypes at s and s xor1111; selected states form four complete complementary pairs','laws':laws,'states':states,'predictions':['100% sign recovery across all 32 starting-world pairs','median signed L2 error <0.001','maximum signed L2 error <0.002','weak gain .001 signs recovered correctly']}
raw=json.dumps(fr,sort_keys=True,separators=(',',':')).encode();fr['sha256_pre_render']=hashlib.sha256(raw).hexdigest();json.dump(fr,open(R/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json','w'),indent=2);print(fr['sha256_pre_render'])
