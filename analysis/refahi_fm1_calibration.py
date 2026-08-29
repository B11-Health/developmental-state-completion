import argparse
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from refahi_fm1_state_completion import build_dataset

def fixed_oof(X, y, groups, splits, alpha=10.0):
    pred = np.empty(len(y))
    for tr, te in splits:
        m = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        m.fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
    return pred

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream', default='refahi_diag')
    ap.add_argument('--reps', type=int, default=250)
    ap.add_argument('--bootstrap', type=int, default=5000)
    args = ap.parse_args()
    _, _, S, X, y, groups = build_dataset(Path(args.upstream))
    H = X[:, S.shape[1]:]
    splits = list(GroupKFold(5).split(S, y, groups))
    pc = fixed_oof(S, y, groups, splits)
    ph = fixed_oof(X, y, groups, splits)
    obs = r2_score(y, ph) - r2_score(y, pc)
    print('observed_current_R2', round(r2_score(y,pc),6))
    print('observed_current_plus_history_R2', round(r2_score(y,ph),6))
    print('observed_delta_history_given_current', round(obs,6))

    rng = np.random.default_rng(20260829)
    Z = (S-S.mean(0))/(S.std(0)+1e-9)
    ZH = (H-H.mean(0))/(H.std(0)+1e-9)
    beta = rng.normal(size=Z.shape[1]); beta /= np.linalg.norm(beta)
    signal = Z @ beta; signal = (signal-signal.mean())/signal.std()
    residual_history = ZH[:,0] - Ridge(alpha=1).fit(Z, ZH[:,0]).predict(Z)
    residual_history = (residual_history-residual_history.mean())/(residual_history.std()+1e-9)
    sigma = np.sqrt((1-0.30)/0.30)

    def simulate(gamma):
        vals=[]
        for _ in range(args.reps):
            ys = signal + gamma*residual_history + rng.normal(0,sigma,len(y))
            a = fixed_oof(S, ys, groups, splits)
            b = fixed_oof(X, ys, groups, splits)
            vals.append(r2_score(ys,b)-r2_score(ys,a))
        return np.array(vals)

    null = simulate(0.0); alt = simulate(0.35); q95=np.quantile(null,0.95)
    print('known_markov_mean_delta', round(float(null.mean()),6))
    print('known_markov_q05_q50_q95', np.round(np.quantile(null,[.05,.5,.95]),6).tolist())
    print('known_nonmarkov_mean_delta_gamma035', round(float(alt.mean()),6))
    print('known_nonmarkov_q05_q50_q95', np.round(np.quantile(alt,[.05,.5,.95]),6).tolist())
    print('known_nonmarkov_power_at_markov95', round(float(np.mean(alt>q95)),6))

    unique=np.unique(groups); boot=[]
    for _ in range(args.bootstrap):
        chosen=rng.choice(unique,len(unique),replace=True)
        idx=np.concatenate([np.where(groups==g)[0] for g in chosen])
        boot.append(r2_score(y[idx],ph[idx])-r2_score(y[idx],pc[idx]))
    print('group_bootstrap_delta_median_q025_q975', np.round(np.quantile(boot,[.5,.025,.975]),6).tolist())

if __name__ == '__main__':
    main()
