import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt

# --- ESTILOS CSS PERSONALIZADOS (Opcional, para dar toque 'libro') ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
    }
    .step-container {
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE NAVEGACIÓN Y UTILIDADES ---

def wizard_navigation(total_pages, current_page_key):
    """Barra de navegación inferior tipo Wizard"""
    curr = st.session_state[current_page_key]
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 4, 1])
    
    if curr > 0:
        if c1.button("« Anterior"):
            st.session_state[current_page_key] -= 1
            st.rerun()
            
    # Indicador de progreso visual
    progress = (curr + 1) / total_pages
    c2.progress(progress, text=f"Paso {curr + 1} de {total_pages}")
    
    if curr < total_pages - 1:
        if c3.button("Siguiente »"):
            st.session_state[current_page_key] += 1
            st.rerun()

# --- GESTIÓN DE DATOS CSV ---
CSV_FILE = 'datos_clase.csv'

def guardar_datos_csv(nuevo_dato):
    """Guarda un diccionario como una nueva fila en el CSV"""
    df_nuevo = pd.DataFrame([nuevo_dato])
    if not os.path.exists(CSV_FILE):
        df_nuevo.to_csv(CSV_FILE, index=False)
    else:
        df_nuevo.to_csv(CSV_FILE, mode='a', header=False, index=False)

