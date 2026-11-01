"""Interfaz del clasificador de seguros de la Actividad 5."""
import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="Asistente de seguros", page_icon="💬")
st.title("Asistente de seguros")
st.write("Escribe una consulta para identificar su categoría.")
st.info("Este modelo fue entrenado con consultas en inglés. Para estas pruebas, escribe en inglés; las consultas en español pueden clasificarse incorrectamente.")
st.caption("Clasifica consultas. No genera cotizaciones ni recomendaciones sobre pólizas.")

with st.form("consulta"):
    texto = st.text_area(
        "Tu consulta", placeholder="I need information about my life insurance",
        max_chars=2000, height=130,
    )
    enviar = st.form_submit_button("Consultar", type="primary")

if enviar:
    if not texto.strip():
        st.warning("Escribe una consulta con contenido.")
    else:
        try:
            with st.spinner("Analizando tu consulta…"):
                respuesta = requests.post(
                    f"{API_URL}/predecir", json={"texto": texto.strip()}, timeout=15,
                )
            if respuesta.status_code == 422:
                detalle = respuesta.json().get("detail")
                if isinstance(detalle, str):
                    st.warning(detalle)
                else:
                    st.warning("Revisa tu consulta: debe contener texto y tener hasta 2,000 caracteres.")
            else:
                respuesta.raise_for_status()
                datos = respuesta.json()
                st.subheader("Resultado")
                st.write("**Categoría:**", datos["categoria"])
                st.metric("Probabilidad del modelo", f"{datos['probabilidad']:.2%}")
                st.caption(f"Términos reconocidos: {datos['terminos_reconocidos']}")
                st.caption("Esta probabilidad no garantiza que la categoría sea correcta.")
        except requests.exceptions.Timeout:
            st.error("La consulta tardó demasiado. Inténtalo de nuevo.")
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con el servicio. Comprueba que el backend siga encendido en la otra Terminal.")
        except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
            st.error("No se pudo obtener un resultado válido. Inténtalo de nuevo o revisa la Terminal del backend.")
