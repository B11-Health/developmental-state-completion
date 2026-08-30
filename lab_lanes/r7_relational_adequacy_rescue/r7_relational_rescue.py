import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error

BASE = Path(__file__).parent
ROOT = BASE.parent.parent
OUT = BASE / "results"
OUT.mkdir(exist_ok=True)
SEED = 20260830
FRAMES = [15, 20, 23, 24, 25, 40]
KS = [3, 5, 10]
EPS = 1e-12

MODELS = {
    "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "random_forest": RandomForestRegressor(
        n_estimators=300, min_samples_leaf=4, max_features=0.8,
        random_state=SEED, n_jobs=-1
    ),
    "extra_trees": ExtraTreesRegressor(
        n_estimators=300, min_samples_leaf=3, max_features=0.9,
        random_state=SEED, n_jobs=-1
    ),
}


def _rank01(s):
    return pd.Series(s).rank(method="average", pct=True).to_numpy(float)


def _safe_tangent(vec, unit):
    mag2 = np.sum(vec * vec, axis=1)
    rad = np.sum(vec * unit, axis=1)
    return np.sqrt(np.maximum(0.0, mag2 - rad * rad))


def load_drosophila():
    src = ROOT / "lab_lanes" / "r5_drosophila_trajectory" / "source_data"
    files = sorted(src.glob("dro_centroids_*.csv"))
    d = pd.concat([pd.read_csv(f, dtype={"sequence": str}) for f in files], ignore_index=True)
    d["sequence"] = d.sequence.str.zfill(2)
    d = d.rename(columns={"x_um": "x", "y_um": "y", "z_um": "z"})
    d["organism"] = "Drosophila"
    eligible = {}
    for seq, g in d.groupby("sequence"):
        sets = [set(g[g.frame == t].label) for t in FRAMES]
        eligible[seq] = set.intersection(*sets)
    return d, ["x", "y", "z"], eligible


def load_tribolium():
    src = ROOT / "lab_lanes" / "r6_tribolium_trajectory" / "source_data"
    d = pd.read_csv(src / "tric_selected_centroids.csv", dtype={"sequence": str})
    d["sequence"] = d.sequence.str.zfill(2)
    d = d.rename(columns={"x_px": "x", "y_px": "y"})
    d["organism"] = "Tribolium"
    eligible = {}
    for seq in ("01", "02"):
        keep = set()
        for line in (src / f"{seq}_man_track.txt").read_text(encoding="utf-8").splitlines():
            lab, st, en, par = map(int, line.split())
            if st <= 15 and en >= 40:
                keep.add(lab)
        eligible[seq] = keep
    return d, ["x", "y"], eligible


def frame_map(g, coords):
    out = {}
    for t in FRAMES:
        q = g[g.frame == t].copy()
        out[t] = {
            int(r.label): (np.array([float(getattr(r, c)) for c in coords], dtype=float), float(r.voxel_count))
            for _, r in q.iterrows()
        }
    return out


