import argparse, binascii, hashlib, importlib.util, io, json, math, sys, zlib
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

BASE = Path(__file__).parent
ROOT = BASE.parents[1]
R5 = ROOT / 'lab_lanes' / 'r5_drosophila_trajectory'
spec = importlib.util.spec_from_file_location('remotezip_r8', R5 / 'remote_zip_extract.py')
rz = importlib.util.module_from_spec(spec); spec.loader.exec_module(rz)
FRAMES = [23,24,25]
EPS = 1e-12
CONFIG = {
 'Drosophila': {'slug':'drosophila','dataset':'Fluo-N3DL-DRO','url':'https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-DRO.zip','mode':'3d','spacing_xyz':(0.406,0.406,2.03)},
 'Tribolium': {'slug':'tribolium','dataset':'Fluo-N3DL-TRIC','url':'https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DL-TRIC.zip','mode':'2d_projection','spacing_xyz':None},
}

def safe_cov(points):
    if len(points) <= 1:
        return np.zeros((points.shape[1], points.shape[1]), float)
    x = points - points.mean(axis=0, keepdims=True)
    return (x.T @ x) / len(points)

def eig_summary(points):
    cov = safe_cov(points)
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals = np.maximum(vals[order], 0.0); vecs = vecs[:,order]
    s = vals.sum()
    frac = vals/s if s > EPS else np.zeros_like(vals)
    major = vecs[:,0] if len(vals) else np.zeros(points.shape[1])
    return vals, frac, major, cov

def surface_3d(coords_zyx, spacing_xyz):
    sx,sy,sz = spacing_xyz
    face_area = {(0,0,1): sy*sz, (0,0,-1): sy*sz,
                 (0,1,0): sx*sz, (0,-1,0): sx*sz,
                 (1,0,0): sx*sy, (-1,0,0): sx*sy}
    S = set(map(tuple, coords_zyx.tolist()))
    area = 0.0
    for q in S:
        z,y,x = q
        for d,a in face_area.items():
            dz,dy,dx=d
            if (z+dz,y+dy,x+dx) not in S: area += a
    return area

def perimeter_2d(points_yx):
    S=set(map(tuple, points_yx.tolist())); per=0
    for y,x in S:
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            if (y+dy,x+dx) not in S: per += 1
    return float(per)

def locate(entries, suffix):
    hits=[e for e in entries if e['name'].replace('\\','/').endswith(suffix)]
    if len(hits)!=1: raise RuntimeError(f'expected one entry for {suffix}, got {len(hits)}')
    return hits[0]

