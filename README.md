# Asistente de Seguros con Inteligencia Artificial

## Descripción del proyecto

Este proyecto desarrolla un prototipo de inteligencia artificial orientado a la clasificación automática de consultas relacionadas con seguros de vida.

La solución forma parte del desarrollo académico de la materia Gestión de Proyectos de Inteligencia Artificial y utiliza modelos preentrenados disponibles en Hugging Face para analizar y comparar su desempeño en un caso de uso relacionado con el sector asegurador.

## Objetivo

Evaluar diferentes modelos preentrenados de Hugging Face para identificar una alternativa adecuada para la clasificación de consultas relacionadas con seguros de vida, considerando tanto su desempeño como su eficiencia.

La evaluación contempla métricas como accuracy, precision, recall y F1-score, así como el tiempo de inferencia de los modelos.

## Caso de uso

El caso de uso consiste en clasificar consultas relacionadas con seguros de vida de acuerdo con su intención o categoría.

Este componente podrá utilizarse posteriormente como parte de un asistente inteligente capaz de orientar al usuario y dirigir cada consulta hacia el proceso o fuente de información correspondiente.

## Entorno de ejecución

El proyecto se desarrolló en Python mediante Google Colab, utilizando bibliotecas del ecosistema Hugging Face para implementar y evaluar tres modelos preentrenados de clasificación de texto.

La evaluación original se realizó con una GPU NVIDIA Tesla T4, utilizando aproximadamente 12.67 GB de memoria RAM y 14.56 GB de memoria de GPU disponibles en el entorno.

Las principales tecnologías y bibliotecas utilizadas fueron Python, Google Colab, Transformers, Datasets, PyTorch, Hugging Face Hub, scikit-learn, Pandas y NumPy.

El desarrollo se organizó en dos notebooks complementarios. El primero permitió ejecutar los experimentos y generar las métricas originales. El segundo incorporó mecanismos para repetir la evaluación cuando existe una GPU disponible o recuperar y verificar las evidencias previamente generadas cuando no se dispone de ella.

Las dependencias necesarias se encuentran especificadas en el archivo `requirements.txt`.

## Estructura del repositorio

```text
asistente-seguros-ia/
├── data/          # Datos utilizados en el proyecto
├── docs/          # Documentación técnica y análisis
├── notebooks/     # Notebooks de Google Colab
├── results/       # Resultados y métricas de evaluación
├── src/           # Scripts y módulos reutilizables
├── .gitignore
├── README.md
└── requirements.txt
```

## Metodología

El desarrollo contempla las siguientes etapas:

1. Definición del caso de uso.
2. Selección de modelos preentrenados de Hugging Face.
3. Preparación del conjunto de datos.
4. Implementación e inferencia en Google Colab.
5. Evaluación mediante accuracy, precision, recall y F1-score.
6. Medición del tiempo de inferencia.
7. Comparación de los modelos.
8. Selección y justificación del modelo más adecuado.

## Modelos evaluados

Esta sección se completará una vez realizada la selección e implementación de los modelos.

## Resultados

Los resultados se incorporarán después de ejecutar los experimentos y obtener las métricas correspondientes.

## Conclusiones

Las conclusiones se documentarán al finalizar la evaluación comparativa de los modelos.

## Reproducibilidad

Las instrucciones detalladas para reproducir los experimentos se incorporarán conforme avance la implementación del prototipo.
