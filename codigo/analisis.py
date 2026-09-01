"""
Replicación y extensión del trabajo final de Pablo S. Martinez Soler.
Todo se estima sobre original/base_final.csv
Ningun numero esta escrito a mano: todo sale de este script.
"""
import numpy as np, pandas as pd
from scipy.optimize import minimize
import json, os

CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE)
DATOS = os.path.join(BASE, "original", "base_final.csv")
OUT   = os.path.join(BASE, "resultados")
FIGS  = os.path.join(BASE, "figuras")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIGS, exist_ok=True)

np.random.seed(20240101)

# ---------------------------------------------------------------- 1. PANEL
d = pd.read_csv(DATOS)
d = d[d.year >= 1995].sort_values(['iso3c', 'year']).reset_index(drop=True)

d['dexmedia'] = d['dexmedia'].fillna(0)
rent = d['tot_index'] * (1 - d['dexmedia']) * (1 / d['brecha_anual'])
rent = rent.where(np.isfinite(rent) & (rent > 0))
d['ln_rentabilidad'] = np.log(rent)
d['ln_gdp'] = np.log(d['gdp_real'])
d['post2011'] = (d.year >= 2011).astype(float)
d['ARG'] = (d.iso3c == 'ARG').astype(float)
d['stress_ca'] = d['current_account'].abs()
d['stress_high'] = (d['stress_ca'] > d['stress_ca'].quantile(.75)).astype(float)
d['L1_rent'] = d.groupby('iso3c')['ln_rentabilidad'].shift(1)
d['L2_rent'] = d.groupby('iso3c')['ln_rentabilidad'].shift(2)
d['L3_rent'] = d.groupby('iso3c')['ln_rentabilidad'].shift(3)
d['empi_l1'] = d.groupby('iso3c')['empi'].shift(1)

d.to_csv(f"{OUT}/panel_construido.csv", index=False)

# ------------------------------------------------- 2. FE TWOWAY + DRISCOLL-KRAAY
def demean_twoway(df, cols, imax=200, tol=1e-11):
    X = df[cols].astype(float).copy()
    i, t = df['iso3c'].values, df['year'].values
    for _ in range(imax):
        prev = X.values.copy()
        X = X - X.groupby(i).transform('mean')
        X = X - X.groupby(t).transform('mean')
        if np.max(np.abs(X.values - prev)) < tol:
            break
    return X

def fe_dk(data, y, xs, label=""):
    df = data.dropna(subset=[y] + xs).copy()
    Z = demean_twoway(df, [y] + xs)
    yy = Z[y].values
    XX = Z[xs].values
    XtX_inv = np.linalg.pinv(XX.T @ XX)
    b = XtX_inv @ (XX.T @ yy)
    e = yy - XX @ b
    n, K = len(yy), len(xs)
    Nc, Tc = df.iso3c.nunique(), df.year.nunique()
    dfree = n - Nc - Tc + 1 - K

    # Driscoll-Kraay (Newey-West sobre momentos agregados por año)
    h = XX * e[:, None]
    years = df.year.values
    ht = pd.DataFrame(h, index=years).groupby(level=0).sum().sort_index().values
    T = ht.shape[0]
    m = int(np.floor(4 * (T / 100) ** (2 / 9)))
    S = ht.T @ ht
    for j in range(1, m + 1):
        w = 1 - j / (m + 1)
        G = ht[j:].T @ ht[:-j]
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv * (n / dfree)
    se = np.sqrt(np.diag(V))
    t = b / se
    from scipy import stats
    p = 2 * (1 - stats.t.cdf(np.abs(t), dfree))

    # R2 within / between / overall
    ss_res = np.sum(e ** 2)
    r2_within = 1 - ss_res / np.sum((yy - yy.mean()) ** 2)
    fit_full = df[xs].values @ b
    g = df.groupby('iso3c')
    yb = g[y].mean().values
    fb = pd.Series(fit_full, index=df.iso3c.values).groupby(level=0).mean().values
    r2_between = np.corrcoef(yb, fb)[0, 1] ** 2
    r2_overall = np.corrcoef(df[y].values, fit_full)[0, 1] ** 2

    res = pd.DataFrame({'variable': xs, 'coef': b, 'se_DK': se, 't': t, 'p': p,
                        'ic_bajo': b - 1.96 * se, 'ic_alto': b + 1.96 * se})
    meta = dict(modelo=label, N=int(n), paises=int(Nc), anios=int(Tc), K=int(K),
                gl=int(dfree), bw_DK=int(m), r2_within=float(r2_within),
                r2_between=float(r2_between), r2_overall=float(r2_overall))
    return res, meta

d['L1rent_x_post'] = d['L1_rent'] * d['post2011']
d['L1rent_x_stress'] = d['L1_rent'] * d['stress_high']
d['L1rent_x_ca'] = d['L1_rent'] * d['current_account']

