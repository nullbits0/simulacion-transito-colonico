Este documento detalla la procedencia, unidades, justificación biofísica y uso dentro del modelo de cada dato y parámetro utilizado en la simulación.

| Dato / Parámetro | Valor o Rango | Unidad | Fuente | Estado de Evidencia | Transformación / Calidad | Uso en el Modelo |
| --- | --- | --- | --- | --- | --- | --- |
| **Agua total ($A$)** | 1000 - 3000 | mL/día | ICBF (2020) / USDA (2019) | Medido / Institucional | Masa diaria unificada ($g/\text{día}$) | Entrante al sistema colónico |
| **Fibra soluble ($F_s$)** | 5.0 - 25.0 | g/día | ICBF (2020) / USDA (2019) | Medido / Institucional | Fracción soluble aislada | Balance de masa y gelificación |
| **Fibra insoluble ($F_i$)** | 10.0 - 40.0 | g/día | ICBF (2020) / USDA (2019) | Medido / Institucional | Fracción insoluble aislada | Balance de masa y volumen fecal |
| **Retención Fibra Soluble ($WHC_s$)** | 12.5 | $\text{g } H_2O/\text{g fibra}$ | McRorie & McKeown (2017) | Literatura | Constante de capacidad hidrofílica | Retención de agua en operador libre |
| **Retención Fibra Insoluble ($WHC_i$)** | 3.2 | $\text{g } H_2O/\text{g fibra}$ | McRorie & McKeown (2017) | Literatura | Constante de captura mecánica | Retención de agua en operador libre |
| **Absorción colónica ($k_{abs,k}$)** | 0.15, 0.10, 0.05 | $\text{h}^{-1}$ | Debongnie & Phillips (1978) | Supuesto / Literatura | Coeficientes de primer orden | Tasa de absorción mucosal por compartimento |
| **Fracción Agua a Colon** | 0.75 | Adimensional | Guyton & Hall (2021) | Literatura | $A_{efectivo} = A \times 0.75$ | Entrada neta al ciego ($k=1$) |