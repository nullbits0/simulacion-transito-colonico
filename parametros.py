"""
Módulo de Parámetros y Configuraciones del Modelo Colónico
"""

# --- PARÁMETROS FISIOLÓGICOS Y BIOFÍSICOS ---

# Capacidad de Retención de Agua (WHC) [g H2O / g fibra]
# Fuente: McRorie & McKeown (2017)
WHC_SOLUBLE = 12.5    # Fibra soluble (formadora de gel)
WHC_INSOLUBLE = 3.2   # Fibra insoluble (efecto mecánico/volumen)

# Coeficientes de Absorción Mucosal Regional [h^-1]
# Fuente provisional: Debongnie & Phillips (1978)
# Rango documentado en literatura: 0.15 a 0.35 h^-1 según región
K_ABS = [0.15, 0.10, 0.05]  # [k1: Ascendente, k2: Transverso, k3: Descendente]

# Coeficientes de Transferencia Convectiva Intercompartimental [h^-1]
# Basado en tiempo de tránsito total fisiológico (~48 horas)
K_TRANS = [0.10, 0.08, 0.06]

# Fracción de agua de ingesta diaria que efectivamente ingresa al ciego (%)
# Fuente: Guyton & Hall (2021) / Johnson (2018) -> El colon recibe aprox. 1.5 L de los ~2 L ingeridos
FRACCION_AGUA_COLON = 0.75 

# --- CONFIGURACIONES DE SIMULACIÓN ---
HORIZONTE_TIEMPO_HORAS = 48.0   # Recomendación docente (horizonte de 48 horas)
PASO_TIEMPO_EVALUACION = 0.5    # Evaluación cada 30 minutos

# --- CONFIGURACIÓN DE CORRIDA BASE ---
INGESTA_BASE = {
    'agua_total_ml': 2000.0,      # Agua total ingerida al día (mL o g)
    'fibra_soluble_g': 10.0,      # Fibra soluble diaria (g)
    'fibra_insoluble_g': 20.0     # Fibra insoluble diaria (g)
}