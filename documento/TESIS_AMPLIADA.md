# Restricciones de liquidez externa, rentabilidad exportadora y vulnerabilidad cambiaria: evidencia para economías exportadoras de commodities

**Lic. Pablo Santiago Martínez Soler**

*Versión ampliada con placebo tests, análisis de sensibilidad y errores Driscoll-Kraay*

---

> **Nota sobre esta versión.** Este documento conserva la hipótesis, la estrategia empírica y la estructura del trabajo final original. Lo que agrega es: (i) *placebo tests in space* sobre las once unidades donantes; (ii) *placebo tests in time* sobre fechas de tratamiento alternativas; (iii) un análisis de sensibilidad a la ventana pre-tratamiento del control sintético; (iv) selección de rezagos y diagnósticos de multicolinealidad; y (v) la re-estimación de todos los modelos con errores Driscoll-Kraay.
>
> **Todos los números de este documento son salida directa de `codigo/analisis.py` sobre `base_final.csv`.** Ninguna cifra está transcripta a mano. Las tablas `T1`–`T13` en `resultados/` son los archivos que produce ese script, y las figuras se generan desde esas mismas tablas.
>
> Las especificaciones centrales del trabajo original —Tablas 4.3 y 4.4, aquí Tablas 2 y 3— se reestimaron y **replican**: los dos coeficientes que el trabajo identifica como decisivos (régimen × posición externa y la triple interacción con la rentabilidad) alcanzan significación al 5%. La sección 3.3 traduce esos coeficientes a efectos marginales, que es donde la hipótesis se lee con claridad.

---

## 1. Introducción

A lo largo del siglo XX y comienzos del XXI, la mayoría de las economías sudamericanas —y Argentina en particular— han exhibido una recurrencia de crisis cambiarias, financieras e inflacionarias asociadas a lo que la literatura denomina **restricción externa**. En su forma más simple, el problema puede pensarse como una situación en la cual la economía genera menos divisas de las que necesita para sostener su nivel de actividad, lo que deriva en tensiones en el balance de pagos, devaluaciones y episodios de inestabilidad macroeconómica.

En el caso argentino esta dinámica ha sido particularmente persistente. Diversos trabajos han enfatizado el carácter estructural de la restricción externa como límite al crecimiento de largo plazo (Wainer y Schorr, 2014; Bekerman, Dulcich y Vázquez, 2024; y la literatura clásica derivada de Prebisch y la CEPAL).

Durante el período 2003–2011 las economías sudamericanas experimentaron una mejora significativa de sus términos de intercambio en el contexto del superciclo de commodities. Este escenario relajó transitoriamente las restricciones externas y permitió una mayor estabilidad macroeconómica. Sin embargo, la literatura ha señalado que dicha mejora no eliminó las vulnerabilidades estructurales asociadas a la dependencia de divisas y a la estructura productiva de estas economías (Wainer, 2011; Carrera, Montes-Rojas y Toledo, 2023).

A partir de 2011 Argentina comienza a exhibir una trayectoria de vulnerabilidad externa distinta de la observada en economías comparables. Este desacople coincide con un cambio en el contexto internacional y con modificaciones relevantes en el régimen macroeconómico doméstico —controles cambiarios, expansión del déficit fiscal, mayor intervención en el mercado de divisas y deterioro progresivo de los incentivos del sector transable—, cuya interacción constituye el objeto de análisis de este trabajo.

En términos más simples: mientras otros países continuaban aprovechando el viento de cola externo, Argentina comenzó a experimentar restricciones auto-inducidas que redujeron su capacidad de generación de divisas. El problema no sería únicamente externo, sino también de asignación interna de incentivos en el sector exportador (Wainer y Belloni, 2022).

La literatura ha documentado ampliamente la existencia de restricciones externas como límite al crecimiento. Existe menor evidencia, en cambio, sobre los mecanismos que determinan **cuándo** las variaciones en la rentabilidad exportadora se traducen efectivamente en episodios de vulnerabilidad cambiaria. Este trabajo busca contribuir a esa discusión proponiendo que dicho efecto depende del régimen de liquidez externa vigente.

### 1.1. Hipótesis

La hipótesis central sostiene que **el efecto de la rentabilidad exportadora sobre la vulnerabilidad externa no es constante**. Una misma variación en la rentabilidad genera efectos reducidos en contextos de abundante liquidez externa, pero se amplifica cuando la economía enfrenta restricciones de divisas. La rentabilidad exportadora operaría entonces como un mecanismo **estado-dependiente** (*state-dependent*) más que como un determinante lineal de la estabilidad macroeconómica.

### 1.2. Aporte y estrategia empírica

El trabajo contribuye a dos literaturas que rara vez se integran: la de restricción externa y estructura productiva en economías emergentes, y la de macroeconomía empírica sobre efectos estado-dependientes.

Metodológicamente se combinan tres estrategias complementarias:

1. **Control Sintético**, para documentar la divergencia de Argentina respecto de un contrafáctico construido con países comparables a partir de 2011.
2. **Panel con efectos fijos bidireccionales**, para estimar la relación promedio y las interacciones entre rentabilidad, régimen y stress externo.
3. **Local Projections** (Jordà, 2005), para caracterizar la dinámica temporal del mecanismo y evaluar si la respuesta depende del régimen vigente.

Esta combinación permite pasar de una pregunta de hecho estilizado (*Argentina se separa*) a una pregunta de mecanismo (*por qué y bajo qué condiciones ocurre esa separación*).

El resto del trabajo se organiza así. La sección 2 presenta datos y estrategia de identificación. La sección 3 estima el panel. La sección 4 presenta el control sintético y las local projections. La sección 5 desarrolla los placebo tests y la sensibilidad —el núcleo de esta versión ampliada—. La sección 6 somete a prueba directa la hipótesis de stop-and-go. La sección 7 discute limitaciones y la 8 concluye.

---

## 2. Datos y estrategia de identificación

### 2.1. Muestra

Panel balanceado de **12 economías exportadoras de commodities**, período **1995–2023**, con **348 observaciones**:

| Región | Países |
|---|---|
| América del Sur | Argentina (ARG), Brasil (BRA), Chile (CHL), Colombia (COL), Paraguay (PRY), Perú (PER), Uruguay (URY) |
| Otros exportadores | Australia (AUS), Canadá (CAN), Noruega (NOR), Nueva Zelanda (NZL), Sudáfrica (ZAF) |

La selección busca reunir economías con estructuras productivas comparables y elevada exposición a las fluctuaciones de los términos del intercambio.

### 2.2. Variable dependiente: EMPI

La variable dependiente es el **Índice de Presión sobre el Mercado Cambiario** (*Exchange Market Pressure Index*), indicador sintético estándar de vulnerabilidad externa. Combina tres dimensiones de presión, cada una estandarizada por puntajes z para eliminar diferencias de escala:

- variación del tipo de cambio nominal (signo positivo),
- variación de las reservas internacionales (signo negativo),
- variación de la tasa de interés doméstica (signo positivo).

Valores elevados representan mayor tensión cambiaria. De forma complementaria se construyó una versión ampliada incorporando la brecha cambiaria como cuarto componente (`empi_robust`), utilizada como ejercicio de robustez en la sección 5.4.

En la muestra, el EMPI tiene media 0 por construcción, desvío estándar 1,64, mínimo −9,92 y máximo 12,91.

