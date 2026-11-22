"""API HTTP de referencia para el despliegue controlado en localhost."""

import argparse
import json
import logging
from tempfile import TemporaryDirectory
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, make_server

from modelo import REVISION, preparar

MAX_BYTES = 8192
MAX_TEXTO = 1000
LOG = logging.getLogger("vidasegura")


class SinRegistroDeAcceso(WSGIRequestHandler):
    def log_message(self, format, *args):
        # La telemetría de aplicación omite ruta, cuerpo y texto de consulta.
        pass


def crear_api(modelo, meta, clasificar):
    identidad = {
        "revision": REVISION["revision"],
        "modelo_version": meta["version_modelo"],
        "run_id": meta["run_id"],
        "sha256": meta["sha256"],
    }
    control = clasificar("¿Qué tipos de planes maneja el seguro de vida?", modelo, meta)
    if control["categoria"] != "LIFE_INSURANCE":
        raise RuntimeError("Falló la inferencia de arranque")

    def atender(entorno, responder):
        metodo, ruta = entorno["REQUEST_METHOD"], entorno["PATH_INFO"]
        if (metodo, ruta) == ("GET", "/salud"):
            estado, salida = "200 OK", {"estado": "listo", **identidad}
        elif (metodo, ruta) == ("POST", "/clasificar"):
            estado, salida = predecir(entorno, modelo, meta, clasificar)
        else:
            estado, salida = "404 Not Found", {"error": "Ruta desconocida"}
        evento = {
            "revision": identidad["revision"],
            "http": int(estado[:3]),
            **{clave: salida[clave] for clave in ("request_id", "estado", "latencia_ms") if clave in salida},
        }
        LOG.info(json.dumps(evento))
        cuerpo = json.dumps(salida).encode("utf-8")
        responder(estado, [("Content-Type", "application/json"), ("Content-Length", str(len(cuerpo)))])
        return [cuerpo]

    return atender


def predecir(entorno, modelo, meta, clasificar):
    tipo = entorno.get("CONTENT_TYPE", "").split(";")[0].strip().lower()
    if tipo != "application/json":
        return "415 Unsupported Media Type", {"error": "Usa application/json"}
    try:
        cantidad = int(entorno.get("CONTENT_LENGTH", ""))
        if cantidad > MAX_BYTES:
            return "413 Payload Too Large", {"error": "Cuerpo demasiado grande"}
        if cantidad <= 0:
            raise ValueError
        cuerpo = json.loads(entorno["wsgi.input"].read(cantidad).decode("utf-8"))
        texto = cuerpo.get("texto") if isinstance(cuerpo, dict) else None
        if not isinstance(texto, str) or not texto.strip() or len(texto) > MAX_TEXTO:
            raise ValueError
        texto.encode("utf-8")
    except (ValueError, RecursionError):
        return "400 Bad Request", {"error": "Envía texto no vacío de hasta 1000 caracteres"}
    return "200 OK", clasificar(texto, modelo, meta)


def servidor(api, puerto):
    return make_server("127.0.0.1", puerto, api, handler_class=SinRegistroDeAcceso)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", type=int, default=8003)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    with TemporaryDirectory() as destino:
        api = crear_api(*preparar(Path(destino)))
        with servidor(api, args.puerto) as http:
            print(f"VidaSegura lista en http://127.0.0.1:{http.server_port}", flush=True)
            try:
                http.serve_forever()
            except KeyboardInterrupt:
                pass
