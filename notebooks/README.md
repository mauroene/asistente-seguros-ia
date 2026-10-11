# Notebooks del proyecto

Esta carpeta contiene los dos notebooks de Google Colab utilizados para implementar, evaluar y comparar tres modelos preentrenados de Hugging Face en la clasificación de consultas sobre seguros de vida.

## 1. Comparación de modelos

**Archivo:** `Actividad_4_Comparacion_Modelos_Seguros_Vida.ipynb`

Contiene la preparación de los datos, configuración de las categorías, carga de los modelos y ejecución de las pruebas de clasificación.

La experimentación se realizó en Google Colab con una GPU NVIDIA Tesla T4. Se evaluaron tres modelos:

- multilingual-MiniLMv2-L6-mnli-xnli
- mDeBERTa-v3-base-mnli-xnli
- xlm-roberta-large-xnli

Se calcularon métricas de clasificación y tiempos de inferencia.

## 2. Evaluación final y verificación

**Archivo:** `Actividad_4_Evaluacion_Final_Modelos_Seguros_Vida.ipynb`

Permite recuperar los resultados de la experimentación, verificar la integridad de los archivos y analizar el desempeño de los modelos.

La ejecución documentada de este segundo notebook se realizó sin GPU, utilizando los resultados previamente generados. El notebook también contempla la posibilidad de realizar nuevas inferencias cuando se dispone de GPU.

## Datos y resultados

Los archivos utilizados se encuentran en las siguientes carpetas del repositorio:

- `data/`: conjuntos de desarrollo y prueba, configuración y trazabilidad.
- `results/`: métricas, predicciones, errores y matrices de confusión.
- `docs/`: registros de ejecución, verificación y decisión final.

## Entorno de ejecución

- Google Colab.
- Python.
- Bibliotecas indicadas en `requirements.txt`.
- GPU recomendada para ejecutar nuevamente la inferencia de los modelos.

## Orden de ejecución

1. Abrir el primer notebook en Google Colab y configurar el entorno.
2. Utilizar los datos preparados de `data/` para ejecutar la comparación.
3. Guardar los resultados de la evaluación.
4. Abrir el segundo notebook para verificar los archivos y analizar los resultados.
5. Consultar las métricas y evidencias almacenadas en `results/` y `docs/`.

Los resultados publicados corresponden a la evaluación académica del prototipo y no representan un sistema listo para producción.
