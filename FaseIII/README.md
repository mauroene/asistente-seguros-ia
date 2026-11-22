# VidaSegura ES V3 · Fase III

El pipeline verifica el paquete congelado de Actividad 8, reproduce sus predicciones históricas y
levanta una API temporal en localhost para verificar la revisión a través de HTTP. La aplicación de
Fase II y los materiales de Actividades 4, 5 y 8 se conservan en sus rutas originales.

## Inventario y alcance

| Fuente | Componentes verificados | Aplicación en Fase III |
|---|---|---|
| Fase II | FastAPI, Streamlit, Docker Compose y pruebas del clasificador en inglés de Actividad 5 | Antecedente de integración y despliegue local |
| Actividad 8 | ZIP de V3, cargador, predicciones, metadatos, MLflow, alertas y runbooks de laboratorio | Fuente del artefacto y de los casos de regresión |
| Actividad 9 | Streamlit local, mediciones, auditoría lingüística y diseño de piloto en Azure | Referencias para operación, métricas y mejoras |
| Fase III | El commit base carecía de CI y de un flujo automatizado para desplegar el V3 | Manifiesto versionado, pruebas, GitHub Actions y despliegue HTTP local |

La revisión `vidasegura-es-v3-1` referencia el modelo versión `3` y la ejecución
`es_v3_20261111T023400Z_13c684`. El manifiesto `revision.json` fija el ZIP, la huella del modelo
y la lista ordenada de las siete categorías. Se extraen tres archivos a un directorio temporal
después de validar el ZIP. Se comprueba el entorno y se ejecuta el cargador original con el
artefacto byte a byte. El pipeline solo realiza inferencia.

## Reproducir en una copia Git

Requiere Python 3.11. El modelo se guardó con 3.11.15 y el workflow configura 3.11.18 en Ubuntu 24.04.
Desde la raíz del repositorio:

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r FaseIII/requirements.txt
python FaseIII/pipeline.py --evidencia ../resultado-vidasegura.json
```

Cada ejecución exitosa escribe un JSON nuevo con el commit, el estado de la copia local, las
huellas, las versiones, los controles HTTP y una muestra de latencia. Usa una ruta nueva para
cada ejecución. Una regresión, un fallo de arranque o un control HTTP fallido termina con un
código de error. La regresión reproduce 74 predicciones diagnósticas y 63 sintéticas, además
de los puntajes sintéticos con tolerancia numérica. Son referencias históricas de comportamiento.

Para mantener el servicio disponible durante una demostración:

```sh
python FaseIII/servicio.py --puerto 8003
```

En otra terminal:

```sh
curl -fsS http://127.0.0.1:8003/salud
curl -fsS http://127.0.0.1:8003/clasificar -H 'Content-Type: application/json' \
  -d '{"texto":"¿Cuánto cuesta el seguro de vida?"}'
```

El servicio registra estado HTTP, revisión y, cuando existe una inferencia, su identificador,
estado y latencia. La telemetría ordinaria omite el texto de las consultas. El servicio usa
un servidor de referencia de Python en localhost para el entorno académico controlado.

## Integración continua y control de revisiones

El workflow corre en solicitudes de cambio a `main`, en cambios enviados a `main` o
`fase-iii/**` y de forma manual. Repite el comando del pipeline en Ubuntu y conserva el registro
y el JSON de éxito como evidencia. Git define la revisión deseada. El job aplica esa revisión
en un entorno efímero y comprueba que el endpoint de salud declara las huellas esperadas.
Este es un flujo GitOps simulado y el proceso termina al concluir las pruebas.

Antes de integrar, revisar el manifiesto y el resultado del workflow en la rama acordada.
Si se requiere revertir una integración, usar un commit de reversión del cambio aprobado y
ejecutar de nuevo el pipeline. Comparar el endpoint de salud con el manifiesto restaurado.
Cuando exista una revisión estable anterior, puede hacerse la demostración en una copia Git
de esa revisión. Este incremento inicial todavía carece de un ensayo de reversión entre dos
revisiones publicadas.

## Evidencia restante para la entrega

- **Antes del 28 de noviembre** · Acordar la publicación de la rama y capturar el enlace e
  identificador de una ejecución real de GitHub Actions cuando esté autorizada.
- **Sábado 28** · Incorporar evidencia operativa de latencia HTTP p50/p95 y fallos con un
  protocolo de carga; vincular alertas y runbooks de Actividad 8. Usar las cifras de Actividad 9
  como referencia de inferencia sin red y su prueba lingüística como hallazgo exploratorio.
- **Domingo 29** · Cerrar el portfolio, la presentación y la práctica de entrevista con los
  cuatro criterios de la rúbrica. Adjuntar y verificar los archivos finales de entrega.