def leer_datos_csv():
    """Lee el CSV si existe, si no devuelve DataFrame vacío con estructura"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Perfil", "Experiencia", "Sector", "Objetivo"])

# --- LÓGICA DE LA DINÁMICA '¿ES ML O NO?' ---
def render_is_it_ml_game():
    """Renderiza el juego de preguntas con estado persistente"""
    st.subheader("🧩 Actividad: ¿Es Machine Learning o Programación Tradicional?")
    st.markdown("Analiza las siguientes situaciones y decide. ¿Hay un algoritmo aprendiendo de datos o son reglas fijas?")

    # Definimos los casos: (Pregunta, Es_ML (bool), Explicación)
    scenarios = [
        {
            "id": "spam",
            "title": "Filtro de Spam de Gmail",
            "desc": "El sistema analiza millones de correos marcados por usuarios para decidir si un nuevo email es basura.",
            "is_ml": True,
            "explanation": "Exacto. No hay una lista fija de palabras prohibidas; el sistema aprende patrones complejos basándose en lo que la gente marca como spam."
        },
        {
            "id": "excel",
            "title": "Suma en Excel",
            "desc": "Escribes =SUMA(A1:A10) y obtienes el resultado total.",
            "is_ml": False,
            "explanation": "Correcto. Es una regla determinista. Siempre que le des los mismos números, dará el mismo resultado siguiendo una instrucción fija programada por un humano."
        },
        {
            "id": "netflix",
            "title": "Recomendaciones de Netflix",
            "desc": "Te sugiere películas basándose en lo que has visto tú y usuarios similares a ti.",
            "is_ml": True,
            "explanation": "¡Sí! El algoritmo encuentra patrones de gusto ocultos entre millones de usuarios para predecir qué te gustará."
        },
        {
            "id": "traffic",
            "title": "Semáforo por Temporizador",
            "desc": "Un semáforo cambia a rojo cada 60 segundos exactos, sin importar el tráfico.",
            "is_ml": False,
            "explanation": "Exacto. Es un sistema automatizado, pero no 'aprende'. Sigue una regla de tiempo fija programada explícitamente."
        }
    ]

    # Inicializamos estado de respuestas si no existe
    if 'quiz_answers' not in st.session_state:
        st.session_state['quiz_answers'] = {}

    # Renderizamos cada escenario en una tarjeta
    for sc in scenarios:
        with st.container():
            st.markdown(f"#### 🔹 {sc['title']}")
            st.write(sc['desc'])
            
            # Verificar si ya se respondió
            user_ans = st.session_state['quiz_answers'].get(sc['id'])
            
            if user_ans is None:
                c1, c2 = st.columns(2)
                if c1.button("🤖 Es Machine Learning", key=f"ml_{sc['id']}"):
                    st.session_state['quiz_answers'][sc['id']] = True
                    st.rerun()
                if c2.button("💻 Es Programación Tradicional", key=f"trad_{sc['id']}"):
                    st.session_state['quiz_answers'][sc['id']] = False
                    st.rerun()
            else:
                # Mostrar resultado
                is_correct = (user_ans == sc['is_ml'])
                if is_correct:
                    st.success(f"✅ ¡Correcto! {sc['explanation']}")
                else:
                    st.error(f"❌ Vaya... {sc['explanation']}")
            st.divider()

# --- APP PRINCIPAL ---
def run():
    SESSION_KEY = 'intro_step'
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = 0
    
    # Generar datos dummy si no existen (para paso 2)
    if 'df_main' not in st.session_state:
        data = {
            'Metros': np.random.randint(50, 200, 10),
            'Habitaciones': np.random.randint(1, 5, 10),
            'Zona': np.random.choice(['Norte', 'Sur', 'Capital'], 10),
            'Precio_Venta': np.random.randint(100000, 500000, 10)
        }
        st.session_state['df_main'] = pd.DataFrame(data)

    #st.title("📘 Módulo 0: Contextualización del ML")
    
    current_step = st.session_state[SESSION_KEY]
    
    # --- PASO 0: ENCUESTA ---
    if current_step == 0:
        st.header("0. Conociendo a la 'Data' de la clase")
        #st.info("👋 ¡Bienvenido! Antes de empezar a hablar de datos, vamos a generarlos. Tu perfil nos ayudará a entender cómo funciona un modelo.")
        
        with st.form("encuesta_clase"):
            col1, col2 = st.columns(2)
            with col1:
                perfil = st.selectbox("Perfil principal", 
                                    ["Desarrollador/a", "Analista", "Estudiante", "Negocio", "Otro"])
                experiencia = st.slider("Nivel Python (0-10)", 0, 10, 3)
            
            with col2:
                sector = st.selectbox("Sector", 
                                    ["Tecnología", "Finanzas", "Salud", "Turismo", "Educación", "Otro"])
                objetivo = st.multiselect("Objetivo", 
                                        ["Aprender a predecir", "Automatizar", "Cambio carrera", "Curiosidad"])
            
            submitted = st.form_submit_button("Enviar datos")
            
            if submitted:
                nuevo_registro = {
                    "Perfil": perfil,
                    "Experiencia": experiencia,
                    "Sector": sector,
                    "Objetivo": ", ".join(objetivo)
                }
                guardar_datos_csv(nuevo_registro)
                st.toast("¡Datos guardados correctamente!", icon="💾")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Datos recopilados en tiempo real")
        df_encuesta = leer_datos_csv()
        
        if not df_encuesta.empty:
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.metric("Total Alumnado", len(df_encuesta))
                st.caption("Distribución por Perfil:")
                st.bar_chart(df_encuesta['Perfil'].value_counts())
            with col_b:
                st.dataframe(df_encuesta, use_container_width=True, height=200)
        else:
            st.warning("Aún no hay datos. ¡Sé el/la primer@ en rellenar el formulario!")

    # --- PASO 1: INTUICIÓN (Incluye la nueva actividad) ---
    elif current_step == 1:
        st.header("1. La Intuición detrás del Algoritmo")
        
        # Uso pedagógico de los datos recolectados
        df_encuesta = leer_datos_csv()
        if not df_encuesta.empty:
            avg_exp = df_encuesta['Experiencia'].mean()
            st.success(f"💡 **Insight de la clase:** La experiencia media en Python es de **{avg_exp:.1f}/10**. Un algoritmo de ML usaría este dato para, por ejemplo, recomendar automáticamente ejercicios más fáciles o difíciles.")

        # 1.1 El Humano como Modelo
        st.markdown("### 1.1 El Humano como Modelo")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/512/263/263115.png", width=100) # Icono casa
            st.markdown("Piso en **Santa Cruz**, **90 m²**, **2 habs**.")
            st.number_input("Estima el precio (€)", 50000, 500000, 150000, step=5000)
        
        with c2:
            st.info("""
            **¿Qué acaba de pasar en tu cerebro?**
            1. Has tomado **Datos de entrada** (zona, metros).
            2. Has aplicado **Reglas internas** basadas en tu experiencia (entrenamiento).
            3. Has generado una **Predicción** (precio).
            
            🤖 **El Machine Learning es simplemente automatizar este proceso a gran escala.**
            """)

        st.markdown("---")
        
        # 1.2 NUEVA ACTIVIDAD: ¿Es ML o no?
        render_is_it_ml_game()

        st.markdown("---")
        
        # 1.3 Diferencia Clave (Código)
        st.subheader("1.2 La Diferencia Técnica")
        st.markdown("¿Cómo se ve esto en código?")
        
        tab1, tab2 = st.tabs(["Programación Tradicional", "Machine Learning"])
        with tab1:
            st.markdown("**Nosotros escribimos las reglas.** Si cambia la situación, tenemos que reescribir el código.")
            st.code("""
            def calcular_precio(zona, metros):
                # REGLAS EXPLÍCITAS (Programadas por humano)
                precio_base = 100000
                if zona == 'Centro':
                    precio_base += 50000
                if metros > 100:
                    precio_base += 20000
                return precio_base
            """, language="python") 
        with tab2:
            st.markdown("**El algoritmo encuentra las reglas.** Nosotros solo le damos los datos (Input) y las respuestas correctas (Output).")
            st.code("""
            # EL ALGORITMO APRENDE SOLO
            from sklearn.linear_model import LinearRegression
            
            modelo = LinearRegression()
            
            # Le enseñamos ejemplos (Entrenamiento)
            modelo.fit(datos_casas, precios_reales)
            
            # Él deduce la fórmula matemática interna
            prediccion = modelo.predict(nuevo_piso)
            """, language="python")

    # --- PASO 2: DATASET ---
    elif current_step == 2:
        st.header("2. Nuestra materia prima: El Dataset")
        st.markdown("Para que el 'mago' (algoritmo) aprenda, necesita libros de hechizos (datos).")
        st.markdown("Este es un ejemplo de cómo se ven los datos que usaremos en el curso:")
        
        df = st.session_state['df_main']
        st.dataframe(df, use_container_width=True)
        
        st.caption("Fíjate que tenemos características (Metros, Habitaciones) y una etiqueta objetivo (Precio_Venta) que queremos predecir.")

    # --- PASO 3: EDA (Análisis Exploratorio) ---
    elif current_step == 3:
        st.header("3. EDA: El arte de 'cotillear' los datos")
        st.markdown("""
        Antes de lanzar algoritmos, debemos entender qué tenemos delante. El EDA (**Exploratory Data Analysis**) 
        consiste en visualizar y limpiar.
        
        **¡Prueba tú mismo!** Usa el gráfico interactivo abajo para buscar relaciones en nuestros datos de casas.
        """)
        
        df = st.session_state['df_main']
        
        # Controles para el gráfico
        c1, c2 = st.columns(2)
        ejex = c1.selectbox("Eje X", df.columns[:-1], index=0) # Quitamos Precio de X
        ejey = c2.selectbox("Eje Y", ["Precio_Venta"], disabled=True) # Fijamos Y para simplificar
        
        # Gráfico interactivo simple
        st.scatter_chart(df, x=ejex, y='Precio_Venta', color='Zona')
        
        st.info("🔍 **Fíjate:** ¿Ves como al aumentar los Metros (Eje X) suele subir el Precio? Eso es una **correlación positiva**.")
    elif current_step == 4:
        st.header("4. Aprendizaje Supervisado: Clasificación")
        st.markdown("""
        En el aprendizaje supervisado, enseñamos al modelo con ejemplos que ya tienen la respuesta (etiqueta).
        
        Imagina que tenemos dos tipos de clientes:
        * 🔴 **Rojos:** No compran
        * 🔵 **Azules:** Sí compran
        
        **TU MISIÓN:** Ajusta la recta para separar los dos grupos lo mejor posible.
        """)
        
        # 1. Generar datos sintéticos (solo si no existen para no cambiarlos al mover el slider)
        if 'blobs_X' not in st.session_state:
            # Grupo 1 (Rojos) centrado en (2, 2)
            x1 = np.random.normal(2, 0.8, (20, 2))
            # Grupo 2 (Azules) centrado en (6, 6)
            x2 = np.random.normal(6, 0.8, (20, 2))
            st.session_state['blobs_X'] = np.concatenate([x1, x2])
            st.session_state['blobs_y'] = np.array([0]*20 + [1]*20) # 0: Rojo, 1: Azul

        X = st.session_state['blobs_X']
        y = st.session_state['blobs_y']

        # 2. Controles de la recta (Usuario)
        col_control, col_viz = st.columns([1, 2])
        
        with col_control:
            st.markdown("### 🎛️ Controles del 'Modelo'")
            m = st.slider("Pendiente (Inclinación)", -5.0, 5.0, -1.0, step=0.1)
            b = st.slider("Intersección (Altura)", -10.0, 20.0, 10.0, step=0.5)
            
            st.caption("Estás modificando los parámetros matemáticos: $y = mx + b$")

        # 3. Lógica de visualización y cálculo de error
        with col_viz:
            fig, ax = plt.subplots(figsize=(6, 4))
            
            # Dibujar puntos
            ax.scatter(X[y==0, 0], X[y==0, 1], c='red', label='No Compra (0)')
            ax.scatter(X[y==1, 0], X[y==1, 1], c='blue', label='Compra (1)')
            
            # Dibujar recta del usuario
            x_vals = np.array([0, 10])
            y_vals = m * x_vals + b
            ax.plot(x_vals, y_vals, '--k', linewidth=2, label='Tu Modelo')
            
            # Calcular cuántos están mal clasificados (Visualmente: por debajo/encima de la recta)
            # Asumimos: Por encima de la recta = Azul (Clase 1), Por debajo = Rojo (Clase 0)
            y_pred = (X[:, 1] > m * X[:, 0] + b).astype(int)
            errores = np.sum(y != y_pred)
            total = len(y)
            acc = ((total - errores) / total) * 100
            
            # Ajustes visuales
            ax.set_xlim(0, 9)
            ax.set_ylim(0, 9)
            ax.legend(loc='lower right')
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
        
        # Feedback inmediato
        if errores == 0:
            st.balloons()
            st.success(f"🏆 **¡PERFECTO!** Precisión: {acc}% (0 errores). Has encontrado el patrón exacto.")
        else:
            st.warning(f"⚠️ **Resultados:** Tienes {errores} puntos en el lado equivocado. Precisión: {acc}%. ¡Sigue ajustando!")
    # --- PASO 5: NO SUPERVISADO (Clustering) ---
    elif current_step == 5:
        st.header("5. Aprendizaje No Supervisado")
        st.markdown("""
        ¿Qué pasa si **no tenemos etiquetas**? ¿Si nadie nos dice qué es rojo o azul?
        
        Aquí el algoritmo actúa como un explorador: busca grupos (**clusters**) por similitud.
        """)
        
        X = st.session_state['blobs_X'] # Usamos los mismos puntos de antes
        
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown("#### 1. Lo que ve el humano")
            st.markdown("Vemos puntos y nuestra intuición dice: 'Ahí hay dos grupos'.")
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            ax1.scatter(X[:, 0], X[:, 1], c='gray', alpha=0.6)
            ax1.set_title("Datos sin etiquetas")
            st.pyplot(fig1)
            
        with c2:
            st.markdown("#### 2. Lo que hace el algoritmo")
            mostrar_clusters = st.checkbox("✨ Ejecutar K-Means (Algoritmo)")
            
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            if mostrar_clusters:
                # Simulamos el resultado de K-Means (que coincidiría con la realidad en este caso fácil)
                ax2.scatter(X[:20, 0], X[:20, 1], c='orange', label='Grupo A')
                ax2.scatter(X[20:, 0], X[20:, 1], c='purple', label='Grupo B')
                ax2.set_title("Patrones detectados")
                st.caption("El algoritmo los ha separado por cercanía.")
            else:
                ax2.text(4, 4, "?", fontsize=50, ha='center')
                ax2.set_xlim(0, 9)
                ax2.set_ylim(0, 9)
            
            st.pyplot(fig2)

    # --- PASO 6: EVALUACIÓN ---
    elif current_step == 6:
        st.header("6. ¿Cómo sabemos si el modelo es bueno?")
        st.markdown("""
        No basta con que 'parezca' que funciona. Necesitamos **métricas**.
        La más básica es la **Accuracy** (Exactitud): ¿Qué porcentaje acertaste?
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Aciertos", value="38", delta="✅ Bien")
        with col2:
            st.metric(label="Fallos", value="2", delta="- ⚠️ Mal", delta_color="inverse")
        with col3:
            st.metric(label="Accuracy Global", value="95%")
            
        st.progress(0.95)
        
        st.info("""
        Pero ojo... si predecimos cáncer, ¿es igual de grave un **Falso Positivo** (susto) que un **Falso Negativo** (no detectar la enfermedad)? 
        En el curso veremos métricas avanzadas para esto (Precision, Recall, F1-Score).
        """)
    elif current_step == 7:
        st.balloons()
        st.header("¡Bloque 0 Completado!")
        st.markdown("""
        ### Resumen:
        1. **Los datos son el combustible**: Sin datos de calidad (como los de vuestra encuesta), no hay magia.
        2. **No todo es IA**: Si puedes escribir una regla fija (`if x > 10`), probablemente no necesites Machine Learning.
        3. **Patrones vs Reglas**: El ML brilla cuando las reglas son demasiado complejas para escribirlas a mano (como detectar spam o una cara).
        
        **En el próximo bloque:** Empezaremos a mancharnos las manos analizando datos reales (EDA).
        """)
        st.success("Puedes cerrar esta pestaña o reiniciar el módulo.")
        if st.button("Reiniciar Módulo"):
            st.session_state[SESSION_KEY] = 0
            st.rerun()

    # Navegación
    wizard_navigation(total_pages=8, current_page_key=SESSION_KEY)

if __name__ == "__main__":
    run()