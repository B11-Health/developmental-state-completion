import argparse, importlib.util, json, math, struct
from pathlib import Path
BASE=Path(__file__).parent; ROOT=BASE.parents[1]; CACHE=BASE/'raw_cache'; CACHE.mkdir(exist_ok=True)
R5=ROOT/'lab_lanes'/'r5_drosophila_trajectory'; spec=importlib.util.spec_from_file_location('rz',R5/'remote_zip_extract.py'); rz=importlib.util.module_from_spec(spec); spec.loader.exec_module(rz)
CFG={'Drosophila':('drosophila','Fluo-N3DL-DRO','https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-DRO.zip'),'Tribolium':('tribolium','Fluo-N3DL-TRIC','https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-TRIC.zip')}
CHUNK=8*1024*1024
ap=argparse.ArgumentParser(); ap.add_argument('--organism',choices=CFG,required=True); ap.add_argument('--sequence',choices=['01','02'],required=True); ap.add_argument('--frame',type=int,choices=[23,24,25],required=True); ap.add_argument('--chunk',type=int,required=True); a=ap.parse_args()
slug,ds,url=CFG[a.organism]; es=rz.entries(url); suffix=f'/{a.sequence}/t{a.frame:03d}.tif'; e=next(x for x in es if x['name'].replace('\\','/').endswith(suffix)); off=e['local_offset']; h=rz.get_range(url,off,off+29); vals=struct.unpack('<4s5H3L2H',h); fnl,xl=vals[-2],vals[-1]; dataoff=off+30+fnl+xl
n=math.ceil(e['comp_size']/CHUNK); assert 0<=a.chunk<n; lo=a.chunk*CHUNK; hi=min(e['comp_size'],(a.chunk+1)*CHUNK)-1; b=rz.get_range(url,dataoff+lo,dataoff+hi)
out=CACHE/f'{slug}_{a.sequence}_{a.frame:03d}.part{a.chunk:02d}of{n:02d}'; out.write_bytes(b)
meta={'organism':a.organism,'sequence':a.sequence,'frame':a.frame,'zip_name':e['name'],'method':e['method'],'crc32':e['crc'],'compressed_size':e['comp_size'],'uncompressed_size':e['uncomp_size'],'local_offset':e['local_offset'],'data_offset':dataoff,'chunk_size':CHUNK,'n_chunks':n}
(CACHE/f'{slug}_{a.sequence}_{a.frame:03d}.meta.json').write_text(json.dumps(meta,indent=2))
print(out.name,len(b),'of',e['comp_size'],'chunks',n)
