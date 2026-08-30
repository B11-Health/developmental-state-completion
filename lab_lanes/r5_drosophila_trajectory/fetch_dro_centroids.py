import csv, io, json, hashlib
from pathlib import Path
import importlib.util
import numpy as np
from PIL import Image

BASE=Path(__file__).parent
URL='https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-DRO.zip'
FRAMES=[15,20,23,24,25,40]
VOXEL=(0.406,0.406,2.03)  # x,y,z microns from CTC dataset page

spec=importlib.util.spec_from_file_location('remotezip',BASE/'remote_zip_extract.py')
rz=importlib.util.module_from_spec(spec); spec.loader.exec_module(rz)
entries=rz.entries(URL)
rows=[]
manifest={'url':URL,'frames':FRAMES,'voxel_um':VOXEL,'files':[]}
for seq in ('01','02'):
    track_entry=next(e for e in entries if e['name'].endswith(f'/{seq}_GT/TRA/man_track.txt'))
    track_raw=rz.extract_bytes(URL,track_entry)
    track_lines=[x.split() for x in track_raw.decode('utf-8').splitlines() if x.strip()]
    labels=sorted(int(x[0]) for x in track_lines)
    n=max(labels)+1
    for frame in FRAMES:
        suffix=f'/{seq}_GT/TRA/man_track{frame:03d}.tif'
        e=next(e for e in entries if e['name'].endswith(suffix))
        raw=rz.extract_bytes(URL,e)
        im=Image.open(io.BytesIO(raw))
        cnt=np.zeros(n,dtype=np.int64); sx=np.zeros(n); sy=np.zeros(n); sz=np.zeros(n)
        for z in range(getattr(im,'n_frames',1)):
            im.seek(z)
            a=np.asarray(im,dtype=np.uint16)
            yy,xx=np.nonzero(a)
            if len(xx)==0: continue
            labs=a[yy,xx].astype(np.int64)
            valid=labs<n
            labs=labs[valid]; xx=xx[valid]; yy=yy[valid]
            bc=np.bincount(labs,minlength=n)
            cnt += bc
            sx += np.bincount(labs,weights=xx,minlength=n)
            sy += np.bincount(labs,weights=yy,minlength=n)
            sz += bc*z
        present=0
        for lab in labels:
            if cnt[lab]==0: continue
            present += 1
            rows.append({'sequence':seq,'frame':frame,'label':lab,
                         'x_um':sx[lab]/cnt[lab]*VOXEL[0],
                         'y_um':sy[lab]/cnt[lab]*VOXEL[1],
                         'z_um':sz[lab]/cnt[lab]*VOXEL[2],
                         'voxel_count':int(cnt[lab])})
        manifest['files'].append({'sequence':seq,'frame':frame,'zip_name':e['name'],'compressed_size':e['comp_size'],'uncompressed_size':e['uncomp_size'],'crc32':e['crc'],'sha256_uncompressed':hashlib.sha256(raw).hexdigest(),'labels_present':present,'z_slices':getattr(im,'n_frames',1),'xy_size':list(im.size)})
        print(seq,frame,'labels',present,'raw_MB',round(len(raw)/1e6,3))

out=BASE/'source_data'; out.mkdir(exist_ok=True)
with (out/'dro_selected_centroids.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(out/'dro_source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('rows',len(rows))
