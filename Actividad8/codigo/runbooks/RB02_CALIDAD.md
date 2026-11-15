# Degradación del clasificador — P2

## Impacto
Consultas asignadas a categorías incorrectas.

## Diagnostico
1. Comparar las 74 consultas etiquetadas con el baseline y verificar la integridad de sus etiquetas.
2. Comprobar variante activa y orden de clases; no deducir calidad del puntaje sin calibrar.

## Respuesta
1. Ante una variante degradada confirmada, restaurar la referencia en memoria al modelo V3 estable.
2. Conservar el original y registrar variante anterior, nueva, hora y alerta. No reentrenar.

## Validacion
1. Repetir las 74 preguntas con V3 restaurada y comprobar exactitud mínima del 80 %.
2. Comparar con el baseline, comprobar ausencia de fallos y registrar la recuperación.

## Escalamiento
Si V3 estable tampoco cumple, detener cambios automáticos y revisar datos y etiquetas.

Responsable: operador del laboratorio (Mauro).
Estado: preparado; ejecución y recuperación pendientes.