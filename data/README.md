# Datos del proyecto

Esta carpeta contiene los datos preparados para evaluar tres modelos
preentrenados de Hugging Face en la clasificación de consultas sobre
seguros de vida.

## Origen de los datos

Se utilizó como referencia el dataset público
`bitext/Bitext-insurance-llm-chatbot-training-dataset`,
disponible en Hugging Face.

A partir de este conjunto se prepararon 300 consultas en español,
organizadas en seis categorías:

- LIFE_INSURANCE
- COVERAGE
- QUOTE
- PAYMENT
- ENROLLMENT
- CONTACT

## Distribución

El conjunto se dividió en:

- Desarrollo: 60 consultas.
- Prueba: 240 consultas, con 40 por categoría.

## Archivos

- `dataset_desarrollo.csv`: consultas de desarrollo.
- `dataset_prueba.csv`: consultas de evaluación final.
- `dataset_completo_trazabilidad.csv`: conjunto preparado y trazabilidad.
- `distribucion_dataset.csv`: distribución de los datos.
- `registros_retirados.csv`: registros excluidos durante la preparación.
- `configuracion_para_prueba.json`: configuración de la evaluación.
- `manifest_insumos.json`: manifiesto para verificar la integridad
  de los archivos.

Los procedimientos de preparación y evaluación se encuentran
documentados en los notebooks de la carpeta `notebooks/`.
