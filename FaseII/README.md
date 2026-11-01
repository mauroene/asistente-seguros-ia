# Fase II — ejecución del asistente de seguros

Esta fase reutiliza el pipeline entrenado en la Actividad 5 y lo integra con
FastAPI, Streamlit y Docker Compose. Se clasifica la **categoría** de una consulta;
no se generan cotizaciones, respuestas de pólizas ni asesoría.

## Arquitectura

```text
Navegador → Streamlit :8501 → FastAPI :8000 → TF-IDF + regresión logística
```

Dentro de Compose, el frontend usa `API_URL=http://backend:8000`. El backend carga
el Joblib al arrancar y no reentrena. El modelo contiene 3,935 términos y 17
categorías. El archivo se conserva con su nombre original:
`backend/modelo/regresion_logistica_optimizada_v1.joblib`.

## Arranque local con Docker

Requisitos: Docker Engine o Docker Desktop encendido, Docker Compose y puertos
8000 y 8501 disponibles. Desde la raíz del repositorio:

```sh
cd FaseII
docker compose up --build
```

Esperar a que el backend esté saludable y la interfaz esté iniciada. Abrir
[la interfaz](http://localhost:8501) o [la documentación de la API](http://localhost:8000/docs).
Los puertos del host se publican sobre `127.0.0.1` para uso local.

Para detener, pulsar Control+C. Para retirar los contenedores y la red del proyecto:

```sh
docker compose down
```

No se necesita descargar datasets ni acceder a Google Drive para ejecutar esta
versión. El modelo entrenado está incluido en la carpeta del backend.

## API

`GET /health` devuelve `{"estado":"ok"}`. El modelo debe cargarse correctamente
antes de que la aplicación esté disponible.

`POST /predecir` recibe:

```json
{"texto": "I need information about my life insurance"}
```

Respuesta observada para ese ejemplo:

```json
{
  "categoria": "LIFE_INSURANCE",
  "probabilidad": 0.9980929646288605,
  "terminos_reconocidos": 6
}
```

La entrada debe ser una cadena con contenido de hasta 2,000 caracteres. Se
eliminan espacios externos. Los textos vacíos, los tipos incorrectos, los campos
adicionales y las consultas sin vocabulario reconocido reciben HTTP 422.

## Idioma y alcance del modelo

El entrenamiento de la Actividad 5 usa `instruction` del dataset original de
Bitext, en inglés. La interfaz está en español, pero eso no cambia el idioma
aprendido por el clasificador. Las pruebas funcionales se realizan en inglés.

La muestra de 300 consultas traducidas de la Actividad 4 se usó para evaluar
modelos multilingües con seis categorías. No se incorporó al entrenamiento de
esta regresión logística de 17 categorías. Para una fase posterior se plantea
recuperar esos datos, preparar y evaluar un nuevo entrenamiento e incorporar
información del PDF de seguros de BBVA con referencias a sus páginas.

Una probabilidad alta no garantiza corrección. El modelo obliga a elegir una
categoría y no resuelve formalmente consultas ambiguas. El rechazo por vocabulario
vacío no identifica todos los textos fuera de dominio. Estas limitaciones se
documentan con ejemplos, incluyendo una discrepancia en una consulta de cobertura.

## Pruebas locales

Para ejecutar pruebas fuera de Docker, se propone Python 3.11. Desde `FaseII`:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-pruebas.txt
pytest pruebas -q
python pruebas/revision_ampliada.py
```

Se aprobaron 13 pruebas automatizadas locales usando TestClient y AppTest. Los
25 casos ampliados usan el modelo real mediante TestClient y sus resultados
están en `pruebas/resultados_ampliados.json`. No son una estimación representativa
de exactitud general y no se ejecutaron dentro de Docker.

Manualmente se comprobó en Docker el arranque, una consulta válida y el rechazo
de texto sin términos reconocidos. Las capturas están en `evidencias/`; la captura
de espacios desde la API corresponde a la ejecución local previa a Docker.

## Documentación final

- [Documento de validación y pruebas](documentacion/Documento_Validacion_Pruebas_FaseII.pdf).
- [Manual de despliegue en la nube](documentacion/Manual_Despliegue_Nube_FaseII.pdf).

El manual describe una ruta propuesta con Azure VM Ubuntu y Docker Compose.
**El despliegue en nube no fue ejecutado.** La ejecución comprobada es local.

## Estructura

```text
FaseII/
├── backend/              # API, Dockerfile, dependencias y modelo
├── frontend/             # Streamlit, Dockerfile y dependencias
├── pruebas/              # Pruebas y resultados completos
├── evidencias/           # Capturas de ejecución
├── documentacion/        # Dos PDF finales
├── docker-compose.yml
├── requirements-pruebas.txt
└── README.md
```

Si el arranque falla, revisar `docker compose logs --tail=100`. Un puerto ocupado
requiere detener el servicio anterior; un fallo de carga del modelo requiere
comprobar la presencia del Joblib y las dependencias. La interfaz muestra un aviso
si no puede conectar con la API.
