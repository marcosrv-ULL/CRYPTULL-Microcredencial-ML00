import streamlit as st
import importlib
from utils import load_css

# Configuración inicial
st.set_page_config(page_title="Microcredencial ML - ULL", page_icon="🏛️", layout="wide")

# Cargar estilos (opcional, si tienes css personalizado)
# load_css() 

# --- SIDEBAR DE NAVEGACIÓN ---
with st.sidebar:
    st.header("Curso de ML")
    st.markdown("---")
    
    # Diccionario: "Nombre en Sidebar": "nombre_archivo_en_carpeta_chapters"
    structure = {
        "Módulo 0: Fundamentos": "intro",
        "Módulo 1: Análisis (EDA)": "eda",
    }
    
    selection_label = st.radio("Navegación", list(structure.keys()))
    
    st.markdown("---")

# --- CARGA DINÁMICA DE CAPÍTULOS ---
module_name = structure[selection_label]

try:
    # Esto busca el archivo en la carpeta chapters/nombre.py
    chapter_module = importlib.import_module(f"chapters.{module_name}")
    
    # Ejecutamos la función run() que debe existir en cada capítulo
    chapter_module.run()
    
except ModuleNotFoundError:
    st.error(f"No se encontró el archivo `chapters/{module_name}.py`")
except Exception as e:
    st.error(f"Error al cargar el módulo: {e}")