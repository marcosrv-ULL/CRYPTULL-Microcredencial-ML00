import streamlit as st
from manim import *
import os

@st.cache_resource
def render_manim_scene(scene_class):
    """Renderiza una escena y devuelve la ruta del video."""
    output_name = scene_class.__name__
    
    # Configuración de calidad
    config.media_width = "100%"
    config.verbosity = "ERROR"
    config.pixel_height = 720 
    config.pixel_width = 1280
    config.output_file = output_name
    
    try:
        scene = scene_class()
        scene.render()
    except Exception as e:
        st.error(f"Error Manim: {e}")
        return None
    
    output_dir = config.media_dir
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file == f"{output_name}.mp4":
                return os.path.join(root, file)
    return None

def load_css():
    # Tu función para cargar CSS si la tienes
    pass