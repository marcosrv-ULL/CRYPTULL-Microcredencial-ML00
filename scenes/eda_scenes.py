from manim import *
import numpy as np

# --- ACTO 1: LA VARIABLE (Sin cambios, incluido por contexto) ---
from manim import *
import numpy as np

class Acto1_Variable(Scene):
    def construct(self):
        # --- PARTE 1: DEFINICIÓN Y TABLA ---
        
        # 1. Título y Definición
        titulo_p1 = Text("¿Qué es una Variable?", font_size=48).to_edge(UP)
        definicion = Text(
            "Es una característica medible que cambia\n(fluctúa) entre diferentes sujetos.",
            font_size=32, t2c={"cambia": YELLOW}
        )
        
        self.play(Write(titulo_p1))
        self.play(FadeIn(definicion))
        self.wait(3) # Pausa para leer
        self.play(FadeOut(definicion))

        # 2. La Tabla de Datos (DataFrame)
        # Creamos una tabla manual simple
        header = VGroup(
            Text("ID", font_size=24), 
            Text("Peso (X1)", font_size=24, color=BLUE), 
            Text("Altura (X2)", font_size=24, color=BLUE), 
            Text("Especie (Y)", font_size=24, color=RED)
        ).arrange(RIGHT, buff=1)
        
        row1 = VGroup(
            Text("001", font_size=24), 
            Text("15.2", font_size=24), 
            Text("5.2", font_size=24), 
            Text("A", font_size=24)
        ).arrange(RIGHT, buff=1).next_to(header, DOWN, buff=0.5)
        
        # Alineamos columnas manualmente para que quede bonito
        for i in range(4):
            row1[i].match_x(header[i])

        tabla_grupo = VGroup(header, row1).move_to(ORIGIN)
        rect_tabla = SurroundingRectangle(tabla_grupo, color=WHITE, buff=0.3)
        
        self.play(Create(rect_tabla), Write(header), Write(row1))
        self.wait(1)

        # 3. Explicación X vs Y
        txt_features = Text("Variables Independientes (X)\nCaracterísticas", font_size=24, color=BLUE)
        txt_features.next_to(rect_tabla, UP).shift(LEFT*2)
        
        txt_target = Text("Variable Objetivo (Y)\nLo que predecimos", font_size=24, color=RED)
        txt_target.next_to(rect_tabla, UP).shift(RIGHT*2)

        # Señalar X
        frame_x = SurroundingRectangle(VGroup(header[1], row1[2]), color=BLUE)
        self.play(Create(frame_x), FadeIn(txt_features))
        self.wait(2)

        # Señalar Y
        frame_y = SurroundingRectangle(VGroup(header[3], row1[3]), color=RED)
        self.play(ReplacementTransform(frame_x, frame_y), FadeOut(txt_features), FadeIn(txt_target))
        self.wait(2)

        # Limpiar escena para pasar a la animación física
        # Nos quedamos con el valor "5.2" de la altura
        valor_destacado = row1[2].copy() # El valor 5.2
        self.play(
            FadeOut(header), FadeOut(row1), FadeOut(rect_tabla), 
            FadeOut(frame_y), FadeOut(txt_target), FadeOut(titulo_p1),
            valor_destacado.animate.move_to(ORIGIN).scale(1.5)
        )
        self.wait(1)

        # --- PARTE 2: VARIABLE CONTINUA ---
        
        # Configuración ejes
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 2], axis_config={"include_numbers": True}, y_length=2)
        titulo_p2 = Text("1. Variable Continua", font_size=36, color=YELLOW).to_edge(UP)
        subtitulo_p2 = Text("Puede tomar infinitos valores (decimales)", font_size=24).next_to(titulo_p2, DOWN)

        self.play(
            Transform(valor_destacado, Dot(ax.c2p(5.2, 2), color=YELLOW)), # Transformamos el número en punto
            Create(ax),
            Write(titulo_p2)
        )
        self.play(Write(subtitulo_p2))
        
        # Referencia al objeto dot
        dot = valor_destacado 
        
        # Animación de caída precisa
        self.play(dot.animate.move_to(ax.c2p(5.2, 0)), run_time=1.5, rate_func=rate_functions.ease_in_elastic)
        
        label_val = Text("Valor exacto: 5.2", font_size=20).next_to(dot, UP)
        self.play(Write(label_val))
        self.wait(2)
        
        # Demostrar el concepto de infinito: Moverse suavemente
        self.play(
            dot.animate.shift(RIGHT * 0.5),
            run_time=1
        )
        label_val2 = Text("5.721...", font_size=20).next_to(dot, UP)
        self.play(Transform(label_val, label_val2))
        self.wait(2)

        # --- PARTE 3: VARIABLE DISCRETA ---
        
        self.play(FadeOut(label_val), FadeOut(dot), FadeOut(subtitulo_p2))
        
        titulo_p3 = Text("2. Variable Discreta", font_size=36, color=BLUE).to_edge(UP)
        subtitulo_p3 = Text("El valor debe 'encajar' en una categoría o entero", font_size=24).next_to(titulo_p3, DOWN)
        
        self.play(Transform(titulo_p2, titulo_p3), Write(subtitulo_p3))

        rects = VGroup()
        labels_cajas = VGroup()
        
        # CAMBIO AQUÍ: Centramos las cajas en el valor entero
        for i in range(10):
            # Caja
            rect = Rectangle(height=1, width=ax.x_axis.unit_size, color=BLUE, fill_opacity=0.2)
            
            # ANTES: ax.c2p(i + 0.5, 0.5) -> Se dibujaba entre i e i+1
            # AHORA: ax.c2p(i, 0.5)       -> Se dibuja centrada en i
            rect.move_to(ax.c2p(i, 0.5))
            
            rects.add(rect)
            
            # Etiqueta de la caja (bucket)
            lbl = Text(str(i), font_size=16).move_to(rect.get_center())
            labels_cajas.add(lbl)
            
        texto_contenedor = Text("Contenedores (Buckets)", font_size=24, color=BLUE).next_to(rects, UP)
        
        self.play(Create(rects), FadeIn(labels_cajas), FadeIn(texto_contenedor))
        self.wait(1)

        # Animación: Intento fallido y corrección
        # Ahora 5.5 es EXACTAMENTE el borde entre la caja 5 y la caja 6
        # (Caja 5 va de 4.5 a 5.5 / Caja 6 va de 5.5 a 6.5)
        # ... (Código previo de las cajas) ...

        # Animación: El dato intenta ser continuo pero es forzado a ser discreto
        
        # 1. Aparición e incertidumbre
        dot_d = Dot(ax.c2p(5.5, 2), color=RED)
        lbl_intento = Text("¿Valor 5.5?", font_size=20, color=RED).next_to(dot_d, UP)
        
        self.play(FadeIn(dot_d), Write(lbl_intento))
        
        # 2. Cae justo en la frontera (la grieta entre 5 y 6)
        self.play(dot_d.animate.move_to(ax.c2p(5.5, 1))) 
        self.wait(0.5)

        # 3. EXPLICACIÓN DE LA REGLA (Paso nuevo)
        # Transformamos la pregunta en una afirmación de la regla
        lbl_regla = Text("Frontera: Redondeamos arriba", font_size=18, color=ORANGE).next_to(texto_contenedor, UP)
        
        self.play(ReplacementTransform(lbl_intento, lbl_regla))
        self.wait(1.5) # Pausa para que lean la regla

        # 4. Resbala al centro de la caja 6
        lbl_final = Text("Categoría/entero 6", font_size=20, color=YELLOW).next_to(rects[6], UP)
        
        self.play(
            dot_d.animate.move_to(rects[6].get_center()), # Se mueve físicamente al centro
            FadeOut(lbl_regla),                           # Desaparece la regla
            Transform(texto_contenedor, lbl_final)        # Cambia el título general por la etiqueta final
        )
        
        self.wait(3)

