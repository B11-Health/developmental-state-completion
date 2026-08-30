import csv, io, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
from PIL import Image
BASE=Path(__file__).parent
URL='https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-TRIC.zip'
FRAMES=[15,20,23,24,25,40]
spec=importlib.util.spec_from_file_location('remotezip',BASE/'remote_zip_extract.py'); rz=importlib.util.module_from_spec(spec); spec.loader.exec_module(rz)
es=rz.entries(URL)
out=BASE/'source_data'; out.mkdir(exist_ok=True)
rows=[]; manifest={'url':URL,'frames':FRAMES,'coordinate_note':'x/y pixel coordinates of cartographic-projection gold labels; z slice centroid retained diagnostically but no physical voxel calibration is claimed','files':[]}
for seq in ('01','02'):
    te=next(e for e in es if e['name'].endswith(f'/{seq}_GT/TRA/man_track.txt'))
    traw=rz.extract_bytes(URL,te); (out/f'{seq}_man_track.txt').write_bytes(traw)
    labels=sorted(int(x.split()[0]) for x in traw.decode().splitlines() if x.strip()); n=max(labels)+1
    for frame in FRAMES:
        e=next(e for e in es if e['name'].endswith(f'/{seq}_GT/TRA/man_track{frame:03d}.tif'))
        raw=rz.extract_bytes(URL,e); im=Image.open(io.BytesIO(raw)); cnt=np.zeros(n,dtype=np.int64); sx=np.zeros(n); sy=np.zeros(n); sz=np.zeros(n)
        for z in range(getattr(im,'n_frames',1)):
            im.seek(z); a=np.asarray(im,dtype=np.uint16); yy,xx=np.nonzero(a)
            if len(xx)==0: continue
            labs=a[yy,xx].astype(np.int64); ok=labs<n; labs=labs[ok]; xx=xx[ok]; yy=yy[ok]
            bc=np.bincount(labs,minlength=n); cnt+=bc
            sx+=np.bincount(labs,weights=xx,minlength=n); sy+=np.bincount(labs,weights=yy,minlength=n); sz+=bc*z
        present=0
        for lab in labels:
            if cnt[lab]==0: continue
            present+=1; rows.append({'sequence':seq,'frame':frame,'label':lab,'x_px':sx[lab]/cnt[lab],'y_px':sy[lab]/cnt[lab],'z_slice':sz[lab]/cnt[lab],'voxel_count':int(cnt[lab])})
        manifest['files'].append({'sequence':seq,'frame':frame,'zip_name':e['name'],'compressed_size':e['comp_size'],'uncompressed_size':e['uncomp_size'],'crc32':e['crc'],'sha256_uncompressed':hashlib.sha256(raw).hexdigest(),'labels_present':present,'z_slices':getattr(im,'n_frames',1),'xy_size':list(im.size)})
        print(seq,frame,'labels',present,'compressed_kB',round(e['comp_size']/1000,1))
with (out/'tric_selected_centroids.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(out/'tric_source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('rows',len(rows))