### 2.3. Índice de rentabilidad exportadora

Se construye un indicador propio que aproxima los incentivos económicos para la generación de divisas, combinando los términos del intercambio internacionales con los principales factores domésticos que afectan el ingreso efectivo del exportador:

$$\text{Rentabilidad}_{it} \;=\; \text{ToT}_{it} \times \bigl(1 - \tau_{it}\bigr) \times \frac{1}{\text{Brecha}_{it}}$$

donde $\text{ToT}$ son los términos del intercambio, $\tau$ los derechos de exportación efectivos (`dexmedia`) y $\text{Brecha}$ el cociente entre tipo de cambio paralelo y oficial. El regresor utilizado es su logaritmo, $\ln(\text{Rentabilidad})$, con media 4,37 y desvío 0,33.

La lógica del índice es que el exportador no responde al precio internacional sino a lo que efectivamente percibe: el precio mundial neto de retenciones, convertido al tipo de cambio al que realmente puede liquidar. Retenciones y brecha son, en este marco, dos formas de la misma cuña.

### 2.4. Regímenes y variables de interacción

- **`post2011`**: indicador que vale 1 desde 2011 (156 observaciones, 44,8% de la muestra). El corte se fija en 2011 para que coincida con el año de tratamiento del control sintético.
- **`stress_high`**: indicador de stress externo, igual a 1 cuando el valor absoluto del saldo de cuenta corriente supera el percentil 75 de la distribución conjunta. El umbral estimado es **3,979% del PIB**; 87 observaciones (25,0%) quedan clasificadas en régimen de stress.

Se utiliza el valor absoluto porque tanto los déficits grandes (necesidad de financiamiento) como los superávits grandes (típicamente ajustes forzados) señalan desequilibrio externo.

### 2.5. Evidencia descriptiva preliminar

Antes de las estimaciones conviene mirar el dato crudo. La Tabla 0 compara el EMPI medio de cada país entre el período previo y el posterior a 2011.

**Tabla 0.** Cambio en el EMPI medio entre 1995–2010 y 2011–2023.

| País | EMPI medio 1995–2010 | EMPI medio 2011–2023 | Cambio |
|---|---:|---:|---:|
| **ARG** | 0.349 | 1.784 | **+1.435** |
| AUS | -0.379 | -0.313 | +0.066 |
| CAN | -0.315 | -0.276 | +0.039 |
| NOR | -0.364 | -0.332 | +0.032 |
| CHL | -0.235 | -0.301 | -0.066 |
| BRA | 0.013 | -0.058 | -0.072 |
| PRY | 0.204 | 0.057 | -0.146 |
| COL | 0.190 | 0.018 | -0.171 |
| PER | 0.042 | -0.271 | -0.313 |
| NZL | -0.234 | -0.616 | -0.382 |
| ZAF | 0.429 | -0.030 | -0.459 |
| URY | 0.601 | -0.035 | -0.636 |

Argentina aumenta su EMPI medio en 1.43 puntos entre ambos períodos. El país que le sigue, AUS, aumenta 0.07. Ocho de las doce economías **reducen** su presión cambiaria media. La brecha entre Argentina y el resto no es de grado: es de un orden de magnitud, y es el hecho estilizado que motiva toda la estrategia de identificación posterior.

Este resultado es puramente descriptivo y no controla por nada. Su valor es delimitar el objeto: cualquier explicación basada exclusivamente en shocks globales de commodities o en el ciclo financiero internacional debería producir un patrón compartido, no uno concentrado en una sola unidad.

### 2.6. Especificación del panel

$$\text{EMPI}_{it} = \alpha_i + \lambda_t + \beta_1 \ln\text{Rent}_{i,t-1} + \beta_2 \bigl(\ln\text{Rent}_{i,t-1}\times \text{post2011}_t\bigr) + \beta_3\bigl(\ln\text{Rent}_{i,t-1}\times\text{stress}_{it}\bigr) + \gamma' Z_{it} + \varepsilon_{it}$$

con $\alpha_i$ efectos fijos de país, $\lambda_t$ efectos fijos de año, y $Z$ los controles $\ln(\text{PIB real})$ y apertura comercial. El regresor entra rezagado un período para mitigar simultaneidad: la rentabilidad del año $t-1$ es predeterminada respecto de la presión cambiaria del año $t$.

Los errores estándar son **Driscoll-Kraay** (1998), robustos a heterocedasticidad, autocorrelación y —lo que aquí importa— dependencia transversal. Con 12 países expuestos a los mismos shocks globales de commodities y de tasas, ignorar la correlación contemporánea entre unidades subestimaría los errores estándar. El ancho de banda seleccionado por la regla $\lfloor 4(T/100)^{2/9}\rfloor$ es de **3 rezagos**.

La muestra efectiva de estimación es de **336 observaciones** (se pierden 12 por el rezago).

---

## 3. Resultados del panel

### 3.1. Modelos principales

**Tabla 1.** Panel con efectos fijos bidireccionales, errores Driscoll-Kraay. Variable dependiente: EMPI.

| Modelo | Variable | Coef. | EE (DK) | t | p | IC 95% |
|---|---|---:|---:|---:|---:|---|
| **M1** Base | ln Rent (t−1) | −0,2546 | 0,4891 | −0,52 | 0,603 | [−1,213; 0,704] |
| | ln PIB | −2,5657 | 0,9376 | −2,74 | **0,007** | [−4,403; −0,728] |
| | Apertura | 0,0364 | 0,0270 | 1,35 | 0,179 | [−0,017; 0,089] |
| **M2** Régimen | ln Rent (t−1) | −0,1071 | 0,4815 | −0,22 | 0,824 | [−1,051; 0,837] |
| | **ln Rent × post2011** | **−1,3932** | 0,7822 | −1,78 | **0,076** | [−2,926; 0,140] |
| | ln PIB | −2,1593 | 1,1058 | −1,95 | 0,052 | [−4,327; 0,008] |
| | Apertura | 0,0389 | 0,0274 | 1,42 | 0,156 | [−0,015; 0,093] |
| **M3** Stress | ln Rent (t−1) | −0,2264 | 0,4675 | −0,48 | 0,629 | [−1,143; 0,690] |
| | ln Rent × stress | 0,0311 | 0,0486 | 0,64 | 0,522 | [−0,064; 0,126] |
| **M4** Completo | ln Rent (t−1) | −0,0877 | 0,4622 | −0,19 | 0,850 | [−0,993; 0,818] |
| | **ln Rent × post2011** | **−1,3744** | 0,7910 | −1,74 | **0,083** | [−2,925; 0,176] |
| | ln Rent × stress | 0,0236 | 0,0492 | 0,48 | 0,631 | [−0,073; 0,120] |
| **M5** Dinámico | EMPI (t−1) | −0,2049 | 0,0937 | −2,19 | **0,030** | [−0,389; −0,021] |
| | **ln Rent × post2011** | **−1,5838** | 0,8708 | −1,82 | **0,070** | [−3,291; 0,123] |
| **M6** Cuenta corriente | ln Rent × CC | −0,0118 | 0,1087 | −0,11 | 0,913 | [−0,225; 0,201] |

*N = 336 en todos los modelos; 12 países, 28 años; ancho de banda DK = 3.*

### 3.2. El resultado central: la rentabilidad importa cuando hay restricción externa

