"""
Proyecto: Simulación Dinámica del Tránsito Colónico e Hidratación Fecal
Materia: Modelado y Simulación de Sistemas (UFPSO)
Estudiantes: Danna Sofía Velandia Arciniegas & Mairin Dayany Bayona Alvarez
Docente: Ing. Jesús Eduardo Guerrero Rodríguez
Versión: 0.2 (Calibrada con Biomasa y Tasas Fisiológicas)
"""

import numpy as np
from scipy.integrate import solve_ivp

# ==========================================
# 1. CONSTANTES BIOFÍSICAS Y FISIOLÓGICAS
# ==========================================
WHC_S = 12.5  # Retención de agua de fibra soluble (g H2O / g)
WHC_I = 3.2   # Retención de agua de fibra insoluble (g H2O / g)

# Tasas de absorción mucosal calibradas (1/h) para k=1, 2, 3
K_ABS = [0.35, 0.25, 0.15]  

# Masa seca diaria base de biomasa bacteriana y residuos (g/día -> g/h)
MASA_SECA_BASE_DIA = 25.0  

# ==========================================
# 2. MODELO DE ECUACIONES DIFERENCIALES (EDOs)
# ==========================================
def modelo_colon(t, y, Fs, Fi, Agua_total):
    """
    Define el sistema de EDOs para los 3 compartimentos (k=1,2,3).
    y = [MF1, MW1, MF2, MW2, MF3, MW3]
    """
    MF = [y[0], y[2], y[4]]
    MW = [y[1], y[3], y[5]]
    
    # Flujos continuos de entrada (g/h)
    qin_F = (Fs + Fi) / 24.0
    qin_W = Agua_total / 24.0
    
    f_sol = Fs / (Fs + Fi) if (Fs + Fi) > 0 else 0.0
    f_ins = Fi / (Fs + Fi) if (Fs + Fi) > 0 else 0.0
    
    dydt = np.zeros(6)
    
    # Coeficiente de tránsito fisiológico realista (1/h) -> ~25-30 horas de tránsito
    k_out = 0.04  
    
    for k in range(3):
        MF_sol_k = MF[k] * f_sol
        MF_ins_k = MF[k] * f_ins
        
        # Agua retenida químicamente por la fibra
        agua_retenida = (WHC_S * MF_sol_k) + (WHC_I * MF_ins_k)
        
        # Agua libre disponible para absorción mucosal
        agua_libre = max(0.0, MW[k] - agua_retenida)
        
        # Absorción de agua libre
        J_abs = K_ABS[k] * agua_libre
        
        qout_F = k_out * MF[k]
        qout_W = k_out * MW[k]
        
        ingreso_F = qin_F if k == 0 else qout_F_prev
        ingreso_W = qin_W if k == 0 else qout_W_prev
        
        dydt[2*k]     = ingreso_F - qout_F           # dMF/dt
        dydt[2*k + 1] = ingreso_W - qout_W - J_abs   # dMW/dt
        
        qout_F_prev, qout_W_prev = qout_F, qout_W
        
    return dydt

# ==========================================
# 3. FUNCIONES DE MAPEO Y RESULTADOS
# ==========================================
def clasificar_bristol(H_f):
    """ Mapea la humedad fecal final al diagnóstico de la Escala de Bristol """
    if H_f < 60.0:
        return "Bristol Tipo 1-2 (Estreñimiento Severo)"
    elif 60.0 <= H_f < 70.0:
        return "Bristol Tipo 2-3 (Estreñimiento Moderado)"
    elif 70.0 <= H_f <= 75.0:
        return "Bristol Tipo 3-4 (Normal / Rango Ideal)"
    elif 75.0 < H_f <= 80.0:
        return "Bristol Tipo 4-5 (Heces Blandas)"
    else:
        return "Bristol Tipo 6-7 (Tendencia Diarreica)"

def calcular_humedad_fecal(MF3, MW3):
    """ Calcula H_f (%) incluyendo la biomasa seca colónica en el sólido total """
    # Biomasa seca proporcional residente en k=3 (~8.33g)
    mbio_k3 = MASA_SECA_BASE_DIA / 3.0  
    masa_seca_total = MF3 + mbio_k3
    
    if (MW3 + masa_seca_total) > 0:
        return (MW3 / (MW3 + masa_seca_total)) * 100.0
    return 0.0

def probar_escenario(nombre, Fs, Fi, Agua_total):
    y0 = [0.0, 50.0, 0.0, 50.0, 0.0, 50.0]
    sol = solve_ivp(
        modelo_colon, 
        (0, 48), 
        y0, 
        args=(Fs, Fi, Agua_total), 
        t_eval=np.linspace(0, 48, 100), 
        method='RK45'
    )
    
    MF3_final = sol.y[4, -1]
    MW3_final = sol.y[5, -1]
    
    H_f = calcular_humedad_fecal(MF3_final, MW3_final)
    diagnostico = clasificar_bristol(H_f)
    
    print(f"--- {nombre} ---")
    print(f"Dieta: Fs={Fs}g | Fi={Fi}g | Agua={Agua_total}mL")
    print(f"Humedad Fecal Final (H_f): {H_f:.2f}%")
    print(f"Diagnóstico: {diagnostico}\n")

if __name__ == "__main__":
    print("==================================================")
    print(" PRUEBAS DE SIMULACIÓN - BALANCE DE MASA COLÓNICO ")
    print("==================================================\n")
    
    probar_escenario("Escenario E01 (Bajo Aporte / Deshidratado)", Fs=2.0, Fi=8.0, Agua_total=1200)
    probar_escenario("Escenario E14 (Línea Base ICBF/FDA)", Fs=5.0, Fi=15.0, Agua_total=2000)
    probar_escenario("Escenario E27 (Alto Aporte / Hiperhidratado)", Fs=10.0, Fi=25.0, Agua_total=3000)