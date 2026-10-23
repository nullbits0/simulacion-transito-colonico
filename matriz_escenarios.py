"""
Ejecución automatizada de la matriz de 27 escenarios (Factorial 3x3x3)
Proyecto: Simulación Tránsito Colónico (UFPSO)
"""

import pandas as pd
from simulador import modelo_colon, clasificar_bristol, calcular_humedad_fecal
from scipy.integrate import solve_ivp
import numpy as np

F_S_NIVELES = [2.0, 5.0, 10.0]       
F_I_NIVELES = [8.0, 15.0, 25.0]      
AGUA_NIVELES = [1200, 2000, 3000]    

def ejecutar_matriz_27():
    resultados = []
    escenario_num = 1
    
    print("Ejecutando simulación calibrada para los 27 escenarios...")
    
    for fs in F_S_NIVELES:
        for fi in F_I_NIVELES:
            for agua in AGUA_NIVELES:
                nombre_id = f"E{escenario_num:02d}"
                
                y0 = [0.0, 50.0, 0.0, 50.0, 0.0, 50.0]
                sol = solve_ivp(
                    modelo_colon, 
                    (0, 48), 
                    y0, 
                    args=(fs, fi, agua), 
                    t_eval=np.linspace(0, 48, 100), 
                    method='RK45'
                )
                
                MF3_final = sol.y[4, -1]
                MW3_final = sol.y[5, -1]
                
                H_f = calcular_humedad_fecal(MF3_final, MW3_final)
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

    df = pd.DataFrame(resultados)
    df.to_csv("resultados_27_escenarios.csv", index=False)
    print("\n✅ ¡Simulación completada con éxito!")
    print("Resultados guardados en 'resultados_27_escenarios.csv'\n")
    
    print(df[['Escenario', 'Fibra Soluble (g)', 'Fibra Insoluble (g)', 'Agua Total (mL)', 'Humedad Fecal Hf (%)', 'Diagnóstico Bristol']])

if __name__ == "__main__":
    ejecutar_matriz_27()