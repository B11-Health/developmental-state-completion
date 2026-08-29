import re, pickle, subprocess, math, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA

ROOT=Path('refahi_diag')
OUT=Path('developmental-state-completion/reproduction')

class DummyDTissue: pass
class RemapUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module=='atlasviewer.dtissue' and name=='DTissue': return DummyDTissue
        if module=='copy_reg': module='copyreg'
        if module=='__builtin__': module='builtins'
        return super().find_class(module,name)

def load_dtissue():
    b=subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:stateAnalysis/FM1_dtissue.tis'])
    import io
    return RemapUnpickler(io.BytesIO(b), encoding='latin1').load()

def read_gene(tp):
    f=ROOT/'data'/'geneExpression'/f't_{tp}h.txt'
    df=pd.read_csv(f, sep=r'\s+')
    df=df.rename(columns={df.columns[0]:'CID'})
    df['CID']=df['CID'].astype(int)
    return df.set_index('CID')

def read_geom(tp):
    f=ROOT/'data'/'FM1'/'tv'/f'{tp}h_segmented_tvformat_volume_position.txt'
    rows=[]
    pat=re.compile(r'cid:\s*(\d+),\s*volume:\s*([0-9eE+\-.]+),\s*center:\s*\[([^\]]+)\]')
    for line in f.read_text().splitlines():
        m=pat.search(line)
        if not m: continue
        cid=int(m.group(1)); vol=float(m.group(2)); xyz=[float(x) for x in m.group(3).split()]
        rows.append((cid,vol,*xyz))
    df=pd.DataFrame(rows,columns=['CID','volume','x','y','z']).set_index('CID')
    nf=ROOT/'data'/'FM1'/'tv'/f'{tp}h_segmented_tvformat_neighbors.txt'
    # Format varies; count integer neighbors after colon and exclude background 1 when present.
    nmap={}
    for line in nf.read_text().splitlines():
        nums=[int(x) for x in re.findall(r'\d+',line)]
        if nums:
            cid=nums[0]; neigh=[x for x in nums[1:] if x!=1 and x!=cid]; nmap[cid]=len(set(neigh))
    df['neighbors']=[nmap.get(int(i),np.nan) for i in df.index]
    return df

def ancestor(obj,cid,from_tp,to_tp):
    tps=obj.timePoints; i=tps.index(from_tp); j=tps.index(to_tp); cur=int(cid)
    if j>i: raise ValueError
    while i>j:
        tp=tps[i]
        cur=int(obj.dtissue[tp]['mother'].get(cur,-1))
        if cur<0: return None
        i-=1
    return cur

def descendants(obj,cid,from_tp,to_tp):
    tps=obj.timePoints; i=tps.index(from_tp); j=tps.index(to_tp); cur=[int(cid)]
    while i<j:
        tp=tps[i]; nxt=[]
        dmap=obj.dtissue[tp].get('daughters',{})
        for c in cur: nxt.extend([int(x) for x in dmap.get(c,[])])
        cur=nxt; i+=1
        if not cur: break
    return cur

def build_dataset():
    obj=load_dtissue(); g96=read_gene(96); g120=read_gene(120); geo96=read_geom(96); geo120=read_geom(120)
    v132=obj.dtissue['132h']['volumes']; t120=obj.dtissue['120h']['real_timepoint']; t132=obj.dtissue['132h']['real_timepoint']
    genes=sorted(set(g96.columns)&set(g120.columns))
    rows=[]
    for cid in sorted(set(g120.index)&set(geo120.index)):
        a96=ancestor(obj,cid,'120h','96h')
        if a96 is None or a96 not in g96.index or a96 not in geo96.index: continue
        ds=descendants(obj,cid,'120h','132h')
        ds=[d for d in ds if d in v132]
        if not ds: continue
        vcur=float(geo120.loc[cid,'volume']); vf=float(sum(float(v132[d]) for d in ds))
        if vcur<=0 or vf<=0: continue
        y=(vf-vcur)/((t132-t120)*vcur)
        r={'cid120':int(cid),'ancestor96':int(a96),'future_growth':float(y),'future_logfold':float(math.log(vf/vcur)),'n_desc132':len(ds)}
        for nm in ['volume','x','y','z','neighbors']:
            r[f'g120_{nm}']=float(geo120.loc[cid,nm])
            r[f'g96_{nm}']=float(geo96.loc[a96,nm])
        r['g120_logvolume']=math.log(max(r['g120_volume'],1e-12)); r['g96_logvolume']=math.log(max(r['g96_volume'],1e-12))
        for ax in ['x','y','z']: r[f'd_{ax}']=r[f'g120_{ax}']-r[f'g96_{ax}']
        r['logvol_ratio_96_120']=math.log(max(r['g120_volume'],1e-12)/max(r['g96_volume'],1e-12))
        for gene in genes:
            r[f'cur_{gene}']=float(g120.loc[cid,gene]); r[f'old_{gene}']=float(g96.loc[a96,gene])
        rows.append(r)
    return pd.DataFrame(rows),genes

