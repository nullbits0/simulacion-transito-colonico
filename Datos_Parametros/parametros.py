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
K_ABS = [0.38, 0.28, 0.18]  # [k1: Ascendente, k2: Transverso, k3: Descendente]

# Coeficientes de Transferencia Convectiva Intercompartimental [h^-1]
# Basado en tiempo de tránsito total fisiológico (~48 horas)
K_TRANS = [0.10, 0.08, 0.06]

# Fracción de agua de ingesta diaria que efectivamente ingresa al ciego (%)
# Fuente: Guyton & Hall (2021) / Johnson (2018) -> El colon recibe aprox. 1.5 L de los ~2 L ingeridos
FRACCION_AGUA_COLON = 0.55 

# --- CONFIGURACIONES DE SIMULACIÓN ---
HORIZONTE_TIEMPO_HORAS = 48.0   # Recomendación docente (horizonte de 48 horas)
PASO_TIEMPO_EVALUACION = 0.5    # Evaluación cada 30 minutos

# --- CONFIGURACIÓN DE CORRIDA BASE ---
INGESTA_BASE = {
    'agua_total_ml': 2000.0,      # Agua total ingerida al día (mL o g)
    'fibra_soluble_g': 10.0,      # Fibra soluble diaria (g)
    'fibra_insoluble_g': 20.0     # Fibra insoluble diaria (g)
}

# --- DICCIONARIO DE CASOS DE PRUEBA DIETÉTICOS (OPCIÓN A) ---
CASOS_PRUEBA = {
    'base': {
        'nombre': 'Dieta Base Promedio (Recomendada)',
        'agua_total_ml': 2000.0,
        'fibra_soluble_g': 10.0,
        'fibra_insoluble_g': 20.0
    },
    'estrenimiento_severo': {
        'nombre': 'Estreñimiento Severo (Baja agua y fibra)',
        'agua_total_ml': 1000.0,
        'fibra_soluble_g': 3.0,
        'fibra_insoluble_g': 8.0
    },
    'alta_fibra_soluble': {
        'nombre': 'Suplementación Soluble (Efecto Gelificante)',
        'agua_total_ml': 2500.0,
        'fibra_soluble_g': 25.0,
        'fibra_insoluble_g': 15.0
    },
    'alta_fibra_insoluble': {
        'nombre': 'Alto Salvador/Cereales (Efecto Volumen)',
        'agua_total_ml': 2000.0,
        'fibra_soluble_g': 5.0,
        'fibra_insoluble_g': 35.0
    }
}

def clasificar_bristol(humedad_pct):
    """
    Regla provisional de correspondencia de Humedad Fecal Hf (%) a Escala de Bristol (Tipos 1 a 7).
    Sustentado preliminarmente en Lewis & Heaton (1997) como supuesto orientativo.
    """
    if humedad_pct <= 0:
        return "N/A (Sin masa fecal)"
    elif humedad_pct < 60.0:
        return "Tipo 1 (Bolitas duras / Estreñimiento severo)"
    elif humedad_pct < 70.0:
        return "Tipo 2 (Salchicha grumosa / Estreñimiento)"
    elif humedad_pct < 75.0:
        return "Tipo 3 (Salchicha con grietas / Normal-Bajo)"
    elif humedad_pct <= 80.0:
        return "Tipo 4 (Salchicha suave y lisa / Normal ideal)"
    elif humedad_pct <= 85.0:
        return "Tipo 5 (Trozos blandos / Tendencia blanda)"
    elif humedad_pct <= 90.0:
        return "Tipo 6 (Trozos esponjosos / Diarrea leve)"
    else:
        return "Tipo 7 (Acuosa / Diarrea severa)"