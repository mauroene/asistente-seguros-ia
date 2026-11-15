# Actividad 8 — Monitorización de VidaSegura

En esta actividad implementé un laboratorio en Google Colab para monitorear el clasificador VidaSegura en español, detectar problemas y comprobar su recuperación mediante respuestas automatizadas.

El modelo V3 utiliza regresión logística con TF-IDF y clasifica consultas de seguros de vida en siete categorías. No genera respuestas contractuales.

## Implementación

- Métricas de éxito técnico, latencia, exactitud y F1 macro.
- Logs y trazas correlacionados mediante el identificador de cada solicitud.
- Seguimiento de ejecuciones y artefactos con MLflow.
- Dashboard actualizado durante los ensayos.
- Detección de cambios en las entradas mediante señales de longitud y vocabulario.
- Alertas vinculadas con objetivos de servicio y presupuestos de error.
- Priorización, deduplicación y procedimientos de respuesta mediante runbooks.

## Incidentes simulados

### Aumento de latencia

Inyecté un retardo artificial de 300 ms. La latencia p95 pasó de 6.38 ms antes del incidente a 305.30 ms durante la falla. Después de retirar automáticamente el retardo, se recuperó a 7.66 ms.

### Degradación de la clasificación

Alteré la correspondencia de categorías en una copia del modelo en memoria. Los aciertos pasaron de 65 a 1 sobre las mismas 74 preguntas. Después de restaurar V3, se recuperaron los 65 aciertos y las predicciones anteriores.

El modelo original permaneció intacto en ambos ensayos.

## Evidencias y reproducibilidad

La ejecución de referencia es `act8_20261115T183737Z_2601a7`, del 15 de noviembre de 2026.

Se generaron configuraciones, logs, trazas, registros de alertas y acciones, gráficas y exportes de MLflow. La auditoría experimental registró 19 controles satisfactorios.

Los archivos de código, modelo y evidencias se incorporarán a esta carpeta para permitir su consulta y reproducción.

## Alcance y limitaciones

El trabajo corresponde a un laboratorio con fallas controladas, no a un despliegue en producción.

Las 74 preguntas diagnósticas eran conocidas durante el desarrollo; sus resultados no representan una evaluación externa ciega. Los tiempos medidos corresponden a ensayos individuales.

La alerta de drift permaneció activa después de restaurar el modelo porque las entradas seguían siendo diferentes de la referencia. Esta señal requiere revisión y no demuestra por sí sola una pérdida de exactitud.

GitHub conserva el trabajo y sus evidencias; la entrega académica se prepara por separado con los documentos finales y el código.
