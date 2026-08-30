from pathlib import Path
import argparse, csv, math
import numpy as np
from PIL import Image

def panel_features(a):
    a=np.asarray(a,dtype=np.float64)
    bg=np.percentile(a,5.0)
    s=np.clip(a-bg,0,None)
    hi=np.percentile(s,99.5)
    if not np.isfinite(hi) or hi<=0: hi=1.0
    s=np.minimum(s,hi)
    total=s.sum()
    h,w=s.shape
    yy,xx=np.mgrid[0:h,0:w]
    if total<=0:
        return dict(cx=.5,cy=.5,sx=0,sy=0,covxy=0,entropy=0,occupancy=0,edge=0)
    wt=s/total
    cx=float((wt*xx).sum()/(w-1)); cy=float((wt*yy).sum()/(h-1))
    xn=xx/(w-1); yn=yy/(h-1)
    sx=float(np.sqrt((wt*(xn-cx)**2).sum())); sy=float(np.sqrt((wt*(yn-cy)**2).sum()))
    cov=float((wt*(xn-cx)*(yn-cy)).sum())
    # coarse spatial entropy (8x8 equal-area blocks)
    hs=(h//8)*8; ws=(w//8)*8; q=s[:hs,:ws].reshape(8,hs//8,8,ws//8).sum(axis=(1,3)).ravel(); q=q/q.sum() if q.sum()>0 else q
    ent=float(-(q[q>0]*np.log(q[q>0])).sum()/math.log(len(q))) if np.any(q>0) else 0.0
    occ=float(np.mean(s/hi))
    gx=np.abs(np.diff(s,axis=1)).mean()/hi; gy=np.abs(np.diff(s,axis=0)).mean()/hi
    edge=float((gx+gy)/2)
    return dict(cx=cx,cy=cy,sx=sx,sy=sy,covxy=cov,entropy=ent,occupancy=occ,edge=edge)

def extract(path,out_csv):
    im=Image.open(path); n=getattr(im,'n_frames',1); W,H=im.size
    if W%4: raise ValueError(f'width {W} not divisible by 4')
    pw=W//4; rows=[]
    for t in range(n):
        im.seek(t); arr=np.array(im)
        row={'time_index':t+1}
        per=[]
        for v in range(4):
            f=panel_features(arr[:,v*pw:(v+1)*pw]); per.append(f)
            for k,val in f.items(): row[f'v{v+1}_{k}']=val
        for k in per[0]:
            vals=np.array([x[k] for x in per],float); row[f'mean_{k}']=float(vals.mean()); row[f'sd_{k}']=float(vals.std())
        rows.append(row)
    keys=list(rows[0]);
    with open(out_csv,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    print({'frames':n,'size':(W,H),'features':len(keys)-1,'out':str(out_csv)})

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('tif');ap.add_argument('out');a=ap.parse_args();extract(a.tif,a.out)
