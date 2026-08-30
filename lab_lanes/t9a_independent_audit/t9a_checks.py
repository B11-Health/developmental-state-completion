import numpy as np


def mse(pred, y):
    pred = np.asarray(pred, dtype=float)
    y = np.asarray(y, dtype=float)
    return float(np.mean((y - pred) ** 2))


def inner(u, v):
    return float(np.mean(np.asarray(u, dtype=float) * np.asarray(v, dtype=float)))


def margin(y, p, b, z, a):
    ya = np.asarray(y, dtype=float) + a * np.asarray(z, dtype=float)
    return mse(b, ya) - mse(p, ya)


def r2(y, p):
    y = np.asarray(y, dtype=float)
    sst = float(np.mean((y - y.mean()) ** 2))
    if sst == 0.0:
        return None
    return 1.0 - mse(p, y) / sst


# 1. Independent random verification of T9.1 with scalar and vector baselines.
rng = np.random.default_rng(20260830)
max_identity_err = 0.0
for n in (2, 7, 31):
    for vector_baseline in (False, True):
        y = rng.normal(size=n)
        p = rng.normal(size=n)
        b = rng.normal(size=n) if vector_baseline else float(rng.normal())
        z = rng.normal(size=n)
        g0 = margin(y, p, b, z, 0.0)
        for a in (-3.0, -0.25, 0.0, 0.5, 4.0):
            rhs = g0 + 2.0 * a * inner(z, p - np.asarray(b))
            max_identity_err = max(max_identity_err, abs(margin(y, p, b, z, a) - rhs))
assert max_identity_err < 1e-11

# 2. Independent exact decomposition check with vector-valued moving baseline.
y = rng.normal(size=19); p = rng.normal(size=19); b = rng.normal(size=19); z = rng.normal(size=19)
p_a = p + rng.normal(scale=0.2, size=19); b_a = b + rng.normal(scale=0.1, size=19); a = 0.8
ya = y + a*z
g0 = margin(y,p,b,z,0.0)
align = 2*a*inner(z,p-b)
B = mse(b_a,ya)-mse(b,ya)
R = mse(p,ya)-mse(p_a,ya)
decomp_err = abs((mse(b_a,ya)-mse(p_a,ya)) - (g0+align+B+R))
assert decomp_err < 1e-11

# 3. Counterexample to the written R2 claim: centered z and positive alignment do NOT imply sign invariance.
y_r2 = np.array([-1.0, 1.0])
z_r2 = np.array([-1.0, 1.0])  # centered
p_r2 = 3.0*y_r2
b_r2 = np.zeros(2)
c_r2 = inner(z_r2, p_r2-b_r2)
g_r2_0 = margin(y_r2,p_r2,b_r2,z_r2,0.0)
g_r2_1 = margin(y_r2,p_r2,b_r2,z_r2,1.0)
r2_0 = r2(y_r2,p_r2)
r2_1 = r2(y_r2+z_r2,p_r2)
assert abs(z_r2.mean()) < 1e-15 and c_r2 > 0 and g_r2_0 < 0 < g_r2_1 and r2_0 < 0 < r2_1

# 4. Even under exact orthogonality, R2 can become undefined if injected target variance vanishes.
y_deg = np.array([-1.0,-1.0,1.0,1.0])
z_deg = -y_deg
p_deg = np.array([1.0,-1.0,1.0,-1.0])
b_deg = np.zeros(4)
c_deg = inner(z_deg,p_deg-b_deg)
g_deg_0 = margin(y_deg,p_deg,b_deg,z_deg,0.0)
g_deg_1 = margin(y_deg,p_deg,b_deg,z_deg,1.0)
r2_deg_1 = r2(y_deg+z_deg,p_deg)
assert abs(c_deg) < 1e-15 and abs(g_deg_0-g_deg_1) < 1e-15 and r2_deg_1 is None

# 5. Train-only-naive baseline: zero train mean of z freezes exactly the scalar training-mean baseline.
train_y = np.array([0.0,2.0]); train_z = np.array([-1.0,1.0])
b0 = train_y.mean(); b1 = (train_y + 3.0*train_z).mean()
held_y = np.array([-1.0,1.0]); held_z = np.array([-1.0,1.0]); held_p = np.zeros(2)
assert abs(b0-b1) < 1e-15 and abs(inner(held_z, held_p-b0)) < 1e-15
assert abs(margin(held_y,held_p,b0,held_z,0.0)-margin(held_y,held_p,b1,held_z,3.0)) < 1e-15

# 6. If train centering fails, the training-mean baseline moves.
train_z_bad = np.ones(2)
b_bad = (train_y + 3.0*train_z_bad).mean()
assert b_bad != b0

# 7. Population oracle identity on a finite equiprobable construction with E[Z|S]=0.
S = np.array([-1.0,-1.0,1.0,1.0])
M = S.copy()
E = np.array([0.5,-0.5,0.25,-0.25])
Z = np.array([1.0,-1.0,2.0,-2.0])
Y = M + E
mu = Y.mean()
assert abs(mu) < 1e-15
assert abs(E[:2].mean()) < 1e-15 and abs(E[2:].mean()) < 1e-15
assert abs(Z[:2].mean()) < 1e-15 and abs(Z[2:].mean()) < 1e-15
varM = float(np.mean((M-M.mean())**2))
pop_err = 0.0
for a in (-2.0,0.0,0.5,3.0):
    ya = Y+a*Z
    advantage = mse(mu,ya)-mse(M,ya)
    pop_err = max(pop_err, abs(advantage-varM))
assert pop_err < 1e-12

# 8. If E[Z|S]=0 fails, the oracle-margin conclusion can fail and adequacy can collapse for positive a.
M_bad = S.copy(); Y_bad = M_bad.copy(); Z_bad = -M_bad; a_bad = 0.75
adv_bad = mse(0.0,Y_bad+a_bad*Z_bad)-mse(M_bad,Y_bad+a_bad*Z_bad)
r2_bad = r2(Y_bad+a_bad*Z_bad,M_bad)
assert adv_bad < 0 and r2_bad is not None and r2_bad < 0

# 9. A moving test-mean baseline with noncentered z reintroduces a quadratic term; fixed baseline is essential.
y_move = np.array([-1.0,1.0]); p_move = y_move.copy(); z_move = np.array([0.0,2.0]); b_fixed = 0.0
def moving_margin(a):
    ya = y_move+a*z_move
    b_a = ya.mean()
    return mse(b_a,ya)-mse(p_move,ya)
g_fixed_3 = margin(y_move,p_move,b_fixed,z_move,3.0)
g_moving_3 = moving_margin(3.0)
assert g_fixed_3 > 0 and g_moving_3 < 0

print('T9A_CHECKS_PASS')
print(f'max_identity_err={max_identity_err:.3e}')
print(f'decomposition_err={decomp_err:.3e}')
print(f'r2_counterexample: alignment={c_r2:.3f} G0={g_r2_0:.3f} G1={g_r2_1:.3f} R2_0={r2_0:.3f} R2_1={r2_1:.3f}')
print(f'orthogonal_degenerate: alignment={c_deg:.3f} G0={g_deg_0:.3f} G1={g_deg_1:.3f} R2_at_a1={r2_deg_1}')
print(f'population_oracle_max_err={pop_err:.3e} VarM={varM:.3f}')
print(f'conditional_centering_failure: margin={adv_bad:.3f} R2={r2_bad:.3f}')
print(f'moving_baseline_counterexample: fixed_G_a3={g_fixed_3:.3f} moving_G_a3={g_moving_3:.3f}')
