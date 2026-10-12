# Actividad 5. Preparación de datos, entrenamiento y seguimiento de modelos

## Gestión de Proyectos de Inteligencia Artificial
**Módulo 2 – Semana 6**

### 1. Descripción del proyecto

Esta actividad forma parte del proyecto académico
"Asistente inteligente para comprensión, orientación y
cotización de seguros de vida mediante inteligencia
artificial generativa".

Su propósito es implementar un proceso reproducible
de preparación de datos, entrenamiento, evaluación
y comparación de modelos de aprendizaje automático.

### 2. Objetivo

Preparar un dataset público relacionado con consultas
de seguros, entrenar y comparar dos algoritmos de
clasificación y registrar los experimentos mediante MLflow.

### 3. Dataset

Se utilizará el dataset público:

bitext/Bitext-insurance-llm-chatbot-training-dataset

Fuente: Hugging Face.

El conjunto contiene aproximadamente 39,000 registros
de consultas relacionadas con seguros.

Las variables principales son:

- instruction: consulta del usuario.
- intent: intención de la consulta.
- category: categoría de la consulta.
- tags: etiquetas asociadas.
- response: respuesta correspondiente.

El problema abordado será la clasificación automática
de consultas relacionadas con seguros.

### 4. Modelos seleccionados

Se utilizarán dos algoritmos de clasificación:

1. Regresión logística.
2. Random Forest.

Los textos serán transformados mediante TF-IDF.

Los modelos serán evaluados mediante métricas
estandarizadas y validación cruzada.

### 5. Seguimiento de experimentos

Se utilizará MLflow para registrar:

- Parámetros e hiperparámetros.
- Métricas de evaluación.
- Modelos entrenados.
- Artefactos generados.
- Resultados comparativos.

### 6. Estructura del proyecto

- datos/datos_ini/: datos originales.
- datos/datos_limp/: datos procesados.
- fuentes/entrena.ipynb: notebook principal.
- fuentes/datos_prep.py: preparación de datos.
- fuentes/train.py: entrenamiento y evaluación.
- README.md: documentación y reproducibilidad.
- CHANGELOG.md: historial de modificaciones.

### 7. Reproducibilidad

El proyecto se desarrollará principalmente en
Google Colab utilizando Python.

Se documentarán las dependencias, configuraciones,
semillas aleatorias y procedimientos necesarios
para reproducir los experimentos.

Las instrucciones de ejecución se completarán
una vez validados los modelos y MLflow.

### 8. Estado del proyecto

En desarrollo.

Actividad 5 – Semana 6.
