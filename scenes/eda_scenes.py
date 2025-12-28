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
        # --- CONFIGURACIÓN ESCENA ---
        # Eje Y reducido [0, 1] para maximizar altura visual
        ax = Axes(x_range=[-5, 5], y_range=[0, 1], y_length=5, axis_config={"include_tip": False})
        
        # Factor de escala visual
        VISUAL_SCALE = 2.0 
        def normal_pdf(x):
            return (np.exp(-x**2/2) / np.sqrt(2*np.pi)) * VISUAL_SCALE

        # ==========================================
        # 1. FUNCIÓN DE DENSIDAD (EL MAPA)
        # ==========================================
        
        # A. DEFINICIÓN TEXTUAL
        titulo_1 = Text("1. Función de Densidad", font_size=36).to_edge(UP)
        def_1 = Text(
            "Es el 'mapa' teórico. Nos dice qué zonas\nson más probables antes de tener datos.",
            font_size=24, t2c={"mapa": BLUE, "probables": YELLOW}
        ).next_to(titulo_1, DOWN)
        
        self.play(Write(titulo_1))
        self.play(FadeIn(def_1))
        self.wait(3)
        
        # B. VISUALIZACIÓN
        self.play(FadeOut(def_1)) 
        
        subtitulo_visual_1 = Text("Donde la curva es alta, hay más probabilidad.", font_size=20, color=BLUE).next_to(titulo_1, DOWN)
        
        ghost_curve = ax.plot(lambda x: normal_pdf(x), color=BLUE, stroke_opacity=0.6)
        area = ax.get_area(ghost_curve, color=BLUE, opacity=0.1)
        
        self.play(Create(ax), FadeIn(subtitulo_visual_1))
        self.play(Create(ghost_curve), FadeIn(area))
        self.wait(1)


        # ==========================================
        # 2. VARIABLE ALEATORIA (EL PROCESO)
        # ==========================================

        # A. DEFINICIÓN TEXTUAL
        # Usamos FadeOut/FadeIn en lugar de Transform para evitar errores gráficos
        self.play(FadeOut(titulo_1), FadeOut(subtitulo_visual_1))

        titulo_2 = Text("2. Variable Aleatoria (X)", font_size=36).to_edge(UP)
        def_2 = Text(
            "No es un número fijo, es un PROCESO.\nEs el acto de 'tirar el dado' y ver qué sale.",
            font_size=24, t2c={"PROCESO": RED, "ver qué sale": YELLOW}
        ).next_to(titulo_2, DOWN)

        self.play(FadeIn(titulo_2), FadeIn(def_2))
        self.wait(3)

        # B. VISUALIZACIÓN (EL CURSOR)
        self.play(FadeOut(def_2))
        
        subtitulo_visual_2 = Text("Buscando un valor...", font_size=20, color=RED).next_to(titulo_2, DOWN)
        self.play(FadeIn(subtitulo_visual_2))

        # --- ANIMACIÓN DEL CURSOR ---
        cursor = Triangle(color=RED, fill_opacity=1).scale(0.2).rotate(PI)
        cursor_label = Text("X", color=RED, font_size=24).next_to(cursor, UP)
        cursor_group = VGroup(cursor, cursor_label)
        
        cursor_group.move_to(ax.c2p(0, 0.1))
        self.play(FadeIn(cursor_group))

        # Simulación 1: Centro
        self.play(cursor_group.animate.move_to(ax.c2p(-2, 0.1)), rate_func=linear, run_time=0.3)
        self.play(cursor_group.animate.move_to(ax.c2p(2, 0.1)), rate_func=linear, run_time=0.3)
        self.play(cursor_group.animate.move_to(ax.c2p(0.2, 0.1)), rate_func=rate_functions.ease_out_elastic, run_time=1)
        
        linea_prob = DashedLine(ax.c2p(0.2, 0), ax.c2p(0.2, normal_pdf(0.2)), color=YELLOW)
        txt_val = Text("¡Probable!", font_size=18, color=YELLOW).next_to(linea_prob, UP)
        
        self.play(Create(linea_prob), Write(txt_val))
        self.wait(1)
        self.play(FadeOut(linea_prob), FadeOut(txt_val))

        # Simulación 2: Extremo
        self.play(cursor_group.animate.move_to(ax.c2p(-3, 0.1)), rate_func=linear, run_time=0.5)
        self.play(cursor_group.animate.move_to(ax.c2p(-1.8, 0.1)), rate_func=rate_functions.ease_out_bounce, run_time=1)
        
        linea_prob_2 = DashedLine(ax.c2p(-1.8, 0), ax.c2p(-1.8, normal_pdf(-1.8)), color=YELLOW)
        txt_val_2 = Text("¡Raro!", font_size=18, color=YELLOW).next_to(linea_prob_2, UP)

        self.play(Create(linea_prob_2), Write(txt_val_2))
        self.wait(0.5)
        
        # Limpieza antes de la fase 3
        self.play(
            FadeOut(linea_prob_2), 
            FadeOut(txt_val_2), 
            FadeOut(cursor_group), 
            FadeOut(subtitulo_visual_2),
            FadeOut(titulo_2),
            FadeOut(ghost_curve),
            FadeOut(area)
        )
        

        # ==========================================
        # 3. DISTRIBUCIÓN (LA ACUMULACIÓN)
        # ==========================================

        titulo_3 = Text("3. La Máquina de Galton", font_size=36).to_edge(UP)
        subtitulo_3 = Text("Si repetimos el proceso mil veces, emerge la forma.", font_size=20, color=GREEN).next_to(titulo_3, DOWN)
        
        self.play(FadeIn(titulo_3), FadeIn(subtitulo_3))

        # Configuración de pilas
        num_dots = 850  # Cantidad de puntos
        dot_radius = 0.05
        col_spacing = dot_radius * 2.1 
        column_heights = {}
        dots_group = VGroup()
        animations = []

        for _ in range(num_dots):
            raw_x = np.random.normal(0, 1)
            snapped_x = round(raw_x / col_spacing) * col_spacing
            
            count = column_heights.get(snapped_x, 0)
            column_heights[snapped_x] = count + 1
            
            # EL PUNTO NACE ARRIBA
            y_start = 1.0 
            start_point = ax.c2p(raw_x, y_start)
            
            d = Dot(point=start_point, color=YELLOW, radius=dot_radius)
            dots_group.add(d)

            # ATERRIZAJE APILADO
            base_point = ax.c2p(snapped_x, 0)
            vertical_offset = UP * (count * 2 + 1) * dot_radius * 0.95 
            final_point = base_point + vertical_offset

            animations.append(
                Succession(
                    FadeIn(d, run_time=0.05),
                    d.animate.move_to(final_point).set_rate_func(linear)
                )
            )
        
        self.play(LaggedStart(*animations, lag_ratio=0.005, run_time=6))
        self.wait(1)

        # CREAR LA CURVA SÓLIDA VERDE (IMPORTANTE: Esto faltaba antes)
        solid_curve = ax.plot(lambda x: normal_pdf(x), color=GREEN)
        
        # Transición limpia: Los puntos desaparecen y queda la curva ideal
        self.play(
            FadeOut(dots_group), 
            FadeOut(ghost_curve),
            FadeOut(area),
            Create(solid_curve),
            solid_curve.animate.set_fill(GREEN, opacity=0.3)
        )
        self.wait(1)

        # ==========================================
        # 4. EL ZOOLÓGICO DE DISTRIBUCIONES
        # ==========================================
        
        # Limpieza de textos anteriores
        self.play(FadeOut(titulo_3), FadeOut(subtitulo_3))

        t4 = Text("4. Zoo de Distribuciones", font_size=32).to_edge(UP)
        st4 = Text("La forma depende de la naturaleza del fenómeno.", font_size=20, color=GRAY).next_to(t4, DOWN)
        
        self.play(FadeIn(t4), FadeIn(st4))
        
        # Eliminamos la curva verde anterior para empezar limpio el ciclo
        if 'solid_curve' in locals():
            self.remove(solid_curve) 

        # --- A. DISTRIBUCIÓN UNIFORME ---
        # 1. La Curva
        curve_uni = ax.plot(lambda x: 0.7 if -2.5 < x < 2.5 else 0, color=BLUE)
        curve_uni.set_fill(BLUE, opacity=0.3)
        
        # 2. La Ficha Técnica (Info)
        lbl_uni = Text("Uniforme", font_size=28, color=BLUE).move_to(ax.c2p(-3, 0.8))
        
        # Usamos MathTex para la fórmula. La r al principio es vital (raw string).
        info_uni = VGroup(
            VGroup(
                Text("", font_size=20), 
                MathTex(r"f(x) = k", font_size=24, color=BLUE)
            ).arrange(RIGHT, buff=0.2),
            
            VGroup(
                Text("Ej.:", font_size=20), 
                Text("Tirar un dado, Lotería", font_size=20, color=YELLOW)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 1.5)
        
        # Animación
        # Nota: Si solid_curve existe de la escena anterior, úsala en el primer argumento.
        # Si no, usa FadeIn(curve_uni). Asumimos que solid_curve viene del paso 3.
        self.play(
            ReplacementTransform(solid_curve, curve_uni), 
            Write(lbl_uni),
            FadeIn(info_uni)
        )
        self.wait(4)

        curve_exp_line = ax.plot(lambda x: np.exp(-x * 0.6), x_range=[0, 5], color=ORANGE)
        
        # B. El Área (El relleno suave)
        # get_area calcula matemáticamente el polígono entre la curva y el eje X
        curve_exp_area = ax.get_area(curve_exp_line, x_range=[0, 5], color=ORANGE, opacity=0.3)
        
        # C. Grupo (Para que actúen como un solo objeto en la animación)
        # Este 'curve_exp' reemplaza al objeto único que tenías antes
        curve_exp = VGroup(curve_exp_line, curve_exp_area)
        
        # 2. LA INFO (Ficha técnica con LaTeX)
        lbl_exp = Text("Exponencial", font_size=28, color=ORANGE).move_to(ax.c2p(2.5, 0.8))
        
        info_exp = VGroup(
            VGroup(
                Text("Fórmula:", font_size=20), 
                MathTex(r"f(x) = \lambda e^{-\lambda x}", font_size=24, color=ORANGE)
            ).arrange(RIGHT, buff=0.2),
            
            VGroup(
                Text("Ej:", font_size=20), 
                Text("Tiempo espera bus / Radiactividad", font_size=20, color=YELLOW)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 1.5)
        
        # 3. ANIMACIÓN
        self.play(
            ReplacementTransform(lbl_uni, lbl_exp),
            ReplacementTransform(info_uni, info_exp),
            # Transformamos la curva uniforme en el NUEVO GRUPO (Línea + Área)
            ReplacementTransform(curve_uni, curve_exp)
        )
        self.wait(4)

        # --- C. DISTRIBUCIÓN BIMODAL ---
        # 1. La Curva
        curve_bi = ax.plot(lambda x: 0.7*np.exp(-(x+2.5)**2) + 0.7*np.exp(-(x-2.5)**2), color=PURPLE)
        curve_bi.set_fill(PURPLE, opacity=0.3)
        
        # 2. La Info
        lbl_bi = Text("Bimodal", font_size=28, color=PURPLE).move_to(ax.c2p(0, 0.4))
        
        info_bi = VGroup(
            VGroup(
                Text("", font_size=20), 
                MathTex(r"f(x) \approx N(\mu_1) + N(\mu_2)", font_size=24, color=PURPLE)
            ).arrange(RIGHT, buff=0.2),
            
            VGroup(
                Text("Ej.", font_size=20), 
                Text("Población mixta", font_size=20, color=YELLOW)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 1.5)
        
        # Animación
        self.play(
            ReplacementTransform(curve_exp, curve_bi), 
            ReplacementTransform(lbl_exp, lbl_bi),
            ReplacementTransform(info_exp, info_bi) # Corregido: transformamos info_uni -> info_bi si info_exp dio error
        )

        self.wait(4)

# --- ACTO 3: EL BALANCÍN (MEDIA) (Sin cambios) ---
class Acto3_Media(Scene):
    def construct(self):

        number_line = NumberLine(
            x_range=[0, 16, 1], 
            length=12, 
            include_numbers=True, 
            font_size=20
        ).shift(DOWN * 1)
        
        self.play(Create(number_line))

        # ==========================================
        # 1. LA MEDIA (EL EQUILIBRIO)
        # ==========================================
        
        titulo_1 = Text("1. La Media (El Equilibrio)", font_size=36).to_edge(UP)
        # Fórmula con LaTeX
        formula_media = MathTex(r"\mu = \frac{\sum x_i}{N}", font_size=32, color=YELLOW).next_to(titulo_1, DOWN)
        
        self.play(Write(titulo_1), FadeIn(formula_media))

        # A. Datos Iniciales (Simétricos y compactos)
        datos = [6, 7, 8, 9, 10] # Media = 8
        bolas = VGroup(*[Dot(number_line.n2p(x), color=BLUE, radius=0.15).shift(UP*0.5) for x in datos])
        
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN) for b in bolas], lag_ratio=0.1))
        
        # B. El Punto de Apoyo (Fulcrum) en la media (8)
        mean_val = np.mean(datos)
        fulcrum = Triangle(color=YELLOW, fill_opacity=1).scale(0.2).rotate(PI)
        fulcrum.move_to(number_line.n2p(mean_val) + DOWN*0.2) # Debajo de la línea
        
        lbl_mu = MathTex(r"\mu", color=YELLOW).next_to(fulcrum, DOWN)
        
        self.play(FadeIn(fulcrum), Write(lbl_mu))
        self.wait(1)

        # C. El Outlier (El desequilibrio)
        # Añadimos un dato muy lejano (15)
        outlier_val = 15
        outlier = Dot(number_line.n2p(outlier_val), color=RED, radius=0.15).shift(UP*0.5)
        
        # Animación de entrada impactante
        self.play(FadeIn(outlier, scale=0.5))
        self.play(outlier.animate.set_color(RED)) # Destacar que es diferente
        
        # Cálculo de la nueva media
        nuevos_datos = datos + [outlier_val]
        nueva_media = np.mean(nuevos_datos) # (40 + 15) / 6 = 9.16
        
        # D. La Reacción Física
        # Texto explicativo
        txt_sensible = Text("¡La media es sensible!", font_size=24, color=RED).next_to(number_line, UP).shift(UP*1.5)
        
        self.play(
            fulcrum.animate.move_to(number_line.n2p(nueva_media) + DOWN*0.2),
            lbl_mu.animate.next_to(number_line.n2p(nueva_media) + DOWN*0.2, DOWN),
            Write(txt_sensible),
            run_time=2
        )
        self.wait(2)

        # ==========================================
        # 2. LA MEDIANA (EL ORDEN)
        # ==========================================
        
        # Limpieza: Quitamos todo lo específico de la media
        self.play(
            FadeOut(fulcrum), FadeOut(lbl_mu), FadeOut(txt_sensible), 
            FadeOut(formula_media), FadeOut(titulo_1), FadeOut(outlier)
        )
        
        # Título Mediana
        titulo_2 = Text("2. La Mediana (El Centro)", font_size=36).to_edge(UP)
        formula_mediana = MathTex(r"Me = x_{(n+1)/2}", font_size=32, color=GREEN).next_to(titulo_2, DOWN)
        
        self.play(Write(titulo_2), FadeIn(formula_mediana))
        
        # A. Colorear las bolas existentes (volvemos a los 5 datos originales)
        # Datos: 6, 7, 8, 9, 10. Mediana = 8 (Tercer elemento)
        
        # Parte Izquierda (Rojo)
        grupo_izq = VGroup(bolas[0], bolas[1]) # 6, 7
        # Parte Derecha (Azul)
        grupo_der = VGroup(bolas[3], bolas[4]) # 9, 10
        # Mediana (Verde)
        bola_mediana = bolas[2] # 8
        
        self.play(
            grupo_izq.animate.set_color(RED),
            grupo_der.animate.set_color(BLUE),
            bola_mediana.animate.set_color(GREEN).scale(1.5)
        )
        
        lbl_me = Text("Mediana", font_size=20, color=GREEN).next_to(bola_mediana, UP)
        self.play(FadeIn(lbl_me))
        self.wait(1)
        
        # B. Añadir el Outlier de nuevo
        # Ahora tenemos 6 datos: 6, 7, 8, 9, 10, 15
        # La mediana cae entre 8 y 9 (8.5).
        # Visualmente, la mediana "se mueve" al hueco entre 8 y 9.
        
        self.play(FadeIn(outlier)) # Vuelve el outlier rojo (es parte del grupo derecho ahora)
        
        # Nueva coloración lógica
        # Izquierda: 6, 7, 8 (3 bolas) -> Rojos
        # Derecha: 9, 10, 15 (3 bolas) -> Azules
        # Mediana: En medio de 8 y 9
        
        # Flecha indicando la nueva mediana
        flecha_mediana = Arrow(start=UP, end=DOWN, color=GREEN).next_to(number_line.n2p(8.5), UP)
        lbl_me_new = Text("Nueva Mediana", font_size=20, color=GREEN).next_to(flecha_mediana, UP)

        self.play(
            bola_mediana.animate.set_color(RED).scale(1/1.5), # El 8 pasa a ser izquierda
            bolas[3].animate.set_color(BLUE), # El 9 es derecha
            outlier.animate.set_color(BLUE),  # El 15 es derecha
            FadeOut(lbl_me),
            GrowArrow(flecha_mediana),
            Write(lbl_me_new)
        )
        
        txt_robusta = Text("¡Apenas se mueve!", font_size=24, color=GREEN).move_to(UP*2)
        self.play(Write(txt_robusta))
        self.wait(2)

        # ==========================================
        # 3. DESVIACIÓN ESTÁNDAR (LA DISTANCIA)
        # ==========================================
        
        # Limpieza
        self.play(
            FadeOut(titulo_2), FadeOut(formula_mediana), FadeOut(grupo_izq), FadeOut(grupo_der), 
            FadeOut(bola_mediana), FadeOut(outlier), FadeOut(flecha_mediana), FadeOut(lbl_me_new), FadeOut(txt_robusta)
        )

        titulo_3 = Text("3. Desviación Estándar (Dispersión)", font_size=36).to_edge(UP)
        formula_sigma = MathTex(r"\sigma = \sqrt{\frac{\sum(x_i - \mu)^2}{N}}", font_size=32, color=ORANGE).next_to(titulo_3, DOWN)
        
        self.play(Write(titulo_3), FadeIn(formula_sigma))
        
        # A. Caso 1: Poca Dispersión (Datos juntos)
        datos_baja = [7, 8, 9] # Media 8
        bolas_baja = VGroup(*[Dot(number_line.n2p(x), color=YELLOW, radius=0.15).shift(UP*0.5) for x in datos_baja])
        
        self.play(FadeIn(bolas_baja))
        
        # Dibujar líneas de distancia a la media (8)
        lineas = VGroup()
        for x in datos_baja:
            l = Line(number_line.n2p(x)+UP*0.5, number_line.n2p(8)+UP*0.5, color=ORANGE)
            lineas.add(l)
            
        self.play(Create(lineas))
        lbl_baja = Text("Poca distancia = Sigma baja", font_size=24, color=ORANGE).next_to(bolas_baja, UP, buff=0.5)
        self.play(Write(lbl_baja))
        self.wait(2)
        
        # B. Caso 2: Mucha Dispersión (Datos lejos)
        self.play(FadeOut(bolas_baja), FadeOut(lineas), FadeOut(lbl_baja))
        
        datos_alta = [4, 8, 12] # Media 8
        bolas_alta = VGroup(*[Dot(number_line.n2p(x), color=YELLOW, radius=0.15).shift(UP*0.5) for x in datos_alta])
        
        self.play(FadeIn(bolas_alta))
        
        lineas_alta = VGroup()
        for x in datos_alta:
            l = Line(number_line.n2p(x)+UP*0.5, number_line.n2p(8)+UP*0.5, color=ORANGE)
            lineas_alta.add(l)
            
        self.play(Create(lineas_alta))
        lbl_alta = Text("Mucha distancia = Sigma alta", font_size=24, color=ORANGE).next_to(bolas_alta, UP, buff=1)
        self.play(Write(lbl_alta))
        self.wait(2)

        # ==========================================
        # 4. TRANSICIÓN A LA DISTRIBUCIÓN
        # ==========================================
        
        self.play(FadeOut(titulo_3), FadeOut(formula_sigma), FadeOut(bolas_alta), FadeOut(lineas_alta), FadeOut(lbl_alta), FadeOut(number_line))
        
        txt_final = Text("Cuando tenemos miles de bolas...", font_size=32).move_to(ORIGIN)
        self.play(Write(txt_final))
        self.wait(1)
        
        # Morphing visual a la curva (simulado)
        # Dibujamos ejes y curva rápidamente
        ax_small = Axes(x_range=[-3, 3], y_range=[0, 1], y_length=3, x_length=6).shift(DOWN*0.5)
        curve_small = ax_small.plot(lambda x: np.exp(-x**2/2), color=BLUE)
        
        self.play(
            Transform(txt_final, Text("...emerge la Distribución", font_size=32).to_edge(UP)),
            Create(ax_small), 
            Create(curve_small)
        )
        self.wait(2)

        self.play(
            FadeOut(txt_final),
            FadeOut(curve_small)
        )

        # --- CONFIGURACIÓN DE EJES ---
        # Eje Y reducido para maximizar altura
        ax = Axes(x_range=[-5, 7], y_range=[0, 1], y_length=5, axis_config={"include_tip": False})
        
        # Función auxiliar para la normal visualmente escalada
        VISUAL_SCALE = 2.0 
        def get_pdf(x, mu=0, sigma=1):
            return (np.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * np.sqrt(2*np.pi))) * VISUAL_SCALE

        # ==========================================
        # 1. TENDENCIA CENTRAL: LA MEDIA (EL BALANCÍN)
        # ==========================================
        
        titulo_1 = Text("Ahora en nuestra distribución la media:", font_size=36).to_edge(UP)
        formula_media = MathTex(r"\mu = \frac{\sum x_i}{N}", font_size=32, color=YELLOW).next_to(titulo_1, DOWN)
        
        self.play(Write(titulo_1), FadeIn(formula_media))
        self.play(Transform(ax_small, ax))

        # A. La Distribución Simétrica (El "Peso")
        curve = ax.plot(lambda x: get_pdf(x), color=BLUE)
        area = ax.get_area(curve, color=BLUE, opacity=0.3)
        self.play(Create(curve), FadeIn(area))

        # B. El Punto de Apoyo (Fulcrum)
        fulcrum = Triangle(color=YELLOW, fill_opacity=1).scale(0.2).rotate(PI)
        fulcrum.move_to(ax.c2p(0, -0.1)) # Justo debajo del 0
        
        lbl_fulcrum = Text("Punto de Equilibrio", font_size=20, color=YELLOW).next_to(fulcrum, DOWN)
        
        self.play(FadeIn(fulcrum), Write(lbl_fulcrum))
        self.wait(1)

        # C. El Evento Disruptivo (El Outlier)
        # Una bola roja pesada cae lejos a la derecha
        outlier_val = 5
        outlier = Dot(ax.c2p(outlier_val, 1), color=RED, radius=0.15)
        lbl_outlier = Text("Outlier (Dato extremo)", font_size=20, color=RED).next_to(outlier, UP)
        
        self.play(FadeIn(outlier), Write(lbl_outlier))
        self.play(outlier.animate.move_to(ax.c2p(outlier_val, 0)), rate_func=rate_functions.ease_out_bounce)
        
        # D. La Reacción Física
        # Texto de advertencia
        txt_tilt = Text("¡Desequilibrio!", font_size=24, color=RED).move_to(ax.c2p(2.5, 0.5))
        self.play(Write(txt_tilt))
        
        # Para recuperar el equilibrio, la media debe desplazarse hacia el peso
        # Simulamos visualmente el desplazamiento (exagerado para efecto didáctico)
        new_mean_x = 1.5 
        
        self.play(
            fulcrum.animate.move_to(ax.c2p(new_mean_x, -0.1)),
            lbl_fulcrum.animate.next_to(ax.c2p(new_mean_x, -0.1), DOWN),
            FadeOut(txt_tilt)
        )
        
        txt_sensitive = Text("La Media es SENSIBLE", font_size=24, color=YELLOW).next_to(curve, UP).shift(RIGHT*2)
        self.play(Write(txt_sensitive))
        self.wait(2)

        # ==========================================
        # 2. TENDENCIA CENTRAL: LA MEDIANA (LA CUCHILLA)
        # ==========================================
        
        # Limpieza parcial: Quitamos fulcrum y textos de media, dejamos curva y outlier
        self.play(
            FadeOut(fulcrum), FadeOut(lbl_fulcrum), FadeOut(txt_sensitive), FadeOut(formula_media),
            FadeOut(titulo_1)
        )

        titulo_2 = Text("La Cuchilla (La Mediana)", font_size=36).to_edge(UP)
        formula_mediana = MathTex(r"Mediana = 50\% \text{ Área}", font_size=32, color=GREEN).next_to(titulo_2, DOWN)
        
        self.play(Write(titulo_2), FadeIn(formula_mediana))

        # A. La Cuchilla
        # La mediana en una normal pura está en 0. 
        # Con el outlier en 5, la mediana apenas se mueve (quizás a 0.1)
        knife = DashedLine(ax.c2p(0.1, 0), ax.c2p(0.1, 1), color=GREEN, stroke_width=5)
        lbl_knife = Text("Corta 50/50", font_size=20, color=GREEN).next_to(knife, UP)
        
        self.play(Create(knife), Write(lbl_knife))
        self.wait(1)

        # B. Comparación
        # Mostramos dónde quedó la media (fantasma)
        ghost_mean = Triangle(color=YELLOW, fill_opacity=0.5).scale(0.2).rotate(PI).move_to(ax.c2p(new_mean_x, -0.1))
        lbl_ghost = Text("Media", font_size=16, color=YELLOW).next_to(ghost_mean, DOWN)
        
        self.play(FadeIn(ghost_mean), FadeIn(lbl_ghost))
        
        txt_robust = Text("La Mediana es ROBUSTA", font_size=24, color=GREEN).move_to(ax.c2p(-3, 0.5))
        self.play(Write(txt_robust))
        self.wait(3)

        # ==========================================
        # 3. DISPERSIÓN: LA RESPIRACIÓN (SIGMA)
        # ==========================================
        
        # Limpieza Total
        self.play(
            FadeOut(titulo_2), FadeOut(formula_mediana), FadeOut(knife), FadeOut(lbl_knife),
            FadeOut(ghost_mean), FadeOut(lbl_ghost), FadeOut(txt_robust),
            FadeOut(outlier), FadeOut(lbl_outlier), FadeOut(curve), FadeOut(area)
        )

        titulo_3 = Text("La distribución 'respira' según la desviación", font_size=36).to_edge(UP)
        # Fórmula de sigma visual
        formula_sigma = MathTex(r"\sigma \to \text{Anchura}", font_size=32, color=ORANGE).next_to(titulo_3, DOWN)
        
        self.play(Write(titulo_3), FadeIn(formula_sigma))

        # A. Curva Estándar
        curve_base = ax.plot(lambda x: get_pdf(x, sigma=1), color=BLUE)
        area_base = ax.get_area(curve_base, color=BLUE, opacity=0.3)
        self.play(Create(curve_base), FadeIn(area_base))
        
        # Dibujar Sigma (Línea desde el centro al punto de inflexión)
        # En una normal N(0,1), el punto de inflexión está en x=1
        center_line = DashedLine(ax.c2p(0,0), ax.c2p(0, get_pdf(0)), color=WHITE, stroke_opacity=0.5)
        sigma_line = Arrow(ax.c2p(0, get_pdf(1)), ax.c2p(1, get_pdf(1)), color=ORANGE, buff=0)
        lbl_sigma = MathTex(r"\sigma = 1", color=ORANGE, font_size=24).next_to(sigma_line, UP)
        
        self.play(Create(center_line), GrowArrow(sigma_line), Write(lbl_sigma))
        self.wait(1)

        # ESTADO 1: INHALAR (Preciso / Estrecho)
        curve_narrow = ax.plot(lambda x: get_pdf(x, sigma=0.5), color=BLUE)
        area_narrow = ax.get_area(curve_narrow, color=BLUE, opacity=0.3)
        # Flecha corta
        arrow_narrow = Arrow(ax.c2p(0, get_pdf(0.5, sigma=0.5)), ax.c2p(0.5, get_pdf(0.5, sigma=0.5)), color=ORANGE, buff=0)
        lbl_narrow = MathTex(r"\sigma = 0.5 \text{ (Preciso)}", color=ORANGE, font_size=24).next_to(arrow_narrow, RIGHT)

        # ESTADO 2: EXHALAR (Ruidoso / Ancho)
        curve_wide = ax.plot(lambda x: get_pdf(x, sigma=2.0), color=BLUE)
        area_wide = ax.get_area(curve_wide, color=BLUE, opacity=0.3)
        # Flecha larga
        arrow_wide = Arrow(ax.c2p(0, get_pdf(2, sigma=2)), ax.c2p(2, get_pdf(2, sigma=2)), color=ORANGE, buff=0)
        lbl_wide = MathTex(r"\sigma = 2.0 \text{ (Ruidoso)}", color=ORANGE, font_size=24).next_to(arrow_wide, UP)

        # --- BUCLE DE RESPIRACIÓN (5 VECES) ---
        for i in range(5):
            # 1. Inhalar (Se hace estrecha)
            self.play(
                Transform(curve_base, curve_narrow),
                Transform(area_base, area_narrow),
                Transform(sigma_line, arrow_narrow),
                Transform(lbl_sigma, lbl_narrow),
                run_time=1.5,
                rate_func=rate_functions.ease_in_out_sine # Movimiento suave
            )
            
            # 2. Exhalar (Se aplasta)
            self.play(
                Transform(curve_base, curve_wide),
                Transform(area_base, area_wide),
                Transform(sigma_line, arrow_wide),
                Transform(lbl_sigma, lbl_wide),
                run_time=1.5,
                rate_func=rate_functions.ease_in_out_sine # Movimiento suave
            )
            
        self.wait(1)

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