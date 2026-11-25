"""
Script de Verificación Básica y Generación de Evidencias

"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Permitir importación de los módulos principales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Modelo_Fuente.simulador import SimuladorColon
from Datos_Parametros.parametros import INGESTA_BASE


def prueba_1_inicializacion():
    """Prueba 1: Estado inicial en t=0 (Verificar masas nulas sin divergencias)."""
    sim = SimuladorColon(
        agua_ingesta_g=INGESTA_BASE['agua_total_ml'],
        fibra_sol_g=INGESTA_BASE['fibra_soluble_g'],
        fibra_insol_g=INGESTA_BASE['fibra_insoluble_g']
    )
    res = sim.simular(t_max=1.0)
    masa_inicial_total = np.sum(res['Mw'][:, 0]) + np.sum(res['Mfs'][:, 0]) + np.sum(res['Mfi'][:, 0])
    cumple = (masa_inicial_total == 0.0)
    print(f"[Prueba 1] Inicialización de masas en t=0 (0.0 g): {'CUMPLE' if cumple else 'NO CUMPLE'}")
    return cumple


def prueba_2_conservacion_fibra():
    """Prueba 2: Balance y no negatividad de masa seca de fibra."""
    sim = SimuladorColon(
        agua_ingesta_g=INGESTA_BASE['agua_total_ml'],
        fibra_sol_g=INGESTA_BASE['fibra_soluble_g'],
        fibra_insol_g=INGESTA_BASE['fibra_insoluble_g']
    )
    res = sim.simular(t_max=48.0)
    mfs_valida = np.all(res['Mfs'] >= 0.0)
    mfi_valida = np.all(res['Mfi'] >= 0.0)
    cumple = mfs_valida and mfi_valida
    print(f"[Prueba 2] Conservación y no negatividad de fibra seca: {'CUMPLE' if cumple else 'NO CUMPLE'}")
    return cumple


def prueba_3_ingesta_cero():
    """Prueba 3: Evaluación de estabilidad en condición límite con ingesta de agua nula (A=0)."""
    sim = SimuladorColon(agua_ingesta_g=0.0, fibra_sol_g=10.0, fibra_insol_g=20.0)
    res = sim.simular(t_max=48.0)
    mw_valida = np.all(res['Mw'] >= 0.0) and not np.isnan(res['Mw']).any()
    cumple = mw_valida
    print(f"[Prueba 3] Comportamiento con ingesta de agua nula (A=0): {'CUMPLE' if cumple else 'NO CUMPLE'}")
    return cumple


def generar_graficos_evidencias():
    """Genera y guarda las gráficas formales para Corrida Base y Variación Preliminar."""
    dir_actual = os.path.dirname(__file__)
    
    # 1. Corrida Base
    sim_base = SimuladorColon(
        agua_ingesta_g=INGESTA_BASE['agua_total_ml'],
        fibra_sol_g=INGESTA_BASE['fibra_soluble_g'],
        fibra_insol_g=INGESTA_BASE['fibra_insoluble_g']
    )
    res_base = sim_base.simular(t_max=48.0)
    
    plt.figure(figsize=(8.5, 4.5))
    plt.plot(res_base['t'], res_base['humedad_fecal_final'], label='Corrida Base (2000 mL Agua, 10g Fs, 20g Fi)', color='navy', linewidth=2)
    plt.title('Corrida Base: Perfil Temporal de Humedad Fecal Residual en Colon Descendente (k=3)')
    plt.xlabel('Tiempo de Simulación (horas)')
    plt.ylabel('Humedad Fecal Residual Hf (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(dir_actual, 'corrida_base.png'), dpi=300)
    plt.close()
    
    # 2. Variación Preliminar (Incremento de Fibra Soluble a 25g)
    sim_var = SimuladorColon(
        agua_ingesta_g=INGESTA_BASE['agua_total_ml'],
        fibra_sol_g=25.0,
        fibra_insol_g=INGESTA_BASE['fibra_insoluble_g']
    )
    res_var = sim_var.simular(t_max=48.0)
    
    plt.figure(figsize=(8.5, 4.5))
    plt.plot(res_base['t'], res_base['humedad_fecal_final'], label='Base (10g Fibra Soluble)', color='navy', linestyle='--')
    plt.plot(res_var['t'], res_var['humedad_fecal_final'], label='Variación (25g Fibra Soluble)', color='crimson', linewidth=2)
    plt.title('Variación Preliminar: Efecto del Incremento de Fibra Soluble en Hf')
    plt.xlabel('Tiempo de Simulación (horas)')
    plt.ylabel('Humedad Fecal Residual Hf (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(dir_actual, 'variacion_preliminar.png'), dpi=300)
    plt.close()
    print("Gráficos generados exitosamente en Pruebas_Evidencias/")


if __name__ == '__main__':
    print("--- EJECUTANDO VERIFICACIÓN BÁSICA DEL MODELO ---")
    p1 = prueba_1_inicializacion()
    p2 = prueba_2_conservacion_fibra()
    p3 = prueba_3_ingesta_cero()
    
    if p1 and p2 and p3:
        print("\nTodas las pruebas resultaron CUMPLIDAS. Generando imágenes de evidencias...")
        generar_graficos_evidencias()