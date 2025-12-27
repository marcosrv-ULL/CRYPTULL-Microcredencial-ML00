import streamlit as st
import numpy as np
import pandas as pd

# Título Principal
st.title("Introducción al Machine Learning")

# --- BLOQUE 1: INTRODUCCIÓN ---
st.markdown("""
**Bienvenido/a al entorno interactivo de aprendizaje.**

El objetivo de esta aplicación no es sustituir la teoría, sino **hacerla tangible**. 
Aquí encontrarás:
1.  **Vídeos Conceptuales:** Animaciones matemáticas creadas con *Manim* para entender el "porqué" de las fórmulas.
2.  **Laboratorios Vivos:** Controles y sliders para romper los modelos y ver cómo reaccionan.
3.  **Gamificación:** Pequeños retos para validar tu intuición numérica.
""")

st.divider()

# --- BLOQUE 2: PEQUEÑO JUEGO (DEMO) ---
st.header("Pequeño juego: Tu Intuición Visual")
st.markdown("Antes de entrar en materia, vamos a probar tu ojo clínico. **¿Eres capaz de ajustar la línea a los datos?**")

col_control, col_grafico = st.columns([1, 3])

with col_control:
    st.write("### Controles")
    # El alumno debe mover esto para encajar la línea
    m = st.slider("Pendiente (Inclinación)", -5.0, 5.0, 0.0, step=0.1)
    b = st.slider("Intercepto (Altura)", -10.0, 10.0, 0.0, step=0.5)
    
    st.caption("Mueve los sliders hasta que la línea roja cruce la nube de puntos azules.")

with col_grafico:
    # Generamos unos datos "falsos" fijos para que el alumno intente adivinar
    # La solución oculta es m=2.5, b=-2.0
    x = np.linspace(-10, 10, 100)
    
    # Datos ruidosos (Target)
    np.random.seed(42) # Semilla fija para que no cambie el reto
    y_target = 2.5 * x - 2.0 + np.random.normal(0, 3, 100)
    
    # Línea del alumno (Predicción)
    y_pred = m * x + b
    
    # Creamos DF para pintar
    chart_data = pd.DataFrame({
        'x': x,
        'Datos Reales (Objetivo)': y_target,
        'Tu Línea': y_pred
    })
    
    # Usamos st.line_chart (o scatter combinado si queremos más detalle, 
    # pero line_chart es rápido para una intro)
    st.line_chart(
        chart_data, 
        x='x', 
        y=['Datos Reales (Objetivo)', 'Tu Línea'],
        color=["#0000FF", "#FF0000"] # Azul datos, Rojo usuario
    )

# --- FEEDBACK DEL JUEGO ---
error = np.mean((y_target - y_pred)**2) # MSE simplificado

if error < 10:
    st.success(f"¡GENIAL! Has encontrado el patrón. (Error: {error:.2f})")
    st.balloons()
elif error < 50:
    st.warning(f"Estás cerca... ajusta un poco más la pendiente. (Error: {error:.2f})")
else:
    st.error(f"Estás muy lejos. ¡Inténtalo de nuevo! (Error: {error:.2f})")

st.markdown("---")
st.caption("<-- *Usa el menú de la izquierda para comenzar con el Módulo 1.*")