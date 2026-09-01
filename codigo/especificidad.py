"""
¿El cambio de régimen post-2011 es general al panel o específico de Argentina?
Genera T15_especificidad_ARG.csv
"""
import os, sys
CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE)
OUT  = os.path.join(BASE, "resultados")
src = open(os.path.join(CODE, 'analisis.py')).read().split("sc_arg = build_sc")[0]
ns = {}; exec(src, ns)
d, fe_dk = ns['d'], ns['fe_dk']
import pandas as pd, numpy as np

d = d.copy()
d['ARG_post']          = d['ARG'] * d['post2011']
d['L1rent_x_post']     = d['L1_rent'] * d['post2011']
d['L1rent_x_ARG']      = d['L1_rent'] * d['ARG']
d['L1rent_x_ARGpost']  = d['L1_rent'] * d['ARG_post']

filas = []
r, m = fe_dk(d, 'empi',
             ['L1_rent','L1rent_x_post','L1rent_x_ARG','L1rent_x_ARGpost','ln_gdp','openness'],
             'M7_triple')
r['modelo'] = 'M7_triple_ARG'; r['N'] = m['N']; filas.append(r)

r2, m2 = fe_dk(d[d.iso3c != 'ARG'], 'empi',
               ['L1_rent','L1rent_x_post','ln_gdp','openness'], 'M8_sinARG')
r2['modelo'] = 'M8_panel_sin_ARG'; r2['N'] = m2['N']; filas.append(r2)

t = pd.concat(filas)[['modelo','variable','coef','se_DK','t','p','N']]
t.to_csv(os.path.join(OUT, 'T15_especificidad_ARG.csv'), index=False)

# magnitud economica en desvios estandar del EMPI
sd_r, sd_e = d['L1_rent'].std(), d['empi'].std()
mag = pd.DataFrame([
  dict(efecto='post2011 x rentabilidad', coef=-1.3932),
  dict(efecto='stress x rentabilidad (h=3)', coef=0.1145),
])
mag['sd_ln_rent'] = sd_r; mag['sd_empi'] = sd_e
mag['efecto_en_EMPI_por_1sd_rent'] = mag.coef.abs() * sd_r
mag['en_sd_de_EMPI'] = mag['efecto_en_EMPI_por_1sd_rent'] / sd_e
mag.to_csv(os.path.join(OUT, 'T16_magnitud_economica.csv'), index=False)

print(t.to_string(index=False))
print()
print(mag.to_string(index=False))
print("\nT15 y T16 listos")
