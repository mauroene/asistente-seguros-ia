
from pathlib import Path
import json
import sys
from mlflow import MlflowClient


def consultar_mlflow(uri, run_id):
    """
    Consulta una ejecución existente sin modificarla.

    Parámetros:
        uri (str): ubicación del almacenamiento de MLflow.
        run_id (str): identificador de la ejecución.

    Retorna:
        dict: experimento, estado, métricas, parámetros,
              etiquetas y listado de archivos asociados.
    """
    cliente = MlflowClient(tracking_uri=uri)
    run = cliente.get_run(run_id)
    experimento = cliente.get_experiment(run.info.experiment_id)

    # Recorrer las carpetas para recuperar los archivos asociados.
    archivos = []
    pendientes = [""]

    while pendientes:
        carpeta = pendientes.pop()

        for item in cliente.list_artifacts(run_id, path=carpeta):
            if item.is_dir:
                pendientes.append(item.path)
            else:
                archivos.append({
                    "ruta": item.path,
                    "tamano_bytes": item.file_size,
                })

    return {
        "experimento": experimento.name,
        "experiment_id": experimento.experiment_id,
        "run_id": run.info.run_id,
        "nombre_run": run.data.tags.get("mlflow.runName", ""),
        "estado": run.info.status,
        "metricas": dict(run.data.metrics),
        "parametros": dict(run.data.params),
        "etiquetas": dict(run.data.tags),
        "artefactos": archivos,
        "metodo": "Consulta directa mediante MlflowClient",
    }


if __name__ == "__main__":
    datos = consultar_mlflow(sys.argv[1], sys.argv[2])

    Path(sys.argv[3]).write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
