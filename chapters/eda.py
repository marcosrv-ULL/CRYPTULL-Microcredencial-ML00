import streamlit as st
import os
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURACIÓN DEL CONTENIDO (GUION)
# ==========================================
ACTOS = [
    {
        "clase": "Acto1_Variable",
        "titulo": "Acto 1: La Variable",
        "desc": "El átomo del dato. Distinción entre continuo (caída libre) y discreto (cajas)."
    },
    {
        "clase": "Acto2_Distribucion",
        "titulo": "Acto 2: La Distribución",
        "desc": "Del caos individual emerge el orden colectivo. La Curva de campana."
    },
    {
        "clase": "Acto3_Media",
        "titulo": "Acto 3: El Balancín (La Media)",
        "desc": "La media es el punto de equilibrio físico. Un outlier 'pesa' mucho y mueve el punto de apoyo."
    },
    {
        "clase": "Acto4_Dispersion",
        "titulo": "Acto 4: La Respiración (Dispersión)",
        "desc": "La incertidumbre visualizada: ¿Es una aguja precisa o una colina incierta?"
    }
]

# ==========================================
# 2. FUNCIÓN DE RENDERIZADO "SAFE"
# ==========================================
def get_safe_video_path(scene_name):
    """
    Busca el video. 
    SI EXISTE -> Devuelve ruta.
    SI NO EXISTE -> Importa Manim y renderiza.
    """
    expected_filename = f"{scene_name}.mp4"
    search_dir = "media" # Carpeta raíz de salida
    
    if os.path.exists(search_dir):
        for root, dirs, files in os.walk(search_dir):
            if expected_filename in files:
                return os.path.join(root, expected_filename)
    
    # Renderizado bajo demanda
    st.info(f"🎥 Renderizando {scene_name} por primera vez... (Esto puede tardar)")
    
    try:
        from manim import config
        import scenes.eda_scenes as manim_scenes 
        
        config.media_width = "100%"
        config.verbosity = "ERROR"
        config.pixel_height = 720
        config.pixel_width = 1280
        config.output_file = scene_name
        
        scene_class = getattr(manim_scenes, scene_name)
        scene = scene_class()
        scene.render()
        
        for root, dirs, files in os.walk(config.media_dir):
            if expected_filename in files:
                return os.path.join(root, expected_filename)
                
    except ImportError:
        st.error("Error Crítico: No se pudo importar Manim.")
        return None
    except Exception as e:
        st.error(f"Error al renderizar: {e}")
        return None
        
    return None

# ==========================================
# 3. INTERFAZ DE CARRUSEL (Lógica Principal)
# ==========================================

# Título de la página (necesario ya que quitamos st.Page title de aquí)
st.title("Estadistica Básica")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO ---
if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = 0

def next_slide():
    if st.session_state.carousel_index < len(ACTOS) - 1:
        st.session_state.carousel_index += 1

def prev_slide():
    if st.session_state.carousel_index > 0:
        st.session_state.carousel_index -= 1

# --- CONTENIDO ACTUAL ---
idx = st.session_state.carousel_index
current_act = ACTOS[idx]

# --- UI: PROGRESO Y HEADER ---
st.header(current_act["titulo"])

# --- VISUALIZADOR DE VIDEO ---
video_container = st.empty()

# Obtener video de forma segura
video_path = get_safe_video_path(current_act["clase"])

if video_path and os.path.exists(video_path):
    # Usamos key única para forzar recarga al cambiar de slide
    video_container.video(video_path)
else:
    video_container.error("No se pudo cargar el video.")

# --- DESCRIPCIÓN ---
st.markdown(current_act["desc"])

st.divider()
st.progress((idx + 1) / len(ACTOS))
st.caption(f"Diapositiva {idx + 1} de {len(ACTOS)}")


# --- NAVEGACIÓN (BOTONES) ---
c1, c2, c3 = st.columns([1, 4, 1])

with c1:
    st.button("⬅️ Anterior", on_click=prev_slide, disabled=(idx == 0))
    
with c3:
    st.button("Siguiente ➡️", on_click=next_slide, disabled=(idx == len(ACTOS) - 1))

# --- HACK PARA TECLAS DE FLECHA ---
components.html("""
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight') {
        const buttons = doc.querySelectorAll('button');
        Array.from(buttons).find(b => b.innerText.includes("Siguiente")).click();
    }
    if (e.key === 'ArrowLeft') {
        const buttons = doc.querySelectorAll('button');
        Array.from(buttons).find(b => b.innerText.includes("Anterior")).click();
    }
});
</script>
""", height=0, width=0)