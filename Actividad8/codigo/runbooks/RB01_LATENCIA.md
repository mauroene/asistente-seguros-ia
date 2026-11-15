# Latencia elevada — P2

## Impacto
Respuestas lentas para consultas válidas.

## Diagnostico
1. Revisar trazas y consumo del presupuesto de latencia.
2. Confirmar si existe retardo artificial; no atribuirlo al modelo sin evidencia.

## Respuesta
1. Si se confirma la inyección, desactivar únicamente el retardo del servicio simulado.
2. Registrar acción, hora, escenario y alerta de origen.

## Validacion
1. Procesar 100 consultas nuevas sin retardo y comprobar el SLO de latencia.
2. Verificar ausencia de fallos y registrar el cierre tras dos evaluaciones sanas nuevas.

## Escalamiento
Si no recupera, detener el ensayo y revisar recursos y trazas con el operador.

Responsable: operador del laboratorio (Mauro).
Estado: preparado; ejecución y recuperación pendientes.