def feature_frame(cfg, entries, seq, frame):
    ds=cfg['dataset']; url=cfg['url']
    me=locate(entries, f'/{seq}_GT/TRA/man_track{frame:03d}.tif')
    re=locate(entries, f'/{seq}/t{frame:03d}.tif')
    mraw=rz.extract_bytes(url,me)
    cache=BASE/'raw_cache'; stem=f"{cfg['slug']}_{seq}_{frame:03d}"; meta_path=cache/f'{stem}.meta.json'
    if meta_path.exists():
        meta=json.loads(meta_path.read_text())
        parts=[cache/f"{stem}.part{i:02d}of{meta['n_chunks']:02d}" for i in range(meta['n_chunks'])]
        if not all(q.exists() for q in parts): raise RuntimeError(f'incomplete cache for {stem}')
        data=b''.join(q.read_bytes() for q in parts)
        if len(data)!=re['comp_size']: raise RuntimeError(f'compressed size mismatch for {stem}')
        rraw=data if re['method']==0 else zlib.decompress(data,-15) if re['method']==8 else (_ for _ in ()).throw(RuntimeError('unsupported compression'))
        if len(rraw)!=re['uncomp_size'] or (binascii.crc32(rraw)&0xffffffff)!=re['crc']: raise RuntimeError(f'cache integrity failure for {stem}')
    else:
        rraw=rz.extract_bytes(url,re)
    mi=Image.open(io.BytesIO(mraw)); ri=Image.open(io.BytesIO(rraw))
    mz=getattr(mi,'n_frames',1); rz_n=getattr(ri,'n_frames',1)
    if mz!=rz_n or mi.size!=ri.size: raise RuntimeError(f'image/mask shape mismatch {seq} {frame}: {mi.size,mz} vs {ri.size,rz_n}')
    labs_l=[]; xs=[]; ys=[]; zs=[]; ints=[]; grads=[]; bflags=[]; out_labs=[]; out_vals=[]
    for z in range(mz):
        mi.seek(z); ri.seek(z)
        M=np.asarray(mi,dtype=np.int64); I=np.asarray(ri).astype(np.float64,copy=False)
        yy,xx=np.nonzero(M)
        if len(xx)==0: continue
        L=M[yy,xx].astype(np.int64)
        h,w=M.shape
        xm=np.maximum(xx-1,0); xp=np.minimum(xx+1,w-1); ym=np.maximum(yy-1,0); yp=np.minimum(yy+1,h-1)
        gx=(I[yy,xp]-I[yy,xm])/np.maximum((xp-xm),1)
        gy=(I[yp,xx]-I[ym,xx])/np.maximum((yp-ym),1)
        gv=np.hypot(gx,gy)
        neigh_labels=[M[yy,xm],M[yy,xp],M[ym,xx],M[yp,xx]]
        bf=np.zeros(len(xx),dtype=bool)
        for nl in neigh_labels: bf |= (nl!=L)
        labs_l.append(L); xs.append(xx.astype(np.int32)); ys.append(yy.astype(np.int32)); zs.append(np.full(len(xx),z,np.int16))
        ints.append(I[yy,xx]); grads.append(gv); bflags.append(bf)
        # In-plane adjacent outside/different-label intensity, attributed to focal label.
        neigh_vals=[I[yy,xm],I[yy,xp],I[ym,xx],I[yp,xx]]
        for nl,nv in zip(neigh_labels,neigh_vals):
            q=(nl!=L)
            if np.any(q): out_labs.append(L[q].astype(np.int64)); out_vals.append(nv[q].astype(float))
    labs=np.concatenate(labs_l); X=np.concatenate(xs); Y=np.concatenate(ys); Z=np.concatenate(zs); V=np.concatenate(ints); G=np.concatenate(grads); B=np.concatenate(bflags)
    OL=np.concatenate(out_labs) if out_labs else np.array([],dtype=np.int64); OV=np.concatenate(out_vals) if out_vals else np.array([],dtype=float)
    rows=[]
    for lab in np.unique(labs):
        q=(labs==lab); z=Z[q].astype(int); y=Y[q].astype(int); x=X[q].astype(int); v=V[q]; g=G[q]; bf=B[q]
        coords_zyx=np.column_stack([z,y,x])
        if cfg['mode']=='3d':
            sx,sy,sz=cfg['spacing_xyz']; P=np.column_stack([x*sx,y*sy,z*sz]).astype(float)
            vals,frac,major,cov=eig_summary(P); rms=math.sqrt(max(float(np.trace(cov)),EPS))
            ex=(x.max()-x.min()+1)*sx; ey=(y.max()-y.min()+1)*sy; ez=(z.max()-z.min()+1)*sz
            ext=np.sort(np.array([ex,ey,ez],float))[::-1]
            surf=surface_3d(coords_zyx,cfg['spacing_xyz']); vol=len(x)*sx*sy*sz
            compact=(math.pi**(1/3)*(6*vol)**(2/3)/surf) if surf>EPS else 0.0
            geom_name='sphericity'; geom_val=compact; area2=np.nan; per2=np.nan
            center=P.mean(axis=0)
        else:
            P_yx=np.unique(np.column_stack([y,x]),axis=0); P=np.column_stack([P_yx[:,1],P_yx[:,0]]).astype(float)
            vals,frac,major,cov=eig_summary(P); rms=math.sqrt(max(float(np.trace(cov)),EPS))
            ex=P[:,0].max()-P[:,0].min()+1; ey=P[:,1].max()-P[:,1].min()+1
            ext=np.sort(np.array([ex,ey],float))[::-1]
            per2=perimeter_2d(P_yx); area2=float(len(P_yx)); compact=(4*math.pi*area2/(per2*per2)) if per2>EPS else 0.0
            geom_name='roundness'; geom_val=compact; surf=np.nan; vol=np.nan; center=P.mean(axis=0)
        weights=np.maximum(v,0.0); wsum=weights.sum()
        if wsum>EPS:
            if cfg['mode']=='3d': allP=np.column_stack([x*sx,y*sy,z*sz]).astype(float)
            else: allP=np.column_stack([x,y]).astype(float)
            iw=(allP*weights[:,None]).sum(axis=0)/wsum; geom=allP.mean(axis=0); shift=iw-geom
            polarity=float(np.linalg.norm(shift)/(rms+EPS)); axis_asym=float(abs(np.dot(shift,major))/(math.sqrt(max(float(vals[0]) if len(vals) else 0.0,0.0))+EPS))
        else: polarity=0.0; axis_asym=0.0
        bmean=float(np.mean(v[bf])) if np.any(bf) else float(np.mean(v)); oq=(OL==lab); omean=float(np.mean(OV[oq])) if np.any(oq) else float(np.mean(v))
        mean=float(np.mean(v)); var=float(np.var(v)); q25,q50,q75=np.quantile(v,[.25,.5,.75])
        row={'sequence':seq,'frame':frame,'label':int(lab),'mask_voxels':int(len(v)),
             'center_x':float(center[0]),'center_y':float(center[1]),'center_z':float(center[2]) if len(center)>2 else 0.0,
             'eig1':float(vals[0]) if len(vals)>0 else 0.0,'eig2':float(vals[1]) if len(vals)>1 else 0.0,'eig3':float(vals[2]) if len(vals)>2 else 0.0,
             'eigfrac1':float(frac[0]) if len(frac)>0 else 0.0,'eigfrac2':float(frac[1]) if len(frac)>1 else 0.0,'eigfrac3':float(frac[2]) if len(frac)>2 else 0.0,
             'axis_ratio21':float(math.sqrt((vals[1]+EPS)/(vals[0]+EPS))) if len(vals)>1 else 0.0,
             'axis_ratio31':float(math.sqrt((vals[2]+EPS)/(vals[0]+EPS))) if len(vals)>2 else 0.0,
             'bbox_major':float(ext[0]),'bbox_mid':float(ext[1]) if len(ext)>1 else 0.0,'bbox_minor':float(ext[2]) if len(ext)>2 else 0.0,
             'bbox_ratio_minor_major':float(ext[-1]/(ext[0]+EPS)),
             'proxy_volume_phys':float(vol) if np.isfinite(vol) else np.nan,'surface_area_phys':float(surf) if np.isfinite(surf) else np.nan,
             'projected_area_px':float(area2) if np.isfinite(area2) else np.nan,'perimeter_px':float(per2) if np.isfinite(per2) else np.nan,
             geom_name:float(geom_val),
             'intensity_mean':mean,'intensity_var':var,'intensity_q25':float(q25),'intensity_median':float(q50),'intensity_q75':float(q75),
             'gradient_mean_inplane':float(np.mean(g)),'gradient_q75_inplane':float(np.quantile(g,.75)),
             'boundary_mean_intensity':bmean,'outside_neighbor_mean_intensity':omean,'boundary_contrast_norm':float((bmean-omean)/(abs(mean)+EPS)),
             'intensity_polarity_norm':polarity,'intensity_axis_asym_abs':axis_asym}
        if cfg['mode']=='3d': row['roundness']=np.nan
        else: row['sphericity']=np.nan
        rows.append(row)
    prov={'sequence':seq,'frame':frame,
          'mask':{'zip_name':me['name'],'compressed_size':me['comp_size'],'uncompressed_size':me['uncomp_size'],'crc32':me['crc'],'sha256_uncompressed':hashlib.sha256(mraw).hexdigest()},
          'raw':{'zip_name':re['name'],'compressed_size':re['comp_size'],'uncompressed_size':re['uncomp_size'],'crc32':re['crc'],'sha256_uncompressed':hashlib.sha256(rraw).hexdigest()},
          'image_xy':list(mi.size),'z_slices':mz,'labels':len(rows)}
    return rows,prov

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--organism',choices=CONFIG,required=True); ap.add_argument('--sequence',choices=['01','02']); ap.add_argument('--frame',type=int,choices=FRAMES); args=ap.parse_args(); cfg=CONFIG[args.organism]
    entries=rz.entries(cfg['url']); rows=[]; files=[]
    seg=[e['name'] for e in entries if '/SEG/' in e['name'].replace('\\','/')]
    seqs=[args.sequence] if args.sequence else ['01','02']; frames=[args.frame] if args.frame else FRAMES
    for seq in seqs:
        for frame in frames:
            rr,pp=feature_frame(cfg,entries,seq,frame); rows.extend(rr); files.append(pp)
            print(args.organism,seq,frame,'labels',len(rr),'raw_comp_MB',round(pp['raw']['compressed_size']/1e6,2),flush=True)
    out=BASE/'source_data'; out.mkdir(exist_ok=True)
    df=pd.DataFrame(rows)
    if args.sequence and args.frame:
        stem=f"{cfg['slug']}_{args.sequence}_{args.frame:03d}"
        df.to_csv(out/f"{stem}_features.csv",index=False)
        manifest={'organism':args.organism,'dataset':cfg['dataset'],'url':cfg['url'],'frames':[args.frame],'mask_role':'GT/TRA tracking-label geometry proxy; not segmentation ground truth','raw_role':'release-native raw intensity','seg_entries_total':len(seg),'seg_entries':[x for x in seg if x and not x.endswith('/')],'files':files}
        (out/f"{stem}_manifest.json").write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    else:
        df.to_csv(out/f"{cfg['slug']}_frame23_25_mask_intensity_features.csv",index=False)
        manifest={'organism':args.organism,'dataset':cfg['dataset'],'url':cfg['url'],'frames':frames,'mask_role':'GT/TRA tracking-label geometry proxy; not segmentation ground truth','raw_role':'release-native raw intensity','seg_entries_total':len(seg),'seg_entries':[x for x in seg if x and not x.endswith('/')],'files':files}
        (out/f"{cfg['slug']}_source_manifest.json").write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('wrote',len(df),'rows',flush=True)
if __name__=='__main__': main()
