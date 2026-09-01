"""
¿Hay dinámica stop-and-go en Argentina post-2011?
Implicancias verificables:
  (A) crecimiento -> presion cambiaria con rezago   (la expansion consume divisas)
  (B) presion cambiaria -> contraccion al ano siguiente (el ajuste frena la economia)
  (C) si (A) y (B) operan juntas, el ciclo se autosostiene
  (D) post-2011 la oscilacion deberia ser mas amplia y frecuente que antes y que en comparables
Genera T17_stop_and_go.csv, T18_ciclo_descriptivo.csv
"""
import os, sys
CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE); OUT = os.path.join(BASE, "resultados")
src = open(os.path.join(CODE,'analisis.py')).read().split("sc_arg = build_sc")[0]
ns={}; exec(src, ns); d, fe_dk = ns['d'], ns['fe_dk']
import pandas as pd, numpy as np

d = d.sort_values(['iso3c','year']).copy()
g = d.groupby('iso3c')
d['growth_l1']   = g['growth'].shift(1)
d['empi_l1_sg']  = g['empi'].shift(1)
d['ARG_post']    = d['ARG']*d['post2011']
d['gl1_x_post']     = d['growth_l1']*d['post2011']
d['gl1_x_ARGpost']  = d['growth_l1']*d['ARG_post']
d['gl1_x_ARG']      = d['growth_l1']*d['ARG']
d['el1_x_post']     = d['empi_l1_sg']*d['post2011']
d['el1_x_ARGpost']  = d['empi_l1_sg']*d['ARG_post']
d['el1_x_ARG']      = d['empi_l1_sg']*d['ARG']

filas=[]
# (A) crecimiento -> EMPI
rA,mA = fe_dk(d,'empi',['growth_l1','gl1_x_post','gl1_x_ARG','gl1_x_ARGpost','ln_gdp','openness'],'A')
rA['bloque']='A_crecimiento_a_presion'; rA['N']=mA['N']; filas.append(rA)
# (B) EMPI -> crecimiento
rB,mB = fe_dk(d,'growth',['empi_l1_sg','el1_x_post','el1_x_ARG','el1_x_ARGpost','ln_gdp','openness'],'B')
rB['bloque']='B_presion_a_contraccion'; rB['N']=mB['N']; filas.append(rB)
t=pd.concat(filas)[['bloque','variable','coef','se_DK','t','p','N']]
t.to_csv(os.path.join(OUT,'T17_stop_and_go.csv'), index=False)
print("=== (A) crecimiento(t-1) -> EMPI(t) ===")
print(rA[['variable','coef','se_DK','p']].to_string(index=False))
print("\n=== (B) EMPI(t-1) -> crecimiento(t) ===")
print(rB[['variable','coef','se_DK','p']].to_string(index=False))

# (D) descriptivo del ciclo: amplitud y frecuencia de reversiones del crecimiento
def ciclo(s):
    s=s.dropna()
    if len(s)<4: return pd.Series(dict(sd=np.nan,reversiones=np.nan,n=len(s)))
    dif=np.sign(s.diff().dropna())
    rev=int((dif.values[1:]*dif.values[:-1]<0).sum())
    return pd.Series(dict(sd=s.std(), reversiones=rev/len(s), n=len(s)))
out=[]
for c in sorted(d.iso3c.unique()):
    for lab,sub in [('1995-2010',d[(d.iso3c==c)&(d.year<2011)]),
                    ('2011-2023',d[(d.iso3c==c)&(d.year>=2011)])]:
        r=ciclo(sub['growth']); r['iso3c']=c; r['periodo']=lab; out.append(r)
cic=pd.DataFrame(out)[['iso3c','periodo','sd','reversiones','n']]
piv0=cic.pivot(index='iso3c',columns='periodo',values='sd')
piv0['cambio_sd']=piv0['2011-2023']-piv0['1995-2010']
cic=cic.merge(piv0[['cambio_sd']],on='iso3c',how='left')
cic.to_csv(os.path.join(OUT,'T18_ciclo_descriptivo.csv'), index=False)
piv=cic.pivot(index='iso3c',columns='periodo',values='sd')
piv['cambio_sd']=piv['2011-2023']-piv['1995-2010']
print("\n=== (D) Volatilidad del crecimiento (desvio estandar) ===")
print(piv.sort_values('cambio_sd',ascending=False).round(3).to_string())
print("\nT17 y T18 listos")

# --- Figura 8: la pata del rebote, Argentina pre vs post 2011
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FIGS=os.path.join(BASE,'figuras')
AZ,RO='#2c5f8d','#c0392b'
a=d[(d.iso3c=='ARG')].dropna(subset=['empi_l1_sg','growth'])
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11,4.6))
for ax,sub,lab,col in [(ax1,a[a.year<2011],'Argentina 1995-2010',AZ),
                       (ax2,a[a.year>=2011],'Argentina 2011-2023',RO)]:
    ax.scatter(sub.empi_l1_sg,sub.growth,color=col,s=45,zorder=3,edgecolor='k',lw=.5)
    if len(sub)>2:
        b=np.polyfit(sub.empi_l1_sg,sub.growth,1)
        xs=np.linspace(sub.empi_l1_sg.min(),sub.empi_l1_sg.max(),50)
        ax.plot(xs,np.polyval(b,xs),color=col,lw=2.2)
        ax.set_title(f'{lab}\npendiente = {b[0]:+.2f}',fontsize=10,weight='bold')
    ax.axhline(0,color='k',lw=.8,alpha=.5); ax.axvline(0,color='k',lw=.8,alpha=.5)
    ax.set_xlabel('EMPI del año anterior'); ax.grid(alpha=.3,ls='--')
ax1.set_ylabel('Crecimiento del PIB (%)')
lo=min(ax1.get_ylim()[0],ax2.get_ylim()[0]); hi=max(ax1.get_ylim()[1],ax2.get_ylim()[1])
ax1.set_ylim(lo,hi); ax2.set_ylim(lo,hi)
fig.suptitle('¿La presión cambiaria es seguida por rebote? Argentina, antes y después de 2011',
             fontsize=11.5,weight='bold')
plt.tight_layout(); plt.savefig(f'{FIGS}/fig8_stop_and_go.png',dpi=200); plt.close()
print("fig8 lista")
