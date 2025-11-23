import streamlit as st
import plotly.express as px
from utils import wizard_navigation

def run():
    # Configuración de estado para la navegación paso a paso
    SESSION_KEY = 'eda_step'
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = 0
        
    current_step = st.session_state[SESSION_KEY]
    
    # Recuperamos el Dataset Maestro (Inmobiliaria Tenerife)
    df = st.session_state['df_main']

    st.title("Módulo 1: Análisis Exploratorio de Datos (EDA)")
    st.caption("Objetivo: Comprender la estructura subyacente de la información antes del modelado.")

    # ------------------------------------------------------------------
    # PASO 0: ANÁLISIS UNIVARIANTE (Histogramas y Distribuciones)
    # ------------------------------------------------------------------
    if current_step == 0:
        st.header("1. Distribución de la Variable Objetivo")
        st.markdown("""
        En cualquier problema de regresión, el primer paso es analizar el comportamiento de la variable dependiente (Target).
        En este caso, analizamos el **Precio de Venta**.
        """)
        
        col_text, col_viz = st.columns([1, 2])
        
        with col_text:
            st.info("""
            **Concepto Clave: Sesgo (Skewness)**
            
            Los precios inmobiliarios raramente siguen una distribución normal perfecta. 
            Suelen presentar una "cola larga" a la derecha debido a las propiedades de lujo.
            """)
            
            # Estadísticos básicos
            st.write("**Estadísticos Descriptivos:**")
            st.write(df['Precio_Venta'].describe().round(2))
            
        with col_viz:
            fig = px.histogram(
                df, 
                x="Precio_Venta", 
                nbins=50, 
                title="Histograma de Precios de Venta",
                color_discrete_sequence=['#2c3e50'],
                opacity=0.75
            )
            # Añadir línea de media
            mean_val = df['Precio_Venta'].mean()
            fig.add_vline(x=mean_val, line_dash="dash", line_color="red", annotation_text="Media")
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # PASO 1: ANÁLISIS BIVARIANTE (Categórico vs Numérico)
    # ------------------------------------------------------------------
    elif current_step == 1:
        st.header("2. Segmentación por Categorías")
        st.markdown("""
        Es imperativo determinar si las variables categóricas (como la Zona) discriminan efectivamente el precio.
        Para ello, utilizamos **Diagramas de Caja (Boxplots)**.
        """)
        
        variable_y = st.selectbox("Seleccione Variable Numérica a comparar:", ["Precio_Venta", "Metros_Cuadrados", "Distancia_Costa_Km"])
        
        col_viz, col_insight = st.columns([3, 1])
        
        with col_viz:
            fig = px.box(
                df, 
                x="Zona", 
                y=variable_y, 
                color="Zona",
                title=f"Distribución de {variable_y} según Zona Geográfica",
                points="outliers" # Solo mostrar puntos atípicos
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_insight:
            st.warning("""
            **Interpretación:**
            
            Observe la línea central de cada caja (la mediana). 
            
            Si las cajas no se solapan verticalmente, existe una diferencia estadística significativa entre las zonas.
            """)

    # ------------------------------------------------------------------
    # PASO 2: ANÁLISIS MULTIVARIANTE (Correlaciones)
    # ------------------------------------------------------------------
    elif current_step == 2:
        st.header("3. Relaciones y Correlación")
        st.markdown("""
        Buscamos relaciones lineales entre las variables predictoras (features) y el precio.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Eje X (Variable Independiente)", ["Metros_Cuadrados", "Antiguedad_Anios", "Distancia_Costa_Km"])
        with c2:
            color_dim = st.selectbox("Dimensión de Color (Segmentación)", ["Zona", "Habitaciones"])
            
        # Scatter Plot con Tendencia
        fig = px.scatter(
            df, 
            x=x_axis, 
            y="Precio_Venta", 
            color=color_dim,
            opacity=0.6,
            trendline="ols", # Regresión lineal ordinaria (Ordinary Least Squares)
            title=f"Correlación: {x_axis} vs Precio",
            labels={"Precio_Venta": "Precio (€)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Nota Académica:** La pendiente de la línea de tendencia indica la sensibilidad del precio ante cambios en la variable X.
        Una pendiente negativa en "Antigüedad" sugiere depreciación del activo.
        """)

    # ------------------------------------------------------------------
    # PASO 3: MATRIZ DE CORRELACIÓN (Síntesis)
    # ------------------------------------------------------------------
    elif current_step == 3:
        st.header("4. Mapa de Calor de Correlaciones")
        st.markdown("Finalmente, cuantificamos la intensidad de las relaciones lineales usando el Coeficiente de Pearson ($r$).")
        
        # Filtramos solo columnas numéricas para la matriz
        numeric_df = df.select_dtypes(include=['float64', 'int64', 'int32'])
        corr_matrix = numeric_df.corr().round(2)
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r", # Rojo a Azul (divergente)
            title="Matriz de Correlación de Pearson"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📝 Evaluación del Módulo")
        
        respuesta = st.radio(
            "Basado en la matriz anterior, ¿qué variable tiene la correlación más fuerte con el Precio?",
            ["Antigüedad", "Metros Cuadrados", "Habitaciones"],
            index=None
        )
        
        if respuesta == "Metros Cuadrados":
            st.success("Correcto. Es habitual que la superficie sea el predictor dominante en bienes raíces.")
        elif respuesta:
            st.error("Incorrecto. Revise los valores en la fila de 'Precio_Venta'. Busque el valor más cercano a 1.0.")

    st.markdown("---")
    # Navegación Wizard (4 pasos: 0, 1, 2, 3)
    wizard_navigation(total_pages=4, current_page_key=SESSION_KEY)