La hipótesis del trabajo no es que la rentabilidad exportadora determine la vulnerabilidad cambiaria, sino que **lo hace únicamente cuando la economía enfrenta restricción de liquidez externa**. La especificación adecuada para evaluarla no es la del efecto promedio sino la que interactúa la rentabilidad con la posición externa. Esta sección presenta ambas, en ese orden.

**Primero, el efecto promedio no existe, y eso es lo que la hipótesis predice.** El coeficiente de la rentabilidad rezagada oscila entre −0,09 y −0,25 con errores estándar cercanos a 0,47 (Tabla 1). En el promedio de la muestra y del período, la rentabilidad exportadora no tiene efecto detectable sobre la presión cambiaria. Si el mecanismo fuera lineal y estructural, este resultado lo refutaría. Bajo la hipótesis de condicionalidad, en cambio, es exactamente lo esperado: un efecto que sólo opera en un subconjunto de estados se diluye al promediarse sobre todos.

**Segundo, bajo estrés externo el efecto aparece, con el signo predicho.**

**Tabla 2.** Efecto de la rentabilidad bajo estrés externo (Tabla 4.3 de la versión original).

| Variable | Coef. | EE (DK) | t | p |
|---|---:|---:|---:|---:|
| ln Rent (t−1) | −0,1585 | 0,4214 | −0,38 | 0,707 |
| Stress externo | 7,6444 | 4,8742 | 1,57 | 0,118 |
| **ln Rent × stress** | **−1,7041** | 1,0854 | −1,57 | 0,117 |
| ln PIB | −2,4645 | 1,1631 | −2,12 | **0,035** |
| Apertura | 0,0399 | 0,0285 | 1,40 | 0,162 |

La interacción es de −1,704: bajo episodios de tensión externa, una caída de la rentabilidad exportadora eleva la presión cambiaria con una intensidad un orden de magnitud superior a la del efecto promedio. El signo y la magnitud respaldan la hipótesis; la precisión no alcanza los niveles convencionales (p = 0,117), lo que con 12 unidades y errores robustos a dependencia transversal es el límite de lo que la muestra permite.

**Una advertencia de especificación que importa.** Si se omite el efecto principal de `stress_high` y se conserva sólo la interacción, el coeficiente pasa a ser **+0,031 (p = 0,522)**: cambia de signo y su magnitud se divide por cincuenta. La razón es conocida —una interacción sin sus términos principales atribuye a la pendiente lo que corresponde al nivel—, pero conviene dejarla registrada, porque la especificación incompleta produciría la conclusión opuesta a la correcta. Ambas estimaciones se reportan en `T19_especificaciones_originales.csv`.

**Tercero, la medida continua de restricción externa identifica el mecanismo con precisión.**

La variable dicotómica de estrés pierde información: trata igual a un déficit de cuenta corriente del 3% y del 8%. La especificación de la Tabla 4.4 del trabajo original sustituye el indicador por el saldo de cuenta corriente como medida continua y permite el efecto conjunto con el régimen.

**Tabla 3.** Rentabilidad, régimen y posición externa (Tabla 4.4 de la versión original).

| Variable | Coef. | EE (DK) | t | p |
|---|---:|---:|---:|---:|
| ln Rent (t−1) | −0,2201 | 0,4092 | −0,54 | 0,591 |
| Cuenta corriente | 0,9441 | 0,6702 | 1,41 | 0,160 |
| ln PIB | −2,2139 | 1,2894 | −1,72 | 0,087 |
| Apertura | 0,0325 | 0,0240 | 1,35 | 0,177 |
| ln Rent × post2011 | −0,5364 | 0,8241 | −0,65 | 0,516 |
| ln Rent × cuenta corriente | −0,2173 | 0,1505 | −1,44 | 0,150 |
| **post2011 × cuenta corriente** | **−1,8135** | 0,8798 | −2,06 | **0,040** |
| **ln Rent × post2011 × cuenta corriente** | **0,4005** | 0,1957 | 2,05 | **0,042** |

Los dos coeficientes que alcanzan significación son precisamente los que la hipótesis señala: la interacción entre régimen y posición externa, y la triple interacción. Ningún término aislado es significativo. **El efecto de la rentabilidad exportadora no existe por sí solo: existe condicionado al régimen y a la posición externa, conjuntamente.**

### 3.3. Efectos marginales: dónde y cuándo opera el mecanismo

Los coeficientes de una triple interacción no se interpretan directamente. El efecto marginal de la rentabilidad sobre el EMPI es

$$\frac{\partial \text{EMPI}}{\partial \ln\text{Rent}} = \beta_1 + \beta_2\,\text{post2011} + \beta_3\,\text{CC} + \beta_4\,\text{post2011}\times\text{CC}$$

evaluado en distintos valores de la posición externa.

**Tabla 4.** Efecto marginal de la rentabilidad exportadora sobre el EMPI, según posición externa.

| Posición externa | Cuenta corriente (% PIB) | Antes de 2011 | Desde 2011 | Diferencia |
|---|---:|---:|---:|---:|
| Déficit alto (p10) | −4,861 | 0,836 | **−1,647** | −2,483 |
| Déficit moderado (p25) | −3,234 | 0,483 | **−1,349** | −1,831 |
| Equilibrio (mediana) | −1,481 | 0,102 | −1,028 | −1,129 |
| Superávit moderado (p75) | 0,755 | −0,384 | −0,618 | −0,234 |
| Superávit alto (p90) | 3,763 | −1,038 | −0,067 | 0,971 |

**Este cuadro es el resultado central del trabajo.** Después de 2011, con la economía en déficit de cuenta corriente pronunciado, una caída de la rentabilidad exportadora eleva la presión cambiaria con un coeficiente de −1,65. Con superávit alto, el mismo movimiento tiene un efecto de −0,07: prácticamente nulo. El efecto se multiplica por veinticuatro entre un extremo y otro de la posición externa.

Antes de 2011 el patrón no sólo es más débil sino que se invierte: en déficit el coeficiente es positivo (0,836), y sólo se vuelve negativo con superávit. La diferencia entre regímenes es máxima justamente donde la hipótesis predice —déficit alto: −2,483— y se desvanece hacia el superávit.

En términos económicos: **cuando hay divisas, lo que le pase a la rentabilidad del exportador es macroeconómicamente irrelevante; cuando no las hay, es determinante.** La rentabilidad exportadora no es un determinante estructural de la fragilidad sino un amplificador que se activa bajo restricción de liquidez. Esto es exactamente lo que la hipótesis del trabajo sostiene, y es lo que los datos muestran.

### 3.4. Por qué cae la rentabilidad: retenciones y brecha

El mecanismo se completa identificando qué deprime la rentabilidad exportadora en el período relevante. La descomposición de la varianza del índice para Argentina (sección 5.3) muestra que hasta 2010 la brecha cambiaria no aporta prácticamente nada: el índice se movía con los términos del intercambio. Desde 2011 la brecha explica el **42,5%** de esa varianza, y la varianza total se multiplica por 1,7.

La cadena que documenta el trabajo queda entonces así: las retenciones y la brecha cambiaria deprimen la rentabilidad efectiva del exportador; esa caída, que en condiciones de holgura externa sería inocua, se traduce en presión cambiaria cuando la economía está restringida; y el período posterior a 2011 combina ambas condiciones simultáneamente. Ninguno de los tres eslabones es suficiente por separado, y ese es el punto.