def sequence_features(g, coords, focal_labels):
    dim = len(coords)
    fm = frame_map(g, coords)
    anchor_labels = sorted(fm[25])
    anchor_pos_raw = np.vstack([fm[25][lab][0] for lab in anchor_labels])
    anchor_logv = np.array([np.log1p(fm[25][lab][1]) for lab in anchor_labels], dtype=float)
    center25 = anchor_pos_raw.mean(axis=0)
    centered = anchor_pos_raw - center25
    radii_raw = np.linalg.norm(centered, axis=1)
    scale = float(np.sqrt(np.mean(radii_raw ** 2)))
    if not np.isfinite(scale) or scale <= 0:
        scale = 1.0
    pos = centered / scale
    radii = np.linalg.norm(pos, axis=1)
    radial_rank = _rank01(radii)
    vol_rank = _rank01(anchor_logv)
    idx = {lab: i for i, lab in enumerate(anchor_labels)}

    # Pairwise anchor geometry, all current released gold labels.
    dif = pos[:, None, :] - pos[None, :, :]
    dist = np.sqrt(np.sum(dif * dif, axis=2))
    np.fill_diagonal(dist, np.inf)
    order = np.argsort(dist, axis=1)

    # Current-state acquisition translation/acceleration estimated only from labels continuous across needed past frames.
    common24 = sorted(set(fm[24]) & set(fm[25]))
    c24 = np.vstack([fm[24][lab][0] for lab in common24]).mean(axis=0)
    c25_common = np.vstack([fm[25][lab][0] for lab in common24]).mean(axis=0)
    centroid_v = (c25_common - c24) / scale
    common23 = sorted(set(fm[23]) & set(fm[24]) & set(fm[25]))
    c23a = np.vstack([fm[23][lab][0] for lab in common23]).mean(axis=0)
    c24a = np.vstack([fm[24][lab][0] for lab in common23]).mean(axis=0)
    c25a = np.vstack([fm[25][lab][0] for lab in common23]).mean(axis=0)
    centroid_a = (c25a - 2 * c24a + c23a) / scale

    # Neighbor recent velocities keyed by current label, relative to acquisition centroid translation.
    recent_v = {}
    for lab in set(fm[24]) & set(fm[25]):
        recent_v[lab] = ((fm[25][lab][0] - fm[24][lab][0]) / scale) - centroid_v

    recs = []
    for lab in sorted(focal_labels):
        if not all(lab in fm[t] for t in FRAMES):
            continue
        i = idx[lab]
        p25 = fm[25][lab][0]
        p24 = fm[24][lab][0]
        p23 = fm[23][lab][0]
        p20 = fm[20][lab][0]
        p15 = fm[15][lab][0]
        p40 = fm[40][lab][0]
        u = pos[i] / (radii[i] + EPS)

        v_recent_abs = (p25 - p24) / scale
        v_recent = v_recent_abs - centroid_v
        a_recent_abs = (p25 - 2 * p24 + p23) / scale
        a_recent = a_recent_abs - centroid_a
        recent_speed = float(np.linalg.norm(v_recent))
        recent_rad = float(np.dot(v_recent, u))
        recent_tan = float(np.sqrt(max(0.0, recent_speed ** 2 - recent_rad ** 2)))
        acc_mag = float(np.linalg.norm(a_recent))
        acc_rad = float(np.dot(a_recent, u))
        acc_tan = float(np.sqrt(max(0.0, acc_mag ** 2 - acc_rad ** 2)))

        # Older history relative to older acquisition-centroid displacement over the 15->20 interval.
        common_old = sorted(set(fm[15]) & set(fm[20]))
        c15 = np.vstack([fm[15][x][0] for x in common_old]).mean(axis=0)
        c20 = np.vstack([fm[20][x][0] for x in common_old]).mean(axis=0)
        centroid_old_v = ((c20 - c15) / scale) / 5.0
        old_v = ((p20 - p15) / scale) / 5.0 - centroid_old_v
        old_speed = float(np.linalg.norm(old_v))
        old_rad = float(np.dot(old_v, u))
        old_tan = float(np.sqrt(max(0.0, old_speed ** 2 - old_rad ** 2)))

        future = ((p40 - p25) / scale) / 15.0
        y_speed = float(np.linalg.norm(future))
        y_rad = float(np.dot(future, u))

        row = {
            "label": int(lab),
            "radius_norm": float(radii[i]),
            "radius_rank": float(radial_rank[i]),
            "log_volume": float(anchor_logv[i]),
            "volume_rank": float(vol_rank[i]),
            "recent_speed_relcentroid": recent_speed,
            "recent_radial_relcentroid": recent_rad,
            "recent_tangential_relcentroid": recent_tan,
            "recent_speed_abs": float(np.linalg.norm(v_recent_abs)),
            "accel_mag_relcentroid": acc_mag,
            "accel_radial_relcentroid": acc_rad,
            "accel_tangential_relcentroid": acc_tan,
            "recent_log_volume_change": float(np.log1p(fm[25][lab][1]) - np.log1p(fm[24][lab][1])),
            "old_speed_relcentroid": old_speed,
            "old_radial_relcentroid": old_rad,
            "old_tangential_relcentroid": old_tan,
            "old_log_volume_change_rate": float((np.log1p(fm[20][lab][1]) - np.log1p(fm[15][lab][1])) / 5.0),
            "future_radial_velocity": y_rad,
            "future_speed": y_speed,
        }

        # kNN distances, density, local shape and volume summaries.
        for k in KS:
            nn_idx = order[i, :min(k, len(anchor_labels) - 1)]
            nn_d = dist[i, nn_idx]
            kk = len(nn_idx)
            row[f"knn{k}_mean_distance"] = float(np.mean(nn_d))
            row[f"knn{k}_max_distance"] = float(np.max(nn_d))
            row[f"knn{k}_distance_sd"] = float(np.std(nn_d))
            row[f"knn{k}_log_density"] = float(np.log((kk + EPS) / (np.max(nn_d) ** dim + EPS)))
            lv = anchor_logv[nn_idx]
            row[f"knn{k}_neighbor_logvol_mean"] = float(np.mean(lv))
            row[f"knn{k}_neighbor_logvol_sd"] = float(np.std(lv))
            row[f"knn{k}_focal_minus_neighbor_logvol"] = float(anchor_logv[i] - np.mean(lv))
            offs = pos[nn_idx] - pos[i]
            cov = (offs.T @ offs) / max(1, kk)
            eig = np.sort(np.linalg.eigvalsh(cov))[::-1]
            es = float(eig.sum()) + EPS
            for j in range(dim):
                row[f"knn{k}_shape_eigfrac{j+1}"] = float(eig[j] / es)

        # Neighbor velocity consensus over the nearest 10 current neighbors that have 24->25 continuity.
        vel_neighbors = []
        vel_neighbor_labs = []
        for j in order[i]:
            nlab = anchor_labels[int(j)]
            if nlab in recent_v:
                vel_neighbors.append(recent_v[nlab])
                vel_neighbor_labs.append(nlab)
            if len(vel_neighbors) >= 10:
                break
        if vel_neighbors:
            vv = np.vstack(vel_neighbors)
            vmean = vv.mean(axis=0)
            speeds = np.linalg.norm(vv, axis=1)
            consensus_mag = float(np.linalg.norm(vmean))
            row["neighbor_velocity_mean_speed"] = float(np.mean(speeds))
            row["neighbor_velocity_speed_sd"] = float(np.std(speeds))
            row["neighbor_velocity_consensus_mag"] = consensus_mag
            row["focal_minus_neighbor_consensus_speed"] = float(np.linalg.norm(v_recent - vmean))
            if recent_speed > EPS and consensus_mag > EPS:
                row["focal_neighbor_velocity_alignment"] = float(np.dot(v_recent, vmean) / (recent_speed * consensus_mag))
            else:
                row["focal_neighbor_velocity_alignment"] = 0.0
            nrad = []
            for nlab, nv in zip(vel_neighbor_labs, vel_neighbors):
                ni = idx[nlab]
                nu = pos[ni] / (radii[ni] + EPS)
                nrad.append(float(np.dot(nv, nu)))
            row["neighbor_radial_velocity_mean"] = float(np.mean(nrad))
            row["neighbor_radial_velocity_sd"] = float(np.std(nrad))
        else:
            for name in [
                "neighbor_velocity_mean_speed", "neighbor_velocity_speed_sd",
                "neighbor_velocity_consensus_mag", "focal_minus_neighbor_consensus_speed",
                "focal_neighbor_velocity_alignment", "neighbor_radial_velocity_mean",
                "neighbor_radial_velocity_sd"
            ]:
                row[name] = 0.0
        recs.append(row)
    return pd.DataFrame(recs), {"anchor_n": len(anchor_labels), "scale": scale}


