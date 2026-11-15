# Fallos internos — P1

## Impacto
Solicitudes válidas que el servicio no puede atender.

## Diagnostico
1. Revisar errores y trazas; separar entradas inválidas de fallos internos.
2. Confirmar si se activó una inyección de fallo.

## Respuesta
1. Desactivar la inyección solo si está confirmada; no ocultar errores desconocidos.
2. Conservar registros de la causa y de la acción.

## Validacion
1. Procesar 100 solicitudes válidas nuevas y comprobar éxito técnico mínimo del 99 %.
2. Comprobar dos evaluaciones sanas nuevas y registrar el cierre.

## Escalamiento
Si persiste, detener el ensayo y solicitar diagnóstico al operador.

Responsable: operador del laboratorio (Mauro).
Estado: preparado; ejecución y recuperación pendientes.