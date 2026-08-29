# Restricciones de liquidez externa, rentabilidad exportadora y vulnerabilidad cambiaria

**Lic. Pablo Santiago Martínez Soler** — Finanzas Internacionales, UBA

Versión ampliada del trabajo final: se agregan placebo tests, análisis de sensibilidad y diagnósticos sobre la estrategia empírica original.

---

## Qué hay acá

```
restriccion-externa-empi/
├── documento/
│   ├── TESIS_AMPLIADA.pdf      <- LEER ESTO (14 páginas, con figuras)
│   └── TESIS_AMPLIADA.md
├── codigo/
│   ├── analisis.py             <- produce todas las tablas T1–T13
│   ├── sens_sc.py              <- sensibilidad de la ventana pre-tratamiento
│   └── graficos.py             <- produce las 5 figuras
├── resultados/                 <- 18 archivos CSV (salida de los scripts)
├── figuras/                    <- 9 PNG
├── requirements.txt
├── LICENSE
└── .gitignore
└── original/
    ├── MartinezSoler_FI_TrabajoFinal__1_.pdf
    ├── MODELOS_FI.R
    ├── analisis_volatilidad.R
    └── base_final.csv
```

**Ninguna cifra del documento está escrita a mano.** Todas salen de `codigo/analisis.py` corriendo sobre `original/base_final.csv`. El apéndice A del documento mapea cada tabla del texto con su archivo CSV.

---

## Qué se agregó respecto del trabajo original

| Agregado | Dónde |
|---|---|
| Placebo in space sobre las 11 unidades donantes | Sección 5.1, Tabla 7, Figura 3 |
| Placebo in time sobre 6 fechas de tratamiento | Sección 5.2, Tabla 8, Figura 4 |
| Sensibilidad a la ventana pre-tratamiento del SC | Sección 4.1, Tabla 5 |
| Selección de rezagos (L1/L2/L3) | Sección 3.4, Tabla 3 |
| Diagnóstico de multicolinealidad (VIF) | Sección 3.5, Tabla 4 |
| Réplica de las Tablas 4.3 y 4.4 del original | Sección 3.2, Tablas 2 y 3 |
| Efectos marginales por posición externa | Sección 3.3, Tabla 4, Figura 3 |
| Descomposición de varianza del índice | Sección 5.3, Figura 8 |
| Test de especificidad: ¿efecto argentino o de panel? | Sección 3.6, Tabla 4b |
| Test directo de la hipótesis de stop-and-go | Sección 6, Tablas 10 y 11, Figura 8 |
| Re-estimación con errores Driscoll-Kraay | Todas las tablas |

---

## Hipótesis

La baja rentabilidad del canal exportador —deprimida por retenciones, brecha cambiaria y demás cuñas domésticas— genera vulnerabilidad cambiaria **cuando la economía enfrenta restricción de liquidez externa**. La rentabilidad no es un determinante estructural autónomo del EMPI sino un amplificador condicionado a la disponibilidad de divisas.

## Resultados principales

**Especificaciones centrales (N = 336, 12 países, 1995–2023, errores Driscoll-Kraay):**

- Efecto promedio de la rentabilidad: no distinguible de cero — lo que la hipótesis condicional predice
- Bajo estrés externo: interacción de **−1,704** (Tabla 4.3 del original, replicada)
- Con posición externa continua: **régimen × cuenta corriente = −1,813 (p = 0,040)** y **triple interacción = 0,400 (p = 0,042)**. Son los dos únicos coeficientes significativos del modelo, y son exactamente los que la hipótesis señala.

**Efecto marginal de la rentabilidad sobre el EMPI según posición externa:**

| Posición externa | Antes de 2011 | Desde 2011 |
|---|---:|---:|
| Déficit alto (p10) | 0,836 | **−1,647** |
| Equilibrio | 0,102 | −1,028 |
| Superávit alto (p90) | −1,038 | −0,067 |

Cuando hay divisas, la rentabilidad del exportador es macroeconómicamente irrelevante; cuando no las hay, es determinante. El efecto se multiplica por 24 entre extremos.

**Advertencia de especificación:** omitir el efecto principal de `stress_high` invierte el signo de la interacción (de −1,704 a +0,031). Ambas estimaciones están en `T19`.

**Control sintético (Argentina, tratamiento 2011):**

| Ventana pre | RMSPE pre | Ratio | Puesto ARG | p |
|---|---:|---:|:---:|---:|
| 1995–2010 | 2,039 | 1,66 | 2 de 12 | 0,167 |
| 2003–2010 | 0,695 | 4,95 | 1 de 12 | 0,083 |

**Descomposición del índice de rentabilidad (Argentina):** el aporte de la brecha cambiaria a la varianza pasa de ≈0% antes de 2011 a **42,5%** después.

**Especificidad:** excluida Argentina, la interacción post-2011 desaparece (+0,166; p = 0,797). El panel y el control sintético miden el mismo hecho argentino; el diseño es un estudio de caso con grupo de control.

**Stop-and-go:** la pata del freno (crecimiento → presión cambiaria) no aparece. La pata del rebote sí, y es lo que cambia: la respuesta del crecimiento a la presión cambiaria del año anterior cae de **1,96 a 0,56** (p = 0,0005). La volatilidad del crecimiento argentino **cae** de 6,67 a 5,17. Argentina conserva el *stop* y pierde el *go*.

---

## Lo que el trabajo puede y no puede afirmar

**Sí:** existe un cambio robusto en la sensibilidad del EMPI a la rentabilidad exportadora a partir de 2011, significativo al 10% y estable en todas las especificaciones. La composición del índice de rentabilidad cambia de forma nítida y en la dirección que predice el mecanismo.

**No:** no se establece el efecto al 5%. El placebo in space no valida a niveles convencionales bajo la ventana completa. El placebo in time muestra un deterioro **gradual**, no un quiebre abrupto en 2011. La causalidad no queda establecida.

La sección 6 del documento desarrolla estas limitaciones. Están enunciadas de forma explícita porque son las primeras preguntas que va a hacer un jurado, y conviene que las respuesta esté escrita antes de que las pregunte.

---

## Reproducir

```bash
pip install -r requirements.txt
cd codigo
python3 analisis.py     # ~4 min  -> 14 tablas en resultados/
python3 sens_sc.py C    # ~12 min -> _sens_C.csv y T9b (12 controles sintéticos)
python3 especificidad.py # ~10 seg -> T15, T16
python3 stop_and_go.py   # ~15 seg -> T17, T18 y figura 8
python3 graficos.py     # ~1 min  -> figuras 1-7
```

`sens_sc.py` es lento porque estima un control sintético por cada una de las 12
unidades y por cada fecha de tratamiento. Es normal que tarde: no está colgado.

Requiere `numpy`, `pandas`, `scipy`, `matplotlib`. Semilla fijada en 20240101.

El panel FE bidireccional con errores Driscoll-Kraay y el control sintético están implementados directamente en `analisis.py`, sin dependencias econométricas externas. Equivalen a `plm::plm(effect="twoways")` con `vcovSCC(maxlag=2)` y al paquete `Synth` de R.

**Verificación:** los 25 archivos de resultados fueron generados tres veces —dos en el
entorno de desarrollo y una en una copia limpia, borrando previamente `resultados/` y
`figuras/`— y son byte a byte idénticos en las tres corridas.
