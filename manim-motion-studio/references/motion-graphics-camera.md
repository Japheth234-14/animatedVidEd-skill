# Motion Graphics & Camera Effects in Manim

## 1. Camera Rigging (`MovingCameraScene` & `ZoomedScene`)

Inherit from `MovingCameraScene` instead of `Scene` to pan, zoom, rotate, and track subjects using `self.camera.frame`.

### Pan, Zoom & Reset

```python
from manim import *

class CameraRigExample(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()  # Save default 16:9 framing

        card = RoundedRectangle(corner_radius=0.25, width=4.5, height=2.6, color=BLUE_C)
        title = Text("Feature Card", font_size=34).move_to(card)
        group = VGroup(card, title).shift(RIGHT * 3.5 + UP * 1.2)
        self.add(group)

        # Smooth punch-in onto target object (scale(0.55) = ~1.8x zoom)
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(group),
            run_time=1.1,
            rate_func=rate_functions.ease_in_out_expo,
        )
        # Return cleanly to full view
        self.play(Restore(self.camera.frame), run_time=0.9, rate_func=smooth)
```

### Auto-Follow Subject (`add_updater`)

Pin the camera smoothly onto a moving dot or particle:

```python
dot = Dot(color=YELLOW).shift(LEFT * 4)
trail = TracedPath(dot.get_center, stroke_color=YELLOW_A, stroke_width=3)
self.add(trail, dot)

def follow_dot(frame):
    # Smooth exponential damping toward dot position
    frame.move_to(0.85 * frame.get_center() + 0.15 * dot.get_center())

self.camera.frame.add_updater(follow_dot)
self.play(dot.animate.shift(RIGHT * 8 + UP * 1.5), run_time=2.5, rate_func=smooth)
self.camera.frame.remove_updater(follow_dot)
```

### Picture-in-Picture Magnifier (`ZoomedScene`)

Use `ZoomedScene` to show a crisp zoomed inset window linked to a region of interest:

```python
class MagnifierExample(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(
            zoom_factor=0.32,
            zoomed_display_height=2.4,
            zoomed_display_width=3.6,
            zoomed_camera_config={"default_frame_stroke_width": 2.5},
            **kwargs,
        )

    def construct(self):
        detail = VGroup(*[Dot(radius=0.05, color=TEAL).shift(RIGHT * i * 0.18) for i in range(-4, 5)])
        self.add(detail)
        self.zoomed_camera.frame.move_to(detail)
        self.zoomed_display.to_corner(UR)
        self.activate_zooming(animate=True)
        self.play(self.zoomed_camera.frame.animate.shift(RIGHT * 0.6), run_time=1.5)
```

---

## 2. Kinetic Typography & Lower Thirds

Use `Text` (with `weight="BOLD"`, `gradient=(...)`) or `MarkupText` (Pango HTML-style spans) + `LaggedStart` for crisp character/word cascades:

```python
headline = Text("MOTION GRAPHICS", font_size=64, weight="BOLD", gradient=(CYAN, BLUE_C, PURPLE_B))
sub = MarkupText('Built with <span fgcolor="#FACC15"><b>Manim</b></span> at 60 FPS', font_size=28)
sub.next_to(headline, DOWN, buff=0.35)

# Letter-by-letter cascade with elastic/expo pop
self.play(
    LaggedStart(
        *[FadeIn(ch, shift=UP * 0.35, scale=0.85) for ch in headline],
        lag_ratio=0.045,
        run_time=1.0,
        rate_func=rate_functions.ease_out_back,
    )
)
self.play(Write(sub), run_time=0.7)
```

### Clean Animated Lower Third

```python
accent_bar = Rectangle(width=0.12, height=1.1, fill_color=TEAL_C, fill_opacity=1, stroke_width=0)
name_txt = Text("Ada Lovelace", font_size=34, weight="BOLD")
role_txt = Text("Creative Technologist", font_size=22, color=GREY_B).next_to(name_txt, DOWN, aligned_edge=LEFT, buff=0.1)
text_blk = VGroup(name_txt, role_txt).next_to(accent_bar, RIGHT, buff=0.25)
lower_third = VGroup(accent_bar, text_blk).to_corner(DL, buff=0.7)

self.play(GrowFromEdge(accent_bar, DOWN), run_time=0.35)
self.play(
    LaggedStart(
        FadeIn(name_txt, shift=RIGHT * 0.4),
        FadeIn(role_txt, shift=RIGHT * 0.4),
        lag_ratio=0.18,
    ),
    run_time=0.6,
)
```

---

## 3. Glow / Neon Layering & Depth Parallax

Manim renders crisp vector anti-aliased strokes. Simulate soft neon bloom by stacking low-opacity wider strokes behind a bright core stroke:

```python
def make_glow(mobject: VMobject, color=CYAN, layers=5, base_width=3.0):
    glow_group = VGroup()
    for i in range(layers, 0, -1):
        copy = mobject.copy()
        copy.set_fill(opacity=0)
        copy.set_stroke(color=color, width=base_width + i * 5.5, opacity=0.06 + 0.04 * (layers - i) / layers)
        glow_group.add(copy)
    core = mobject.copy().set_stroke(color=WHITE, width=base_width, opacity=1.0)
    return VGroup(*glow_group, core)
```

### Multi-Plane Parallax

Group background grid/particles (`z_index=-2`), mid-ground UI cards (`z_index=0`), and foreground callouts (`z_index=2`). When panning the camera, shift background layers slightly in the same direction (`shift(vec * 0.4)`) to create convincing depth parallax.

---

## 4. Rate Function Choreography Cheat Sheet

| Effect | Recommended `rate_func` | Use Case |
|---|---|---|
| Snappy UI slide-in | `rate_functions.ease_out_expo` | Cards, titles, panels settling smoothly |
| Playful bounce pop | `rate_functions.ease_out_back` | Badges, icons, callout pills |
| Quick accent pulse | `rate_functions.there_and_back` | Highlights, button taps, eye blinks |
| Anticipation + follow-through | `rate_functions.running_start` | Launching objects across screen |
| Continuous loops / physics | `linear` | Rotating gears, `ValueTracker` timebases |
| Dramatic camera reveal | `rate_functions.ease_in_out_expo` | Fast mid-flight pan with gentle landing |
