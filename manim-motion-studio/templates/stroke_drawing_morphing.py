from manim import (
    BLUE_C,
    DOWN,
    GOLD_C,
    GREY_B,
    LEFT,
    PI,
    PURPLE_B,
    RIGHT,
    TEAL_C,
    UP,
    WHITE,
    Circle,
    Create,
    DrawBorderThenFill,
    FadeOut,
    Homotopy,
    NumberPlane,
    RoundedRectangle,
    Scene,
    ShowPassingFlash,
    Star,
    Text,
    Transform,
    TransformMatchingShapes,
    VMobject,
    Write,
    rate_functions,
)
import numpy as np


class StrokeMorphShowcase(Scene):
    """Demonstrates Bezier stroke drawing, passing flash, shape morphs, matching-shape text morphs, and Homotopy."""

    def construct(self):
        # 1) Custom Bezier stroke-by-stroke reveal + passing light pulse
        header = Text("Stroke Drawing & Morphing", font_size=36, weight="BOLD", color=WHITE).to_edge(UP, buff=0.55)
        self.play(Write(header), run_time=0.6)

        bezier = VMobject(color=GOLD_C, stroke_width=5)
        bezier.start_new_path(LEFT * 3.8 + DOWN * 0.6)
        bezier.add_cubic_bezier_curve_to(LEFT * 1.8 + UP * 2.1, RIGHT * 1.4 + DOWN * 2.2, RIGHT * 3.8 + UP * 0.7)

        self.play(Create(bezier), run_time=1.25, rate_func=rate_functions.ease_in_out_sine)
        self.play(ShowPassingFlash(bezier.copy().set_color(WHITE).set_stroke(width=9), time_width=0.35), run_time=0.85)
        self.play(FadeOut(bezier), run_time=0.35)

        # 2) Shape Morph Chain (Circle -> RoundedRectangle -> Star)
        shape = Circle(radius=1.35, color=TEAL_C, fill_opacity=0.35, stroke_width=4)
        rect = RoundedRectangle(corner_radius=0.35, width=2.8, height=2.2, color=PURPLE_B, fill_opacity=0.35, stroke_width=4)
        star = Star(n=5, outer_radius=1.65, color=GOLD_C, fill_opacity=0.45, stroke_width=4)

        self.play(DrawBorderThenFill(shape), run_time=0.8)
        self.play(Transform(shape, rect, path_arc=PI / 3), run_time=0.95)
        self.play(Transform(shape, star, path_arc=-PI / 3), run_time=0.95)
        self.play(FadeOut(shape, scale=0.8), run_time=0.35)

        # 3) Matching-Shapes Anagram Morph
        w1 = Text("LISTEN", font_size=72, weight="BOLD", color=BLUE_C)
        w2 = Text("SILENT", font_size=72, weight="BOLD", color=TEAL_C)
        self.play(Write(w1), run_time=0.7)
        self.play(TransformMatchingShapes(w1, w2, path_arc=PI / 2), run_time=1.0)
        self.play(FadeOut(w2), run_time=0.35)

        # 4) Space-Time Homotopy Grid Warp
        grid = NumberPlane(
            x_range=[-4.5, 4.5, 1],
            y_range=[-2.3, 2.3, 1],
            background_line_style={"stroke_color": BLUE_C, "stroke_width": 2, "stroke_opacity": 0.75},
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * 0.3)
        grid.prepare_for_nonlinear_transform()

        def wave_warp(x, y, z, t):
            return np.array([x, y + 0.45 * np.sin(x * 1.2 + 2.0 * PI * t) * np.sin(PI * t), z])

        self.play(Create(grid), run_time=0.75)
        self.play(Homotopy(wave_warp, grid), run_time=1.6)
        self.wait(0.4)
