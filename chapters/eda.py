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
            # Acto 2: La Anatomía de la Distribución
            
            A menudo usamos "Variable Aleatoria" y "Distribución" como sinónimos, pero son etapas distintas de una misma historia. Este vídeo desglosa el proceso paso a paso.

            ### 1. El Mapa Invisible (La 'Probability Density Function')
            Antes de que caiga el primer dato, ya existe una **Función de Densidad de Probabilidad** (esa curva azul fantasma).
            * No es el dato en sí, es el "molde".
            * **La Regla:** Donde la curva es alta, la "gravedad" es más fuerte. Es mucho más probable que los datos aterricen ahí.

            ### 2. Variable Aleatoria ($X$): El "Cursor"
            Fíjate en el triángulo rojo inquieto. Eso es la Variable Aleatoria.
            * **No es un número:** Es una función, un proceso. Es el acto de tirar el dado o medir a una persona.
            * **La Incertidumbre:** Cada vez que ejecutamos $X$, el cursor busca un valor. La mayoría de las veces acabará en el centro (zona alta de la curva), pero de vez en cuando, el azar lo llevará a los extremos (eventos raros).

            ### 3. El Milagro Estadístico (La Acumulación)
            Bueno no es un milagro pero aquí ocurre la magia. Un solo punto es impredecible, caos, pero **800 puntos son perfectamente predecibles**, orden.
            * Al apilarse, las bolas amarillas reconstruyen físicamente la curva verde teórica.
            * Esto se conoce como la **Ley de los Grandes Números**: el comportamiento colectivo revela la verdad oculta que el individuo no puede mostrar.

            ---

            ### 4. El Zoológico de Distribuciones
            NO todo es una camapana de Gauss la forma de la curva depende del problema:

            | Distribución | Forma | ¿Por qué tiene esa forma? |
            | :--- | :--- | :--- |
            | **Uniforme** | Rectangular | **Justicia ciega.** El azar no tiene favoritos. Todos los valores tienen exactamente la misma probabilidad (ej. un dado perfecto). |
            | **Exponencial** | Tobogán | **Fatiga o Espera.** Es muy probable que el evento ocurra pronto (pico alto al inicio), y cada vez más difícil que tarde mucho (cola larga). Típico en tiempos de espera o decaimiento radiactivo. |
            | **Bimodal** | Dos Jorobas | **Mezcla oculta.** Si ves esto, tus datos gritan: "¡Aquí hay dos grupos distintos!". Por ejemplo, si mezclas alturas de jugadores de baloncesto y gimnastas en la misma gráfica. |
        """)
    },
    {
        "clase": "Acto3_Media",
        "titulo": "Acto 3: El Balancín (Tendencia Central)",
        "desc": textwrap.dedent("""
            ### 1. El Punto de Equilibrio: La Media ($$\mu$$)
                                
            Imagina que tus datos no son números abstractos, sino objetos con peso físico colocados sobre una balanza. La **media aritmética** ($$\mu$$) es el punto exacto donde esa balanza se mantiene perfectamente horizontal. Matemáticamente, se define como la suma de todos los valores dividida por el número total de observaciones:
            $$\mu = \\frac{\sum_{i=1}^{N} x_i}{N}$$
            En la animación, vemos cómo un conjunto de datos simétricos encuentra su equilibrio de forma natural en el centro. Sin embargo, la media tiene una debilidad: es **extremadamente sensible**. Al introducir un **outlier** (un valor atípico muy lejano, como el punto rojo), el punto de equilibrio debe desplazarse drásticamente hacia ese extremo para compensar el "peso" extra y evitar que la balanza se vuelque. Esto nos enseña que la media, aunque útil, puede ser engañosa si nuestros datos tienen valores extremos.
            
            ### 2. El Centro Ordenado: La Mediana ($$Me$$)
                                
            A diferencia de la media, que busca el equilibrio de pesos, la **mediana** busca el centro del orden. Si alineamos todos nuestros datos de menor a mayor, la mediana es el valor que ocupa la posición central, dividiendo al conjunto en dos mitades exactas: 50% de los datos quedan a su izquierda y 50% a su derecha. Su posición se determina por el índice:
            $$Me = x_{\\frac{N+1}{2}}$$
            Visualmente, la mediana actúa como una barrera que separa los datos "bajos" (rojos) de los "altos" (azules). Su gran fortaleza es la **robustez**: cuando añadimos el mismo outlier que desestabilizó la media, la mediana apenas se inmuta. Simplemente se desplaza un lugar en la fila ordenada, ignorando qué tan lejos está el valor extremo. Por eso, la mediana es el estadístico preferido para datos asimétricos, como los salarios o los precios de vivienda.
            
            ### 3. La Medida de la Incertidumbre: La Desviación Estándar ($$\sigma$$)
                                
            Conocer el centro no es suficiente; necesitamos saber qué tan dispersos están los datos alrededor de él. La **desviación estándar** ($$\sigma$$) es, en esencia, la distancia promedio de cada punto respecto a la media. Su fórmula calcula la raíz cuadrada del promedio de las distancias al cuadrado:
            $$\sigma = \sqrt{\\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}}$$
            En la animación, representamos esto con líneas naranjas que conectan cada bola con el centro.
            * **Poca dispersión ($$\sigma$$ baja):** Las bolas están agrupadas cerca del centro, las líneas naranjas son cortas. Esto indica alta precisión y consistencia en los datos.
            * **Mucha dispersión ($$\sigma$$ alta):** Las bolas están muy separadas, generando líneas largas. Esto señala una mayor variabilidad e incertidumbre.
            > **Finalmente:** Cuando dejamos de ver puntos individuales y pasamos a tener miles de datos, estas propiedades físicas (centro y dispersión) moldean la **distribución continua** que emerge, transformando el histograma discreto en la suave curva de densidad que estudiamos en estadística teórica.
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
    st.button("◄", on_click=prev_slide, disabled=(idx == 0))
    
with c3:
    st.button("►", on_click=next_slide, disabled=(idx == len(ACTOS) - 1))

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