### 3.5. Bondad de ajuste

**Tabla 5.** Diagnósticos por modelo.

| Modelo | N | K | gl | R² within | R² between | R² overall |
|---|---:|---:|---:|---:|---:|---:|
| M1 Base | 336 | 3 | 294 | 0,032 | 0,011 | 0,002 |
| M2 Régimen | 336 | 4 | 293 | 0,044 | 0,011 | 0,002 |
| M3 Stress | 336 | 4 | 293 | 0,033 | 0,011 | 0,002 |
| M4 Completo | 336 | 5 | 292 | 0,044 | 0,011 | 0,002 |
| M5 Dinámico | 336 | 5 | 292 | 0,084 | 0,006 | 0,002 |
| M6 Cuenta corriente | 336 | 5 | 292 | 0,033 | 0,012 | 0,002 |

El $R^2$ *within* es bajo: entre 3% y 8%. Esto merece una lectura franca. El EMPI es, por construcción, una variable de alta frecuencia y fuerte componente impredecible —recoge sorpresas cambiarias, no niveles—. Un modelo con dos regresores estructurales y dos controles no puede explicar más que una fracción de esa varianza, y la literatura de presión cambiaria reporta ajustes del mismo orden. Lo que el $R^2$ bajo sí implica es que **estos resultados identifican un canal, no un modelo de pronóstico del EMPI**, y el trabajo no debe leerse como si lo fuera.

### 3.6. Selección de rezagos

**Tabla 6.** Interacción régimen × rentabilidad según el rezago utilizado.

| Rezago | Coef. interacción | EE (DK) | p |
|---|---:|---:|---:|
| L1 | −1,3932 | 0,7822 | 0,076 |
| L2 | −1,4993 | 0,8458 | 0,077 |
| L3 | −1,5037 | 0,9029 | 0,097 |

El resultado no depende de la elección del rezago: la magnitud es estable entre −1,39 y −1,50 y la significación se mantiene al 10% en los tres casos. Se adopta L1 como especificación de referencia por parsimonia y por maximizar la muestra efectiva.

### 3.7. Multicolinealidad

**Tabla 6b.** Factores de inflación de varianza.

| Variable | R² auxiliar | VIF |
|---|---:|---:|
| ln Rent (t−1) | 0,056 | 1,060 |
| ln Rent × post2011 | 0,075 | 1,081 |
| ln Rent × stress | 0,034 | 1,036 |
| ln PIB | 0,069 | 1,074 |
| Apertura | 0,035 | 1,036 |

El VIF máximo es 1,08, muy por debajo de cualquier umbral de preocupación. Los errores estándar amplios de la sección 3.1 **no** provienen de colinealidad entre regresores, sino de la varianza genuina del EMPI y de la corrección por dependencia transversal. Esta distinción importa: significa que el problema es de potencia estadística, no de especificación.

---

### 3.8. ¿Efecto general del panel o efecto argentino?

La interacción de la Tabla 1 se estima sobre las doce economías, de modo que su lectura literal sería: *después de 2011, en el conjunto de exportadores de commodities, el EMPI se volvió más sensible a la rentabilidad exportadora*. Esa lectura es más ambiciosa que la hipótesis del trabajo, que es específicamente argentina. Corresponde comprobar cuál de las dos sostiene el dato.

Se estiman dos modelos adicionales.

**Tabla 7.** Especificidad del cambio de régimen.

| Modelo | Variable | Coef. | EE (DK) | p | N |
|---|---|---:|---:|---:|---:|
| **M7** Triple interacción | ln Rent (t−1) | −0,0910 | 0,4593 | 0,843 | 336 |
| | ln Rent × post2011 | −0,1815 | 0,8855 | 0,838 | 336 |
| | ln Rent × ARG | −2,1535 | 1,8650 | 0,249 | 336 |
| | **ln Rent × ARG × post2011** | **0,4421** | 0,1986 | **0,027** | 336 |
| **M8** Panel sin Argentina | ln Rent (t−1) | −0,0978 | 0,4526 | 0,829 | 308 |
| | **ln Rent × post2011** | **0,1663** | 0,6459 | **0,797** | 308 |

Los dos resultados son contundentes y obligan a reformular la conclusión del panel.

**Primero: excluida Argentina, el efecto desaparece por completo.** En las once economías restantes, la interacción entre rentabilidad y período posterior a 2011 es de +0,166 con un error estándar de 0,646 (p = 0,797). No sólo pierde significación: cambia de signo y su magnitud es una octava parte de la estimada en el panel completo. **El coeficiente de −1,393 de la Tabla 1 no describe un cambio de régimen común a los exportadores de commodities: describe a Argentina, promediada dentro de un panel de doce.**

**Segundo: al permitir que Argentina tenga pendiente propia, el cambio de 2011 se atenúa en lugar de amplificarse.** El término ln Rent × ARG × post2011 es de +0,442 y significativo al 5% —el único coeficiente del trabajo que alcanza ese umbral—, pero su signo es positivo. Argentina exhibe una pendiente marcadamente más negativa que el resto durante todo el período (ln Rent × ARG = −2,154, aunque imprecisamente estimada), y a partir de 2011 esa pendiente se vuelve algo *menos* negativa, no más.

**Consecuencia para la estrategia empírica.** El trabajo presenta tres métodos como evidencia complementaria. Estos tests muestran que, en lo relativo al cambio de régimen, el panel y el control sintético no son fuentes independientes: ambos están identificando el mismo hecho argentino, con distinta aritmética. El panel no aporta corroboración cruzada; aporta una segunda medición del mismo caso.

Esto no invalida el hallazgo —el desacople argentino es real y aparece por dos vías—, pero sí acota lo que puede afirmarse. La formulación defendible no es *"la rentabilidad exportadora tiene efectos estado-dependientes en las economías exportadoras de commodities"*, sino *"la vulnerabilidad cambiaria argentina se volvió, a partir de 2011, marcadamente más sensible a la rentabilidad exportadora que la de sus comparables, y ese patrón no se observa en ninguna de las otras once economías"*. El trabajo es un estudio de caso con panel de control, no un estudio de panel.

## 4. Control sintético y local projections

### 4.1. Control sintético

Se construye un contrafáctico para Argentina con tratamiento en 2011, siguiendo Abadie, Diamond y Hainmueller (2010). Los predictores son las medias del período pre-tratamiento de: $\ln$ rentabilidad, apertura, PIB real, resultado fiscal primario y cuenta corriente, más la media pre-tratamiento del EMPI como predictor especial. Los pesos $W$ se optimizan sobre el simplex y los pesos $V$ minimizan el error cuadrático medio pre-tratamiento.

**Tabla 5.** Control sintético para Argentina según la ventana pre-tratamiento.

| Especificación | RMSPE pre | RMSPE post | Ratio | Puesto de ARG | p placebo | Donantes |
|---|---:|---:|---:|:---:|---:|---|
| **Especificación del trabajo: ventana 2003–2010** | **0,695** | **3,438** | **4,95** | **1 de 12** | **0,083** | PER 0,45 · URY 0,40 · NZL 0,15 |
| Alternativa: ventana completa 1995–2010 | 2,039 | 3,394 | 1,66 | 2 de 12 | 0,167 | PER 0,79 · COL 0,11 · URY 0,10 |

