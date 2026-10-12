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

---

## Versión 0.3.0 – 11 de octubre de 2026

### Entrenamiento y optimización de modelos

- Implementación de dos modelos de clasificación de consultas relacionadas con seguros:
  - Regresión logística.
  - Random Forest.
- Transformación de las consultas mediante TF-IDF.
- División estratificada del dataset en entrenamiento y prueba:
  - Entrenamiento: 31,186 registros.
  - Prueba: 7,797 registros.
- Aplicación de validación cruzada de cinco particiones.
- Optimización de hiperparámetros mediante GridSearchCV.
- Selección de F1 macro como métrica principal.

### Hiperparámetros optimizados

**Regresión logística:**
- C = 2.
- max_features = 5000.
- ngram_range = (1, 1).

**Random Forest:**
- n_estimators = 200.
- max_depth = None.
- min_samples_leaf = 1.

### Evaluación de modelos

| Métrica | Regresión logística | Random Forest |
|---|---:|---:|
| Accuracy | 0.9935 | 0.9909 |
| Precision macro | 0.9912 | 0.9871 |
| Recall macro | 0.9903 | 0.9856 |
| F1 macro | 0.9907 | 0.9863 |
| ROC-AUC | 0.9999 | 0.9998 |

La regresión logística obtuvo el mejor desempeño general.

### Comparación estadística

- Aplicación de la prueba de McNemar.
- Valor p = 0.01111756.
- Se identificó una diferencia estadísticamente significativa
  entre los modelos al nivel de significancia de 0.05.

### Seguimiento con MLflow

- Configuración de MLflow con almacenamiento persistente
  en Google Drive.
- Registro de dos ejecuciones correspondientes a los modelos.
- Almacenamiento de parámetros, métricas y artefactos.
- Conservación de gráficas y resultados comparativos.

### Reproducibilidad

- Elaboración de datos_prep.py para preparar los datos.
- Elaboración de train.py para entrenar y evaluar los modelos.
- Verificación de la preparación del dataset.
- Ejecución independiente del entrenamiento.
- Confirmación de coincidencia entre las métricas originales
  y las obtenidas durante la verificación.
- Conservación del notebook definitivo entrena.ipynb.

### Estado

Entrenamiento, optimización, evaluación y verificación
de reproducibilidad completados.

---

## Versión 0.4.0 – 12 de octubre de 2026

### Publicación y versionamiento en GitHub

- Incorporación del dataset original al repositorio:
  datos/datos_ini/seguros_original_v1.csv.zip
- Incorporación del dataset procesado:
  datos/datos_limp/seguros_limpio_v1.csv.zip
- Compresión sin pérdida de los archivos CSV para facilitar
  su publicación mediante el navegador.
- Publicación del notebook principal:
  fuentes/entrena.ipynb
- Publicación de los scripts:
  fuentes/datos_prep.py
  fuentes/train.py
- Registro de los cambios mediante commits en GitHub.

### Documentación

- Actualización del historial de cambios.
- Preparación de la documentación técnica del proyecto.
- Actualización de la información sobre modelos,
  datasets, resultados y reproducibilidad.

### Estado

Datos y código fuente incorporados al repositorio.

Pendiente:
- Incorporar las evidencias visuales de MLflow.
- Completar el reporte técnico en PDF.
- Realizar la revisión final conforme a la rúbrica.
