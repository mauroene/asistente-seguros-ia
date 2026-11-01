import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from main import app


@pytest.fixture
def client():
    with TestClient(app) as instance:
        yield instance


def test_modelo_real(client):
    assert client.get("/health").status_code == 200
    response = client.post("/predecir", json={"texto": "I need information about my life insurance"})
    assert response.status_code == 200
    result = response.json()
    assert result["categoria"] == "LIFE_INSURANCE"
    assert 0 <= result["probabilidad"] <= 1
    assert result["terminos_reconocidos"] > 0


@pytest.mark.parametrize("payload", [
    {"texto": ""}, {"texto": "   \n"}, {"texto": "zzzzqwerty123"},
    {"texto": "!!! 🦄"}, {"texto": "a" * 2001}, {"texto": None},
    {"texto": 123}, {}, {"texto": "life insurance", "extra": True},
])
def test_entradas_invalidas(client, payload):
    assert client.post("/predecir", json=payload).status_code == 422


def test_espacios_externos(client):
    first = client.post("/predecir", json={"texto": "life insurance"}).json()
    second = client.post("/predecir", json={"texto": "  life insurance  "}).json()
    assert first == second
