import argparse, io, math, pickle, re, subprocess
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class DummyDTissue:
    pass

class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'atlasviewer.dtissue' and name == 'DTissue':
            return DummyDTissue
        if module == 'copy_reg':
            module = 'copyreg'
        if module == '__builtin__':
            module = 'builtins'
        return super().find_class(module, name)

def load_dtissue(repo):
    raw = subprocess.check_output(['git', '-C', str(repo), 'show', 'HEAD:stateAnalysis/FM1_dtissue.tis'])
    return CompatUnpickler(io.BytesIO(raw), encoding='latin1').load()

def gene_matrix(repo, hour):
    rows = (repo / f'data/geneExpression/t_{hour}h.txt').read_text().splitlines()
    names = rows[0].split()[1:]
    data = {int(r.split()[0]): np.array(r.split()[1:], dtype=float) for r in rows[1:]}
    return names, data

GEOM_RE = re.compile(r'cid:\s*(\d+), volume:\s*([^,]+), center:\s*\[([^\]]+)\]')
def geometry(repo, hour):
    out = {}
    fn = repo / f'data/FM1/tv/{hour}h_segmented_tvformat_volume_position.txt'
    for line in fn.read_text().splitlines():
        m = GEOM_RE.search(line)
        if m:
            out[int(m.group(1))] = (float(m.group(2)), np.array(m.group(3).split(), dtype=float))
    return out

def build_dataset(repo, return_ids=False):
    obj = load_dtissue(repo)
    dt, tps = obj.dtissue, obj.timePoints
    idx = {t:i for i,t in enumerate(tps)}
    genes, g96 = gene_matrix(repo, 96)
    _, g120 = gene_matrix(repo, 120)
    z96, z120 = geometry(repo, 96), geometry(repo, 120)

    def ancestor(cid):
        c = cid
        for k in range(idx['120h'], idx['96h'], -1):
            c = dt[tps[k]]['mother'].get(c, -1)
            if c in (-1, None):
                return None
        return c

    def descendants(cid):
        cur = [cid]
        for k in range(idx['120h'], idx['132h']):
            dmap = dt[tps[k]].get('daughters', {})
            cur = [x for c in cur for x in dmap.get(c, [])]
            if not cur:
                break
        return cur

    geom_now, current, full, y, groups, cell_ids = [], [], [], [], [], []
    for cid in sorted(set(g120) & set(z120)):
        a = ancestor(cid)
        if a is None or a not in g96 or a not in z96:
            continue
        ds = descendants(cid)
        vf = sum(dt['132h']['volumes'].get(d, 0.0) for d in ds)
        if not ds or vf <= 0 or z120[cid][0] <= 0:
            continue
        cur_geom = np.r_[math.log(z120[cid][0]), z120[cid][1]]
        hist_geom = np.r_[math.log(z96[a][0]), z96[a][1]]
        geom_now.append(cur_geom)
        current.append(np.r_[cur_geom, g120[cid]])
        full.append(np.r_[cur_geom, g120[cid], hist_geom, g96[a]])
        y.append(math.log(vf / z120[cid][0]))
        groups.append(a)
        cell_ids.append(cid)
    base = (genes, np.array(geom_now), np.array(current), np.array(full), np.array(y), np.array(groups))
    return base + (np.array(cell_ids),) if return_ids else base

def ridge_oof(X, y, groups, splits):
    pred = np.full(len(y), np.nan)
    chosen = []
    for tr, te in splits:
        grid = GridSearchCV(
            Pipeline([('scale', StandardScaler()), ('ridge', Ridge())]),
            {'ridge__alpha':[0.1, 1, 10, 100]},
            cv=GroupKFold(3), scoring='r2', n_jobs=-1)
        grid.fit(X[tr], y[tr], groups=groups[tr])
        pred[te] = grid.predict(X[te])
        chosen.append(grid.best_params_['ridge__alpha'])
    return pred, chosen

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream', default='../refahi_diag')
    args = ap.parse_args()
    repo = Path(args.upstream)
    commit = subprocess.check_output(['git','-C',str(repo),'rev-parse','--short','HEAD'], text=True).strip()
    genes, Xg, Xs, Xh, y, groups = build_dataset(repo)
    splits = list(GroupKFold(5).split(Xg, y, groups))
    print('upstream_commit', commit)
    print('eligible_cells', len(y), 'ancestor_groups', len(np.unique(groups)), 'genes', len(genes))
    results = {}
    for name, X in [('geometry',Xg), ('current',Xs), ('current_plus_history',Xh)]:
        pred, alphas = ridge_oof(X, y, groups, splits)
        results[name] = r2_score(y, pred)
        print(name, 'ridge_oof_R2', round(results[name],6), 'MAE', round(mean_absolute_error(y,pred),6), 'alphas', alphas)
    print('ridge_delta_current_minus_geometry', round(results['current']-results['geometry'],6))
    print('ridge_delta_history_given_current', round(results['current_plus_history']-results['current'],6))
    for name, X in [('geometry',Xg), ('current',Xs), ('current_plus_history',Xh)]:
        pred = np.full(len(y), np.nan)
        for tr, te in splits:
            model = RandomForestRegressor(n_estimators=500, min_samples_leaf=8, max_features=0.7, random_state=17, n_jobs=-1)
            model.fit(X[tr], y[tr]); pred[te] = model.predict(X[te])
        print(name, 'rf_oof_R2', round(r2_score(y,pred),6), 'MAE', round(mean_absolute_error(y,pred),6))

if __name__ == '__main__':
    main()
