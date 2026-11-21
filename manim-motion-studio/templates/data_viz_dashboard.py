from manim import (
    BLUE_C,
    DOWN,
    GOLD_C,
    GREEN_C,
    GREY_B,
    LEFT,
    PI,
    PURPLE_B,
    RIGHT,
    TEAL_C,
    UP,
    WHITE,
    AnnularSector,
    Axes,
    BarChart,
    Create,
    FadeIn,
    Scene,
    Text,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    smooth,
)
import numpy as np


class DataVizDashboard(Scene):
    """LaTeX-free animated Axes, BarChart transitions, and live ValueTracker KPI ring."""

    def construct(self):
        title = Text("Analytics Motion Dashboard", font_size=36, weight="BOLD", color=WHITE).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=0.55)

        # 1) Left panel: Animated BarChart (using Text labels so zero LaTeX dependency)
        chart = BarChart(
            values=[24, 52, 38, 66],
            bar_names=["Q1", "Q2", "Q3", "Q4"],
            y_range=[0, 100, 25],
            x_length=5.0,
            y_length=3.6,
            bar_colors=[BLUE_C, TEAL_C, PURPLE_B, GOLD_C],
            x_axis_config={"label_constructor": Text, "font_size": 22},
            y_axis_config={"include_numbers": True, "label_constructor": Text, "font_size": 18},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.35)

        self.play(Create(chart), run_time=1.0)
        self.play(chart.animate.change_bar_values([48, 74, 62, 92]), run_time=1.2, rate_func=smooth)

        # 2) Right panel: Live ValueTracker KPI Gauge + Curve
        kpi = ValueTracker(0.0)
        gauge_center = RIGHT * 3.6 + UP * 1.1

        bg_ring = AnnularSector(
            inner_radius=0.85, outer_radius=1.12, angle=2 * PI, start_angle=PI / 2,
            arc_center=gauge_center, color=GREY_B, fill_opacity=0.22,
        )
        live_ring = always_redraw(
            lambda: AnnularSector(
                inner_radius=0.85,
                outer_radius=1.12,
                angle=-2 * PI * max(0.001, kpi.get_value() / 100.0),
                start_angle=PI / 2,
                arc_center=gauge_center,
                color=TEAL_C,
                fill_opacity=0.95,
            )
        )
        live_num = always_redraw(
            lambda: Text(f"{kpi.get_value():.0f}%", font_size=34, weight="BOLD", color=WHITE).move_to(gauge_center)
        )
        kpi_lbl = Text("Growth Target", font_size=22, color=GREY_B).next_to(bg_ring, DOWN, buff=0.22)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=4.5,
            y_length=2.1,
            axis_config={"include_numbers": False, "label_constructor": Text},
        ).move_to(RIGHT * 3.6 + DOWN * 1.9)
        curve = axes.plot(lambda x: 0.22 * x ** 2 + 0.3, x_range=[0, 3.8], color=GREEN_C, stroke_width=4)
        area = axes.get_area(curve, x_range=[0, 3.8], color=(TEAL_C, GREEN_C), opacity=0.35)

        self.add(bg_ring, live_ring, live_num)
        self.play(FadeIn(kpi_lbl), Create(axes), run_time=0.6)
        self.play(
            kpi.animate.set_value(92.0),
            Create(curve),
            FadeIn(area),
            run_time=1.6,
            rate_func=smooth,
        )
        self.wait(0.6)
