import os
CODE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
BASE = os.path.dirname(CODE)
DATOS = os.path.join(BASE, "original", "base_final.csv")
OUT   = os.path.join(BASE, "resultados")
FIGS  = os.path.join(BASE, "figuras")
os.makedirs(OUT, exist_ok=True); os.makedirs(FIGS, exist_ok=True)
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
S=OUT; G=FIGS
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.3,'grid.linestyle':'--'})
AZ,RO,GR='#2c5f8d','#c0392b','#7f8c8d'

# --- Fig 1: SC baseline (spec C: pre 2003-2010) -> reconstruir serie
src = open(os.path.join(CODE,'analisis.py')).read().split("sc_arg = build_sc")[0]
ns={}; exec(src, ns); d, build_sc = ns['d'], ns['build_sc']
s = build_sc('ARG', 2011, d[d.year>=2003], outcome='empi')
pd.DataFrame({'year':s['anios'],'ARG_real':s['real'],'sintetico':s['synth'],
              'gap':s['real']-s['synth']}).to_csv(f'{S}/T6b_sc_series_specC.csv', index=False)
pd.Series(s['pesos']).sort_values(ascending=False).rename('peso').to_csv(f'{S}/T7b_sc_pesos_specC.csv')

fig,ax=plt.subplots(figsize=(10,5.2))
ax.plot(s['anios'],s['real'],'o-',color=RO,lw=2.2,ms=5,label='Argentina (observado)')
ax.plot(s['anios'],s['synth'],'s--',color=AZ,lw=2,ms=4,label='Control sintético')
ax.axvline(2010.5,color='k',ls=':',lw=1.5,alpha=.7)
ax.text(2010.6,ax.get_ylim()[1]*.85,'2011',fontsize=9)
ax.set_xlabel('Año'); ax.set_ylabel('EMPI')
ax.set_title(f"Synthetic Control — Argentina vs. sintético (pre 2003-2010)\n"
             f"RMSPE pre={s['rmspe_pre']:.3f} · post={s['rmspe_post']:.3f} · ratio={s['ratio']:.2f}",
             fontsize=11,weight='bold')
ax.legend(); plt.tight_layout(); plt.savefig(f'{G}/fig1_synthetic_control.png',dpi=200); plt.close()

# --- Fig 2: placebo in space (baseline pre completo, T8) + spec C
ps=pd.read_csv(f'{S}/T8_placebo_in_space.csv').sort_values('ratio')
fig,ax=plt.subplots(figsize=(10,5.2))
col=[RO if u=='ARG' else AZ for u in ps.unidad]
ax.bar(ps.unidad,ps.ratio,color=col,edgecolor='k',lw=.7)
ax.axhline(1,color='k',lw=1)
ax.set_ylabel('RMSPE post / RMSPE pre'); ax.set_xlabel('País')
arg=ps[ps.unidad=='ARG'].iloc[0]
ax.set_title(f"Placebo in space (ventana pre 1995-2010)\nArgentina: ratio={arg.ratio:.2f}, "
             f"puesto 2 de 12, p={arg.p_value:.3f}",fontsize=11,weight='bold')
plt.tight_layout(); plt.savefig(f'{G}/fig2_placebo_space.png',dpi=200); plt.close()

# --- Fig 3: placebo in time (spec C)
pt=pd.read_csv(f'{S}/T9b_placebo_in_time_specC.csv')
fig,ax=plt.subplots(figsize=(10,5.2))
col=[RO if t=='real' else AZ for t in pt.tipo]
ax.bar(pt.anio_tratamiento.astype(str),pt.ratio,color=col,edgecolor='k',lw=.7,width=.6)
ax.set_ylabel('RMSPE post / RMSPE pre'); ax.set_xlabel('Año supuesto de tratamiento')
ax.set_title("Placebo in time (ventana pre desde 2003)\n"
             "2011 alcanza el ratio máximo (4.95) pero 2010 es casi idéntico (4.83)",
             fontsize=11,weight='bold')
plt.tight_layout(); plt.savefig(f'{G}/fig3_placebo_time.png',dpi=200); plt.close()

# --- Fig 4: Local projections
lp=pd.read_csv(f'{S}/T10_local_projections.csv')
fig,axs=plt.subplots(1,2,figsize=(11,4.6))
for ax,v,tit in zip(axs,['L1_rent','L1rent_x_stress'],
                    ['Rentabilidad (L1)','Rentabilidad × stress externo']):
    z=lp[lp.variable==v]
    ax.fill_between(z.h,z.ic_bajo,z.ic_alto,color=AZ,alpha=.25)
    ax.plot(z.h,z.coef,'o-',color=RO,lw=2)
    ax.axhline(0,color='k',ls='--',lw=1)
    ax.set_title(tit,fontsize=10,weight='bold'); ax.set_xlabel('Horizonte h (años)')
axs[0].set_ylabel('Coeficiente')
fig.suptitle('Local Projections (FE bidireccional, errores Driscoll-Kraay, IC 95%)',
             fontsize=11,weight='bold')
