import sys,types,json,re,shutil
from pathlib import Path
R=Path('/root/plant_m2_reeb_global');O=R/'two_phenotype_prospective_source';shutil.rmtree(O,ignore_errors=True);O.mkdir();fr=json.load(open(R/'TWO_PHENOTYPE_PROSPECTIVE_FROZEN_2026-08-26.json'))
m=types.ModuleType('matplotlib');p=types.ModuleType('matplotlib.pyplot');m.pyplot=p;sys.modules['matplotlib']=m;sys.modules['matplotlib.pyplot']=p
sys.path.insert(0,'/root/leaf-shape-evolution/vlab/oofs/ext/NPHLeafModels/LeafGenerator');import pdict,pwriter
idx0=pdict.leafids.index('p8ae');base={k:pdict.pdict[k][idx0] for k in pdict.pdict};params=[('CURVATURE1',0.05),('STRETCH1',10.5),('CFLOW1',0.008),('NORMAL1',0.0041)];links=[('CURVATURE2','CURVATURE1'),('STRETCH2','STRETCH1'),('CFLOW2','CFLOW1'),('NORMAL2','NORMAL1')];base2={d:base[d] for d,s in links};jobs=[];meta={}
for l,g in fr['laws'].items():
 for ss in fr['states']:
  st=int(ss,2);bits=[int(c) for c in ss];par=dict(base)
  for pos in range(2,11):par[f'I{pos}']=1
  for (k,v),bb in zip(params,bits):
   if bb:par[k]=v
  key=f'{l}_{ss}';d=O/key;d.mkdir();pwriter.Input(par,str(d.resolve()),0);hp=d/'MyParameters0.h';txt=hp.read_text()
  for aa,(dst,srcn) in zip(g,links):txt=re.sub(rf'^#define {dst} .+$',f'#define {dst} ({base2[dst]} + {float(aa)}*(({srcn}) - {base2[dst]}))',txt,flags=re.M)
  hp.write_text(txt);jobs.append(key);meta[key]={'law':l,'gains':g,'state':ss}
json.dump({'freeze_sha':fr['sha256_pre_render'],'meta':meta},open(O/'meta.json','w'),indent=2)
for q in range(4):(R/f'tpp_jobs_{q}').write_text('\n'.join(jobs[q::4])+'\n')
print('jobs',len(jobs))
