"""Validaciones del artefacto y regresión contra las evidencias de Actividad 8."""

import csv
import io
import json
import math
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from modelo import PAQUETE, PREFIJO, REVISION, preparar


class ModeloCongelado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        destino = cls.enterClassContext(TemporaryDirectory())
        cls.modelo, cls.meta, clasificar = preparar(Path(destino))
        cls.clasificar = staticmethod(clasificar)

    def test_paquete_alterado_rechazado_antes_de_extraer(self):
        with TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            alterado = raiz / "alterado.zip"
            alterado.write_bytes(PAQUETE.read_bytes() + b"alterado")
            destino = raiz / "extraido"
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                preparar(destino, alterado)
            self.assertFalse(destino.exists())

    def test_regresion_sintetica_63(self):
        with ZipFile(PAQUETE) as paquete:
            datos = paquete.read(PREFIJO + "evidencias/predicciones_sintetica_nueva_63.csv")
        filas = list(csv.DictReader(io.StringIO(datos.decode("utf-8-sig"))))
        self.assertEqual(len(filas), 63)
        for fila in filas:
            with self.subTest(consulta_id=fila["id"]):
                resultado = self.clasificar(fila["consulta_es"], self.modelo, self.meta)
                self.assertEqual(resultado["categoria"], fila["prediccion_V3"])
                self.assertTrue(math.isclose(
                    resultado["puntaje_no_calibrado"],
                    float(fila["puntaje_maximo_V3_no_calibrado"]),
                    rel_tol=1e-8,
                ))

    def test_regresion_diagnostica_74(self):
        with ZipFile(PAQUETE) as paquete:
            consultas = json.loads(paquete.read(PREFIJO + "configuracion/consultas_recarga.json"))
            esperado = json.loads(paquete.read(PREFIJO + "evidencias/verificacion_recarga.json"))
        self.assertEqual(len(consultas), 74)
        categorias = [self.clasificar(texto, self.modelo, self.meta)["categoria"] for texto in consultas]
        self.assertEqual(categorias, esperado["predicciones"])
        self.assertEqual(set(categorias), set(REVISION["categorias"]))

    def test_vacio_y_sin_vocabulario(self):
        with self.assertRaises(ValueError):
            self.clasificar("   ", self.modelo, self.meta)
        resultado = self.clasificar("🦄🛸", self.modelo, self.meta)
        self.assertEqual(resultado["estado"], "sin_caracteristicas_conocidas")
        self.assertIsNone(resultado["categoria"])
        self.assertIsNone(resultado["puntaje_no_calibrado"])
