"""API de clasificación por categoría de la Actividad 5."""
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sklearn.utils.validation import check_is_fitted

MODEL_PATH = Path(__file__).parent / "modelo" / "regresion_logistica_optimizada_v1.joblib"


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = joblib.load(MODEL_PATH)
    for step in ("tfidf", "clasificador"):
        check_is_fitted(model.named_steps[step])
    app.state.model = model
    yield


app = FastAPI(title="Asistente de seguros — clasificación", version="0.1.0", lifespan=lifespan)


class Consulta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    texto: str = Field(strict=True, min_length=1, max_length=2000)

    @field_validator("texto")
    @classmethod
    def validar_texto(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Escribe una consulta con contenido.")
        return value


class Prediccion(BaseModel):
    categoria: str
    probabilidad: float
    terminos_reconocidos: int


@app.get("/health")
def health():
    return {"estado": "ok"}


@app.post("/predecir", response_model=Prediccion)
def predecir(consulta: Consulta, request: Request):
    model = request.app.state.model
    vector = model.named_steps["tfidf"].transform([consulta.texto])
    if vector.nnz == 0:
        raise HTTPException(status_code=422, detail="La consulta no contiene términos reconocidos por el modelo.")
    classifier = model.named_steps["clasificador"]
    probabilities = classifier.predict_proba(vector)[0]
    index = int(probabilities.argmax())
    return Prediccion(
        categoria=str(classifier.classes_[index]),
        probabilidad=float(probabilities[index]),
        terminos_reconocidos=int(vector.nnz),
    )
