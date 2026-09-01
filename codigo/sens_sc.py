import os
CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE)
DATOS = os.path.join(BASE, "original", "base_final.csv")
OUT   = os.path.join(BASE, "resultados")
FIGS  = os.path.join(BASE, "figuras")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIGS, exist_ok=True)
import pandas as pd, numpy as np, sys
src = open(os.path.join(CODE,'analisis.py')).read().split("sc_arg = build_sc")[0]
ns={}; exec(src, ns)
d, build_sc = ns['d'], ns['build_sc']
which = sys.argv[1]
cfg = {'B': ("B. empi_robust, pre 1995-2010", d, 'empi_robust'),
       'C': ("C. empi, pre 2003-2010 (excluye crisis 2001-02)", d[d.year>=2003], 'empi')}[which]
nombre, dd, outc = cfg
s = build_sc('ARG', 2011, dd, outcome=outc)
ratios=[s['ratio']]
for c in sorted(dd.iso3c.unique()):
    if c!='ARG': ratios.append(build_sc(c,2011,dd,outcome=outc)['ratio'])
ratios=np.array(ratios)
pesos={k:round(v,3) for k,v in sorted(s['pesos'].items(), key=lambda x:-x[1]) if v>0.01}
pd.DataFrame([dict(variante=nombre, rmspe_pre=s['rmspe_pre'], rmspe_post=s['rmspe_post'],
    ratio=s['ratio'], rank_ARG=int((ratios>=s['ratio']).sum()), n=len(ratios),
    p_placebo=(ratios>=s['ratio']).sum()/len(ratios), pesos=str(pesos))]).to_csv(
    os.path.join(OUT, f'_sens_{which}.csv'), index=False)
print(which, "listo")

# --- Placebo in time bajo esta variante -> T9b
if which == 'C':
    filas = []
    for anio in range(2007, 2012):
        r = build_sc('ARG', anio, dd, outcome=outc)
        filas.append(dict(anio_tratamiento=anio, rmspe_pre=r['rmspe_pre'],
                          rmspe_post=r['rmspe_post'], ratio=r['ratio'],
                          tipo='real' if anio==2011 else 'placebo'))
    t9b = pd.DataFrame(filas)
    t9b['percentil'] = t9b['ratio'].rank(pct=True) * 100
    t9b.to_csv(
        os.path.join(OUT, 'T9b_placebo_in_time_specC.csv'), index=False)
    print("T9b listo")
