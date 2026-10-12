# Historial de cambios – Actividad 5

## Gestión de Proyectos de Inteligencia Artificial
Módulo 2 – Semana 6

Este documento registra las modificaciones realizadas
durante el desarrollo de la Actividad 5.

Su propósito es mantener la trazabilidad de los datos,
el código, los modelos y los experimentos.

---

## Versión 0.1.0 – 11 de octubre de 2026

### Preparación del proyecto

- Creación de la carpeta Actividad5.
- Creación de la estructura para datos originales.
- Creación de la estructura para datos procesados.
- Creación de la carpeta de código fuente.
- Elaboración inicial del archivo README.md.
- Definición del problema de clasificación de consultas.
- Selección de regresión logística y Random Forest.
- Selección del dataset público de Hugging Face.

### Estado

Estructura inicial del proyecto creada.

Pendiente:
- Obtención y preparación del dataset.
- Análisis exploratorio de datos.
- Entrenamiento de modelos.
- Ajuste de hiperparámetros.
- Configuración de MLflow.
- Comparación y documentación de resultados.

---

## Próximas versiones

Los cambios posteriores se documentarán indicando:

- Número de versión.
- Fecha de modificación.
- Archivos modificados.
- Transformaciones realizadas al dataset.
- Cambios en modelos e hiperparámetros.
- Resultados y evidencias generadas.

---

## Versión 0.2.0 – 11 de octubre de 2026

### Obtención y preparación de datos

- Descarga del dataset público de Hugging Face.
- Verificación de 39,000 registros y cinco columnas.
- Identificación de 17 categorías de clasificación.
- Comprobación de valores nulos y cadenas vacías.
- Identificación de 17 consultas repetidas.
- Confirmación de ausencia de conflictos entre categorías.
- Estandarización de espacios en variables textuales.
- Eliminación de 17 consultas repetidas.
- Generación del dataset limpio con 38,983 registros.

### Resultados de calidad

| Indicador | Resultado |
|---|---:|
| Registros originales | 39,000 |
| Registros procesados | 38,983 |
| Registros eliminados | 17 |
| Porcentaje eliminado | 0.0436% |
| Valores nulos | 0 |
| Conflictos entre categorías | 0 |
| Categorías | 17 |

### Análisis exploratorio

- Generación de la gráfica de distribución de categorías.
- Identificación de desequilibrio entre clases.
- Categoría mayoritaria: CLAIMS, con 5,997 registros.
- Categoría LIFE_INSURANCE: 999 registros (2.56%).
- Selección de F1 macro como métrica principal de comparación.

### Almacenamiento

Se generaron dos archivos CSV:

- seguros_original_v1.csv
- seguros_limpio_v1.csv

Ambos se almacenaron en Google Drive, dentro de
Master IA / Gestión de Proyectos / Modulo 2 / Actividad 5.

### Estado

Preparación inicial de datos completada.

Pendiente:
- Incorporar scripts de preparación al repositorio.
- Documentar la obtención reproducible del dataset.
- Dividir los datos en entrenamiento y prueba.
- Entrenar los modelos de clasificación.
- Configurar y registrar experimentos con MLflow.
