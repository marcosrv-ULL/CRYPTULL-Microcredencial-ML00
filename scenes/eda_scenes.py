from manim import *
import numpy as np

# --- ACTO 1: LA VARIABLE ---
class Acto1_Variable(Scene):
    def construct(self):
        # 1. Lienzo Vacío
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 2], axis_config={"include_numbers": True}, y_length=2)
        titulo = Text("La Variable: El Contenedor", font_size=36).to_edge(UP)
        
        self.play(Create(ax), Write(titulo))
        
        # 2. La Caída (Continuo)
        val = 5.2
        dot = Dot(ax.c2p(val, 0), color=YELLOW)
        dot.move_to(ax.c2p(val, 2)) # Empezar arriba
        label = Text(f"Valor = {val}", font_size=24).next_to(dot, UP)
        
        self.play(dot.animate.move_to(ax.c2p(val, 0)), run_time=1, rate_func=linear)
        self.play(Write(label))
        self.wait(1)
        
        # 3. Transformación a Discreto (Buckets)
        self.play(FadeOut(label), FadeOut(dot))
        
        rects = VGroup()
        for i in range(10):
            rect = Rectangle(height=1, width=ax.x_axis.unit_size, color=BLUE)
            rect.move_to(ax.c2p(i + 0.5, 0.5))
            rects.add(rect)
            
        texto_discreto = Text("Variable Discreta (Cajas)", font_size=24, color=BLUE).next_to(rects, UP)
        
        self.play(Create(rects), FadeIn(texto_discreto))
        
        # Bola intentando caer en medio y resbalando
        dot_d = Dot(ax.c2p(5.5, 2), color=RED) # Cae en 5.5
        self.play(FadeIn(dot_d))
        self.play(dot_d.animate.move_to(ax.c2p(5.5, 1))) # Cae al borde
        self.play(dot_d.animate.move_to(ax.c2p(6.0, 0.5))) # Resbala al centro del bucket 6
        
        self.wait(2)

# --- ACTO 2: LA DISTRIBUCIÓN ---
class Acto2_Distribucion(Scene):
    def construct(self):
        ax = Axes(x_range=[-4, 4], y_range=[0, 1])
        titulo = Text("Del Caos al Orden", font_size=36).to_edge(UP)
        self.play(Create(ax), Write(titulo))
        
        # Lluvia de datos (Simulada visualmente)
        dots = VGroup()
        for _ in range(50):
            x = np.random.normal(0, 1)
            d = Dot(ax.c2p(x, 0), color=YELLOW, radius=0.05, fill_opacity=0.6)
            d.shift(UP * 3) # Empezar arriba
            dots.add(d)
        
        # Caída aleatoria
        self.play(LaggedStart(*[d.animate.move_to(ax.c2p(d.get_center()[0], 0)) for d in dots], lag_ratio=0.01, run_time=3))
        self.wait(1)
        
        # La forma emergente
        curve = ax.plot(lambda x: np.exp(-x**2/2) / np.sqrt(2*np.pi), color=BLUE)
        self.play(FadeOut(dots), Create(curve))
        self.play(curve.animate.set_fill(BLUE, opacity=0.3))
        self.wait(2)

# --- ACTO 3: EL BALANCÍN (MEDIA) ---
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

# --- ACTO 4: DISPERSIÓN ---
class Acto4_Dispersion(Scene):
    def construct(self):
        ax = Axes(x_range=[-5, 5], y_range=[0, 1], axis_config={"include_tip": False})
        titulo = Text("Incertidumbre (Desviación Estándar)", font_size=36).to_edge(UP)
        
        def get_curve(sigma):
            return ax.plot(lambda x: (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5 * (x/sigma)**2), color=GREEN)
        
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