"""
Script de Evaluación de Múltiples Casos de Prueba Dietéticos
Proyecto: Simulación Dinámica del Tránsito Colónico
"""

import sys
import os
import pandas as pd

# Permitir importaciones de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Modelo_Fuente.simulador import SimuladorColon
from Datos_Parametros.parametros import CASOS_PRUEBA, clasificar_bristol

def evaluar_todos_los_casos():
    resultados = []
    
    print("==================================================================================")
    print(" EVALUACIÓN DE MÚLTIPLES CASOS DE PRUEBA Y CLASIFICACIÓN EN ESCALA DE BRISTOL")
    print("==================================================================================\n")
    
    for clave, datos in CASOS_PRUEBA.items():
        sim = SimuladorColon(
            agua_ingesta_g=datos['agua_total_ml'],
            fibra_sol_g=datos['fibra_soluble_g'],
            fibra_insol_g=datos['fibra_insoluble_g']
        )
        res = sim.simular(t_max=48.0)
        
        # Obtener porcentaje de humedad final en t=48h (compartimento k=3)
        hf_final = res['humedad_fecal_final'][-1]
        bristol_est = clasificar_bristol(hf_final)
        
        resultados.append({
            'ID Caso': clave,
            'Descripción Dietética': datos['nombre'],
            'Agua (mL)': datos['agua_total_ml'],
            'Fibra Sol (g)': datos['fibra_soluble_g'],
            'Fibra Insol (g)': datos['fibra_insoluble_g'],
            'Humedad Final Hf (%)': round(hf_final, 2),
            'Escala Bristol Estimada': bristol_est
        })
    
    df = pd.DataFrame(resultados)
    print(df.to_string(index=False))
    
    # Exportar resultados a un archivo CSV en Pruebas_Evidencias
    ruta_csv = os.path.join(os.path.dirname(__file__), 'resultados_casos_prueba.csv')
    df.to_csv(ruta_csv, index=False)
    print(f"\n[OK] Resultados de la matriz de casos exportados a: {ruta_csv}")

if __name__ == '__main__':
    evaluar_todos_los_casos()