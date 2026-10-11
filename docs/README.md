# Documentación técnica del proyecto

Esta carpeta reúne los archivos de configuración, trazabilidad y verificación utilizados durante la evaluación de tres modelos preentrenados de Hugging Face para clasificar consultas en español sobre seguros de vida.

Los documentos permiten identificar el entorno de ejecución, consultar los registros experimentales y justificar la selección del modelo con mejor desempeño.

## Archivos disponibles

| Archivo | Descripción |
|---|---|
| `LEEME_COLAB_2.txt` | Instrucciones de ejecución y uso del segundo notebook de Google Colab. |
| `configuracion_modelo_seleccionado.json` | Configuración registrada para el modelo seleccionado. |
| `decision_final.json` | Registro de la decisión final sobre el modelo elegido para continuar el prototipo. |
| `entorno_actual_notebook.json` | Información del entorno correspondiente a la sesión de verificación. |
| `inventario_archivos.csv` | Inventario de los archivos incluidos en el paquete de resultados. |
| `manifest_entrega.json` | Manifiesto del paquete de entrega y sus componentes. |
| `registro_evaluacion_original.json` | Registro de la evaluación experimental original. |
| `registro_resultados.json` | Registro de resultados utilizado para su recuperación y verificación. |

## Entorno de ejecución

La evaluación experimental inicial se realizó en Google Colab utilizando una GPU NVIDIA Tesla T4.

Posteriormente, se utilizó un segundo notebook para recuperar y verificar los resultados previamente generados. La ejecución documentada de esta segunda sesión se realizó sin GPU.

Los registros correspondientes se encuentran en los archivos JSON de esta carpeta.

## Selección del modelo

Se seleccionó **XLM-RoBERTa-large** para continuar el desarrollo del prototipo académico.

La decisión se fundamentó en los resultados obtenidos sobre 240 consultas de prueba:

- Accuracy: 0.6583.
- Precisión macro: 0.7460.
- Recall macro: 0.6583.
- F1 macro: 0.6492.
- Tiempo promedio de inferencia: 0.1108 segundos por consulta.

Este modelo obtuvo el mejor desempeño general de los tres evaluados.

## Limitaciones

La selección corresponde a una evaluación académica de clasificación zero-shot, sin ajuste fino de los modelos.

Los resultados todavía no son suficientes para considerar el prototipo apto para producción. Se requiere mejorar el desempeño de las categorías con mayores errores y realizar nuevas validaciones.

## Relación con otras carpetas

- `data/`: conjuntos de datos y archivos de preparación.
- `notebooks/`: implementación, evaluación y verificación.
- `results/`: métricas, predicciones, errores y matrices de confusión.

La documentación de esta carpeta complementa los resultados experimentales y permite dar seguimiento a las decisiones técnicas del proyecto.
