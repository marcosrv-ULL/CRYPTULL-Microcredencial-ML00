from manim import *
import numpy as np

class ScatterPlotScene(Scene):
    def construct(self):
        title = Text("Correlación Positiva", font_size=36).to_edge(UP)
        axes = Axes(x_range=[0, 10], y_range=[0, 10], axis_config={"include_numbers": True})
        
        # Puntos simulando correlación
        x_vals = np.linspace(1, 9, 15)
        y_vals = x_vals + np.random.normal(0, 0.5, 15)
        dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in zip(x_vals, y_vals)])
        
        line = axes.plot(lambda x: x, color=RED)
        
        self.play(Write(title), Create(axes))
        self.play(FadeIn(dots, lag_ratio=0.1))
        self.wait(1)
        self.play(Create(line), run_time=2)
        self.wait(2)