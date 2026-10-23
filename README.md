# Simulación Dinámica del Tránsito Colónico e Hidratación Fecal

Modelo compartimental continuo basado en balance de masa de fibra y agua ($3^3 = 27$ escenarios dietarios) para la materia de **Modelado y Simulación de Sistemas** en la **Universidad Francisco de Paula Santander Ocaña (UFPSO)**.

---

## Integrantes y Docente
* **Estudiantes:** Danna Sofía Velandia Arciniegas & Mairin Dayany Bayona Alvarez
* **Docente Asesor:** Ing. Jesús Eduardo Guerrero Rodríguez
* **Semestre:** 5.º Semestre - Ingeniería de Sistemas (2026)

---

## Estructura del Repositorio
* `simulador.py`: Modelo biofísico de EDOs resuelto con algoritmo Runge-Kutta 4-5 (`scipy.integrate.solve_ivp`).
* `matriz_escenarios.py`: Script para la ejecución automatizada de la matriz factorial de 27 escenarios.
* `requirements.txt`: Dependencias científicas del entorno de Python (`numpy`, `scipy`, `pandas`).

---

## Cómo Ejecutar la Simulación

1. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
2. Probar el modelo base con 3 escenarios piloto:
    ```Terminal
    python simulador.py
3. Ejecutar la matriz completa de 27 escenarios y generar el archivo CSV:
    ```Terminal
    python matriz_escenarios.py