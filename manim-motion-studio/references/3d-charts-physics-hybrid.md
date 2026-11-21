# 3D Scenes, Charts, Physics & Hybrid Video in Manim

Manim goes far beyond 2D text and shapes. Here are the high-impact modules you can combine in the same project.

---

## 1. 3D Scenes, Surfaces & Camera (`ThreeDScene`)

Use `ThreeDScene` + `ThreeDAxes` + `Surface` + `add_fixed_in_frame_mobjects` for 3D math, product mockups, and orbital camera sweeps:

```python
class Surface3DExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES)

        title = Text("3D Wave Surface", font_size=34, weight="BOLD").to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)  # Pins HUD to 2D screen

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-1.5, 1.5, 0.5],
            axis_config={"include_numbers": False, "label_constructor": Text},
        )
        surface = Surface(
            lambda u, v: axes.c2p(u, v, 0.65 * np.sin(u * 1.4) * np.cos(v * 1.4)),
            u_range=[-2.8, 2.8],
            v_range=[-2.8, 2.8],
            resolution=(32, 32),
            fill_opacity=0.85,
        )
        surface.set_fill_by_value(axes=axes, colorscale=[(BLUE_E, -0.6), (TEAL_C, 0.0), (GOLD_C, 0.6)], axis=2)

        self.play(Create(axes), Create(surface), run_time=1.8)
        self.begin_ambient_camera_rotation(rate=0.35)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=45 * DEGREES, theta=30 * DEGREES, run_time=1.4)
```

---

## 2. Animated Data Visualization (`Axes`, `BarChart`, `Sector`, `DecimalNumber`)

**Portability Note:** Pass `label_constructor=Text` inside `axis_config` so numeric tick labels render via Pango with zero LaTeX dependency.

- **Animated Function Curves & Area (`get_area` / `get_riemann_rectangles`)**
- **Bar Chart Transitions:** Animate `chart.change_bar_values([new_vals])` smoothly across time steps.
- **Live Counters (`always_redraw`):** Bind `Text(f"{tracker.get_value():.1f}%")` to a `ValueTracker` so numbers update smoothly in lockstep with charts, progress arcs (`AnnularSector`), or sliders.

---

## 3. Physics, Vector Fields & Algorithm Graphs

### Vector Fields & Streamlines

```python
func = lambda pos: np.array([-pos[1], pos[0], 0]) * 0.5  # Rotational vortex
field = ArrowVectorField(func, x_range=[-5, 5, 0.8], y_range=[-3, 3, 0.8])
stream = StreamLines(func, stroke_width=2.5, max_anchors_per_line=30)

self.add(field)
self.add(stream)
stream.start_animation(warm_up=True, flow_speed=1.4)
self.wait(3.0)
```

### Time-Stepped Physics (`add_updater(mob, dt)`)

Use `dt` inside updaters for damped springs, pendulums, orbital mechanics, or particle systems:

```python
theta = ValueTracker(0.9)
omega = ValueTracker(0.0)
def step_pendulum(mob, dt):
    alpha = -(9.8 / 2.2) * np.sin(theta.get_value()) - 0.15 * omega.get_value()
    omega.increment_value(alpha * dt)
    theta.increment_value(omega.get_value() * dt)
```

### Graphs, Trees & Algorithms (`Graph` / `DiGraph`)

Animate BFS/DFS, shortest paths, or neural network forward passes using `Graph(vertices, edges, layout="kamada_kawai")` and highlighting traversed edges with `ShowPassingFlash` or `edge.animate.set_color(GOLD)`.

---

## 4. Linear Algebra, Calculus, Code & Slide Callouts

### Linear Transformations & Calculus
- **Matrix transforms:** Use `NumberPlane` + `scene.apply_matrix([[2, 1], [0, 1]])` (or `LinearTransformationScene`) to visualize eigenvectors, shears, and determinants.
- **Calculus:** Animate `axes.get_secant_slope_group(...)`, `TangentLine`, and `axes.get_riemann_rectangles(curve, dx=...)` shrinking `dx` smoothly via `ValueTracker`.
- **Complex analysis:** `ComplexPlane` + `.apply_complex_function(lambda z: z**2)`.

### Code Blocks, Tables & Presentation Callouts (Zero-LaTeX)
- **Syntax-highlighted code:** `Code(code_string=..., language="python", background="window")` + `Circumscribe`, `Indicate`, or `SurroundingRectangle` on target lines.
- **Tables & Annotations:** `Table([["Metric", "Score"], ...], include_outer_lines=True)` (uses `Text` by default, zero LaTeX), `Brace(mob, DOWN)` + `brace.get_text(...)`, `Flash`, `Wiggle`, and `self.next_section("SceneName")` for chaptered presentations.

---

## 5. Hybrid Photo / Video & Computer Vision Compositing

Combine `ImageMobject` with `OpenCV` + `MediaPipe` + `SciPy` for photo-realistic character animation, UI screen replacements, and portrait effects:

1. **Landmarks & segmentation:** In `mediapipe>=1.x` (no `mp.solutions`), use `mp.tasks.vision.FaceLandmarker` and `HandLandmarker` with `.task` models.
2. **Clean masks:** Exclude `FACE_OVAL` and fingertips from background-wall masks before segmenting arms/hands; never shrink `face_mask` below `FACE_OVAL` or swing a waving hand across the face.
3. **Smooth frame warping (`cv2.remap`):** Build piecewise-linear displacement grids cast explicitly to **`np.float32`** (not `float64`), drive `blink_t` and `wave_deg` via `ValueTracker`, composite only the active ROI inside `always_redraw`, and pass RGB arrays to `ImageMobject(frame_rgb)`.

---

## 6. Audio Sync & Post-Production (`self.add_sound` & `ffmpeg`)

- **Trigger SFX/Music on exact beats:**
  ```python
  self.add_sound("whoosh.wav", time_offset=0.2, gain=-4)
  self.play(card.animate.shift(RIGHT * 4), run_time=0.5)
  ```
- **Voiceover / Narration:** Match `run_time` + `self.wait()` to audio clip durations, or use `scripts/video_edit.py` (`combine`, `trim`, `speed`, `overlay`, `mux-audio`, `gif`). See `references/video-editing-postprod.md` for full pipelines.