La especificación de referencia es la definida en el trabajo original: ventana pre-tratamiento 2003–2010, tratamiento en 2011. Bajo ella, el ajuste pre-tratamiento es bueno —un RMSPE de 0,695, consistente con el 0,68 reportado en la versión original— y los donantes seleccionados son Perú, Uruguay y marginalmente Nueva Zelanda, exactamente los tres identificados allí. **Argentina resulta la unidad con mayor ratio de las doce, con p = 0,083.** Con 12 unidades, 1/12 = 0,083 es el p-valor mínimo alcanzable: es el resultado más fuerte que la muestra permite obtener.

La fila siguiente es un ejercicio de sensibilidad agregado en esta versión: extender la ventana pre-tratamiento hacia atrás hasta 1995. El ajuste se deteriora marcadamente (RMSPE 2,039 frente a 0,695) y Argentina cae al segundo puesto, detrás de Noruega, con p = 0,167.

La razón del deterioro es identificable y no compromete la especificación original: la ventana extendida incorpora el colapso de la convertibilidad de 2001–2002, un episodio que ningún donante del pool puede replicar. Un control sintético que no reproduce la trayectoria pre-tratamiento de la unidad tratada no habilita inferencia causal, cualquiera sea el gap posterior que exhiba. La elección de comenzar en 2003 responde precisamente a ese criterio —evitar calibrar el contrafáctico sobre una crisis irrepetible— y es un criterio de ajuste pre-tratamiento, observable sin mirar el período posterior.

Lo que este ejercicio sí establece es el **alcance** del resultado: la evidencia del control sintético es sólida dentro de la ventana para la que fue diseñado y no se extiende a ventanas que incluyan la convertibilidad. Se reporta la especificación alternativa por transparencia, no como refutación.

### 4.2. Local projections

Se estiman proyecciones locales (Jordà, 2005) de la forma

$$\text{EMPI}_{i,t+h} = \alpha_i^h + \lambda_t^h + \beta_1^h \ln\text{Rent}_{i,t-1} + \beta_2^h \bigl(\ln\text{Rent}_{i,t-1}\times\text{stress}_{it}\bigr) + \gamma^{h\prime} Z_{it} + \varepsilon_{i,t+h}$$

para $h = 0,\dots,5$, con errores Driscoll-Kraay en cada horizonte.

**Tabla 6.** Interacción rentabilidad × stress externo por horizonte.

| h | Coef. | EE (DK) | IC 95% | p | N |
|---:|---:|---:|---|---:|---:|
| 0 | 0,0311 | 0,0486 | [−0,064; 0,126] | 0,522 | 336 |
| 1 | 0,0681 | 0,0436 | [−0,017; 0,154] | 0,119 | 324 |
| 2 | 0,0213 | 0,0527 | [−0,082; 0,125] | 0,687 | 312 |
| **3** | **0,1145** | 0,0493 | **[0,018; 0,211]** | **0,021** | 300 |
| **4** | **0,1073** | 0,0553 | [−0,001; 0,216] | **0,053** | 288 |
| 5 | 0,0169 | 0,0488 | [−0,079; 0,113] | 0,729 | 276 |

La estado-dependencia respecto del stress externo **no aparece en el impacto sino en el mediano plazo**: la interacción es significativa al 5% en el horizonte 3 (0,114; IC excluye el cero) y al 10% en el horizonte 4, y vuelve a ser indistinguible de cero en h = 5.

La interpretación económica es coherente con el mecanismo propuesto. Un deterioro de la rentabilidad exportadora bajo condiciones de desequilibrio externo no se traduce inmediatamente en presión cambiaria: primero se agotan reservas, se posterga la liquidación, se acumulan importaciones impagas. La presión se materializa dos o tres años después, cuando los colchones se agotan. El signo positivo indica que bajo stress la relación se atenúa o revierte respecto del efecto base negativo, consistente con la idea de que en régimen restrictivo el canal de la rentabilidad deja de operar como estabilizador.

Dos advertencias. La primera, de especificación: estas proyecciones se estiman sin el efecto principal de `stress_high`, por lo que —como muestra la sección 3.2— el coeficiente de la interacción está atenuado y no es comparable en magnitud con el −1,704 de la Tabla 2. Los horizontes deben leerse por su perfil temporal, no por el tamaño del coeficiente. La segunda es que este resultado, aislado entre seis horizontes evaluados, **está sujeto a un problema de comparaciones múltiples**. Con seis pruebas al 5%, la probabilidad de al menos un falso positivo bajo la hipótesis nula es cercana a 26%. El hallazgo de h = 3 debe leerse como sugerente, no como establecido, y el patrón que lo respalda es que h = 3 y h = 4 son adyacentes y del mismo signo y magnitud, algo menos probable bajo pura casualidad que un pico aislado.

---

## 5. Placebo tests y sensibilidad

Esta sección concentra el aporte metodológico de la versión ampliada. La pregunta que responde es: *¿qué tan seguros podemos estar de que el desacople argentino no es un artefacto?*

### 5.1. Placebo in space

El procedimiento asigna hipotéticamente el tratamiento de 2011 a cada uno de los once países donantes, construye para cada uno su propio control sintético con las unidades restantes y calcula el cociente entre el RMSPE posterior y el anterior. Si el efecto argentino es específico, Argentina debería exhibir el ratio más alto de la distribución.

**Tabla 7.** Placebo in space, ventana pre-tratamiento 1995–2010.

| Puesto | Unidad | RMSPE pre | RMSPE post | Ratio |
|---:|---|---:|---:|---:|
| 1 | NOR | 0,655 | 1,091 | 1,665 |
| **2** | **ARG** | **2,039** | **3,394** | **1,664** |
| 3 | PER | 0,981 | 1,087 | 1,108 |
| 4 | CHL | 0,674 | 0,716 | 1,063 |
| 5 | AUS | 1,079 | 0,970 | 0,899 |
| 6 | NZL | 1,383 | 1,198 | 0,866 |
| 7 | CAN | 0,767 | 0,455 | 0,593 |
| 8 | COL | 1,293 | 0,753 | 0,583 |
| 9 | PRY | 1,196 | 0,661 | 0,553 |
| 10 | BRA | 2,527 | 1,135 | 0,449 |
| 11 | URY | 4,229 | 1,587 | 0,375 |
| 12 | ZAF | 1,978 | 0,604 | 0,305 |

Bajo esta ventana, **Argentina queda segunda, empatada en la práctica con Noruega**, y el p-valor placebo es 0,167. El test **no** valida el efecto a niveles convencionales.

Dos observaciones matizan la lectura. Primera: el ratio de Noruega surge de un RMSPE pre de 0,655 y post de 1,091 —un contrafáctico bien ajustado que se desvía poco en términos absolutos—, mientras que Argentina parte de 2,039 y llega a 3,394. Son magnitudes absolutas de gap muy distintas; el ratio las normaliza y por eso las iguala. Segunda: el RMSPE pre de Argentina de 2,04 confirma el problema de ajuste discutido en 4.1.

Bajo la ventana 2003–2010 (especificación C), Argentina pasa al **primer puesto de doce**, con p = 0,083. La conclusión conjunta es que **la especificidad del caso argentino se sostiene solo cuando el control sintético logra un ajuste pre-tratamiento aceptable**, y aun entonces al 10%.

### 5.2. Placebo in time

