from pathlib import Path
import csv, math, sys
import numpy as np
from PIL import Image

COORDS=('cx','cy','sx','sy','covxy','entropy','occupancy','edge')

def compute_panel(panel):
    a=np.asarray(panel,dtype=np.float64)
    bg=float(np.percentile(a,5.0))
    s=np.clip(a-bg,0.0,None)
    cap=float(np.percentile(s,99.5))
    if (not np.isfinite(cap)) or cap<=0.0:
        cap=1.0
    s=np.minimum(s,cap)
    total=float(s.sum())
    h,w=s.shape
    if total<=0.0:
        return {'cx':0.5,'cy':0.5,'sx':0.0,'sy':0.0,'covxy':0.0,'entropy':0.0,'occupancy':0.0,'edge':0.0}
    y,x=np.mgrid[0:h,0:w]
    wt=s/total
    xn=x/(w-1); yn=y/(h-1)
    cx=float((wt*x).sum()/(w-1)); cy=float((wt*y).sum()/(h-1))
    sx=float(np.sqrt((wt*(xn-cx)**2).sum())); sy=float(np.sqrt((wt*(yn-cy)**2).sum()))
    covxy=float((wt*(xn-cx)*(yn-cy)).sum())
    hh=(h//8)*8; ww=(w//8)*8
    blocks=s[:hh,:ww].reshape(8,hh//8,8,ww//8).sum(axis=(1,3)).ravel()
    bsum=float(blocks.sum())
    if bsum>0.0:
        q=blocks/bsum; q=q[q>0]
        entropy=float(-(q*np.log(q)).sum()/math.log(64.0))
    else:
        entropy=0.0
    occupancy=float(np.mean(s/cap))
    gx=float(np.abs(np.diff(s,axis=1)).mean()/cap)
    gy=float(np.abs(np.diff(s,axis=0)).mean()/cap)
    edge=(gx+gy)/2.0
    return {'cx':cx,'cy':cy,'sx':sx,'sy':sy,'covxy':covxy,'entropy':entropy,'occupancy':occupancy,'edge':edge}

def extract(tif_path,csv_path):
    im=Image.open(tif_path)
    n=int(getattr(im,'n_frames',1)); W,H=im.size
    if W%4!=0: raise RuntimeError(f'width {W} not divisible by four')
    pw=W//4; rows=[]
    for idx in range(n):
        im.seek(idx); a=np.asarray(im)
        row={'time_index':idx+1}; panels=[]
        for view in range(4):
            feat=compute_panel(a[:,view*pw:(view+1)*pw]); panels.append(feat)
            for k in COORDS: row[f'v{view+1}_{k}']=feat[k]
        for k in COORDS:
            vals=np.asarray([p[k] for p in panels],dtype=np.float64)
            row[f'mean_{k}']=float(vals.mean()); row[f'sd_{k}']=float(vals.std(ddof=0))
        rows.append(row)
    with open(csv_path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return {'frames':n,'width':W,'height':H,'columns':len(rows[0])}

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: independent_extract.py INPUT.TIF OUTPUT.csv')
    print(extract(Path(sys.argv[1]),Path(sys.argv[2])))
