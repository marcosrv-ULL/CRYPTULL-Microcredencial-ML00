import streamlit as st
import pandas as pd
import numpy as np
import os # Necesario para comprobar si existe el archivo
import time

# Simulamos la función de navegación
def wizard_navigation(total_pages, current_page_key):
    curr = st.session_state[current_page_key]
    c1, c2, c3 = st.columns([1, 3, 1])
    if curr > 0:
        if c1.button("⬅️ Anterior"):
            st.session_state[current_page_key] -= 1
            st.rerun()
    if curr < total_pages - 1:
        if c3.button("Siguiente ➡️"):
            st.session_state[current_page_key] += 1
            st.rerun()

# --- FUNCIONES NUEVAS PARA GESTIONAR CSV ---
CSV_FILE = 'datos_clase.csv'

def guardar_datos_csv(nuevo_dato):
    """Guarda un diccionario como una nueva fila en el CSV"""
    df_nuevo = pd.DataFrame([nuevo_dato])
    
    # Si el archivo no existe, lo creamos con cabeceras.
    # Si existe, añadimos sin cabeceras (mode='a' es append)
    if not os.path.exists(CSV_FILE):
        df_nuevo.to_csv(CSV_FILE, index=False)
    else:
        df_nuevo.to_csv(CSV_FILE, mode='a', header=False, index=False)

def leer_datos_csv():
    """Lee el CSV si existe, si no devuelve DataFrame vacío"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Perfil", "Experiencia", "Sector", "Objetivo"])

def run():
    SESSION_KEY = 'intro_step'
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = 0
    
    # Datos dummy del curso (para pasos posteriores)
    if 'df_main' not in st.session_state:
        data = {
            'Metros': np.random.randint(50, 200, 10),
            'Habitaciones': np.random.randint(1, 5, 10),
            'Zona': np.random.choice(['Norte', 'Sur', 'Capital'], 10),
            'Precio_Venta': np.random.randint(100000, 500000, 10)
        }
        st.session_state['df_main'] = pd.DataFrame(data)

    st.title("Módulo 0: Contextualización del ML")
    
    current_step = st.session_state[SESSION_KEY]
    
    # --- PASO 0: ENCUESTA DEMOGRÁFICA (MODIFICADO CON CSV) ---
    if current_step == 0:
        st.header("0. Conociendo a la 'Data' de la clase")
        st.markdown("""
        Vamos a generar nuestros propios datos. Rellena la encuesta para alimentar el CSV del curso.
        """)
        
        with st.form("encuesta_clase"):
            col1, col2 = st.columns(2)
            with col1:
                perfil = st.selectbox("Perfil principal", 
                                    ["Desarrollador", "Analista", "Estudiante", "Negocio", "Otro"])
                experiencia = st.slider("Nivel Python (0-10)", 0, 10, 3)
            
            with col2:
                sector = st.selectbox("Sector", 
                                    ["Tecnología", "Finanzas", "Salud", "Turismo", "Educación", "Otro"])
                # Convertimos multiselect a string para guardarlo fácil en CSV
                objetivo = st.multiselect("Objetivo", 
                                        ["Aprender a predecir", "Automatizar", "Cambio carrera", "Curiosidad"])
            
            submitted = st.form_submit_button("Enviar mis datos 🚀")
            
            if submitted:
                # Preparamos el dato
                nuevo_registro = {
                    "Perfil": perfil,
                    "Experiencia": experiencia,
                    "Sector": sector,
                    "Objetivo": ", ".join(objetivo) # Unimos lista en string
                }
                # Guardamos en CSV
                guardar_datos_csv(nuevo_registro)
                
                st.success("¡Datos guardados en el archivo local!")
                time.sleep(1) # Pequeña pausa para feedback visual
                st.rerun() # Recargamos para actualizar gráficas abajo
        
        st.markdown("---")
        st.subheader("📊 Datos recopilados hasta ahora")
        
        # Leemos el CSV para mostrar resultados en tiempo real
        df_encuesta = leer_datos_csv()
        
        if not df_encuesta.empty:
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.metric("Total Respuestas", len(df_encuesta))
                st.write("Distribución de Perfiles:")
                st.bar_chart(df_encuesta['Perfil'].value_counts())
            
            with col_b:
                st.dataframe(df_encuesta, use_container_width=True)
                
                # BOTÓN DE EMERGENCIA: Descargar CSV
                # (Muy útil si estás en Streamlit Cloud y no quieres perder los datos al cerrar)
                csv_data = df_encuesta.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Descargar CSV (Backup)",
                    data=csv_data,
                    file_name='datos_clase_backup.csv',
                    mime='text/csv',
                )
        else:
            st.info("Aún no hay datos. ¡Sé el primero en rellenar el formulario!")

    # --- PASO 1: CONCEPTOS PREVIOS ---
    elif current_step == 1:
        st.header("1. La Intuición detrás del Algoritmo")
        
        # Recuperamos los datos de la encuesta para usarlos pedagógicamente
        df_encuesta = leer_datos_csv()
        if not df_encuesta.empty:
            avg_exp = df_encuesta['Experiencia'].mean()
            st.info(f"💡 Dato curioso: La experiencia media en Python de esta clase es de **{avg_exp:.1f}/10**. Un algoritmo usaría este dato para personalizar el nivel de los ejercicios.")

        st.markdown("### Actividad 1.1: El Humano como Modelo")
        # ... (Resto de tu código igual) ...
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("Imagine un piso en **Santa Cruz**, de **90 m²** y **2 habitaciones**.")
            user_guess = st.number_input("¿Qué precio le pondrías? (€)", min_value=50000, max_value=500000, step=5000, value=150000)
        
        with c2:
            st.markdown("#### ¿Qué acabas de hacer?")
            if st.button("Analizar mi pensamiento"):
                st.markdown("""
                Has aplicado un **Modelo Mental** basado en inputs y experiencia.
                🤖 **El Machine Learning automatiza esto.**
                """)

        st.divider()
        st.subheader("Diferencia Clave: Reglas vs. Patrones")
        
        tab1, tab2 = st.tabs(["💻 Programación Tradicional", "🧠 Machine Learning"])
        with tab1:
            st.code("""
            if zona == 'Centro':
                precio = base + 50000
            """, language="python") 
        with tab2:
            st.code("""
            modelo.fit(datos)
            prediccion = modelo.predict(nuevo_caso)
            """, language="python")

    # --- PASO 2: DATASET ---
    elif current_step == 2:
        st.header("2. Nuestra materia prima")
        df = st.session_state['df_main']
        st.dataframe(df.head(5), use_container_width=True)

    # --- PASO 3: CIERRE ---
    elif current_step == 3:
        st.header("3. Próximos Pasos")
        st.success("Fin de la introducción.")

    st.divider()
    wizard_navigation(total_pages=4, current_page_key=SESSION_KEY)

if __name__ == "__main__":
    run()