def grouped_oof(df, feature_sets, target='future_growth'):
    groups=df['ancestor96'].values; y=df[target].values
    splitter=GroupKFold(n_splits=5)
    splits=list(splitter.split(df, y, groups))
    results=[]
    models={
      'ridge': lambda: make_pipeline(StandardScaler(),Ridge(alpha=10.0)),
      'histgb': lambda: HistGradientBoostingRegressor(max_iter=300,max_leaf_nodes=15,min_samples_leaf=20,l2_regularization=2.0,random_state=7),
      'rf': lambda: RandomForestRegressor(n_estimators=400,min_samples_leaf=5,max_features=0.7,n_jobs=-1,random_state=7),
      'extra': lambda: ExtraTreesRegressor(n_estimators=400,min_samples_leaf=5,max_features=0.8,n_jobs=-1,random_state=7)
    }
    for mname,maker in models.items():
      for sname,cols in feature_sets.items():
        pred=np.full(len(df),np.nan); fold=[]
        for k,(tr,te) in enumerate(splits):
            Xtr=df.iloc[tr][cols].values; Xte=df.iloc[te][cols].values
            model=maker(); model.fit(Xtr,y[tr]); p=model.predict(Xte); pred[te]=p
            fold.append(r2_score(y[te],p))
        results.append({'model':mname,'features':sname,'n_features':len(cols),'r2_oof':float(r2_score(y,pred)),'rmse_oof':float(mean_squared_error(y,pred)**0.5),'fold_r2_mean':float(np.mean(fold)),'fold_r2_median':float(np.median(fold)),'fold_r2':fold})
    # PC1 current gene, fitted inside each fold, paired to geometry trajectory
    traj=feature_sets['trajectory_geom']; cur=[c for c in df.columns if c.startswith('cur_')]
    for mname,maker in models.items():
        pred=np.full(len(df),np.nan); fold=[]
        for tr,te in splits:
            pca=PCA(n_components=1).fit(df.iloc[tr][cur].values)
            Xtr=np.column_stack([df.iloc[tr][traj].values,pca.transform(df.iloc[tr][cur].values)])
            Xte=np.column_stack([df.iloc[te][traj].values,pca.transform(df.iloc[te][cur].values)])
            model=maker(); model.fit(Xtr,y[tr]); pp=model.predict(Xte); pred[te]=pp; fold.append(r2_score(y[te],pp))
        results.append({'model':mname,'features':'trajectory_geom+current_gene_PC1','n_features':len(traj)+1,'r2_oof':float(r2_score(y,pred)),'rmse_oof':float(mean_squared_error(y,pred)**0.5),'fold_r2_mean':float(np.mean(fold)),'fold_r2_median':float(np.median(fold)),'fold_r2':fold})
    return pd.DataFrame(results)

def main():
    df,genes=build_dataset()
    traj=['g96_logvolume','g96_x','g96_y','g96_z','g96_neighbors','g120_logvolume','g120_x','g120_y','g120_z','g120_neighbors','d_x','d_y','d_z','logvol_ratio_96_120']
    cur=[f'cur_{g}' for g in genes]; old=[f'old_{g}' for g in genes]
    sets={'current_geom':['g120_logvolume','g120_x','g120_y','g120_z','g120_neighbors'], 'trajectory_geom':traj, 'trajectory_geom+current_genes':traj+cur, 'trajectory_geom+current+old_genes':traj+cur+old}
    res=grouped_oof(df,sets)
    df.to_csv(OUT/'fm1_grouped_dataset.csv',index=False)
    res.to_csv(OUT/'fm1_grouped_results.csv',index=False)
    summary={'n_cells':len(df),'n_ancestor_groups':int(df.ancestor96.nunique()),'n_genes':len(genes),'target_mean':float(df.future_growth.mean()),'target_sd':float(df.future_growth.std()),'results':res.sort_values(['model','r2_oof'],ascending=[True,False]).to_dict(orient='records')}
    (OUT/'fm1_grouped_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
