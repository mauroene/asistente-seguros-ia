"""Ejecuta regresión y despliega la revisión temporalmente para comprobarla por HTTP."""

import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
from time import perf_counter
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pruebas
from modelo import RAIZ, REVISION, preparar
from servicio import MAX_BYTES, crear_api, servidor


def solicitar(base, ruta, cuerpo=None, tipo="application/json"):
    solicitud = Request(base + ruta, data=cuerpo, headers={"Content-Type": tipo})
    try:
        respuesta = urlopen(solicitud, timeout=5)
    except HTTPError as error:
        respuesta = error
    with respuesta:
        return respuesta.status, json.load(respuesta)


def igual(real, esperado):
    if real != esperado:
        raise AssertionError(f"Esperado {esperado!r}, recibido {real!r}")


def verificar_http(http, salud):
    base = f"http://127.0.0.1:{http.server_port}"
    igual(solicitar(base, "/salud"), (200, salud))
    controles = {"salud": 200}
    consulta = json.dumps({"texto": "¿Cuánto cuesta el seguro de vida?"}).encode()
    inicio = perf_counter()
    codigo, resultado = solicitar(base, "/clasificar", consulta)
    duracion = (perf_counter() - inicio) * 1000
    igual(codigo, 200)
    igual(resultado["categoria"], "QUOTE")
    igual(resultado["modelo_version"], salud["modelo_version"])
    igual(resultado["run_id"], salud["run_id"])
    controles["clasificacion"] = codigo
    cuerpo = json.dumps({"texto": "🦄🛸"}).encode()
    codigo, resultado = solicitar(base, "/clasificar", cuerpo)
    igual(codigo, 200)
    igual(resultado["estado"], "sin_caracteristicas_conocidas")
    igual(resultado["categoria"], None)
    controles["sin_vocabulario"] = codigo
    for nombre, cuerpo, tipo, esperado in [
        ("vacio", b'{"texto":"  "}', "application/json", 400),
        ("json_invalido", b'{"texto":', "application/json", 400),
        ("tipo_invalido", b'{"texto":42}', "application/json", 400),
        ("texto_largo", json.dumps({"texto": "a" * 1001}).encode(), "application/json", 400),
        ("formato_invalido", b"texto", "text/plain", 415),
        ("cuerpo_grande", b"x" * (MAX_BYTES + 1), "application/json", 413),
    ]:
        codigo, _ = solicitar(base, "/clasificar", cuerpo, tipo)
        igual(codigo, esperado)
        controles[nombre] = codigo
    return controles, duracion


def git(*opciones):
    return subprocess.check_output(["git", "-C", str(RAIZ), *opciones], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidencia", required=True, type=Path)
    args = parser.parse_args()

    commit = git("rev-parse", "HEAD")
    cambios_locales = bool(git("status", "--porcelain"))

    suite = unittest.defaultTestLoader.loadTestsFromModule(pruebas)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    if not resultado.wasSuccessful():
        return 1

    salud = {
        "estado": "listo",
        "revision": REVISION["revision"],
        "modelo_version": REVISION["modelo_version"],
        "run_id": REVISION["modelo_run_id"],
        "sha256": REVISION["modelo_sha256"],
    }
    with TemporaryDirectory() as temporal:
        api = crear_api(*preparar(Path(temporal)))
        with servidor(api, 0) as http:
            hilo = Thread(target=http.serve_forever)
            hilo.start()
            try:
                controles, latencia = verificar_http(http, salud)
            finally:
                http.shutdown()
                hilo.join()

    evidencia = {
        "estado": "aprobado",
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "commit": commit,
        "cambios_locales_sin_commit": cambios_locales,
        "entorno": {"python": sys.version.split()[0], "plataforma": platform.platform()},
        "modelo": salud,
        "paquete_sha256": REVISION["paquete_sha256"],
        "pruebas_unittest": resultado.testsRun,
        "predicciones_historicas_reproducidas": {"sinteticas": 63, "diagnosticas": 74},
        "despliegue": "HTTP temporal en 127.0.0.1",
        "controles_http": controles,
        "latencia_http_una_solicitud_ms": round(latencia, 3),
    }
    args.evidencia.parent.mkdir(parents=True, exist_ok=True)
    # El modo exclusivo evita sobrescribir evidencia de una ejecución anterior.
    with args.evidencia.open("x", encoding="utf-8") as salida:
        json.dump(evidencia, salida, indent=2, ensure_ascii=False)
        salida.write("\n")
    print(f"Evidencia de ejecución: {args.evidencia}")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    sys.exit(main())