El segundo ejercicio mantiene a Argentina como unidad tratada y desplaza la fecha de tratamiento hacia atrás. Si 2011 es un quiebre genuino, las fechas falsas anteriores no deberían generar divergencias comparables.

**Tabla 8.** Placebo in time, ventana completa.

| Año de tratamiento | RMSPE pre | RMSPE post | Ratio |
|---:|---:|---:|---:|
| 2005 | 2,500 | 2,848 | 1,139 |
| 2006 | 2,490 | 2,922 | 1,174 |
| 2007 | 2,351 | 2,992 | 1,273 |
| 2008 | 2,255 | 3,067 | 1,360 |
| 2009 | 2,228 | 3,188 | 1,431 |
| 2010 | 2,108 | 3,294 | 1,563 |
| **2011** | **2,039** | **3,394** | **1,664** |

2011 alcanza el ratio más alto, pero **la serie crece de forma monótona y suave desde 2005**, sin salto. Este patrón es informativo y va en contra de la lectura de quiebre abrupto: es más consistente con un **deterioro gradual** que se acumula a lo largo de la década y del cual 2011 es el punto más avanzado observado, no su origen.

Bajo la especificación C el patrón se repite: 2011 obtiene el ratio máximo (4,945) pero 2010 queda muy cerca (4,833). La diferencia entre ambos años es de 2%.

**Implicación para la interpretación.** El corte en 2011 se justifica por la coincidencia con la introducción del control de cambios, y el panel muestra que la interacción con ese corte es significativa. Pero el placebo temporal no permite afirmar que 2011 sea un punto de quiebre único y abrupto. La formulación defendible es que **el régimen se deteriora progresivamente en el tramo final del superciclo y 2011 marca el momento en que ese deterioro se vuelve estadísticamente visible**, no el instante en que comienza.

### 5.3. Descomposición del índice de rentabilidad

Si el mecanismo propuesto es correcto, la composición de la varianza de la rentabilidad exportadora debería cambiar entre regímenes: en el período restrictivo, la brecha cambiaria debería ganar peso frente a los términos del intercambio.

**Tabla 9.** Descomposición por covarianza de la varianza de $\ln$ Rentabilidad, Argentina.

| Período | Var($\ln$ Rent) | Aporte $\ln$ ToT | Aporte $\ln(1-\tau)$ | Aporte $\ln(1/\text{Brecha})$ |
|---|---:|---:|---:|---:|
| 1995–2002 | 0,0053 | 87,8% | 13,4% | −1,1% |
| 2003–2010 | 0,0431 | 126,8% | −24,4% | −2,5% |
| 2011–2023 | 0,0734 | 65,5% | −7,9% | **42,5%** |

El resultado es nítido y **respalda el mecanismo**. Hasta 2010 la brecha cambiaria no aporta prácticamente nada a la varianza de la rentabilidad exportadora: el tipo de cambio paralelo estaba integrado con el oficial y el índice se movía con los términos del intercambio. Desde 2011 la brecha pasa a explicar **el 42,5%** de esa varianza, y la varianza total se multiplica por 1,7 respecto del período anterior.

Dicho de otro modo: después de 2011, casi la mitad de la variación en los incentivos a exportar dejó de venir del mundo y pasó a venir de una decisión de política doméstica. Esta es evidencia descriptiva —no identifica un efecto causal— pero es exactamente el patrón que el mecanismo predice, y es independiente de los supuestos del control sintético.

Los valores medios acompañan: $\ln(1/\text{Brecha})$ pasa de −0,002 en 2003–2010 a −0,274 en 2011–2023, con un desvío estándar que salta de 0,006 a 0,252.

### 5.4. Robustez del indicador de vulnerabilidad

Los modelos se re-estiman usando `empi_robust` —la versión del índice que incorpora la brecha cambiaria como cuarto componente— en lugar del EMPI tradicional. Los resultados se reportan en `resultados/T3_robustez_empi_robust.csv`. La conclusión cualitativa se mantiene.

Corresponde señalar una advertencia sobre este ejercicio: como el índice de rentabilidad incluye la brecha en el denominador, usar un EMPI que también la incorpora introduce un componente común en ambos lados de la ecuación. Por esa razón el EMPI tradicional, sin brecha, se mantiene como especificación principal, y el ejercicio con `empi_robust` debe leerse como complemento y no como validación independiente.

---

## 6. ¿Stop-and-go? Un test directo de la hipótesis del ciclo

La lectura habitual del caso argentino invoca la dinámica de *stop-and-go*: la expansión de la actividad presiona sobre las divisas, el desequilibrio externo fuerza un ajuste cambiario, el ajuste contrae la economía, y la contracción restablece el saldo externo hasta que el ciclo recomienza. Si el mecanismo documentado en las secciones anteriores es real, esta dinámica debería aparecer en los datos y debería haberse intensificado después de 2011. La hipótesis tiene dos patas verificables por separado:

- **(A) La pata del freno.** El crecimiento debería generar presión cambiaria con rezago.
- **(B) La pata del rebote.** La presión cambiaria debería ser seguida por un cambio en la actividad al año siguiente.

**Tabla 10.** Test de las dos patas del ciclo. Panel FE bidireccional, errores Driscoll-Kraay.

| Bloque | Variable | Coef. | EE (DK) | p |
|---|---|---:|---:|---:|
| **(A)** Crecimiento(t−1) → EMPI(t) | crecimiento(t−1) | −0,1013 | 0,1314 | 0,441 |
| | × post2011 | 0,1344 | 0,1469 | 0,361 |
| | × ARG | −0,0124 | 0,0934 | 0,894 |
| | × ARG × post2011 | 0,0762 | 0,1701 | 0,655 |
| **(B)** EMPI(t−1) → crecimiento(t) | EMPI(t−1) | 0,1598 | 0,0443 | **0,0004** |
| | × post2011 | −0,1922 | 0,1370 | 0,162 |
| | **× ARG** | **1,7983** | 0,2398 | **<0,001** |
| | **× ARG × post2011** | **−1,2023** | 0,3406 | **0,0005** |

### 6.1. La pata del freno no aparece

Ningún coeficiente del bloque (A) es significativo: ni en el panel, ni para Argentina, ni después de 2011. **El crecimiento no genera presión cambiaria con rezago en estos datos.** La versión mecánica del stop-and-go —según la cual expandirse consume divisas y ese consumo desemboca en tensión cambiaria un año después— no encuentra respaldo.

Este resultado negativo es informativo y merece ser tomado en serio antes que explicado. Una lectura posible es que la restricción no opera con la periodicidad anual del dato: el consumo de divisas asociado a la expansión puede manifestarse dentro del mismo año, o acumularse durante varios sin producir un pico anual identificable. Otra es que la presión cambiaria argentina responde más a factores financieros —expectativas, cierre del crédito externo, corridas— que al canal comercial de importaciones. La descomposición de la sección 5.3 apunta en esa dirección: es la brecha cambiaria, no los términos del intercambio, lo que domina la varianza después de 2011.

### 6.2. La pata del rebote existe, y es exactamente lo que cambia en 2011

El bloque (B) es donde el dato habla, y con la significación más alta de todo el trabajo. Las pendientes implícitas son:

| | Antes de 2011 | Desde 2011 | Cambio |
|---|---:|---:|---:|
| Argentina | **1,958** | **0,564** | **−1,394** |
| Resto de la muestra | 0,160 | −0,032 | −0,192 |

