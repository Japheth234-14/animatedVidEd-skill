"""Zero-LaTeX template covering Code blocks, Tables, Vector Fields, Matrix Transforms & Callouts."""

import numpy as np
from manim import *


class MathCodeDiagramsShowcase(Scene):
    def construct(self):
        self.camera.background_color = "#0D1117"

        header = Text("Code, Vector Fields & Matrices", font_size=34, weight="BOLD", color=WHITE).to_edge(UP, buff=0.35)
        self.play(Write(header), run_time=0.7)

        # 1. Code block + Table side-by-side
        code = Code(
            code_string="def transform(v):\n    return [[2, 1], [0, 1]] @ v",
            language="python",
            background="window",
            formatter_style="monokai",
        ).scale(0.68).to_edge(LEFT, buff=0.55).shift(UP * 0.9)

        table = Table(
            [["Determinant", "2.0"], ["Shear", "+1.0"], ["Trace", "3.0"]],
            include_outer_lines=True,
            element_to_mobject_config={"font_size": 24},
        ).scale(0.65).to_edge(RIGHT, buff=0.6).shift(UP * 0.9)

        box = SurroundingRectangle(code, color="#38B2AC", corner_radius=0.1, buff=0.12)
        brace = Brace(table, DOWN, color="#F6AD55")
        brace_lbl = Text("Linear Operator Stats", font_size=22, color="#F6AD55").next_to(brace, DOWN, buff=0.1)

        self.play(FadeIn(code, shift=RIGHT * 0.3), Create(table), run_time=1.1)
        self.play(Create(box), GrowFromCenter(brace), FadeIn(brace_lbl), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(code, table, box, brace, brace_lbl)), run_time=0.5)

        # 2. NumberPlane Matrix Transform + Vector Field
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": "#2D3748", "stroke_width": 1.5},
        ).scale(0.82).shift(DOWN * 0.3)

        vec_field = ArrowVectorField(
            lambda p: np.array([-p[1], p[0], 0]) * 0.35,
            x_range=[-4, 4, 1.0],
            y_range=[-2, 2, 1.0],
        )

        self.play(Create(plane), Create(vec_field), run_time=1.0)
        self.play(plane.animate.apply_matrix([[1.4, 0.5], [0.0, 0.9]]), run_time=1.4)
        self.wait(0.5)
