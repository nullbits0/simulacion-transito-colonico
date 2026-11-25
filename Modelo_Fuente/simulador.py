import numpy as np
from scipy.integrate import solve_ivp
from Datos_Parametros.parametros import (
    WHC_SOLUBLE, WHC_INSOLUBLE, K_ABS, K_TRANS, 
    FRACCION_AGUA_COLON, HORIZONTE_TIEMPO_HORAS, PASO_TIEMPO_EVALUACION
)

class SimuladorColon:
    """
    Modelo de Dinámica de Sistemas de Balance de Masa Colónico en 3 Compartimentos:
    1: Colon Ascendente
    2: Colon Transverso
    3: Colon Descendente / Sigmoide
    """
    def __init__(self, agua_ingesta_g, fibra_sol_g, fibra_insol_g):
        # Entradas diarias
        self.agua_ingre = agua_ingesta_g * FRACCION_AGUA_COLON
        self.fibra_sol = fibra_sol_g
        self.fibra_insol = fibra_insol_g
        
    def _sistema_edos(self, t, y):
        """
        Formulación del sistema de 9 EDOs acopladas:
        y[0..2]: Masa de Agua [Mw1, Mw2, Mw3]
        y[3..5]: Masa de Fibra Soluble [Mfs1, Mfs2, Mfs3]
        y[6..8]: Masa de Fibra Insoluble [Mfi1, Mfi2, Mfi3]
        """
        Mw = y[0:3]
        Mfs = y[3:6]
        Mfi = y[6:9]
        
        dMw_dt = np.zeros(3)
        dMfs_dt = np.zeros(3)
        dMfi_dt = np.zeros(3)
        
        # Tasa continua de entrada al primer compartimento (g/h)
        qin_w = self.agua_ingre / 24.0
        qin_fs = self.fibra_sol / 24.0
        qin_fi = self.fibra_insol / 24.0
        
        for k in range(3):
            # 1. Operador de Agua Libre (discontinuo/positivo)
            # M_libre = max(0, Mw_k - WHCs * Mfs_k - WHCi * Mfi_k)
            retencion_total = (WHC_SOLUBLE * Mfs[k]) + (WHC_INSOLUBLE * Mfi[k])
            agua_libre = max(0.0, Mw[k] - retencion_total)
            
            # Tasa de absorción mucosal regional
            j_abs = K_ABS[k] * agua_libre
            
            # Entradas y Salidas de Masa
            w_in = qin_w if k == 0 else K_TRANS[k-1] * Mw[k-1]
            fs_in = qin_fs if k == 0 else K_TRANS[k-1] * Mfs[k-1]
            fi_in = qin_fi if k == 0 else K_TRANS[k-1] * Mfi[k-1]
            
            w_out = K_TRANS[k] * Mw[k]
            fs_out = K_TRANS[k] * Mfs[k]
            fi_out = K_TRANS[k] * Mfi[k]
            
            # Ecuaciones Diferenciales Ordinarias por compartimento
            dMw_dt[k] = w_in - w_out - j_abs
            dMfs_dt[k] = fs_in - fs_out
            dMfi_dt[k] = fi_in - fi_out
            
        return np.concatenate([dMw_dt, dMfs_dt, dMfi_dt])

    def simular(self, t_max=HORIZONTE_TIEMPO_HORAS):
        """Ejecuta la integración numérica mediante RK45 (solve_ivp)."""
        # Condiciones iniciales: masa nula en t=0 (estado estacionario se alcanza con la ingesta continuous)
        y0 = np.zeros(9)
        t_eval = np.arange(0, t_max + PASO_TIEMPO_EVALUACION, PASO_TIEMPO_EVALUACION)
        
        solucion = solve_ivp(
            fun=self._sistema_edos,
            t_span=(0, t_max),
            y0=y0,
            t_eval=t_eval,
            method='RK45'
        )
        
        # Extracción de variables de salida
        Mw3 = solucion.y[2, :]
        Mfs3 = solucion.y[5, :]
        Mfi3 = solucion.y[8, :]
        
        # Cálculo del porcentaje de Humedad Fecal residual en el compartimento final (k=3)
        masa_total_fecal = Mw3 + Mfs3 + Mfi3
        # Evitar división por cero en t=0
        humedad_fecal = np.zeros_like(masa_total_fecal)
        mask = masa_total_fecal > 0
        humedad_fecal[mask] = (Mw3[mask] / masa_total_fecal[mask]) * 100.0
        
        return {
            't': solucion.t,
            'Mw': solucion.y[0:3, :],
            'Mfs': solucion.y[3:6, :],
            'Mfi': solucion.y[6:9, :],
            'humedad_fecal_final': humedad_fecal
        }