# ==========================================
# --- ACTO 2: LA DISTRIBUCIÓN (CORREGIDO) ---
# ==========================================
class Acto2_Distribucion(Scene):
    def construct(self):
        # Aumentamos un poco el rango Y para dejar espacio a la pila
        ax = Axes(x_range=[-4, 4], y_range=[0, 1.5], y_length=4) 
        titulo = Text("Del Caos al Orden (Acumulación)", font_size=36).to_edge(UP)
        self.play(Create(ax), Write(titulo))
        
        # Configuración de las bolas
        num_dots = 200  # Más bolas para ver mejor la forma
        dot_radius = 0.05
        # Espaciado horizontal entre columnas (un poco más que el diámetro)
        col_spacing = dot_radius * 2.2 

        # Diccionario para controlar la altura de cada columna
        # clave: posición X ajustada, valor: contador de bolas en esa columna
        column_heights = {}

        dots = VGroup()
        animations = []

        # Generación de la lluvia de datos
        for _ in range(num_dots):
            # 1. Generar X aleatoria
            raw_x = np.random.normal(0, 1)

            # 2. "Ajustar" la X a la columna más cercana para que se apilen rectos
            snapped_x = round(raw_x / col_spacing) * col_spacing

            # 3. Obtener la altura actual de esta columna
            count = column_heights.get(snapped_x, 0)
            column_heights[snapped_x] = count + 1

            # 4. Crear la bola arriba (usamos raw_x para que la caída parezca natural)
            start_point = ax.c2p(raw_x, 1.5) 
            d = Dot(point=start_point, color=YELLOW, radius=dot_radius, fill_opacity=0.8)
            dots.add(d)

            # 5. Calcular el punto de aterrizaje físico
            # Punto base en el suelo (eje X) en la posición ajustada
            base_point = ax.c2p(snapped_x, 0)
            
            # Desplazamiento vertical físico basado en cuántas bolas hay debajo.
            # (count * 2 + 1) * radius coloca el centro de la bola a la altura correcta.
            # Multiplicamos por 1.05 para dejar un pequeño hueco visual entre bolas.
            vertical_offset = UP * (count * 2 + 1) * dot_radius * 1.05
            
            final_point = base_point + vertical_offset

            # Crear la animación de caída hacia el punto final calculado
            animations.append(d.animate.move_to(final_point))
        
        # Ejecutar la caída aleatoria con retraso (lag)
        self.play(LaggedStart(*animations, lag_ratio=0.02, run_time=6, rate_func=linear))
        self.wait(1)
        
        # La forma emergente (Curva teórica)
        # Ajustamos la altura de la curva para que coincida visualmente con la pila
        scale_factor = 0.8 # Factor de escala visual para la curva
        curve = ax.plot(lambda x: scale_factor * np.exp(-x**2/2) / np.sqrt(2*np.pi), color=BLUE)
        
        self.play(FadeOut(dots), Create(curve))
        self.play(curve.animate.set_fill(BLUE, opacity=0.3))
        self.wait(2)

