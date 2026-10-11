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

Se implementaron y compararon tres modelos preentrenados de Hugging Face para clasificar consultas en español relacionadas con seguros de vida.

| Modelo | Identificador en Hugging Face | Parámetros aproximados |
|---|---|---|
| MiniLMv2 | `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli` | 100 millones |
| mDeBERTa-v3-base | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` | 300 millones |
| XLM-RoBERTa-large | `joeddav/xlm-roberta-large-xnli` | 600 millones |

Los tres modelos se utilizaron mediante clasificación zero-shot, sin realizar un ajuste fino (fine-tuning).

Se definieron seis categorías de intención para las consultas:

1. `LIFE_INSURANCE`: información general sobre seguros de vida.
2. `COVERAGE`: coberturas y exclusiones.
3. `QUOTE`: cotizaciones.
4. `PAYMENT`: pagos.
5. `ENROLLMENT`: contratación, renovación y cancelación.
6. `CONTACT`: atención y contacto con un asesor.

La comparación consideró el desempeño de clasificación y la eficiencia de inferencia de cada modelo.

## Resultados

La evaluación final se realizó con 240 consultas en español sobre seguros de vida, distribuidas en seis categorías de intención (40 consultas por categoría).

Se utilizaron las métricas accuracy, precisión macro, recall macro y F1-score macro para comparar la calidad de clasificación. También se midió el tiempo promedio de inferencia por consulta.

| Modelo | Accuracy | Precisión macro | Recall macro | F1-score macro | Tiempo por consulta |
|---|---:|---:|---:|---:|---:|
| MiniLMv2 | 0.4417 | 0.4116 | 0.4417 | 0.4002 | 0.0772 s |
| mDeBERTa-v3-base | 0.3125 | 0.5596 | 0.3125 | 0.2893 | 0.1421 s |
| XLM-RoBERTa-large | 0.6583 | 0.7460 | 0.6583 | 0.6492 | 0.1108 s |

XLM-RoBERTa-large obtuvo el mejor desempeño general, con un F1-score macro de 0.6492 y una exactitud de 65.83 %.

MiniLMv2 fue el modelo más rápido, con un tiempo promedio de 0.0772 segundos por consulta.

Aunque XLM-RoBERTa-large presentó los mejores resultados, su desempeño todavía es insuficiente para utilizarlo en producción sin mejoras y validaciones adicionales.

## Conclusiones

La evaluación comparativa permitió identificar diferencias importantes en el desempeño y la eficiencia de los tres modelos preentrenados de Hugging Face.

XLM-RoBERTa-large obtuvo el mejor resultado general, con un F1-score macro de 0.6492 y una exactitud de 65.83 %, por lo que se seleccionó como la alternativa más adecuada para continuar desarrollando el prototipo de clasificación de consultas sobre seguros de vida.

MiniLMv2 presentó el menor tiempo de inferencia, con 0.0772 segundos por consulta, lo que lo convierte en una alternativa interesante para escenarios donde la velocidad de respuesta sea prioritaria.

Por su parte, mDeBERTa-v3-base obtuvo resultados inferiores en la evaluación general, por lo que no se seleccionó como modelo principal.

Los resultados también evidenciaron limitaciones importantes, especialmente en las categorías PAYMENT y ENROLLMENT. Por ello, el modelo seleccionado todavía no reúne las condiciones necesarias para implementarse en un entorno de producción.

Como trabajo futuro, se propone ampliar y mejorar el conjunto de datos, analizar los errores de clasificación, optimizar las descripciones de las categorías y evaluar técnicas de ajuste fino.

En conclusión, la implementación permitió demostrar la viabilidad técnica de utilizar modelos preentrenados para identificar intenciones en consultas relacionadas con seguros de vida, aunque se requieren mejoras adicionales para alcanzar un desempeño confiable en aplicaciones reales.

## Reproducibilidad

El proyecto se desarrolló mediante dos notebooks de Google Colab que permiten documentar la implementación, evaluación y verificación de los modelos preentrenados.

### Requisitos

- Python y acceso a Google Colab.
- Bibliotecas especificadas en `requirements.txt`.
- Conexión a Internet para descargar los modelos de Hugging Face.
- GPU recomendada para ejecutar nuevamente las inferencias.

### Pasos de ejecución

1. Descargar o clonar el repositorio de GitHub.
2. Abrir Google Colab y cargar el primer notebook de la carpeta `notebooks/`.
3. Instalar las dependencias necesarias y preparar el entorno de ejecución.
4. Cargar los datos de evaluación y los modelos preentrenados.
5. Ejecutar las celdas del primer notebook para realizar las inferencias y generar los resultados.
6. Guardar los archivos de datos, configuración y resultados generados.
7. Abrir el segundo notebook y proporcionar los archivos de soporte correspondientes.
8. Ejecutar las celdas de verificación para comprobar la integridad de los archivos y recuperar las métricas obtenidas.

### Consideraciones de ejecución

La evaluación original se realizó utilizando una GPU NVIDIA Tesla T4.

El segundo notebook también permite recuperar y verificar resultados previamente generados sin disponer de una GPU. Esta modalidad no ejecuta nuevamente las inferencias y, por tanto, no debe confundirse con una nueva evaluación de los modelos.

Para reproducir completamente los experimentos es necesario disponer de los datos preparados, los notebooks y los archivos de configuración correspondientes.

Los resultados reportados corresponden a una evaluación experimental de un prototipo académico y no constituyen una validación para su uso en producción.
