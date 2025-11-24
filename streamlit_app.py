import streamlit as st
from utils import load_css, get_intro_data, get_main_dataset
import importlib

st.set_page_config(page_title="Microcredencial ML - ULL", page_icon="🏛️", layout="wide")
load_css()

# Inicialización de datasets en sesión
if 'df_intro' not in st.session_state:
    st.session_state['df_intro'] = get_intro_data()
    
if 'df_main' not in st.session_state:
    st.session_state['df_main'] = get_main_dataset()

# Sidebar Estática
with st.sidebar:
    st.header("Introducción al Machine Learning")
    st.markdown("*CryptULL - Universidad de La Laguna*")
    st.markdown("---")
    
    structure = {
        "Módulo 0: Fundamentos": "intro",
        "Módulo 1: EDA": "eda",
        "Módulo 2: Supervisado": "model" # Desactivado por ahora
    }
    
    selection_label = st.radio("Navegación", list(structure.keys()))
    
    st.markdown("---")
    st.info("[Notebooks de la tareas](https://drive.google.com/drive/folders/1Qibrfn0YCSlb6qo2t30A1Qz9CKDcMTNo?usp=sharing)")

# Carga dinámica
module_name = structure[selection_label]
try:
    chapter_module = importlib.import_module(f"chapters.{module_name}")
    chapter_module.run()
except Exception as e:
    st.error(f"Error en el módulo: {e}")