modelos = {
 'M1_base':        ['L1_rent', 'ln_gdp', 'openness'],
 'M2_post2011':    ['L1_rent', 'L1rent_x_post', 'ln_gdp', 'openness'],
 'M3_stress':      ['L1_rent', 'L1rent_x_stress', 'ln_gdp', 'openness'],
 'M4_completo':    ['L1_rent', 'L1rent_x_post', 'L1rent_x_stress', 'ln_gdp', 'openness'],
 'M5_dinamico':    ['empi_l1', 'L1_rent', 'L1rent_x_post', 'ln_gdp', 'openness'],
 'M6_ca':          ['L1_rent', 'L1rent_x_ca', 'current_account', 'ln_gdp', 'openness'],
}
tab, metas = [], []
for k, xs in modelos.items():
    r, m = fe_dk(d, 'empi', xs, k)
    r.insert(0, 'modelo', k)
    tab.append(r); metas.append(m)
pd.concat(tab).to_csv(f"{OUT}/T1_panel_fe_dk.csv", index=False)
pd.DataFrame(metas).to_csv(f"{OUT}/T2_diagnosticos_modelos.csv", index=False)

# robustez: empi_robust como dependiente
tabr = []
for k, xs in modelos.items():
    r, m = fe_dk(d, 'empi_robust', xs, k)
    r.insert(0, 'modelo', k); tabr.append(r)
pd.concat(tabr).to_csv(f"{OUT}/T3_robustez_empi_robust.csv", index=False)

# rezagos L1/L2/L3
lags = []
for L in ['L1_rent', 'L2_rent', 'L3_rent']:
    dd = d.copy(); dd['LX'] = dd[L]; dd['LX_post'] = dd[L] * dd['post2011']
    r, m = fe_dk(dd, 'empi', ['LX', 'LX_post', 'ln_gdp', 'openness'], L)
    r.insert(0, 'rezago', L); lags.append(r)
pd.concat(lags).to_csv(f"{OUT}/T4_rezagos.csv", index=False)

# VIF sobre el modelo completo (datos demeaneados)
xs = modelos['M4_completo']
dfv = d.dropna(subset=['empi'] + xs)
Zv = demean_twoway(dfv, xs)
vifs = []
for j, c in enumerate(xs):
    Y = Zv[c].values; Xo = Zv.drop(columns=[c]).values
    bb = np.linalg.pinv(Xo.T @ Xo) @ (Xo.T @ Y)
    r2 = 1 - np.sum((Y - Xo @ bb) ** 2) / np.sum((Y - Y.mean()) ** 2)
    vifs.append(dict(variable=c, R2_auxiliar=r2, VIF=1 / (1 - r2)))
pd.DataFrame(vifs).to_csv(f"{OUT}/T5_vif.csv", index=False)

# ------------------------------------------------------- 3. SYNTHETIC CONTROL
W_PRED = ['ln_rentabilidad', 'ln_gdp', 'openness', 'current_account', 'tot_index']

def build_sc(treat, t0, data, outcome='empi'):
    donors = sorted([c for c in data.iso3c.unique() if c != treat])
    pre = data[data.year < t0]
    def predmat(country):
        s = pre[pre.iso3c == country]
        v = [s[p].mean() for p in W_PRED]
        for yr in [t0 - 10, t0 - 7, t0 - 4, t0 - 2]:
            row = s[s.year == yr]
            v.append(row[outcome].values[0] if len(row) else np.nan)
        return np.array(v, float)
    X1 = predmat(treat)
    X0 = np.column_stack([predmat(c) for c in donors])
    ok = ~np.isnan(X1) & ~np.isnan(X0).any(1)
    X1, X0 = X1[ok], X0[ok]
    sd = np.std(np.column_stack([X1[:, None], X0]), axis=1); sd[sd == 0] = 1
    X1s, X0s = X1 / sd, X0 / sd[:, None]

    Y = data.pivot_table(index='year', columns='iso3c', values=outcome)
    Y1pre = Y.loc[Y.index < t0, treat].values
    Y0pre = Y.loc[Y.index < t0, donors].values

    def w_given_v(v):
        P = X0s * np.sqrt(v)[:, None]; q = X1s * np.sqrt(v)
        f = lambda w: np.sum((q - P @ w) ** 2)
        cons = ({'type': 'eq', 'fun': lambda w: w.sum() - 1},)
        w0 = np.ones(len(donors)) / len(donors)
        r = minimize(f, w0, method='SLSQP', bounds=[(0, 1)] * len(donors),
                     constraints=cons, options={'maxiter': 400, 'ftol': 1e-12})
        return np.clip(r.x, 0, None) / max(np.clip(r.x, 0, None).sum(), 1e-12)

    def outer(lv):
        v = np.exp(lv); v = v / v.sum()
        w = w_given_v(v)
        return np.mean((Y1pre - Y0pre @ w) ** 2)

    best = minimize(outer, np.zeros(X1s.size), method='Nelder-Mead',
                    options={'maxiter': 3000, 'xatol': 1e-6, 'fatol': 1e-10})
    v = np.exp(best.x); v = v / v.sum()
    w = w_given_v(v)

    synth = Y[donors].values @ w
    real = Y[treat].values
    yrs = Y.index.values
    pre_m = yrs < t0
    rmspe_pre = np.sqrt(np.nanmean((real[pre_m] - synth[pre_m]) ** 2))
    rmspe_post = np.sqrt(np.nanmean((real[~pre_m] - synth[~pre_m]) ** 2))
    return dict(unidad=treat, t0=t0, pesos=dict(zip(donors, w)),
                anios=yrs, real=real, synth=synth,
                rmspe_pre=rmspe_pre, rmspe_post=rmspe_post,
                ratio=rmspe_post / rmspe_pre if rmspe_pre > 0 else np.nan)

