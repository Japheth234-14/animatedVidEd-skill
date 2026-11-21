from manim import (
    BLUE_C,
    BLUE_E,
    DOWN,
    GREY_A,
    GREY_B,
    LEFT,
    PINK,
    PURPLE_B,
    RIGHT,
    TEAL_C,
    UL,
    UP,
    WHITE,
    YELLOW,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    LaggedStart,
    MarkupText,
    MoveAlongPath,
    MovingCameraScene,
    Rectangle,
    Restore,
    RoundedRectangle,
    ShowPassingFlash,
    Text,
    TracedPath,
    VGroup,
    VMobject,
    Write,
    rate_functions,
    smooth,
)
import numpy as np


def make_glow(mobject: VMobject, color=TEAL_C, layers: int = 5, base_width: float = 3.0) -> VGroup:
    """Stack soft wide strokes behind a bright core stroke for a neon bloom effect."""
    glow = VGroup()
    for i in range(layers, 0, -1):
        layer = mobject.copy()
        layer.set_fill(opacity=0)
        layer.set_stroke(color=color, width=base_width + i * 5.5, opacity=0.12 + 0.10 * (layers - i) / layers)
        glow.add(layer)
    core = mobject.copy().set_fill(opacity=0).set_stroke(color=WHITE, width=base_width, opacity=1.0)
    return VGroup(*glow, core)


class MotionGraphicsShowcase(MovingCameraScene):
    """Demonstrates kinetic typography, glowing strokes, lower thirds, and smooth camera panning/zooming."""

    def construct(self):
        self.camera.frame.save_state()

        # Subtle background parallax particle field
        rng = np.random.default_rng(42)
        bg_dots = VGroup(
            *[
                Dot(
                    point=[rng.uniform(-7.5, 7.5), rng.uniform(-4.5, 4.5), 0],
                    radius=rng.uniform(0.02, 0.055),
                    color=BLUE_E,
                ).set_opacity(rng.uniform(0.25, 0.7))
                for _ in range(45)
            ]
        )
        bg_dots.set_z_index(-2)
        self.add(bg_dots)

        # 1) Kinetic Headline Reveal
        headline = Text("MOTION GRAPHICS", font_size=64, weight="BOLD", gradient=(TEAL_C, BLUE_C, PURPLE_B))
        subtitle = MarkupText(
            'Camera Rigs · <span fgcolor="#FACC15"><b>60 FPS</b></span> · Glow Layers',
            font_size=28,
            color=GREY_A,
        ).next_to(headline, DOWN, buff=0.35)

        self.play(
            LaggedStart(
                *[FadeIn(ch, shift=UP * 0.35, scale=0.82) for ch in headline],
                lag_ratio=0.04,
            ),
            run_time=1.0,
            rate_func=rate_functions.ease_out_back,
        )
        self.play(Write(subtitle), run_time=0.65)
        self.wait(0.25)

        # 2) Transition headline out while sliding in a Feature Card + Glowing Signal Curve
        self.play(FadeOut(headline, shift=UP * 0.4), FadeOut(subtitle, shift=UP * 0.4), run_time=0.45)

        card = RoundedRectangle(corner_radius=0.25, width=6.2, height=3.4, fill_color="#0F172A", fill_opacity=0.92, stroke_color=BLUE_C, stroke_width=2.5)
        card.shift(RIGHT * 2.2 + UP * 0.4)
        card_label = Text("Signal Velocity", font_size=28, weight="BOLD", color=WHITE).move_to(card.get_top() + DOWN * 0.45)

        wave = VMobject()
        xs = np.linspace(-2.4, 2.4, 80)
        pts = [card.get_center() + np.array([x, 0.65 * np.sin(2.4 * x) - 0.15, 0]) for x in xs]
        wave.set_points_smoothly(pts)
        glow_wave = make_glow(wave, color=TEAL_C, layers=4, base_width=2.8)

        # Animated pulse dot following the curve + camera zoom
        pulse_dot = Dot(pts[0], color=YELLOW, radius=0.09)
        trail = TracedPath(pulse_dot.get_center, stroke_color=YELLOW, stroke_width=3, dissipating_time=0.45)

        self.play(FadeIn(card, scale=0.92), Write(card_label), run_time=0.6, rate_func=rate_functions.ease_out_expo)
        self.play(Create(glow_wave[-1]), FadeIn(glow_wave[:-1]), run_time=0.85)
        self.add(trail, pulse_dot)

        # Camera punches into the feature card + subtle parallax shift on bg_dots
        self.play(
            self.camera.frame.animate.scale(0.62).move_to(card),
            bg_dots.animate.shift(LEFT * 0.4),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_expo,
        )
        self.play(
            MoveAlongPath(pulse_dot, wave),
            ShowPassingFlash(wave.copy().set_color(PINK).set_stroke(width=7), time_width=0.35),
            run_time=1.0,
        )

        # 3) Reset camera and display animated lower third
        self.play(
            Restore(self.camera.frame),
            bg_dots.animate.shift(RIGHT * 0.4),
            run_time=0.85,
            rate_func=smooth,
        )

        accent = Rectangle(width=0.11, height=1.0, fill_color=TEAL_C, fill_opacity=1, stroke_width=0)
        lt_name = Text("Manim Studio", font_size=32, weight="BOLD", color=WHITE)
        lt_role = Text("Programmatic Motion Engine", font_size=20, color=GREY_B).next_to(lt_name, DOWN, aligned_edge=LEFT, buff=0.08)
        lt_grp = VGroup(accent, VGroup(lt_name, lt_role).next_to(accent, RIGHT, buff=0.22)).to_corner(UL, buff=0.65)

        self.play(GrowFromEdge(accent, DOWN), run_time=0.3)
        self.play(
            LaggedStart(FadeIn(lt_name, shift=RIGHT * 0.35), FadeIn(lt_role, shift=RIGHT * 0.35), lag_ratio=0.18),
            run_time=0.55,
        )
        self.wait(0.6)
