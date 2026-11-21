from manim import (
    BLUE_E,
    DEGREES,
    GOLD_C,
    TEAL_C,
    UL,
    WHITE,
    Create,
    Surface,
    Text,
    ThreeDAxes,
    ThreeDScene,
    Write,
)
import numpy as np


class ThreeDShowcase(ThreeDScene):
    """3D parametric surface with height-mapped colors, ambient orbital camera, and pinned 2D HUD."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES)

        hud_title = Text("3D Wave Surface", font_size=34, weight="BOLD", color=WHITE).to_corner(UL, buff=0.55)
        self.add_fixed_in_frame_mobjects(hud_title)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1.5, 1.5, 0.5],
            axis_config={"include_numbers": False, "label_constructor": Text},
        )
        surface = Surface(
            lambda u, v: axes.c2p(u, v, 0.7 * np.sin(u * 1.4) * np.cos(v * 1.4)),
            u_range=[-2.8, 2.8],
            v_range=[-2.8, 2.8],
            resolution=(28, 28),
            fill_opacity=0.88,
        )
        surface.set_fill_by_value(axes=axes, colorscale=[(BLUE_E, -0.65), (TEAL_C, 0.0), (GOLD_C, 0.65)], axis=2)

        self.play(Write(hud_title), Create(axes), run_time=0.9)
        self.play(Create(surface), run_time=1.4)
        self.begin_ambient_camera_rotation(rate=0.45)
        self.wait(2.2)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=50 * DEGREES, theta=25 * DEGREES, run_time=1.1)
        self.wait(0.4)