sc_arg = build_sc('ARG', 2011, d)
pd.DataFrame({'year': sc_arg['anios'], 'ARG_real': sc_arg['real'],
              'control_sintetico': sc_arg['synth'],
              'gap': sc_arg['real'] - sc_arg['synth']}).to_csv(f"{OUT}/T6_sc_series.csv", index=False)
pd.Series(sc_arg['pesos']).sort_values(ascending=False).rename('peso').to_csv(f"{OUT}/T7_sc_pesos.csv")

# placebo in space
rows = [dict(unidad='ARG', rmspe_pre=sc_arg['rmspe_pre'], rmspe_post=sc_arg['rmspe_post'],
             ratio=sc_arg['ratio'], tipo='tratada')]
for c in sorted(d.iso3c.unique()):
    if c == 'ARG': continue
    s = build_sc(c, 2011, d)
    rows.append(dict(unidad=c, rmspe_pre=s['rmspe_pre'], rmspe_post=s['rmspe_post'],
                     ratio=s['ratio'], tipo='placebo'))
ps = pd.DataFrame(rows).sort_values('ratio', ascending=False)
ps['percentil'] = ps['ratio'].rank(pct=True) * 100
ps['p_value'] = ps['ratio'].apply(lambda r: (ps['ratio'] >= r).sum() / len(ps))
ps.to_csv(f"{OUT}/T8_placebo_in_space.csv", index=False)

# placebo in time
rows = []
for t0 in [2005, 2006, 2007, 2008, 2009, 2010, 2011]:
    s = build_sc('ARG', t0, d)
    rows.append(dict(anio_tratamiento=t0, rmspe_pre=s['rmspe_pre'],
                     rmspe_post=s['rmspe_post'], ratio=s['ratio'],
                     tipo='real' if t0 == 2011 else 'placebo'))
pt = pd.DataFrame(rows)
pt['percentil'] = pt['ratio'].rank(pct=True) * 100
pt.to_csv(f"{OUT}/T9_placebo_in_time.csv", index=False)

# ------------------------------------------------------ 4. LOCAL PROJECTIONS
lp = []
for h in range(6):
    dd = d.copy()
    dd['dep_h'] = dd.groupby('iso3c')['empi'].shift(-h)
    r, m = fe_dk(dd, 'dep_h', ['L1_rent', 'L1rent_x_stress', 'ln_gdp', 'openness'], f'h={h}')
    for _, row in r.iterrows():
        lp.append(dict(h=h, variable=row['variable'], coef=row['coef'], se_DK=row['se_DK'],
                       ic_bajo=row['ic_bajo'], ic_alto=row['ic_alto'], p=row['p'], N=m['N']))
pd.DataFrame(lp).to_csv(f"{OUT}/T10_local_projections.csv", index=False)

# ---------------------------------------- 5. DESCOMPOSICION DEL INDICE (ARG)
a = d[d.iso3c == 'ARG'].copy()
a['ln_tot'] = np.log(a['tot_index'])
a['ln_1mdex'] = np.log(1 - a['dexmedia'])
a['ln_brecha'] = -np.log(a['brecha_anual'])
per = pd.cut(a.year, [1994, 2002, 2010, 2023], labels=['1995-2002', '2003-2010', '2011-2023'])
desc = a.groupby(per, observed=True)[['ln_tot', 'ln_1mdex', 'ln_brecha', 'ln_rentabilidad']].agg(['mean', 'std'])
desc.to_csv(f"{OUT}/T11_descomposicion_ARG.csv")

# varianza aportada por cada componente, por periodo
var_rows = []
for lab, sub in a.groupby(per, observed=True):
    v = sub[['ln_tot', 'ln_1mdex', 'ln_brecha']].var()
    cov = sub[['ln_tot', 'ln_1mdex', 'ln_brecha']].cov()
    tot_var = sub['ln_rentabilidad'].var()
    share = {c: cov[c].sum() / tot_var for c in v.index}   # descomposicion por covarianza
    var_rows.append(dict(periodo=lab, var_ln_rent=tot_var, **{f'share_{k}': v_ for k, v_ in share.items()}))
pd.DataFrame(var_rows).to_csv(f"{OUT}/T12_varianza_componentes_ARG.csv", index=False)

# descriptivas
d[['empi', 'empi_robust', 'ln_rentabilidad', 'ln_gdp', 'openness',
   'current_account', 'brecha_anual', 'dexmedia']].describe().T.to_csv(f"{OUT}/T13_descriptivas.csv")

print("OK")
