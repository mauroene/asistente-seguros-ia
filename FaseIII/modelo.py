"""Prepara únicamente los archivos de inferencia del paquete congelado."""

import hashlib
import json
import runpy
from importlib.metadata import version
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

RAIZ = Path(__file__).resolve().parent
REVISION = json.loads((RAIZ / "revision.json").read_text(encoding="utf-8"))
MODELO = "modelos/modelo_seleccionado.joblib"
METADATA = "modelos/metadata_modelo.json"
PREFIJO = "VidaSegura_ES_V3/entrenamiento/"
ARCHIVOS = ("cargar_modelo.py", MODELO, METADATA)
PAQUETE = RAIZ.parent / REVISION["paquete"]


def comprobar_sha(datos, esperado):
    if hashlib.sha256(datos).hexdigest() != esperado:
        raise ValueError("La huella SHA-256 no coincide con la revisión aprobada")


def preparar(destino, paquete=PAQUETE):
    datos = paquete.read_bytes()
    comprobar_sha(datos, REVISION["paquete_sha256"])
    # Leer los mismos bytes que se verificaron y extraer solo rutas conocidas.
    with ZipFile(BytesIO(datos)) as zip_modelo:
        archivos = {nombre: zip_modelo.read(PREFIJO + nombre) for nombre in ARCHIVOS}
    comprobar_sha(archivos[MODELO], REVISION["modelo_sha256"])
    meta = json.loads(archivos[METADATA])
    esperado = {
        "archivo": MODELO,
        "sha256": REVISION["modelo_sha256"],
        "run_id": REVISION["modelo_run_id"],
        "version_modelo": REVISION["modelo_version"],
        "categorias": REVISION["categorias"],
    }
    if any(meta[clave] != valor for clave, valor in esperado.items()):
        raise ValueError("Los metadatos del modelo difieren de revision.json")
    for linea in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines():
        nombre, esperado_version = linea.split("==")
        if version(nombre) != esperado_version:
            raise RuntimeError(f"Instala {nombre}=={esperado_version}")

    for nombre, contenido in archivos.items():
        archivo = destino / nombre
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_bytes(contenido)

    cargador = runpy.run_path(str(destino / "cargar_modelo.py"))
    modelo, meta = cargador["cargar"](destino)
    if list(modelo.classes_) != REVISION["categorias"]:
        raise ValueError("Las clases del modelo difieren de revision.json")
    return modelo, meta, cargador["clasificar"]
