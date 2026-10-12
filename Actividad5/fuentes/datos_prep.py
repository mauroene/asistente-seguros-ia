"""
Actividad 5 - Gestión de Proyectos de Inteligencia Artificial.

Preparación del dataset de consultas de seguros.

Fuente:
bitext/Bitext-insurance-llm-chatbot-training-dataset

El script:
- Valida la estructura del dataset.
- Elimina registros incompletos.
- Elimina instrucciones duplicadas.
- Genera un archivo limpio y un resumen de calidad.
"""

import argparse
import json
from pathlib import Path

import pandas as pd


COLUMNAS_ESPERADAS = [
    "instruction",
    "intent",
    "category",
    "tags",
    "response",
]


def preparar_datos(ruta_entrada, ruta_salida, ruta_reporte=None):
    """Prepara y guarda el dataset de clasificación."""

    ruta_entrada = Path(ruta_entrada)
    ruta_salida = Path(ruta_salida)

    if not ruta_entrada.is_file():
        raise FileNotFoundError(
            f"No existe el dataset original: {ruta_entrada}"
        )

    # 1. Cargar datos originales
    datos = pd.read_csv(ruta_entrada)

    registros_originales = len(datos)

    # 2. Validar columnas
    columnas_faltantes = [
        columna
        for columna in COLUMNAS_ESPERADAS
        if columna not in datos.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            f"Columnas faltantes: {columnas_faltantes}"
        )

    # 3. Eliminar registros incompletos
    # Se requieren texto y categoría para la clasificación.
    datos = datos.dropna(
        subset=["instruction", "category"]
    ).copy()

    registros_sin_nulos = len(datos)

    # 4. Eliminar instrucciones vacías
    instrucciones_validas = (
        datos["instruction"]
        .astype(str)
        .str.strip()
        .ne("")
    )

    categorias_validas = (
        datos["category"]
        .astype(str)
        .str.strip()
        .ne("")
    )

    datos = datos.loc[
        instrucciones_validas & categorias_validas
    ].copy()

    registros_validos = len(datos)

    # 5. Eliminar instrucciones duplicadas
    # Se conserva la primera aparición.
    datos = datos.drop_duplicates(
        subset=["instruction"],
        keep="first"
    ).copy()

    # 6. Reiniciar índices
    datos = datos.reset_index(drop=True)

    # 7. Guardar dataset limpio
    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    datos.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8"
    )

    # 8. Elaborar reporte de preparación
    reporte = {
        "dataset_original": str(ruta_entrada),
        "dataset_limpio": str(ruta_salida),
        "registros_originales": registros_originales,
        "registros_sin_nulos": registros_sin_nulos,
        "registros_validos": registros_validos,
        "registros_finales": len(datos),
        "registros_eliminados": (
            registros_originales - len(datos)
        ),
        "categorias_finales": int(
            datos["category"].nunique()
        ),
        "columnas": datos.columns.tolist(),
    }

    if ruta_reporte is not None:
        ruta_reporte = Path(ruta_reporte)

        ruta_reporte.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        ruta_reporte.write_text(
            json.dumps(
                reporte,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    return reporte


def main():
    """Ejecuta la preparación desde la terminal."""

    parser = argparse.ArgumentParser(
        description="Preparación del dataset de seguros."
    )

    parser.add_argument(
        "--entrada",
        required=True,
        help="Ruta del dataset original CSV."
    )

    parser.add_argument(
        "--salida",
        required=True,
        help="Ruta del dataset limpio CSV."
    )

    parser.add_argument(
        "--reporte",
        default=None,
        help="Ruta opcional para el reporte JSON."
    )

    argumentos = parser.parse_args()

    resultado = preparar_datos(
        argumentos.entrada,
        argumentos.salida,
        argumentos.reporte
    )

    print("\\nPREPARACIÓN COMPLETADA")

    print(
        json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