def build_dataset(name):
    if name == "Drosophila":
        d, coords, eligible = load_drosophila()
    elif name == "Tribolium":
        d, coords, eligible = load_tribolium()
    else:
        raise ValueError(name)
    pieces = []
    seqmeta = {}
    for seq in sorted(eligible):
        q, meta = sequence_features(d[d.sequence == seq], coords, eligible[seq])
        q["sequence"] = seq
        q["organism"] = name
        pieces.append(q)
        seqmeta[seq] = meta
    return pd.concat(pieces, ignore_index=True), seqmeta


def fit_fold(model, Xtr, ytr, Xte):
    m = clone(model)
    m.fit(Xtr, ytr)
    return m.predict(Xte)


def score(y, pred):
    return {
        "r2": float(r2_score(y, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y, pred))),
        "mae": float(np.mean(np.abs(np.asarray(y) - np.asarray(pred))))
    }


def main():
    feature_schema = {}
    all_adequacy = []
    all_history = []
    all_perm = []
    dataset_meta = {}

    for organism in ["Drosophila", "Tribolium"]:
        D, seqmeta = build_dataset(organism)
        dataset_meta[organism] = {
            "n_total": int(len(D)),
            "sequence_counts": {str(k): int(v) for k, v in D.sequence.value_counts().sort_index().items()},
            "sequence_present_meta": seqmeta,
        }
        outcome_cols = ["future_radial_velocity", "future_speed"]
        history_cols = [
            "old_speed_relcentroid", "old_radial_relcentroid",
            "old_tangential_relcentroid", "old_log_volume_change_rate"
        ]
        id_cols = {"label", "sequence", "organism"}
        feature_cols = [c for c in D.columns if c not in id_cols and c not in outcome_cols and c not in history_cols]
        # Deterministic fixed feature order.
        feature_cols = sorted(feature_cols)
        feature_schema[organism] = {"present": feature_cols, "history": history_cols, "outcomes": outcome_cols}
        D.to_csv(OUT / f"{organism.lower()}_analysis_table.csv", index=False)

        # Gate 1: present-only S_R, outcome by outcome.
        fold_rows = []
        decisions = []
        for outcome in outcome_cols:
            y = D[outcome].to_numpy(float)
            X = D[feature_cols].to_numpy(float)
            groups = D.sequence.to_numpy()
            for test_seq in sorted(D.sequence.unique()):
                tr = groups != test_seq
                te = groups == test_seq
                mu = float(np.mean(y[tr]))
                naive_pred = np.full(np.sum(te), mu)
                ns = score(y[te], naive_pred)
                fold_rows.append({
                    "organism": organism, "outcome": outcome, "estimator": "naive_train_mean",
                    "test_sequence": test_seq, **ns, "n_train": int(np.sum(tr)), "n_test": int(np.sum(te))
                })
                for est, model in MODELS.items():
                    pred = fit_fold(model, X[tr], y[tr], X[te])
                    ss = score(y[te], pred)
                    fold_rows.append({
                        "organism": organism, "outcome": outcome, "estimator": est,
                        "test_sequence": test_seq, **ss, "n_train": int(np.sum(tr)), "n_test": int(np.sum(te))
                    })
            F = pd.DataFrame(fold_rows)
            this = F[(F.organism == organism) & (F.outcome == outcome)]
            naive = this[this.estimator == "naive_train_mean"].set_index("test_sequence")
            passers = []
            per_est = {}
            for est in MODELS:
                q = this[this.estimator == est].set_index("test_sequence")
                fold_pass = {}
                for seq in sorted(q.index):
                    ok = bool((q.loc[seq, "r2"] > 0.0) and (q.loc[seq, "rmse"] < naive.loc[seq, "rmse"]))
                    fold_pass[str(seq)] = ok
                per_est[est] = fold_pass
                if all(fold_pass.values()):
                    passers.append(est)
            gate1 = len(passers) >= 2
            decisions.append({
                "organism": organism, "outcome": outcome,
                "gate1_absolute_adequacy_pass": gate1,
                "n_estimators_passing_both_folds": len(passers),
                "estimators_passing_both_folds": passers,
                "per_estimator_fold_pass": per_est,
            })
        F = pd.DataFrame(fold_rows)
        F.to_csv(OUT / f"{organism.lower()}_adequacy_fold_metrics.csv", index=False)
        all_adequacy.extend(decisions)

        # Gate 2 only for tasks that passed Gate 1.
        for dec in decisions:
            outcome = dec["outcome"]
            if not dec["gate1_absolute_adequacy_pass"]:
                continue
            y = D[outcome].to_numpy(float)
            Xs = D[feature_cols].to_numpy(float)
            H = D[history_cols].to_numpy(float)
            Xh = np.c_[Xs, H]
            groups = D.sequence.to_numpy()
            hrows = []
            for est, model in MODELS.items():
                for test_seq in sorted(D.sequence.unique()):
                    tr = groups != test_seq
                    te = groups == test_seq
                    p_s = fit_fold(model, Xs[tr], y[tr], Xs[te])
                    p_h = fit_fold(model, Xh[tr], y[tr], Xh[te])
                    s0 = score(y[te], p_s)
                    s1 = score(y[te], p_h)
                    hrows.append({
                        "organism": organism, "outcome": outcome, "estimator": est,
                        "test_sequence": test_seq,
                        "r2_S": s0["r2"], "r2_S_plus_H": s1["r2"],
                        "delta_r2": s1["r2"] - s0["r2"],
                        "rmse_S": s0["rmse"], "rmse_S_plus_H": s1["rmse"],
                        "delta_rmse": s0["rmse"] - s1["rmse"],
                    })
            HF = pd.DataFrame(hrows)
            all_history.extend(HF.to_dict(orient="records"))
            pass_est = []
            for est in MODELS:
                q = HF[HF.estimator == est]
                if bool((q.delta_r2 > 0).all()) and float(q.delta_r2.mean()) >= 0.02:
                    pass_est.append(est)
            gate2 = len(pass_est) >= 2
            dec["gate2_history_stability_pass"] = gate2
            dec["gate2_estimators"] = pass_est
            dec["gate2_n_estimators"] = len(pass_est)

            # Gate 3: only after Gate 2, deterministic H permutation in the training acquisition.
            if gate2:
                rng = np.random.default_rng(SEED)
                for est in pass_est:
                    model = MODELS[est]
                    for test_seq in sorted(D.sequence.unique()):
                        tr = groups != test_seq
                        te = groups == test_seq
                        p_s = fit_fold(model, Xs[tr], y[tr], Xs[te])
                        obs = fit_fold(model, Xh[tr], y[tr], Xh[te])
                        obs_delta = score(y[te], obs)["r2"] - score(y[te], p_s)["r2"]
                        null = []
                        for b in range(200):
                            perm = rng.permutation(np.sum(tr))
                            xperm = np.c_[Xs[tr], H[tr][perm]]
                            pp = fit_fold(model, xperm, y[tr], Xh[te])
                            null.append(score(y[te], pp)["r2"] - score(y[te], p_s)["r2"])
                        null = np.asarray(null)
                        p_ge = float((1 + np.sum(null >= obs_delta)) / (len(null) + 1))
                        all_perm.append({
                            "organism": organism, "outcome": outcome, "estimator": est,
                            "test_sequence": test_seq, "observed_delta_r2": float(obs_delta),
                            "null_mean_delta_r2": float(np.mean(null)),
                            "null_q95_delta_r2": float(np.quantile(null, 0.95)),
                            "permutation_p_ge": p_ge, "n_permutations": 200,
                        })
                dec["gate3_permutation_run"] = True
            else:
                dec["gate3_permutation_run"] = False

    A = pd.DataFrame(all_adequacy)
    A.to_json(OUT / "adequacy_decisions.json", orient="records", indent=2)
    if all_history:
        pd.DataFrame(all_history).to_csv(OUT / "history_fold_metrics.csv", index=False)
    else:
        pd.DataFrame(columns=["organism","outcome","estimator","test_sequence","r2_S","r2_S_plus_H","delta_r2","rmse_S","rmse_S_plus_H","delta_rmse"]).to_csv(OUT / "history_fold_metrics.csv", index=False)
    if all_perm:
        pd.DataFrame(all_perm).to_csv(OUT / "permutation_results.csv", index=False)
    else:
        pd.DataFrame(columns=["organism","outcome","estimator","test_sequence","observed_delta_r2","null_mean_delta_r2","null_q95_delta_r2","permutation_p_ge","n_permutations"]).to_csv(OUT / "permutation_results.csv", index=False)

    summary = {
        "seed": SEED,
        "frames": FRAMES,
        "gate_order": ["absolute_present_adequacy", "history_increment", "permutation_sensitivity"],
        "dataset_meta": dataset_meta,
        "feature_schema": feature_schema,
        "adequacy_decisions": all_adequacy,
        "history_rows_written": len(all_history),
        "permutation_rows_written": len(all_perm),
    }
    (OUT / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
