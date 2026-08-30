import csv, io, json, hashlib, sys, importlib.util
from pathlib import Path
import numpy as np
from PIL import Image
BASE=Path(__file__).parent
URL='https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-DRO.zip'
VOXEL=(0.406,0.406,2.03)
seq=sys.argv[1]; frames=[int(x) for x in sys.argv[2].split(',')]
spec=importlib.util.spec_from_file_location('remotezip',BASE/'remote_zip_extract.py'); rz=importlib.util.module_from_spec(spec); spec.loader.exec_module(rz)
es=rz.entries(URL)
te=next(e for e in es if e['name'].endswith(f'/{seq}_GT/TRA/man_track.txt'))
labels=sorted(int(x.split()[0]) for x in rz.extract_bytes(URL,te).decode().splitlines() if x.strip()); n=max(labels)+1
rows=[]; files=[]
for frame in frames:
 e=next(e for e in es if e['name'].endswith(f'/{seq}_GT/TRA/man_track{frame:03d}.tif')); raw=rz.extract_bytes(URL,e); im=Image.open(io.BytesIO(raw))
 cnt=np.zeros(n,dtype=np.int64); sx=np.zeros(n); sy=np.zeros(n); sz=np.zeros(n)
 for z in range(im.n_frames):
  im.seek(z); a=np.asarray(im,dtype=np.uint16); yy,xx=np.nonzero(a)
  if len(xx)==0: continue
  labs=a[yy,xx].astype(np.int64); valid=labs<n; labs=labs[valid]; xx=xx[valid]; yy=yy[valid]
  bc=np.bincount(labs,minlength=n); cnt+=bc; sx+=np.bincount(labs,weights=xx,minlength=n); sy+=np.bincount(labs,weights=yy,minlength=n); sz+=bc*z
 present=0
 for lab in labels:
  if cnt[lab]==0: continue
  present+=1; rows.append({'sequence':seq,'frame':frame,'label':lab,'x_um':sx[lab]/cnt[lab]*VOXEL[0],'y_um':sy[lab]/cnt[lab]*VOXEL[1],'z_um':sz[lab]/cnt[lab]*VOXEL[2],'voxel_count':int(cnt[lab])})
 files.append({'sequence':seq,'frame':frame,'zip_name':e['name'],'compressed_size':e['comp_size'],'uncompressed_size':e['uncomp_size'],'crc32':e['crc'],'sha256_uncompressed':hashlib.sha256(raw).hexdigest(),'labels_present':present,'z_slices':im.n_frames,'xy_size':list(im.size)})
 print(seq,frame,'labels',present)
out=BASE/'source_data'; out.mkdir(exist_ok=True); stem=f'dro_centroids_{seq}_'+('_'.join(map(str,frames)))
with (out/(stem+'.csv')).open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(out/(stem+'.json')).write_text(json.dumps({'url':URL,'voxel_um':VOXEL,'files':files},indent=2),encoding='utf-8')
print('saved',stem,len(rows))
