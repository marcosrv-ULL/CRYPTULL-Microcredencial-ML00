import streamlit as st
from utils import load_css

# --- CONFIGURACIÓN GLOBAL ---
# st.set_page_config debe ser lo primero, aunque st.Page gestionará los títulos individuales
st.set_page_config(page_title="Microcredencial ML - ULL", layout="wide")

# Cargar estilos globales
load_css() 

# --- DEFINICIÓN DE LAS PÁGINAS ---
# El primer argumento es la ruta al archivo.
# El título es lo que aparecerá en la sidebar.

pg_intro = st.Page("chapters/intro.py", title="Intro", url_path="intro")
pg_eda = st.Page("chapters/eda.py", title="Estadistica Básica", url_path="eda")

# Si tienes más módulos, añádelos aquí:
# pg_model = st.Page("chapters/model.py", title="Aprendizaje Supervisado", icon="🤖")

# --- DEFINICIÓN DE LA NAVEGACIÓN ---
# Aquí agrupamos las páginas por secciones (Módulos)
pg = st.navigation(
    {
        "": [pg_intro],
        "Fundamentos": [pg_eda],
        # "Módulo 2": [pg_model],
    }
)

# --- ELEMENTOS COMUNES (LOGO Y SIDEBAR) ---
# Todo lo que pongas aquí se ejecutará en CADA página.
# st.logo es la nueva forma nativa de poner el logo arriba a la izquierda

with st.sidebar:
    st.caption("Microcredencial ML - CryptULL")

# --- EJECUTAR EL ENRUTADOR ---
pg.run()