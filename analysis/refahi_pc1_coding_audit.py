#!/usr/bin/env python3
import importlib.util, json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr, pearsonr
from sklearn.decomposition import PCA

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rep',REPO/'analysis/refahi_state_completion_replication.py')
rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
OUT=REPO/'results'; OUT.mkdir(exist_ok=True)

def margin(z):
    d=np.abs(z[:,None]-z[None,:]); d[d==0]=np.inf; return float(d.min())
def stdmargin(z): return margin(z)/float(np.std(z))

def main():
    dt=rep.load_dtissue(); df,genes=rep.build_window(dt,96,120,132,True)
    cur=[f'cur_g_{g}' for g in genes]; X=df[cur].to_numpy(float)
    p=PCA(n_components=1).fit(X); z=p.transform(X)[:,0]
    patterns={}
    for i,row in enumerate(X.astype(int)):
        patterns.setdefault(tuple(row.tolist()),[]).append(i)
    state_rows=[]
    for n,(pat,idx) in enumerate(sorted(patterns.items(),key=lambda kv:-len(kv[1]))):
        vals=z[idx]
        state_rows.append({'state_id':n,'count':len(idx),'pc1_mean':float(vals.mean()),'pc1_sd':float(vals.std()),'target_mean':float(df.iloc[idx].target.mean()),'genes_on':[g for g,v in zip(genes,pat) if v==1]})
    pcs=sorted(r['pc1_mean'] for r in state_rows); mind=min(abs(a-b) for a,b in zip(pcs[:-1],pcs[1:])); load=sorted(zip(genes,p.components_[0]),key=lambda x:abs(x[1]),reverse=True)
    state_out={'n_cells':len(df),'n_states':len(state_rows),'pc1_explained_variance':float(p.explained_variance_ratio_[0]),'n_unique_pc1_state_means':len(set(round(r['pc1_mean'],12) for r in state_rows)),'min_state_pc1_separation':float(mind),'top_loadings':[{'gene':g,'loading':float(v)} for g,v in load[:12]],'states':state_rows}
    (OUT/'refahi_pc1_state_code_audit.json').write_text(json.dumps(state_out,indent=2))

    pats,inv=np.unique(X,axis=0,return_inverse=True); means=np.array([df.target.to_numpy()[inv==i].mean() for i in range(len(pats))]); counts=np.array([(inv==i).sum() for i in range(len(pats))]); pc=pats@p.components_[0]
    pc_s=float(spearmanr(pc,means).statistic); pc_m=margin(pc); pc_sm=stdmargin(pc)
    rng=np.random.default_rng(20260829); N=10000; margins=[]; sm=[]; sp=[]
    for _ in range(N):
        w=rng.normal(size=X.shape[1]); w/=np.linalg.norm(w); zz=pats@w; margins.append(margin(zz)); sm.append(stdmargin(zz)); sp.append(abs(float(spearmanr(zz,means).statistic)))
    et=json.loads((OUT/'refahi_random_projection_extra_trees.json').read_text()); rng=np.random.default_rng(20260829); perf=[]
    for row in et['rows']:
        w=rng.normal(size=X.shape[1]); w/=np.linalg.norm(w); zz=pats@w; perf.append((row['r2'],margin(zz),abs(float(spearmanr(zz,means).statistic))))
    perf=np.array(perf)
    robust_out={'n_states':len(pats),'pc1':{'explained_variance':float(p.explained_variance_ratio_[0]),'min_margin':pc_m,'standardized_min_margin':pc_sm,'spearman_state_mean_target':pc_s,'abs_spearman':abs(pc_s)},'random_10000':{'margin_median':float(np.median(margins)),'margin_q95':float(np.quantile(margins,.95)),'pc1_margin_percentile':float(np.mean(np.array(margins)<=pc_m)),'standardized_margin_median':float(np.median(sm)),'pc1_standardized_margin_percentile':float(np.mean(np.array(sm)<=pc_sm)),'abs_spearman_median':float(np.median(sp)),'pc1_abs_spearman_percentile':float(np.mean(np.array(sp)<=abs(pc_s)))},'extra_trees_random30_correlations':{'r2_vs_min_margin_pearson':float(pearsonr(perf[:,0],perf[:,1]).statistic),'r2_vs_abs_state_target_spearman_pearson':float(pearsonr(perf[:,0],perf[:,2]).statistic)},'state_target_means':means.tolist(),'state_counts':counts.tolist()}
    (OUT/'refahi_pc1_robustness_alignment_audit.json').write_text(json.dumps(robust_out,indent=2))
    print(json.dumps({'state_code':state_out,'robustness':robust_out},indent=2))
if __name__=='__main__': main()