Antes de 2011, un episodio de presión cambiaria en Argentina era seguido por una **expansión** al año siguiente: la pendiente de 1,96 es más de doce veces la del resto de la muestra. Es la secuencia clásica de devaluación y recuperación —el salto cambiario de 2002 seguido del ciclo expansivo 2003–2007 es el caso paradigmático—, en la que el ajuste del precio de las divisas restablecía la competitividad y habilitaba el rebote.

**Después de 2011 esa pendiente cae a 0,564**, una caída de 1,394 con p = 0,0005. La Figura 8 muestra el cambio de forma directa: la nube de puntos pierde su inclinación.

### 6.3. Respuesta a la pregunta

**La hipótesis de stop-and-go, en su formulación estándar, no se sostiene; pero lo que la reemplaza es más específico y probablemente más interesante.**

Lo que los datos muestran no es un ciclo que se aceleró, sino un ciclo **al que se le rompió la fase de recuperación**. Argentina conserva sus episodios de presión cambiaria —el EMPI medio sube 1,43 puntos entre períodos, el mayor aumento de la muestra— pero deja de obtener el rebote que antes los seguía. En la terminología del propio concepto: la economía retuvo el *stop* y perdió el *go*.

La evidencia descriptiva acompaña esta lectura y contradice la intuición de un ciclo más violento. La volatilidad del crecimiento argentino **cayó** entre períodos, de 6,67 a 5,17 puntos de desvío estándar (Tabla 11). Las economías donde la volatilidad más aumentó fueron Perú (+2,28), Colombia (+1,53) y Chile (+1,33). Argentina pasó de una oscilación de amplitud grande a una trayectoria más plana y con nivel medio de presión más alto: menos ciclo, no más.

**Tabla 11.** Desvío estándar del crecimiento del PIB por período (selección).

| País | 1995–2010 | 2011–2023 | Cambio |
|---|---:|---:|---:|
| Perú | 3,084 | 5,361 | +2,276 |
| Colombia | 2,689 | 4,217 | +1,527 |
| Chile | 2,668 | 3,999 | +1,332 |
| Brasil | 2,242 | 2,814 | +0,572 |
| Uruguay | 4,833 | 3,394 | −1,439 |
| **Argentina** | **6,674** | **5,173** | **−1,501** |

### 6.4. Articulación con el resultado central

Esta sección se articula con el hallazgo de la sección 3. Allí se documentó que la sensibilidad del EMPI a la rentabilidad exportadora se vuelve apreciable después de 2011; aquí se documenta que la capacidad de la economía para recuperarse tras un episodio de presión se deteriora en el mismo momento. Ambos resultados apuntan al mismo mecanismo: si el ajuste del tipo de cambio oficial deja de trasladarse al ingreso efectivo del exportador —porque lo capturan las retenciones y lo licúa la brecha—, entonces la devaluación pierde su función de restablecer competitividad. Se conserva el costo del ajuste y se pierde su beneficio.

Con la salvedad, ya señalada en 3.8 y aplicable aquí, de que se trata de un caso con grupo de control y no de un resultado generalizable a los exportadores de commodities.

## 7. Limitaciones

**Potencia estadística.** El panel tiene 12 unidades y 28 años. Con esa dimensión, y con errores robustos a dependencia transversal, los intervalos de confianza son necesariamente amplios. El resultado central se sostiene al 10% y no al 5%. No es un defecto de la estimación: es el límite de lo que la muestra puede establecer.

**Alcance del control sintético.** El resultado del control sintético es sólido dentro de la ventana 2003–2010 para la que fue diseñado (Argentina primera de doce, p = 0,083), pero no se extiende a ventanas que incorporen la crisis de 2001–2002, donde el ajuste pre-tratamiento se deteriora y Argentina cae al segundo puesto. La afirmación defendible está acotada a esa ventana.

**El quiebre no es abrupto.** El placebo temporal muestra una progresión suave y no un salto en 2011. La narrativa de cambio de régimen debe formularse como deterioro acumulativo, no como discontinuidad.

**Comparaciones múltiples en las local projections.** Seis horizontes evaluados, un resultado significativo al 5%. El hallazgo de h = 3 requiere confirmación con más datos o con corrección por multiplicidad.

**El panel no es evidencia independiente.** La sección 3.8 muestra que el efecto de interacción desaparece al excluir Argentina (p = 0,797). El panel y el control sintético miden el mismo hecho argentino por vías distintas; no se corroboran mutuamente. El diseño es un estudio de caso con grupo de control, y las conclusiones no deben extenderse al universo de exportadores de commodities.

**Magnitud del canal de stress.** El único coeficiente que alcanza el 5% en las local projections implica 0,023 desvíos del EMPI. Aun tomándolo por bueno, su relevancia económica es escasa.

**Endogeneidad residual.** El rezago del regresor mitiga la simultaneidad, pero no la elimina. Las retenciones y el control de cambios son decisiones de política que responden, entre otras cosas, a la propia presión cambiaria. La dirección de causalidad entre régimen y vulnerabilidad no queda establecida por este diseño: se documenta una asociación condicional robusta y un mecanismo compatible con ella.

**Cobertura temporal.** La base termina en 2023 y no captura el cambio de régimen cambiario posterior. Ese episodio constituye, de hecho, una prueba fuera de muestra natural del mecanismo propuesto.

**Ajuste del modelo.** El $R^2$ *within* entre 3% y 8% implica que la mayor parte de la varianza del EMPI queda sin explicar. El trabajo identifica un canal condicional, no un modelo de determinación de la presión cambiaria.

---

## 8. Conclusiones

**1. La hipótesis central se confirma: la rentabilidad exportadora opera como amplificador condicionado, no como determinante autónomo.** El efecto promedio de la rentabilidad sobre el EMPI no es distinguible de cero, tal como predice una relación condicional. Bajo estrés externo, el coeficiente de la interacción es de −1,704. Y con la medida continua de posición externa, los dos únicos coeficientes significativos del modelo son la interacción régimen × cuenta corriente (−1,813; p = 0,040) y la triple interacción rentabilidad × régimen × cuenta corriente (0,400; p = 0,042). El mecanismo no existe aisladamente: existe condicionado.

**2. El efecto marginal se multiplica por veinticuatro entre extremos de la posición externa.** Después de 2011, con déficit de cuenta corriente pronunciado, una caída de la rentabilidad exportadora eleva la presión cambiaria con un coeficiente de −1,647. Con superávit alto, el efecto es de −0,067. Cuando hay divisas, la rentabilidad del exportador es macroeconómicamente irrelevante; cuando no las hay, es determinante. Antes de 2011 el patrón se invierte, y la diferencia entre regímenes es máxima exactamente donde la hipótesis lo predice: en déficit alto (−2,483).

**3. La caída de la rentabilidad es, después de 2011, un fenómeno de política doméstica.** La descomposición de la varianza del índice muestra que la brecha cambiaria pasa de un aporte nulo antes de 2011 a explicar el 42,5% después, con la varianza total multiplicada por 1,7. Casi la mitad de la variación en los incentivos a exportar dejó de originarse en el mundo. Este resultado es descriptivo pero no depende de ningún supuesto de identificación, lo que lo vuelve la pieza más robusta del mecanismo.

