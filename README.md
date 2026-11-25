# Guía de Ejecución y Reproducibilidad del Modelo
## Simulación Dinámica del Tránsito Colónico e Hidratación Fecal

**Asignatura:** Modelado y Simulación de Sistemas  
**Institución:** Universidad Francisco de Paula Santander Ocaña (UFPSO)  
**Integrantes:**  
- Danna Sofía Velandia Arciniegas (Código: 0192478)  
- Mairin Dayany Bayona Álvarez (Código: 0192470)  

---

### 1. Nombre y Propósito del Modelo
**Simulador Colónico de Balance de Masa (v0.3):** Evaluar el impacto de variaciones en la ingesta diaria de agua (A), fibra soluble (F_s) y fibra insoluble (F_i) sobre el porcentaje de humedad fecal residual (H_f) a través de un sistema de 3 compartimentos colónicos acoplados en serie.

### 2. Herramienta y Versión
- **Lenguaje:** Python 3.10+
- **Integrador:** `scipy.integrate.solve_ivp` (método de Runge-Kutta RK45)
- **Entorno recomendado:** VS Code / Terminal con `venv`

### 3. Requisitos de Dependencias
Las librerías requeridas se encuentran declaradas en `requirements.txt`:
- `numpy>=1.24.0`
- `scipy>=1.10.0`
- `matplotlib>=3.7.0`
- `pandas>=2.0.0`

### 4. Instalación del Entorno
```bash
# 1. Clonar o descargar el repositorio
cd simulacion-transito-colonico

# 2. Crear y activar entorno virtual (opcional pero recomendado)
python -m venv venv
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### 5. Procedimiento de Ejecución
- **A. Verificación Básica y Generación de Evidencias:** 
 ```bash
   python Pruebas_Evidencias/pruebas_verificacion.py
 ```  
- **B. Ejecución del Grid de Escenarios (27 combinaciones de ingesta):** 
```bash
   python Modelo_Fuente/matriz_escenarios.py
 ```  

 ### 6. Archivos de Entrada y Configuración
- **Datos_Parametros/parametros.py** Contiene los coeficientes fisiológicos (WHC_s, WHC_i, k_abs, k_trans) y configuraciones de simulación.
- **Datos_Parametros/diccionario_parametros.md:** Documenta la fuente primaria de cada parámetro.

### 7. onfiguración de la Corrida Base
- **Agua Total (A):** 2000 mL/día
- **Fibra Soluble (F_s):** 10.0 g/día
- **Fibra Insoluble (F_i):** 20.0 g/día
- **Horizonte de Simulación:** 48.0 horas

### 8. Salidas Esperadas y Ubicación
- **Pruebas_Evidencias/corrida_base.png:** Gráfico de la evolución de H_f(%) en el tiempo.
- **Pruebas_Evidencias/variacion_preliminar.png:** Comparativa entre la corrida base y el incremento de fibra soluble (25 g).
- **resultados_escenarios.csv** (generado por *matriz_escenarios.py*): Tabla con las 27 variaciones de ingesta y su humedad final.

### 9. Control de Aleatoriedad / Semillas
El modelo es un sistema de Ecuaciones Diferenciales Ordinarias (EDO) determinista. No utiliza distribuciones estocásticas en esta fase, por lo que los resultados son 100% reproducibles de forma directa sin requerir semillas aleatorias (*seed*).

### 10. Problemas Conocidos y Limitaciones
- El modelo asume mezcla perfecta e instantánea dentro de cada compartimento.
- Los coeficientes de absorción k_abs se mantienen con valores provisionales de literatura de primer orden.
- No se incluye la clasificación automatizada de la Escala de Bristol debido a la falta de umbrales numéricos validados bibliográficamente.

### 11. Contacto Académico
- Danna Sofía Velandia Arciniegas – *dsvelandiag@ufpso.edu.co*
- Mairin Dayany Bayona Álvarez – *mdbayonaa@ufpso.edu.co*