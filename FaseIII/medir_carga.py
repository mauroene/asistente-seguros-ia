"""Mide la API local con consultas de control y concurrencia escalonada."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from functools import partial
import json
import math
from pathlib import Path
import platform
import statistics
from tempfile import TemporaryDirectory
from threading import Thread
from time import perf_counter
from urllib.error import URLError
from zipfile import ZipFile

from modelo import PAQUETE, PREFIJO, REVISION, preparar
from pipeline import git, solicitar
from servicio import crear_api, servidor


def casos_de_control():
    with ZipFile(PAQUETE) as paquete:
        textos = json.loads(paquete.read(PREFIJO + "configuracion/consultas_recarga.json"))
        referencia = json.loads(paquete.read(PREFIJO + "evidencias/verificacion_recarga.json"))
    casos = {}
    for texto, categoria in zip(textos, referencia["predicciones"], strict=True):
        casos.setdefault(categoria, json.dumps({"texto": texto}).encode())
    if set(casos) != set(REVISION["categorias"]):
        raise RuntimeError("Los casos de control deben cubrir las siete categorías")
    return [(casos[categoria], categoria) for categoria in REVISION["categorias"]]


def medir_solicitud(base, caso):
    cuerpo, categoria = caso
    inicio = perf_counter()
    try:
        codigo, respuesta = solicitar(base, "/clasificar", cuerpo)
        if codigo != 200:
            estado = f"http_{codigo}"
        elif (
            respuesta.get("categoria") != categoria
            or respuesta.get("estado") != "clasificado"
            or respuesta.get("run_id") != REVISION["modelo_run_id"]
        ):
            estado = "respuesta_inesperada"
        else:
            estado = "ok"
    except (URLError, OSError, ValueError) as error:
        estado = type(error).__name__
    return estado, (perf_counter() - inicio) * 1000


def medir_ronda(medir, casos, concurrencia):
    with ThreadPoolExecutor(max_workers=concurrencia) as clientes:
        inicio = perf_counter()
        resultados = list(clientes.map(medir, casos))
        segundos = perf_counter() - inicio
    estados = Counter(estado for estado, _ in resultados)
    latencias = sorted(ms for estado, ms in resultados if estado == "ok")
    p95 = latencias[math.ceil(len(latencias) * 0.95) - 1] if latencias else None
    return {
        "concurrencia_maxima": concurrencia,
        "solicitudes": len(casos),
        "exitos": estados["ok"],
        "fallos": len(casos) - estados["ok"],
        "estados": dict(estados),
        "duracion_s": round(segundos, 6),
        "exitos_por_segundo": round(estados["ok"] / segundos, 2),
        "p50_ms": round(statistics.median(latencias), 3) if latencias else None,
        "p95_ms": round(p95, 3) if p95 is not None else None,
    }


def ejecutar():
    with TemporaryDirectory() as temporal:
        api = crear_api(*preparar(Path(temporal)))
        casos = casos_de_control()
        with servidor(api, 0) as http:
            hilo = Thread(target=http.serve_forever)
            hilo.start()
            try:
                base = f"http://127.0.0.1:{http.server_port}"
                codigo, salud = solicitar(base, "/salud")
                if codigo != 200 or salud.get("sha256") != REVISION["modelo_sha256"]:
                    raise RuntimeError("La revisión desplegada no pasó la comprobación de salud")
                medir = partial(medir_solicitud, base)
                calentamiento = medir_ronda(medir, casos * 2, 1)
                rondas = [
                    {"ronda": ronda, **medir_ronda(medir, casos * 20, concurrencia)}
                    for concurrencia in (1, 4, 8)
                    for ronda in range(1, 4)
                ]
            finally:
                http.shutdown()
                hilo.join()
    return salud, calentamiento, rondas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidencia", required=True, type=Path)
    args = parser.parse_args()
    contexto = {
        "fecha_inicio_utc": datetime.now(timezone.utc).isoformat(),
        "commit": git("rev-parse", "HEAD"),
        "cambios_locales_sin_commit": bool(git("status", "--porcelain")),
        "entorno": {"python": platform.python_version(), "plataforma": platform.platform()},
    }
    salud, calentamiento, rondas = ejecutar()
    total = sum(ronda["solicitudes"] for ronda in rondas)
    fallos = sum(ronda["fallos"] for ronda in rondas)
    evidencia = {
        **contexto,
        "modelo": salud,
        "entorno_http": "Servidor local de un solo hilo, cliente en el mismo equipo",
        "muestra": "Siete consultas de control de Actividad 8, una por categoría, repetidas",
        "calentamiento_excluido": calentamiento,
        "solicitudes_medidas": total,
        "fallos_medidos": fallos,
        "rondas": rondas,
    }
    args.evidencia.parent.mkdir(parents=True, exist_ok=True)
    with args.evidencia.open("x", encoding="utf-8") as salida:
        json.dump(evidencia, salida, indent=2, ensure_ascii=False)
        salida.write("\n")
    print(f"{total} solicitudes medidas, {fallos} fallos. Evidencia: {args.evidencia}")
    return int(bool(fallos or calentamiento["fallos"]))


if __name__ == "__main__":
    raise SystemExit(main())
