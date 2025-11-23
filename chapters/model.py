import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
from utils import wizard_navigation

def run():
    SESSION_KEY = 'model_step'
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = 0
    
    current_step = st.session_state[SESSION_KEY]
    df = st.session_state['df_main']  # Dataset Inmobiliario Tenerife
    
    st.title("Módulo 2: Modelado Supervisado")
    st.caption("De los datos a las reglas de decisión.")

    # ==============================================================================
    # PASO 0: FUNDAMENTOS Y SPLIT (La base académica)
    # ==============================================================================
    if current_step == 0:
        st.header("1. Partición del Conjunto de Datos")
        st.markdown("""
        Para evaluar honestamente la capacidad de generalización de un modelo, debemos separar los datos en dos subconjuntos estancos:
        
        1.  **Entrenamiento (Training Set):** Datos que el modelo "ve" para aprender.
        2.  **Prueba (Test Set):** Datos ocultos usados exclusivamente para examen final.
        """)
        
        col_conf, col_viz = st.columns([1, 2])
        
        with col_conf:
            test_size = st.slider("Porcentaje de Test (%)", 10, 50, 20)
            st.info(f"Entrenamiento: {100-test_size}%  \nPrueba: {test_size}%")
            
            # Guardamos esta config para pasos siguientes
            st.session_state['test_size'] = test_size / 100

        with col_viz:
            # Visualización simple de la partición
            labels = ['Entrenamiento', 'Prueba']
            values = [df.shape[0] * (1 - test_size/100), df.shape[0] * (test_size/100)]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=['#3498db', '#e74c3c'])])
            fig.update_layout(title_text="Distribución de Muestras", height=300)
            st.plotly_chart(fig, use_container_width=True)

    # ==============================================================================
    # PASO 1: REGRESIÓN (Predicción Numérica)
    # ==============================================================================
    elif current_step == 1:
        st.header("2. Tarea de Regresión: Predicción de Precios")
        st.markdown("""
        Entrenaremos un **Random Forest Regressor** para estimar el valor de mercado (`Precio_Venta`).
        
        **Variables Predictoras (X):** Metros, Habitaciones, Antigüedad, Distancia al mar, Zona.
        """)
        
        # Preparación de datos (Preprocesamiento invisible)
        X = pd.get_dummies(df.drop("Precio_Venta", axis=1), columns=["Zona"])
        y = df["Precio_Venta"]
        
        test_size = st.session_state.get('test_size', 0.2)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Panel de Control del Modelo
        with st.expander("⚙️ Hiperparámetros del Algoritmo", expanded=True):
            n_trees = st.slider("Complejidad (Número de Árboles)", 10, 200, 50)
        
        if st.button("🚀 Entrenar Regresor", type="primary"):
            with st.spinner("Ajustando pesos del modelo..."):
                model = RandomForestRegressor(n_estimators=n_trees, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                # Métricas
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                # Guardar modelo para el paso final
                st.session_state['regressor_model'] = model
                st.session_state['model_columns'] = X.columns
                
            # Resultados visuales
            c1, c2 = st.columns(2)
            c1.metric("Precisión Global (R²)", f"{r2:.1%}", help="100% es perfecto. 0% es aleatorio.")
            c2.metric("Error Medio Absoluto", f"{mae:,.0f} €", help="Cuánto nos equivocamos de media.")
            
            st.markdown("#### Realidad vs Predicción")
            # Gráfico Predicho vs Real
            comparison_df = pd.DataFrame({'Real': y_test, 'Predicho': y_pred})
            
            fig = px.scatter(comparison_df, x="Real", y="Predicho", opacity=0.6, 
                             title="Dispersión de Errores", labels={'Real': 'Precio Real (€)', 'Predicho': 'Precio Estimado (€)'})
            # Línea de perfección
            fig.add_shape(type="line", line=dict(dash='dash', color='red'),
                          x0=y_test.min(), y0=y_test.max(), x1=y_test.min(), y1=y_test.max())
            st.plotly_chart(fig, use_container_width=True)

    # ==============================================================================
    # PASO 2: CLASIFICACIÓN VISUAL (Fronteras de Decisión)
    # ==============================================================================
    elif current_step == 2:
        st.header("3. Tarea de Clasificación: Fronteras de Decisión")
        st.markdown("""
        Para entender "cómo piensa" el modelo, simplificaremos el problema a 2 dimensiones.
        
        **Objetivo:** Clasificar si una propiedad es **"Premium"** (> 300.000 €) basándonos solo en **Metros** y **Distancia al Mar**.
        """)
        
        # Crear target binario
        df_class = df.copy()
        df_class['Es_Premium'] = (df_class['Precio_Venta'] > 300000).astype(int)
        
        X_simple = df_class[['Metros_Cuadrados', 'Distancia_Costa_Km']]
        y_simple = df_class['Es_Premium']
        
        # Entrenar modelo ligero para visualización
        clf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
        clf.fit(X_simple, y_simple)
        
        st.success(f"Precisión en Clasificación: {clf.score(X_simple, y_simple):.1%}")
        
        # --- GENERACIÓN DE LA MALLA DE DECISIÓN (Visualización Avanzada) ---
        x_min, x_max = X_simple.iloc[:, 0].min() - 10, X_simple.iloc[:, 0].max() + 10
        y_min, y_max = X_simple.iloc[:, 1].min() - 1, X_simple.iloc[:, 1].max() + 1
        
        # Crear grid
        h = 2.0 # Paso de la malla (resolución)
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, 0.5))
        
        # Predecir toda la malla
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        # Plot con Plotly
        fig = go.Figure()
        
        # 1. Mapa de Calor (Las zonas de decisión del modelo)
        fig.add_trace(go.Contour(
            z=Z, x=np.arange(x_min, x_max, h), y=np.arange(y_min, y_max, 0.5),
            showscale=False, opacity=0.4, colorscale=[[0, 'blue'], [1, 'gold']],
            name="Región Predicha"
        ))
        
        # 2. Puntos reales (Scatter)
        fig.add_trace(go.Scatter(
            x=X_simple['Metros_Cuadrados'], y=X_simple['Distancia_Costa_Km'],
            mode='markers',
            marker=dict(color=y_simple, colorscale=[[0, 'blue'], [1, 'gold']], line_width=1, size=8),
            text=['Premium' if v else 'Estándar' for v in y_simple],
            name="Datos Reales"
        ))
        
        fig.update_layout(
            title="Mapa de Decisión del Algoritmo",
            xaxis_title="Superficie (m²)",
            yaxis_title="Distancia al Mar (km)",
            legend_title="Clase"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Las áreas amarillas son donde el modelo predice 'Premium'. Las azules, 'Estándar'. Observe cómo la frontera no es lineal.")

    # ==============================================================================
    # PASO 3: DESPLIEGUE (Interacción Final)
    # ==============================================================================
    elif current_step == 3:
        st.header("4. Despliegue del Modelo")
        
        if 'regressor_model' not in st.session_state:
            st.warning("⚠️ Debe entrenar el modelo de Regresión en el **Paso 2** antes de usar esta sección.")
        else:
            st.markdown("El modelo está cargado en memoria listo para inferencia.")
            
            with st.form("prediction_form"):
                st.subheader("Simulador de Tasación")
                c1, c2, c3 = st.columns(3)
                metros = c1.number_input("Superficie (m²)", 40, 500, 100)
                habs = c2.number_input("Habitaciones", 1, 10, 3)
                antig = c3.number_input("Antigüedad (años)", 0, 100, 10)
                
                c4, c5 = st.columns(2)
                dist = c4.slider("Distancia Mar (km)", 0.0, 20.0, 5.0)
                zona = c5.selectbox("Zona Geográfica", ["Santa Cruz", "La Laguna", "Sur (Turístico)", "Norte (Rural)"])
                
                submitted = st.form_submit_button("Calcular Valor de Mercado")
                
                if submitted:
                    # 1. Crear DF con una fila
                    input_data = pd.DataFrame({
                        'Metros_Cuadrados': [metros], 'Habitaciones': [habs],
                        'Antiguedad_Anios': [antig], 'Distancia_Costa_Km': [dist],
                        'Zona': [zona] # Columna auxiliar
                    })
                    
                    # 2. Replicar el One-Hot Encoding manual
                    # Creamos dataframe vacío con las columnas del modelo
                    model_cols = st.session_state['model_columns']
                    final_input = pd.DataFrame(0, index=[0], columns=model_cols)
                    
                    # Rellenamos numéricos
                    final_input['Metros_Cuadrados'] = metros
                    final_input['Habitaciones'] = habs
                    final_input['Antiguedad_Anios'] = antig
                    final_input['Distancia_Costa_Km'] = dist
                    
                    # Rellenamos la categoría zona correcta
                    zona_col = f"Zona_{zona}"
                    if zona_col in final_input.columns:
                        final_input[zona_col] = 1
                        
                    # 3. Predecir
                    model = st.session_state['regressor_model']
                    pred_price = model.predict(final_input)[0]
                    
                    st.success(f"💰 Valoración Estimada: **{pred_price:,.2f} €**")
                    if pred_price > 300000:
                        st.balloons()

    st.markdown("---")
    # Navegación del Módulo
    wizard_navigation(total_pages=4, current_page_key=SESSION_KEY)