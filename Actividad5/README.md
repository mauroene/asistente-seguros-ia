# Actividad 5. Entrenar, optimizar y evaluar modelos de aprendizaje automático mediante validación cruzada y MLflow

## Gestión de Proyectos de Inteligencia Artificial
**Módulo 2 – Semana 6**

### 1. Descripción del proyecto

Esta actividad forma parte del proyecto académico:

**Asistente inteligente para comprensión, orientación y
cotización de seguros de vida mediante inteligencia
artificial generativa.**

El propósito de la actividad es implementar un proceso
de preparación de datos, entrenamiento, optimización,
evaluación y seguimiento de modelos de aprendizaje
automático.

El trabajo se centra en la clasificación automática
de consultas relacionadas con seguros.

Los modelos desarrollados representan un componente
de clasificación que podría integrarse posteriormente
en el asistente inteligente del proyecto.

### 2. Objetivo

Preparar un dataset público de consultas relacionadas
con seguros, entrenar y comparar dos algoritmos de
clasificación, optimizar sus hiperparámetros mediante
validación cruzada y registrar los experimentos
utilizando MLflow.

Los modelos seleccionados fueron:

1. Regresión logística.
2. Random Forest.

Ambos se implementaron utilizando representaciones
textuales TF-IDF.

### 3. Dataset

**Fuente:** Hugging Face.

**Dataset:**
bitext/Bitext-insurance-llm-chatbot-training-dataset

**Enlace:**
https://huggingface.co/datasets/bitext/Bitext-insurance-llm-chatbot-training-dataset

El conjunto de datos contiene consultas relacionadas
con seguros, organizadas en 17 categorías.

#### Variables principales

| Variable | Descripción |
|---|---|
| instruction | Consulta formulada por el usuario |
| intent | Intención asociada a la consulta |
| category | Categoría de clasificación |
| tags | Etiquetas complementarias |
| response | Respuesta asociada |

#### Preparación y limpieza

Se realizaron las siguientes operaciones:

- Revisión de valores nulos.
- Identificación de registros duplicados.
- Estandarización de espacios en variables textuales.
- Eliminación de 17 consultas repetidas.
- Verificación de consistencia de categorías.

#### Resultados de preparación

| Indicador | Resultado |
|---|---:|
| Registros originales | 39,000 |
| Registros procesados | 38,983 |
| Registros eliminados | 17 |
| Categorías | 17 |
| Registros de entrenamiento | 31,186 |
| Registros de prueba | 7,797 |

Se utilizó una división estratificada del 80 % para
entrenamiento y 20 % para prueba.

Los archivos originales y procesados se encuentran
versionados en GitHub mediante archivos ZIP.

### 4. Modelos seleccionados y evaluación

Se entrenaron dos modelos supervisados de clasificación:

**Modelo 1: Regresión logística**

- Representación TF-IDF.
- Optimización mediante GridSearchCV.
- Validación cruzada de cinco particiones.
- C = 2.
- max_features = 5000.
- ngram_range = (1, 1).

**Modelo 2: Random Forest**

- Representación TF-IDF.
- Optimización mediante GridSearchCV.
- Validación cruzada de cinco particiones.
- n_estimators = 200.
- max_depth = None.
- min_samples_leaf = 1.

#### Resultados en el conjunto de prueba

| Métrica | Regresión logística | Random Forest |
|---|---:|---:|
| Accuracy | 0.9935 | 0.9909 |
| Precision macro | 0.9912 | 0.9871 |
| Recall macro | 0.9903 | 0.9856 |
| F1 macro | 0.9907 | 0.9863 |
| ROC-AUC | 0.9999 | 0.9998 |

La regresión logística presentó el mejor desempeño
general en las métricas evaluadas.

#### Comparación estadística

Se aplicó la prueba de McNemar para comparar las
predicciones de ambos modelos sobre el mismo conjunto
de prueba.

**Valor p:** 0.01111756.

El resultado indica una diferencia estadísticamente
significativa al nivel de 0.05.

### 5. Seguimiento de experimentos con MLflow

Se utilizó MLflow para documentar y comparar
los experimentos de entrenamiento.

Se registraron:

- Parámetros e hiperparámetros.
- Métricas de evaluación.
- Resultados comparativos.
- Gráficas y artefactos de los experimentos.

La información persistente de MLflow se almacenó
en Google Drive.

Se configuró un experimento persistente con dos
ejecuciones correspondientes a los modelos evaluados.

Los modelos entrenados también se conservaron
por separado en archivos Joblib.

