import streamlit as st
import pandas as pd
import numpy as np

def load_css():
    """Estilos CSS más formales y académicos."""
    st.markdown("""
        <style>
        /* Tipografía más académica */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Roboto', sans-serif;
        }
        
        /* Encabezados sobrios */
        h1, h2, h3 {
            color: #202124;
            font-weight: 600;
        }
        
        /* Contenedor principal tipo documento */
        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        
        /* Ocultar elementos de UI innecesarios */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Estilo para las tarjetas de navegación */
        .nav-card {
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            background-color: #ffffff;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data
def get_intro_data():
    """Dataset simple para la introducción (Notas estudiantes)."""
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "Horas_Estudio": np.random.normal(5, 2, n).clip(0, 12).round(1),
        "Asistencia_Pct": np.random.randint(50, 100, n),
        "Examen_Previo": np.random.normal(6, 2, n).clip(0, 10).round(1)
    })
    df["Nota_Final"] = (df.Horas_Estudio * 0.4 + df.Examen_Previo * 0.5 + np.random.normal(0, 1, n)).clip(0, 10).round(1)
    return df

@st.cache_data
def get_main_dataset():
    """
    Dataset Maestro: Real Estate Tenerife (Sintético).
    Más complejo, incluye variables categóricas, numéricas y coordenadas.
    """
    np.random.seed(101)
    n_houses = 1000
    
    # Generación de variables
    zonas = np.random.choice(['Santa Cruz', 'La Laguna', 'Sur (Turístico)', 'Norte (Rural)'], n_houses, p=[0.3, 0.3, 0.25, 0.15])
    m2 = np.random.normal(100, 40, n_houses).clip(40, 400).round(0)
    habitaciones = np.clip(m2 // 30 + np.random.randint(-1, 2, n_houses), 1, 6)
    antiguedad = np.random.randint(0, 50, n_houses)
    distancia_mar = np.random.exponential(5, n_houses).round(1) # En km
    
    # Lógica de precio base
    precio_m2_base = {'Santa Cruz': 2200, 'La Laguna': 1900, 'Sur (Turístico)': 3500, 'Norte (Rural)': 1500}
    precios = []
    
    for i in range(n_houses):
        base = precio_m2_base[zonas[i]]
        # Penalización por antigüedad
        factor_edad = 1 - (antiguedad[i] * 0.005) 
        # Bonus por cercanía al mar
        factor_mar = 1 + (1 / (distancia_mar[i] + 0.5)) * 0.2
        
        valor = m2[i] * base * factor_edad * factor_mar
        valor += np.random.normal(0, 20000) # Ruido aleatorio
        precios.append(valor)
        
    df = pd.DataFrame({
        "Zona": zonas,
        "Metros_Cuadrados": m2,
        "Habitaciones": habitaciones,
        "Antiguedad_Anios": antiguedad,
        "Distancia_Costa_Km": distancia_mar,
        "Precio_Venta": np.array(precios).round(-2) # Redondear a centenas
    })
    
    return df

def wizard_navigation(total_pages, current_page_key):
    """Componente de navegación Anterior / Siguiente."""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    curr = st.session_state.get(current_page_key, 0)
    
    with col1:
        if curr > 0:
            if st.button("⬅️ Anterior", use_container_width=True):
                st.session_state[current_page_key] -= 1
                st.rerun()
                
    with col3:
        if curr < total_pages - 1:
            if st.button("Siguiente ➡️", use_container_width=True):
                st.session_state[current_page_key] += 1
                st.rerun()
    
    # Barra de progreso visual
    st.progress((curr + 1) / total_pages)
    st.caption(f"Sección {curr + 1} de {total_pages}")