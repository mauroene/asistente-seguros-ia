# Resultados de la evaluación

Esta carpeta contiene los resultados obtenidos al comparar tres modelos preentrenados de Hugging Face para clasificar consultas en español relacionadas con seguros de vida.

La evaluación se realizó sobre un conjunto de prueba de 240 consultas, distribuidas en seis categorías, con 40 consultas por categoría.

## Modelos evaluados

1. MiniLMv2 multilingüe.
2. mDeBERTa-v3-base.
3. XLM-RoBERTa-large.

Los tres modelos se evaluaron mediante clasificación zero-shot, sin realizar entrenamiento adicional ni ajuste fino.

## Comparación general

| Modelo | Accuracy | Precisión macro | Recall macro | F1 macro | Aciertos | Tiempo por consulta |
|---|---:|---:|---:|---:|---:|---:|
| MiniLMv2 | 0.4417 | 0.4116 | 0.4417 | 0.4002 | 106/240 | 0.0772 s |
| mDeBERTa-v3-base | 0.3125 | 0.5596 | 0.3125 | 0.2893 | 75/240 | 0.1421 s |
| XLM-RoBERTa-large | 0.6583 | 0.7460 | 0.6583 | 0.6492 | 158/240 | 0.1108 s |

Las métricas se obtuvieron durante la evaluación experimental documentada en los notebooks del proyecto.

## Interpretación de resultados

XLM-RoBERTa-large obtuvo el mejor desempeño general, con un F1 macro de 0.6492 y una exactitud de 65.83 %.

MiniLMv2 presentó el menor tiempo de inferencia, con aproximadamente 0.0772 segundos por consulta, por lo que constituye una alternativa más rápida, aunque con menor desempeño de clasificación.

mDeBERTa-v3-base obtuvo resultados inferiores en exactitud y F1 macro dentro de esta evaluación.

## Limitaciones identificadas

Aunque XLM-RoBERTa-large fue el modelo con mejor desempeño general, presentó dificultades en determinadas categorías.

En particular, las categorías PAYMENT y ENROLLMENT alcanzaron una exhaustividad (recall) de 0.425 cada una, equivalente a 17 aciertos de 40 consultas por categoría.

Por ello, el modelo seleccionado debe considerarse una alternativa para continuar desarrollando el prototipo académico, no una solución lista para producción.

## Archivos disponibles

- `comparacion_prueba.csv`: comparación general de los tres modelos.
- `metricas_por_categoria.csv`: precisión, recall y F1 por categoría y modelo.
- `confusiones_frecuentes.csv`: principales confusiones de clasificación.
- `modelo_1_predicciones.csv`, `modelo_2_predicciones.csv` y `modelo_3_predicciones.csv`: predicciones individuales.
- `modelo_1_errores.csv`, `modelo_2_errores.csv` y `modelo_3_errores.csv`: registros de errores.
- `modelo_1_matriz_confusion.csv`, `modelo_2_matriz_confusion.csv` y `modelo_3_matriz_confusion.csv`: matrices de confusión.
- `modelo_1_metricas_categoria.csv`, `modelo_2_metricas_categoria.csv` y `modelo_3_metricas_categoria.csv`: métricas individuales por categoría.

## Conclusión

Se seleccionó XLM-RoBERTa-large como la alternativa más adecuada para continuar el desarrollo del prototipo, debido a su mejor equilibrio entre desempeño de clasificación y tiempo de inferencia.

Antes de considerar una implementación operativa, será necesario ampliar y validar los datos, mejorar el desempeño de las categorías con mayores errores y realizar nuevas pruebas.

Los resultados corresponden exclusivamente al alcance experimental de esta actividad académica.