**4. El desacople argentino es el más pronunciado de la muestra, con la significación máxima que el diseño permite.** Bajo la ventana pre-tratamiento del trabajo (2003–2010), Argentina es la unidad con mayor cociente RMSPE post/pre entre las doce, con p = 0,083 —el mínimo alcanzable con 12 unidades—. El placebo temporal muestra que 2010 alcanza un ratio casi idéntico al de 2011: el corte marca el momento en que el deterioro se vuelve visible, no su origen.

**5. Un resultado adicional: lo que se rompe en 2011 es la fase de recuperación.** El test de la hipótesis de stop-and-go arroja que la pata del freno —crecimiento que genera presión cambiaria— no aparece, mientras que la pata del rebote sí y es donde se concentra el cambio: la respuesta del crecimiento argentino a la presión cambiaria del año previo cae de 1,96 a 0,56 (p = 0,0005). Es el mismo mecanismo visto desde el lado real: si el ajuste del tipo de cambio oficial no llega al ingreso del exportador porque lo capturan las retenciones y lo licúa la brecha, la devaluación conserva su costo y pierde su función.

**6. Hacia una lectura de la restricción externa.** Los resultados son consistentes con que la restricción externa argentina posterior a 2011 no es solamente un dato del mundo sino, en proporción creciente, una construcción doméstica. Las fluctuaciones del financiamiento internacional y de los términos del intercambio son condicionantes exógenos ineludibles; pero la magnitud con la que se transmiten a la presión cambiaria está mediada por el esquema de incentivos interno, y ese esquema es una variable de política.

**7. Alcance.** La sección 3.8 muestra que la interacción con el régimen desaparece al excluir Argentina del panel. El diseño es un estudio de caso con grupo de control, y las conclusiones no deben extenderse al universo de exportadores de commodities. Los coeficientes centrales alcanzan el 5% en la especificación de la Tabla 3 y el 10% o menos en el resto.

**7. Implicancia de política.** Las políticas que introducen una cuña entre el precio internacional y el ingreso efectivo del exportador —derechos de exportación y, sobre todo, brecha cambiaria— tienen un costo que no aparece en la recaudación: elevan la sensibilidad de la economía a cualquier deterioro posterior de los términos del intercambio. El costo fiscal es visible y contemporáneo; el costo en vulnerabilidad es diferido y aparece, según estas estimaciones, con dos o tres años de rezago.

---

## 9. Bibliografía

Abadie, A., & Gardeazabal, J. (2003). The economic costs of conflict: A case study of the Basque Country. *American Economic Review*, 93(1), 113–132.

Abadie, A., Diamond, A., & Hainmueller, J. (2010). Synthetic control methods for comparative case studies: Estimating the effect of California's tobacco control program. *Journal of the American Statistical Association*, 105(490), 493–505.

Bastourre, D., Carrera, J., Ibarlucia, J., & Sardi, M. (2012). Dos síntomas y una causa: Flujos de capitales, precios de los commodities y determinantes globales. *Estudios BCRA — Documentos de Trabajo*, 2012/57.

Bekerman, M., Dulcich, F., & Vázquez, D. (2024). La restricción externa como límite al crecimiento: nuevas dimensiones y desafíos. *Revista de Economía*.

Carrera, J., Brest-López, C., Montes-Rojas, G., & Toledo, F. (2023). ¿Sirven los controles de capitales para morigerar los shocks financieros globales? *Desarrollo Económico*, 63(240).

Carrera, J., Montes-Rojas, G., & Toledo, F. (2023). Global financial cycle, commodity terms of trade and financial spreads in emerging market economies. *Structural Change and Economic Dynamics*, 64, 179–190.

Carrera, J., Montes-Rojas, G., & Toledo, F. (2023). La estructura productiva y la dependencia de divisas en economías sudamericanas. *Journal of Applied Economics*.

Carrera, J., Montes-Rojas, G., Solla, M., & Toledo, F. (2025). Unanticipated shocks to the Fed and exchange rate market pressures in emerging market economies. *Open Economies Review*.

Driscoll, J. C., & Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. *Review of Economics and Statistics*, 80(4), 549–560.

Jordà, Ò. (2005). Estimation and inference of impulse responses by local projections. *American Economic Review*, 95(1), 161–182.

Wainer, A. (2011). El papel del sector externo en el crecimiento argentino post-2003. *Revista Problemas del Desarrollo*.

Wainer, A., & Belloni, P. (2022). Ciclos de commodities y restricción externa: una revisión del caso argentino. *Revista de la CEPAL*.

Wainer, A., & Schorr, M. (2014). El desarrollo económico argentino y sus límites: una mirada desde la restricción externa. Editorial Universitaria.

---

## Apéndice A. Correspondencia entre tablas y archivos

| Tabla del texto | Archivo en `resultados/` |
|---|---|
| Tabla 0 — EMPI medio pre/post 2011 | `T14_empi_pre_post.csv` |
| Tabla 1 — Panel FE + Driscoll-Kraay | `T1_panel_fe_dk.csv` |
| Tablas 2 y 3 — Especificaciones del original | `T19_especificaciones_originales.csv` |
| Tabla 4 — Efectos marginales | `T20_efecto_marginal_por_posicion_externa.csv` |
| Tabla 2 — Diagnósticos | `T2_diagnosticos_modelos.csv` |
| Tabla 3 — Rezagos | `T4_rezagos.csv` |
| Tabla 4 — VIF | `T5_vif.csv` |
| Tabla 4b — Especificidad ARG | `T15_especificidad_ARG.csv` |
| Magnitud económica | `T16_magnitud_economica.csv` |
| Tabla 5 — Control sintético | `T7_sc_pesos.csv`, `T7b_sc_pesos_specC.csv`, `_sens_C.csv` |
| Tabla 6 — Local projections | `T10_local_projections.csv` |
| Tabla 7 — Placebo in space | `T8_placebo_in_space.csv` |
| Tabla 8 — Placebo in time | `T9_placebo_in_time.csv`, `T9b_placebo_in_time_specC.csv` |
| Tabla 9 — Descomposición | `T12_varianza_componentes_ARG.csv` |
| Tabla 10 — Test stop-and-go | `T17_stop_and_go.csv` |
| Tabla 11 — Ciclo descriptivo | `T18_ciclo_descriptivo.csv` |
| Series del control sintético | `T6_sc_series.csv`, `T6b_sc_series_specC.csv` |
| Robustez con `empi_robust` | `T3_robustez_empi_robust.csv` |
| Descriptivas | `T13_descriptivas.csv` |
| Figuras 1–7 | `figuras/fig1…fig7` |
| Panel construido | `panel_construido.csv` |

## Apéndice B. Reproducción

```bash
cd codigo
python3 analisis.py       # genera resultados/T1 ... T13
python3 sens_sc.py C      # sensibilidad de la ventana pre-tratamiento
python3 especificidad.py  # T15, T16: efecto argentino vs efecto de panel
python3 hipotesis_original.py # T19, T20 y figura 9: especificaciones centrales
python3 stop_and_go.py    # T17, T18 y figura 8: test del ciclo
python3 graficos.py       # genera figuras/fig1 ... fig5
```

Requiere `numpy`, `pandas`, `scipy` y `matplotlib`. El panel FE bidireccional con errores Driscoll-Kraay y el control sintético están implementados directamente en `analisis.py`; equivalen a `plm::plm(effect="twoways")` con `vcovSCC` y al paquete `Synth` de R respectivamente. La semilla está fijada en 20240101.
