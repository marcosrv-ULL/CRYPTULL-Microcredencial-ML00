import streamlit as st
import os

@st.cache_resource
def render_manim_scene(scene_class):
    """
    Renderiza una escena y devuelve la ruta del video.
    Tiene carga perezosa (Lazy Loading): Solo importa Manim si realmente
    necesita generar el video.
    """
    output_name = scene_class.__name__
    target_filename = f"{output_name}.mp4"
    
    # 1. BÚSQUEDA PREVIA (Sin tocar Manim)
    # Buscamos si el video ya existe en la carpeta 'media' estándar.
    # Esto es puro Python y no requiere librerías pesadas.
    search_dir = "media"
    if os.path.exists(search_dir):
        for root, dirs, files in os.walk(search_dir):
            if target_filename in files:
                # ¡Encontrado! Devolvemos la ruta y salimos sin importar Manim
                return os.path.join(root, target_filename)

    # 2. SI NO EXISTE -> IMPORTAMOS MANIM Y RENDERIZAMOS
    try:
        # ⚠️ AQUÍ está el truco: Importamos dentro del bloque try
        from manim import config
        
        # Configuración de calidad para Web
        config.media_width = "100%"
        config.verbosity = "ERROR" # Silenciar logs
        config.pixel_height = 720 
        config.pixel_width = 1280
        config.output_file = output_name
        
        # Información para el usuario
        st.toast(f"🎨 Renderizando {output_name}... espera un momento.", icon="⏳")
        
        # Instanciamos y renderizamos
        scene = scene_class()
        scene.render()
        
        # 3. BÚSQUEDA POSTERIOR (Usando la config de Manim)
        output_dir = config.media_dir
        for root, dirs, files in os.walk(output_dir):
            if target_filename in files:
                return os.path.join(root, target_filename)
                
    except ImportError:
        st.error(" Error Crítico: No se pudo importar la librería 'manim'. ¿Está instalada en el entorno?")
        return None
    except Exception as e:
        st.error(f" Error durante el renderizado: {e}")
        return None
    
    return None

def load_css():
    # Tu función para cargar CSS si la tienes
    st.markdown("""
        <style>
        .stVideo {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)