import streamlit as st
import pandas as pd
import numpy as np
from utils import render_manim_scene
# Importamos la escena específica para este capítulo
from scenes.eda_scenes import ScatterPlotScene

def run():
    st.title("Módulo 1: Análisis Exploratorio de Datos (EDA)")
    
    # --- SECCIÓN 1: TEORÍA ---
    st.subheader("1. ¿Por qué visualizamos?")
    st.markdown("""
    Antes de lanzar algoritmos complejos, debemos entender la **forma** de los datos.
    El EDA nos permite detectar:
    * Outliers (Valores atípicos).
    * Patrones de distribución.
    * Correlaciones ocultas.
    """)
    
    # --- SECCIÓN 2: VIDEO EXPLICATIVO (MANIM) ---
    st.write("### Concepto Visual: La Correlación")
    
    col_video, col_texto = st.columns([3, 2])
    
    with col_video:
        with st.spinner("Renderizando concepto matemático..."):
            video_path = render_manim_scene(ScatterPlotScene)
            if video_path:
                st.video(video_path)
    
    with col_texto:
        st.info("""
        **Lo que ves en el video:**
        
        A medida que aumenta X, aumenta Y. Los puntos se agrupan alrededor de una línea imaginaria.
        
        Esto indica una **Correlación de Pearson** cercana a 1.
        """)

    st.divider()

    # --- SECCIÓN 3: CÓDIGO Y PRÁCTICA ---
    st.subheader("2. Llevándolo a Python")
    st.markdown("Para replicar lo que hemos visto en el video, usamos `pandas` y `matplotlib`.")

    code_snippet = '''
import matplotlib.pyplot as plt
import numpy as np

# Generar datos simulados
x = np.linspace(0, 10, 50)
y = x + np.random.normal(0, 1, 50) # Ruido aleatorio

plt.scatter(x, y)
plt.title("Correlación Lineal")
plt.show()
    '''
    st.code(code_snippet, language='python')
    
    # --- SECCIÓN 4: INTERACTIVIDAD ---
    st.write("### 🧪 Pruébalo tú mismo")
    st.write("Ajusta el nivel de 'Ruido' (desorden) en los datos y mira cómo afecta a la gráfica.")
    
    noise_level = st.slider("Nivel de Ruido", 0.0, 5.0, 1.0)
    
    # Generación en tiempo real (Plotly es más rápido para esto que Manim)
    x = np.linspace(0, 10, 100)
    y = x + np.random.normal(0, noise_level, 100)
    df = pd.DataFrame({'Variable X': x, 'Variable Y': y})
    
    st.scatter_chart(df, x='Variable X', y='Variable Y')
    
    if noise_level > 3:
        st.warning("¡Cuidado! Con tanto ruido, el modelo no podrá encontrar el patrón.")