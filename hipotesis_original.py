"""
Replica y extension de las especificaciones centrales del trabajo original
(Tablas 4.3 y 4.4). Genera T19, T20, T21 y la figura 9.

Hipotesis: la BAJA rentabilidad del canal exportador genera vulnerabilidad
cambiaria CUANDO la economia enfrenta restriccion externa. La rentabilidad no
es determinante autonomo sino amplificador condicionado a la liquidez externa.
"""
import os
CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE); OUT=os.path.join(BASE,"resultados"); FIGS=os.path.join(BASE,"figuras")
src = open(os.path.join(CODE,'analisis.py')).read().split("sc_arg = build_sc")[0]
ns={}; exec(src, ns); d, fe_dk = ns['d'], ns['fe_dk']
import pandas as pd, numpy as np

d=d.copy()
d['L1rent_x_stress']    = d['L1_rent']*d['stress_high']
d['L1rent_x_post']      = d['L1_rent']*d['post2011']
d['L1rent_x_ca']        = d['L1_rent']*d['current_account']
d['post_x_ca']          = d['post2011']*d['current_account']
d['L1rent_x_post_x_ca'] = d['L1_rent']*d['post2011']*d['current_account']

# --- T19: Tabla 4.3 del original (stress como efecto principal)
r43,m43 = fe_dk(d,'empi',['L1_rent','stress_high','L1rent_x_stress','ln_gdp','openness'],'')
r43['modelo']='O1_stress_con_efecto_principal'; r43['N']=m43['N']

# comparacion: la misma sin el efecto principal (especificacion incompleta)
r43b,m43b = fe_dk(d,'empi',['L1_rent','L1rent_x_stress','ln_gdp','openness'],'')
r43b['modelo']='O1b_sin_efecto_principal'; r43b['N']=m43b['N']

# --- T20: Tabla 4.4 del original (triple interaccion con cuenta corriente)
xs=['L1_rent','current_account','ln_gdp','openness','L1rent_x_post','L1rent_x_ca',
    'post_x_ca','L1rent_x_post_x_ca']
r44,m44 = fe_dk(d,'empi',xs,'')
r44['modelo']='O2_triple_cuenta_corriente'; r44['N']=m44['N']

pd.concat([r43,r43b,r44])[['modelo','variable','coef','se_DK','t','p','N']].to_csv(
    os.path.join(OUT,'T19_especificaciones_originales.csv'), index=False)

# --- T20: efecto marginal de la rentabilidad segun la posicion externa
b = dict(zip(r44.variable, r44.coef))
V = m44['V'] if 'V' in m44 else None
def efecto(cc, post):
    return (b['L1_rent'] + b['L1rent_x_post']*post +
            b['L1rent_x_ca']*cc + b['L1rent_x_post_x_ca']*post*cc)
q = d['current_account'].quantile([.10,.25,.50,.75,.90])
filas=[]
for et,cc in [('déficit alto (p10)',q[.10]),('déficit moderado (p25)',q[.25]),
              ('equilibrio (mediana)',q[.50]),('superávit moderado (p75)',q[.75]),
              ('superávit alto (p90)',q[.90])]:
    filas.append(dict(posicion_externa=et, current_account=round(cc,3),
                      efecto_pre2011=efecto(cc,0), efecto_post2011=efecto(cc,1),
                      diferencia=efecto(cc,1)-efecto(cc,0)))
mg=pd.DataFrame(filas)
mg.to_csv(os.path.join(OUT,'T20_efecto_marginal_por_posicion_externa.csv'), index=False)

print("=== TABLA 4.3 (con efecto principal de stress) ===")
print(r43[['variable','coef','se_DK','p']].to_string(index=False))
print("\n--- la misma SIN el efecto principal: la interaccion cambia de signo ---")
print(r43b[r43b.variable=='L1rent_x_stress'][['variable','coef','se_DK','p']].to_string(index=False))
print("\n=== TABLA 4.4 (triple interaccion) ===")
print(r44[['variable','coef','se_DK','p']].to_string(index=False))
print("\n=== EFECTO MARGINAL DE LA RENTABILIDAD SOBRE EL EMPI ===")
print(mg.round(3).to_string(index=False))

# --- Figura 9
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
AZ,RO='#2c5f8d','#c0392b'
cc=np.linspace(d.current_account.quantile(.05), d.current_account.quantile(.95),100)
fig,ax=plt.subplots(figsize=(10,5.4))
ax.plot(cc,[efecto(x,0) for x in cc],color=AZ,lw=2.6,label='Antes de 2011')
ax.plot(cc,[efecto(x,1) for x in cc],color=RO,lw=2.6,label='Desde 2011')
ax.axhline(0,color='k',lw=1); ax.axvline(0,color='k',lw=.8,ls=':',alpha=.6)
ax.fill_between(cc,[efecto(x,1) for x in cc],0,
                where=[efecto(x,1)<0 for x in cc],color=RO,alpha=.12)
ax.set_xlabel('Posición externa: saldo de cuenta corriente (% del PIB)')
ax.set_ylabel('Efecto de la rentabilidad exportadora sobre el EMPI')
ax.set_title('La rentabilidad exportadora importa cuando hay restricción externa\n'
             'Efecto marginal según posición externa, antes y después de 2011',
             fontsize=11.5,weight='bold')
ax.annotate('con déficit de cuenta corriente\nuna caída de la rentabilidad\neleva la presión cambiaria',
            xy=(cc[10],efecto(cc[10],1)), xytext=(cc[35],efecto(cc[10],1)-.05),
            fontsize=8.5,color=RO,style='italic', va='center',
            bbox=dict(boxstyle='round,pad=.4',fc='white',ec=RO,alpha=.9),
            arrowprops=dict(arrowstyle='->',color=RO,lw=1.2))
ax.margins(y=.12)
ax.legend(fontsize=10); ax.grid(alpha=.3,ls='--')
plt.tight_layout(); plt.savefig(f'{FIGS}/fig9_efecto_marginal.png',dpi=200); plt.close()
print("\nT19, T20 y figura 9 listos")
