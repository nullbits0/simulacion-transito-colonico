"""
Proyecto: Simulación Dinámica del Tránsito Colónico e Hidratación Fecal
Materia: Modelado y Simulación de Sistemas (UFPSO)
Versión: 0.1 (Base funcional para pruebas de escenarios)
"""

import numpy as np
from scipy.integrate import solve_ivp

# ==========================================
# 1. CONSTANTES BIOFÍSICAS (McRorie & Debongnie)
# ==========================================
WHC_S = 12.5  # Retención de agua de fibra soluble (g H2O / g)
WHC_I = 3.2   # Retención de agua de fibra insoluble (g H2O / g)
K_ABS = [0.15, 0.10, 0.05]  # Tasas de absorción mucosal k_abs (1/h) para k=1, 2, 3

# ==========================================
# 2. MODELO DE ECUACIONES DIFERENCIALES (EDOs)
# ==========================================
def modelo_colon(t, y, Fs, Fi, Agua_total):
    """
    Define el sistema de EDOs para los 3 compartimentos (k=1,2,3).
    y = [MF1, MW1, MF2, MW2, MF3, MW3]
    MF: Masa de Fibra (g), MW: Masa de Agua (g)
    """
    MF = [y[0], y[2], y[4]]
    MW = [y[1], y[3], y[5]]
    
    # Entradas diarias convertidas a flujo continuo por hora (g/h o mL/h)
    qin_F = (Fs + Fi) / 24.0
    qin_W = Agua_total / 24.0
    
    # Fracción constante de tipo de fibra en la mezcla
    f_sol = Fs / (Fs + Fi) if (Fs + Fi) > 0 else 0.0
    f_ins = Fi / (Fs + Fi) if (Fs + Fi) > 0 else 0.0
    
    dydt = np.zeros(6)
    
    # Coeficiente de vaciado/tránsito por compartimento (1/h)
    k_out = 0.08 
    
    for k in range(3):
        # 1. Calcular fibra soluble e insoluble en este compartimento
        MF_sol_k = MF[k] * f_sol
        MF_ins_k = MF[k] * f_ins
        
        # 2. Agua retenida por la fibra en el compartimento k
        agua_retenida = (WHC_S * MF_sol_k) + (WHC_I * MF_ins_k)
        
        # 3. Agua libre disponible para absorción mucosal ()+
        agua_libre = max(0.0, MW[k] - agua_retenida)
        
        # 4. Tasa de absorción mucosal (solo absorbe agua libre)
        J_abs = K_ABS[k] * agua_libre
        
        # 5. Flujos de salida hacia el siguiente compartimento
        qout_F = k_out * MF[k]
        qout_W = k_out * MW[k]
        
        # 6. EDOs de Balance de Masa
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
        return "Bristol Tipo 2-3 (Estreñimiento Moderado / Ligero)"
    elif 70.0 <= H_f <= 75.0:
        return "Bristol Tipo 3-4 (Normal / Rango Fisiológico Ideal)"
    elif 75.0 < H_f <= 80.0:
        return "Bristol Tipo 4-5 (Heces Blandas)"
    else:
        return "Bristol Tipo 6-7 (Tendencia Diarreica)"

def probar_escenario(nombre, Fs, Fi, Agua_total):
    """ Ejecuta la simulación RK45 para un escenario específico """
    y0 = [0.0, 50.0, 0.0, 50.0, 0.0, 50.0]
    t_span = (0, 48)
    t_eval = np.linspace(0, 48, 100)
    
    sol = solve_ivp(
        modelo_colon, 
        t_span, 
        y0, 
        args=(Fs, Fi, Agua_total), 
        t_eval=t_eval, 
        method='RK45'
    )
    
    MF3_final = sol.y[4, -1]
    MW3_final = sol.y[5, -1]
    
    H_f = (MW3_final / (MW3_final + MF3_final)) * 100.0 if (MW3_final + MF3_final) > 0 else 0.0
    diagnostico = clasificar_bristol(H_f)
    
    print(f"--- {nombre} ---")
    print(f"Dieta: Fs={Fs}g | Fi={Fi}g | Agua={Agua_total}mL")
    print(f"Masa final en k=3: Fibra={MF3_final:.2f}g, Agua={MW3_final:.2f}g")
    print(f"Humedad Fecal Final (H_f): {H_f:.2f}%")
    print(f"Diagnóstico: {diagnostico}\n")

# ==========================================
# 4. PRUEBA DE ESCENARIOS PILOTO
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print(" PRUEBAS DE SIMULACIÓN - BALANCE DE MASA COLÓNICO ")
    print("==================================================\n")
    
    probar_escenario("Escenario E01 (Bajo Aporte / Deshidratado)", Fs=2.0, Fi=8.0, Agua_total=1200)
    probar_escenario("Escenario E14 (Línea Base ICBF/FDA)", Fs=5.0, Fi=15.0, Agua_total=2000)
    probar_escenario("Escenario E27 (Alto Aporte / Hiperhidratado)", Fs=10.0, Fi=25.0, Agua_total=3000)