### 6. Estructura del proyecto

La estructura de la Actividad 5 es:

```Actividad5/
├── datos/
│   ├── datos_ini/
│   │   └── seguros_original_v1.csv.zip
│   └── datos_limp/
│       └── seguros_limpio_v1.csv.zip
├── fuentes/
│   ├── entrena.ipynb
│   ├── datos_prep.py
│   └── train.py
├── resultados/
│   ├── graficos/
│   │   ├── Evidencia_011_comparacion_metricas.png
│   │   ├── Evidencia_012_comparacion_tiempos.png
│   │   ├── Evidencia_013_matriz_confusion_regresion_logistica.png
│   │   └── Evidencia_014_matriz_confusion_bosque_aleatorio.png
│   ├── evidencias_mlflow/
│   │   └── 6 capturas de los experimentos
│   ├── metricas_finales_v1.csv
│   ├── gridsearch_logistico_v1.csv
│   ├── gridsearch_random_forest_v1.csv
│   ├── comparacion_estadistica_mcnemar.csv
│   └── configuracion_modelos.json
├── README.md
└── CHANGELOG.md
```

**Descripción:**

- datos_ini: versión original del dataset.
- datos_limp: versión procesada del dataset.
- entrena.ipynb: notebook principal de experimentación.
- datos_prep.py: preparación y limpieza de datos.
- train.py: entrenamiento y evaluación de modelos.
- README.md: documentación general del proyecto.
- CHANGELOG.md: historial de versiones y modificaciones.

### 7. Reproducibilidad

El proyecto se desarrolló principalmente en
Google Colab utilizando Python.

#### Herramientas utilizadas

- Python.
- Google Colab.
- Hugging Face Datasets.
- Pandas.
- Scikit-learn.
- MLflow.
- Joblib.
- GitHub.

#### Procedimiento general

1. Obtener el dataset público desde Hugging Face.
2. Preparar y limpiar los datos.
3. Dividir los registros en entrenamiento y prueba.
4. Transformar las consultas mediante TF-IDF.
5. Entrenar los modelos de clasificación.
6. Optimizar los hiperparámetros mediante GridSearchCV.
7. Evaluar los modelos sobre el conjunto de prueba.
8. Realizar la comparación estadística.
9. Registrar métricas y artefactos en MLflow.
10. Conservar los resultados y modelos entrenados.

#### Archivos para reproducción

El notebook principal se encuentra en:

fuentes/entrena.ipynb

Los scripts de preparación y entrenamiento están en:

fuentes/datos_prep.py
fuentes/train.py

Los datasets publicados en GitHub deben descomprimirse
antes de utilizarse como archivos CSV.

**Consideración de ejecución:**

Los scripts se desarrollaron utilizando rutas de
Google Drive y archivos de configuración del entorno
de trabajo.

Para ejecutarlos en un entorno diferente es necesario
adaptar dichas rutas y disponer de las dependencias
y configuraciones correspondientes.

#### Verificación realizada

Se ejecutaron nuevamente los procesos de preparación
y entrenamiento.

Los resultados de evaluación coincidieron con las
métricas obtenidas durante los experimentos originales.

Esta comprobación permitió verificar la reproducibilidad
de los resultados en el entorno utilizado.

### 8. Estado del proyecto

**Estado actual: desarrollo, experimentación y publicación
de evidencias completados.**

Se finalizaron:

- Preparación y limpieza del dataset.
- Entrenamiento de regresión logística y Random Forest.
- Optimización de hiperparámetros mediante GridSearchCV.
- Evaluación de los modelos y comparación estadística
  mediante la prueba de McNemar.
- Registro persistente de experimentos en MLflow.
- Verificación de reproducibilidad de los resultados.
- Versionamiento de datos y código en GitHub.
- Publicación de cuatro gráficas de evaluación.
- Publicación de seis capturas de evidencia de MLflow.
- Publicación de métricas finales, resultados de
  optimización, comparación estadística y configuración
  de los modelos.

#### Evidencias disponibles

Los resultados y evidencias pueden consultarse en:

- [Gráficas de evaluación](resultados/graficos/)
- [Evidencias de MLflow](resultados/evidencias_mlflow/)
- [Resultados y configuración de modelos](resultados/)

#### Actividades pendientes

- Elaboración del reporte técnico final en PDF.
- Integración de tablas, gráficas y capturas en el reporte.
- Revisión académica conforme a la rúbrica.

**Actividad 5 – Semana 6.**
