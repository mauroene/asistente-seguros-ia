from pathlib import Path
from unittest.mock import patch

import requests
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from test_api import app

FRONTEND = Path(__file__).resolve().parents[1] / "frontend" / "app.py"


def test_interfaz_con_api_real():
    with TestClient(app) as client:
        def enviar(url, json, timeout):
            return client.post("/predecir", json=json)

        with patch("requests.post", side_effect=enviar) as llamada:
            pantalla = AppTest.from_file(str(FRONTEND)).run()
            pantalla.text_area[0].input("I need information about my life insurance")
            pantalla.button[0].click().run()
            assert not pantalla.exception
            assert pantalla.metric[0].value == "99.81%"
            assert any("LIFE_INSURANCE" in item.value for item in pantalla.markdown)
            assert llamada.call_count == 1

            pantalla.text_area[0].input("zzzzqwerty123")
            pantalla.button[0].click().run()
            assert "términos reconocidos" in pantalla.warning[0].value
            assert not pantalla.metric

            pantalla.text_area[0].input("   ")
            pantalla.button[0].click().run()
            assert pantalla.warning[0].value == "Escribe una consulta con contenido."
            assert llamada.call_count == 2


def test_interfaz_sin_backend():
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError):
        pantalla = AppTest.from_file(str(FRONTEND)).run()
        pantalla.text_area[0].input("life insurance")
        pantalla.button[0].click().run()
        assert not pantalla.exception
        assert "No se pudo conectar" in pantalla.error[0].value