# --- ACTO 3: EL BALANCÍN (MEDIA) (Sin cambios) ---
class Acto3_Media(Scene):
    def construct(self):
        # Configuración inicial
        linea = NumberLine(x_range=[-5, 15, 1], length=12, include_numbers=True)
        linea.shift(UP * 0.5)
        
        # Datos iniciales (simétricos)
        datos = [4, 5, 6]
        bolas = VGroup(*[Dot(linea.n2p(x), color=BLUE, radius=0.2).shift(UP*0.3) for x in datos])
        
        # El triángulo (Media)
        media_val = np.mean(datos)
        fulcrum = Triangle(color=WHITE, fill_opacity=1).scale(0.2).rotate(PI)
        fulcrum.move_to(linea.n2p(media_val) + DOWN*0.3)
        lbl_mu = Text("Media").next_to(fulcrum, DOWN)
        
        self.add(linea, bolas, fulcrum, lbl_mu)
        self.wait(1)
        
        # Aparece el Outlier
        outlier = Dot(linea.n2p(14), color=RED, radius=0.25).shift(UP*0.3)
        self.play(FadeIn(outlier))
        
        # Cálculo nueva media
        nuevos_datos = datos + [14]
        nueva_media = np.mean(nuevos_datos)
        
        # Animación del re-equilibrio
        self.play(
            fulcrum.animate.move_to(linea.n2p(nueva_media) + DOWN*0.3),
            lbl_mu.animate.next_to(linea.n2p(nueva_media) + DOWN*0.3, DOWN),
            run_time=2
        )
        self.wait(2)

# --- ACTO 4: DISPERSIÓN (Sin cambios) ---
class Acto4_Dispersion(Scene):
    def construct(self):
        ax = Axes(x_range=[-5, 5], y_range=[0, 1], axis_config={"include_tip": False})
        titulo = Text("Incertidumbre (Desviación Estándar)", font_size=36).to_edge(UP)
        
        # Usamos una función auxiliar para generar curvas con diferente sigma
        # Añadimos un factor de escala visual (1.2) para que se vea bien en pantalla
        def get_curve(sigma):
            return ax.plot(lambda x: 1.2 * (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5 * (x/sigma)**2), color=GREEN)
        
        curve_normal = get_curve(1)
        area = ax.get_area(curve_normal, color=GREEN, opacity=0.3)
        label = Text("σ = 1", color=GREEN).next_to(curve_normal, UP)
        
        self.play(Create(ax), Write(titulo))
        self.play(Create(curve_normal), FadeIn(area), Write(label))
        self.wait(1)
        
        # Respiración: Poca incertidumbre (Estrecha)
        curve_narrow = get_curve(0.5)
        self.play(
            Transform(curve_normal, curve_narrow),
            Transform(label, Text("σ = 0.5 (Preciso)", color=GREEN).next_to(curve_narrow, UR)),
            run_time=2
        )
        self.wait(1)
        
        # Respiración: Mucha incertidumbre (Ancha)
        curve_wide = get_curve(2.0)
        self.play(
            Transform(curve_normal, curve_wide),
            Transform(label, Text("σ = 2.0 (Incierto)", color=GREEN).next_to(curve_wide, UP)),
            run_time=2
        )
        self.wait(2)