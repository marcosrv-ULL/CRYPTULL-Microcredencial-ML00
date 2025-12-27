import streamlit as st
import os
import streamlit.components.v1 as components
import textwrap  # <--- IMPORTANTE: Para limpiar la indentación del texto

# ==========================================
# 1. CONFIGURACIÓN DEL CONTENIDO (GUION)
# ==========================================

# Usamos textwrap.dedent para poder escribir el markdown ordenado en el código
# sin que se rompa la visualización en la web.

ACTOS = [
    {
        "clase": "Acto1_Variable",
        "titulo": "Acto 1: La Variable",
        "desc": textwrap.dedent("""
            En ciencia de datos, no trabajamos con números abstractos en el vacío, sino con **variables**. Como hemos visto en la animación, una variable es simplemente una característica que *fluctúa* (cambia) de un sujeto a otro.

            ### 1. La Anatomía de un Dataset
            Antes de visualizar nada, los datos suelen vivir en tablas (DataFrames). Es crucial distinguir dos roles fundamentales:

            * **Variables Independientes ($X$):** Son las **características** o *features* (ej. Peso, Altura). Son los datos que *tenemos*.
            * **Variable Objetivo ($Y$):** Es la etiqueta o *target* (ej. Especie). Es el dato que queremos *predecir*.

            ---

            ### 2. La Naturaleza del Dato: ¿Fluido o Caja?

            Una vez extraemos una columna de esa tabla, el dato se comporta de dos formas muy distintas. Entender esto es vital para elegir el modelo correcto más adelante.

            #### A. Variable Continua (El Espectro)
            Imagina una rampa suave. Una variable continua puede tomar **infinitos valores** dentro de un rango.
            * **Comportamiento:** Si haces *zoom* entre 5.2 y 5.3, siempre encontrarás otro valor (5.25, 5.251...).
            * **La Animación:** El punto amarillo se desliza suavemente (`5.2` $\\to$ `5.721...`). No hay saltos.
            * **Ejemplos:** Temperatura, Tiempo, Distancia, pH.

            #### B. Variable Discreta (El Contenedor)
            Imagina una escalera o una serie de cajas. Una variable discreta **no permite valores intermedios**. El dato debe "encajar" a la fuerza en una categoría o un número entero.
            * **Comportamiento:** Es binario o categórico. O eres una cosa, o eres otra.
            * **La Animación:** Vemos cómo el espacio se divide en **Buckets** (Cajas).
            * **El Dilema del 5.5:** ¿Qué pasa en la frontera? En la animación vimos un punto caer en **5.5** (tierra de nadie).
                * *La Regla:* En variables discretas, forzamos el dato al contenedor más cercano o aplicamos una regla de redondeo (en este caso, hacia arriba: **Categoría 6**).
            * **Ejemplos:** Número de hijos, Clasificación de especies, Días de la semana.

            > **Nota para el futuro:**
            > * Si tu $Y$ es **Continua** $-->$ Usaremos **Regresión**.
            > * Si tu $Y$ es **Discreta** $-->$ Usaremos **Clasificación**.
        """)
    },
    {
        "clase": "Acto2_Distribucion",
        "titulo": "Acto 2: La Distribución",
        "desc": textwrap.dedent("""
            # Acto 2: La Distribución (Del Caos al Orden)
            
            Lo fascinante de la estadística es cómo el comportamiento individual es impredecible, pero el comportamiento colectivo es matemáticamente perfecto.

            ### 1. La Lluvia de Datos
            En la animación hemos simulado una **Máquina de Galton**. 
            * Cada punto cae de forma aleatoria. No podemos saber dónde aterrizará el próximo punto amarillo.
            * Sin embargo, cuando caen 200 puntos, **se apilan formando una silueta reconocible**.

            ### 2. La Función de Densidad
            Esa silueta suave que dibujamos sobre las bolas apiladas es la **Distribución**.
            * Nos dice la **probabilidad** de encontrar un dato en esa zona.
            * En la naturaleza, muchas variables (altura, errores de medición, notas de examen) tienden a acumularse en el centro y descender hacia los lados.
            
            > **Concepto Clave:** A esta forma de campana perfecta la llamamos **Distribución Normal** o Gaussiana. Es la "forma por defecto" del universo para muchos fenómenos.
        """)
    },
    {
        "clase": "Acto3_Media",
        "titulo": "Acto 3: El Balancín (Tendencia Central)",
        "desc": textwrap.dedent("""
            # ⚖️ Acto 3: El Mapa de la Curva (El Centro)
            
            Una vez tenemos la forma (la distribución), necesitamos números para describirla. La primera pregunta es: **¿Dónde está el centro?**

            ### 1. La Media ($\mu$): El Punto de Equilibrio
            Visualízalo como un balancín físico. La media es el punto exacto donde la barra se mantiene horizontal.
            * **El Problema del Outlier:** En el video, añadimos un dato rojo muy lejano (un outlier).
            * **La Reacción:** Para que el balancín no se vuelque, el punto de apoyo (la media) tuvo que desplazarse rápidamente hacia la derecha.
            * **Lección:** La media es **muy sensible** a los valores extremos. Si Bill Gates entra en un bar, la "media" de riqueza sube a millones, pero nadie es más rico.

            ### 2. La Mediana: La Cuchilla
            Aunque no sale en la animación, la mediana es una cuchilla que corta el área en dos mitades iguales de masa (bolas).
            * La mediana apenas se mueve con el outlier. Es una medida **robusta**.
        """)
    },
    {
        "clase": "Acto4_Dispersion",
        "titulo": "Acto 4: La Respiración (Dispersión)",
        "desc": textwrap.dedent("""
            # 🌬️ Acto 4: La Incertidumbre (Dispersión)
            
            Saber el centro no es suficiente. Necesitamos saber cuánto confiamos en ese centro. Aquí entra la **Desviación Estándar ($\sigma$)**.

            ### La Metáfora de la Respiración
            En la animación vemos la curva "respirar", haciéndose más ancha o más estrecha.

            #### 🟢 Curva Estrecha ($\sigma$ bajo)
            * La curva es alta y delgada, como una aguja.
            * Significa que todos los datos están muy pegados a la media.
            * **Interpretación:** Tenemos mucha **precisión** y poca incertidumbre.

            #### 🟢 Curva Ancha ($\sigma$ alto)
            * La curva se aplasta como una colina suave.
            * Los datos están muy dispersos, lejos del centro.
            * **Interpretación:** Hay mucho **ruido** o variabilidad. El dato promedio es menos representativo.
            
            > **En Machine Learning:** Un modelo con alta varianza (curva ancha) suele ser inestable. Entender la dispersión es clave para calcular el error de tus predicciones.
        """)
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

# Título de la página
st.title("Estadística Básica")

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
# Aquí se renderiza el markdown limpio gracias a textwrap.dedent
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