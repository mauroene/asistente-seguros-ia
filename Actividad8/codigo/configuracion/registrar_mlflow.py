
from pathlib import Path
import sys
import json
import math
import mlflow
from mlflow import MlflowClient


def registrar(especificacion):
    """
    Registra una ejecución y comprueba las métricas recuperadas.

    Parámetros:
        especificacion (dict): ubicación, experimento,
            parámetros, métricas y archivos asociados.

    Retorna:
        dict: identificadores, estado y métricas verificadas.
    """
    mlflow.set_tracking_uri(especificacion["uri"])
    cliente = MlflowClient()

    experimento = cliente.get_experiment_by_name(
        especificacion["experimento"]
    )

    if experimento is None:
        experiment_id = cliente.create_experiment(
            especificacion["experimento"],
            artifact_location=Path(
                especificacion["artefactos"]
            ).as_uri(),
        )
    else:
        experiment_id = experimento.experiment_id

    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name=especificacion["nombre_run"],
    ) as run:
        mlflow.set_tags(especificacion["etiquetas"])
        mlflow.log_params(especificacion["parametros"])
        mlflow.log_metrics(especificacion["metricas"])

        for archivo in especificacion["archivos"]:
            mlflow.log_artifact(
                archivo["ruta"],
                artifact_path=archivo["grupo"],
            )

        run_id = run.info.run_id

    recuperado = cliente.get_run(run_id)
    assert recuperado.info.status == "FINISHED"

    for nombre, valor in especificacion["metricas"].items():
        assert math.isclose(
            recuperado.data.metrics[nombre],
            float(valor),
            rel_tol=1e-9,
            abs_tol=1e-9,
        ), nombre

    return {
        "run_id": run_id,
        "experiment_id": experiment_id,
        "estado": recuperado.info.status,
        "metricas_verificadas": recuperado.data.metrics,
        "uri": especificacion["uri"],
    }


if __name__ == "__main__":
    entrada = json.loads(
        Path(sys.argv[1]).read_text(encoding="utf-8")
    )
    resultado = registrar(entrada)

    Path(sys.argv[2]).write_text(
        json.dumps(resultado, indent=2),
        encoding="utf-8",
    )