plt.tight_layout(); plt.savefig(f'{G}/fig4_local_projections.png',dpi=200); plt.close()

# --- Fig 5: descomposicion del indice para ARG (dos paneles)
a = d[d.iso3c=='ARG'].copy()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                               gridspec_kw={'height_ratios': [1, 1]})

# Panel superior: nivel del indice y su componente internacional
ax1.plot(a.year, a.ln_rentabilidad, color='k', lw=2.4, ls='--',
         label='ln(rentabilidad exportadora)')
ax1.plot(a.year, np.log(a.tot_index), color=AZ, lw=2, label='ln(ToT)')
ax1.axvline(2010.5, color='k', ls=':', lw=1.5, alpha=.7)
ax1.set_ylabel('Log')
ax1.set_title('Argentina: descomposición del índice de rentabilidad exportadora',
              fontsize=11, weight='bold')
ax1.legend(fontsize=9, loc='upper left')

# Panel inferior: las dos cunas de politica domestica, en su propia escala
ax2.plot(a.year, np.log(1 - a.dexmedia), color='#27ae60', lw=2.2,
         label='ln(1 − retenciones)')
ax2.plot(a.year, -np.log(a.brecha_anual), color=RO, lw=2.2, label='−ln(brecha)')
ax2.axhline(0, color='k', lw=.8)
ax2.axvline(2010.5, color='k', ls=':', lw=1.5, alpha=.7)
ax2.set_xlabel('Año'); ax2.set_ylabel('Log')
ax2.set_title('Cuñas de política doméstica (escala propia)', fontsize=10)
ax2.legend(fontsize=9, loc='lower left')

# aporte de la brecha a la varianza post-2011 (las shares vienen en fraccion)
v = pd.read_csv(f'{S}/T12_varianza_componentes_ARG.csv')
fila = v[v.periodo == '2011-2023'].iloc[0]
pct = float(fila['share_ln_brecha']) * 100
ax2.annotate(f'desde 2011 la brecha explica\nel {pct:.1f}% de la varianza de ln(rent.)',
             xy=(2016.5, -0.62), fontsize=8.5, color=RO, style='italic',
             ha='center',
             bbox=dict(boxstyle='round,pad=0.4', fc='white', ec=RO, alpha=.85))

plt.tight_layout()
plt.savefig(f'{G}/fig5_descomposicion.png', dpi=200); plt.close()

# --- Fig 6: EMPI de todos los paises (Argentina resaltada)  [Figura 2 del original]
fig,ax=plt.subplots(figsize=(10,5.2))
for c in sorted(d.iso3c.unique()):
    s=d[d.iso3c==c]
    if c=='ARG': continue
    ax.plot(s.year,s.empi,color='#b0bec5',lw=1.1,zorder=1)
s=d[d.iso3c=='ARG']
ax.plot(s.year,s.empi,color=RO,lw=2.6,zorder=3,label='Argentina')
ax.plot([],[],color='#b0bec5',lw=1.1,label='Resto de la muestra (11 países)')
ax.axvline(2010.5,color='k',ls=':',lw=1.5,alpha=.7)
ax.axhline(0,color='k',lw=.8,alpha=.5)
ax.set_xlabel('Año'); ax.set_ylabel('EMPI')
ax.set_title('Evolución del EMPI, 1995-2023 (Argentina resaltada)',fontsize=11,weight='bold')
ax.legend(fontsize=9)
plt.tight_layout(); plt.savefig(f'{G}/fig6_empi_muestra.png',dpi=200); plt.close()

# --- Fig 7: EMPI medio pre vs post 2011 por pais  [Figura 3 del original]
pre  = d[d.year<2011].groupby('iso3c').empi.mean()
post = d[d.year>=2011].groupby('iso3c').empi.mean()
cmp  = pd.DataFrame({'pre':pre,'post':post}).dropna()
cmp['delta']=cmp.post-cmp.pre
cmp=cmp.sort_values('delta')
fig,ax=plt.subplots(figsize=(10,5.2))
col=[RO if i=='ARG' else AZ for i in cmp.index]
ax.barh(cmp.index,cmp.delta,color=col,edgecolor='k',lw=.6)
ax.axvline(0,color='k',lw=1)
ax.set_xlabel('Cambio en el EMPI medio: 2011-2023 menos 1995-2010')
ax.set_title('Argentina vs. comparables: cambio del EMPI medio entre períodos',
             fontsize=11,weight='bold')
n_suben=int((cmp.delta>0).sum())
ax.text(.98,.04,f'{n_suben} de {len(cmp)} países aumentan su EMPI medio',
        transform=ax.transAxes,ha='right',fontsize=8.5,style='italic',
        bbox=dict(boxstyle='round,pad=.4',fc='white',ec=GR,alpha=.9))
cmp.round(4).to_csv(f'{S}/T14_empi_pre_post.csv')
plt.tight_layout(); plt.savefig(f'{G}/fig7_empi_pre_post.png',dpi=200); plt.close()

print("graficos OK")
