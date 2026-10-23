"""
Ejecución automatizada de la matriz de 27 escenarios (Factorial 3x3x3)
Proyecto: Simulación Tránsito Colónico (UFPSO)
"""

import pandas as pd
from simulador import modelo_colon, clasificar_bristol
from scipy.integrate import solve_ivp
import numpy as np

# --- DEFINICIÓN DE NIVELES (FACTORIAL 3x3x3) ---
F_S_NIVELES = [2.0, 5.0, 10.0]       # Fibra Soluble (g/día): Bajo, Medio, Alto
F_I_NIVELES = [8.0, 15.0, 25.0]      # Fibra Insoluble (g/día): Bajo, Medio, Alto
AGUA_NIVELES = [1200, 2000, 3000]    # Agua Total (mL/día): Bajo, Medio, Alto

def ejecutar_matriz_27():
    resultados = []
    escenario_num = 1
    
    print("Ejecutando simulación para los 27 escenarios...")
    
    for fs in F_S_NIVELES:
        for fi in F_I_NIVELES:
            for agua in AGUA_NIVELES:
                nombre_id = f"E{escenario_num:02d}"
                
                # Simulación RK45 a 48 horas
                y0 = [0.0, 50.0, 0.0, 50.0, 0.0, 50.0]
                sol = solve_ivp(
                    modelo_colon, 
                    (0, 48), 
                    y0, 
                    args=(fs, fi, agua), 
                    t_eval=np.linspace(0, 48, 100), 
                    method='RK45'
                )
                
                # Estado final en k=3 (recto/sigmoide)
                MF3_final = sol.y[4, -1]
                MW3_final = sol.y[5, -1]
                
                H_f = (MW3_final / (MW3_final + MF3_final)) * 100.0 if (MW3_final + MF3_final) > 0 else 0.0
                diag = clasificar_bristol(H_f)
                
                resultados.append({
                    'Escenario': nombre_id,
                    'Fibra Soluble (g)': fs,
                    'Fibra Insoluble (g)': fi,
                    'Agua Total (mL)': agua,
                    'Fibra en Recto (g)': round(MF3_final, 2),
                    'Agua en Recto (g)': round(MW3_final, 2),
                    'Humedad Fecal Hf (%)': round(H_f, 2),
                    'Diagnóstico Bristol': diag
                })
                
                escenario_num += 1

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(resultados)
    
    # Guardar en CSV
    df.to_csv("resultados_27_escenarios.csv", index=False)
    print("\n✅ ¡Simulación completada con éxito!")
    print("Resultados guardados en 'resultados_27_escenarios.csv'\n")
    
    # Mostrar la tabla en consola
    print(df[['Escenario', 'Fibra Soluble (g)', 'Fibra Insoluble (g)', 'Agua Total (mL)', 'Humedad Fecal Hf (%)', 'Diagnóstico Bristol']])

if __name__ == "__main__":
    ejecutar_matriz_27()