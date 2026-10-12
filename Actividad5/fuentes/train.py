"""
Actividad 5 - Gestión de Proyectos de IA.

Entrenamiento reproducible de clasificadores de
consultas relacionadas con seguros.

Modelos:
- Regresión logística con TF-IDF.
- Random Forest con TF-IDF.

Los hiperparámetros se recuperan desde un archivo JSON.
"""

import argparse
import ast
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


def convertir_valor(valor):
    """Recupera valores guardados como texto en el JSON."""

    if not isinstance(valor, str):
        return valor

    try:
        return ast.literal_eval(valor)
    except (ValueError, SyntaxError):
        return valor


def crear_modelo(configuracion):
    """Construye el pipeline a partir de la configuración."""

    parametros_vectorizador = dict(
        configuracion["vectorizador"]
    )

    parametros_vectorizador["ngram_range"] = tuple(
        parametros_vectorizador["ngram_range"]
    )

    tipo = configuracion["clasificador"]["tipo"]

    parametros = {
        clave: convertir_valor(valor)
        for clave, valor in
        configuracion["clasificador"]["parametros"].items()
    }

    if tipo == "LogisticRegression":

        clasificador = LogisticRegression(
            **parametros
        )

    elif tipo == "RandomForestClassifier":

        clasificador = RandomForestClassifier(
            **parametros
        )

    else:
        raise ValueError(
            f"Clasificador no reconocido: {tipo}"
        )

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                **parametros_vectorizador
            )
        ),
        (
            "clasificador",
            clasificador
        )
    ])


def entrenar_modelos(
    ruta_datos,
    ruta_configuracion,
    ruta_salida
):
    """Entrena, evalúa y almacena los modelos."""

    ruta_datos = Path(ruta_datos)
    ruta_configuracion = Path(ruta_configuracion)
    ruta_salida = Path(ruta_salida)

    ruta_salida.mkdir(
        parents=True,
        exist_ok=True
    )

    # 1. Cargar dataset y configuración
    datos = pd.read_csv(ruta_datos)

    configuraciones = json.loads(
        ruta_configuracion.read_text(
            encoding="utf-8"
        )
    )

    # 2. Preparar variables
    X = datos["instruction"]
    y = datos["category"]

    # 3. División estratificada
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    print(
        f"Entrenamiento: {len(X_train):,} registros"
    )

    print(
        f"Prueba: {len(X_test):,} registros"
    )

    resultados = []

    # 4. Entrenar ambos modelos
    for nombre, configuracion in configuraciones.items():

        print(f"\nEntrenando: {nombre}")

        modelo = crear_modelo(
            configuracion
        )

        modelo.fit(
            X_train,
            y_train
        )

        # 5. Evaluar
        predicciones = modelo.predict(X_test)

        probabilidades = modelo.predict_proba(
            X_test
        )

        clases = (
            modelo.named_steps[
                "clasificador"
            ].classes_
        )

        metricas = {
            "Modelo": nombre,

            "Accuracy": accuracy_score(
                y_test,
                predicciones
            ),

            "Precision macro": precision_score(
                y_test,
                predicciones,
                average="macro",
                zero_division=0
            ),

            "Recall macro": recall_score(
                y_test,
                predicciones,
                average="macro",
                zero_division=0
            ),

            "F1 macro": f1_score(
                y_test,
                predicciones,
                average="macro",
                zero_division=0
            ),

            "ROC-AUC": roc_auc_score(
                y_test,
                probabilidades,
                labels=clases,
                multi_class="ovr",
                average="macro"
            )
        }

        resultados.append(metricas)

        # 6. Guardar modelo entrenado
        archivo_modelo = (
            ruta_salida /
            f"{nombre}_reentrenado.joblib"
        )

        joblib.dump(
            modelo,
            archivo_modelo
        )

        print(
            f"F1 macro: {metricas['F1 macro']:.4f}"
        )

        print(
            f"Modelo guardado: {archivo_modelo.name}"
        )

    # 7. Guardar métricas
    tabla = pd.DataFrame(
        resultados
    )

    archivo_metricas = (
        ruta_salida /
        "metricas_reentrenamiento.csv"
    )

    tabla.to_csv(
        archivo_metricas,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nENTRENAMIENTO COMPLETADO")

    print(tabla.to_string(index=False))

    return tabla


def main():

    parser = argparse.ArgumentParser(
        description="Entrenamiento de modelos de seguros."
    )

    parser.add_argument(
        "--datos",
        required=True
    )

    parser.add_argument(
        "--configuracion",
        required=True
    )

    parser.add_argument(
        "--salida",
        required=True
    )

    argumentos = parser.parse_args()

    entrenar_modelos(
        argumentos.datos,
        argumentos.configuracion,
        argumentos.salida
    )


if __name__ == "__main__":
    main()
