# Stroke-by-Stroke Drawing & Morphing in Manim

## 1. Stroke-by-Stroke Drawing Techniques

### Built-In Stroke Reveals

| Animation | Behavior | Best For |
|---|---|---|
| `Create(mob)` | Draws stroke sequentially along the path | Shapes, curves, vector icons, diagrams |
| `DrawBorderThenFill(mob)` | Traces stroke first, then fades in interior fill | Filled badges, logos, solid UI cards |
| `Write(mob)` | Traces border then fills each submobject staggered | `Text`, `MarkupText`, `MathTex` |
| `Uncreate(mob)` / `Unwrite(mob)` | Reverses the stroke draw cleanly | Exit transitions |
| `ShowPassingFlash(mob.copy())` | Sends a glowing highlight pulse along the stroke | Signal flow, circuit traces, emphasis |
| `ShowIncreasingSubsets(group)` | Reveals discrete submobjects one by one | Step sequences, point clouds, bars |

### Custom Multi-Stroke & Bezier Paths (`VMobject`)

Build smooth hand-drawn curves or custom logos directly with Bezier segments:

```python
path = VMobject(color=GOLD_C, stroke_width=5)
path.start_new_path(LEFT * 3 + DOWN * 0.5)
path.add_cubic_bezier_curve_to(
    LEFT * 1.5 + UP * 2.5,   # control 1
    RIGHT * 1.0 + DOWN * 2.5, # control 2
    RIGHT * 3 + UP * 0.8,    # anchor end
)
self.play(Create(path), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
self.play(ShowPassingFlash(path.copy().set_color(WHITE).set_stroke(width=8), time_width=0.35), run_time=1.0)
```

### Staggered Submobject Drawing & `SVGMobject`

When importing multi-path vector art (`SVGMobject("logo.svg")`), trace individual strokes sequentially with `LaggedStart`:

```python
svg = SVGMobject("icon.svg").scale(2.0)
svg.set_fill(opacity=0)
svg.set_stroke(color=BLUE_B, width=3.5)

self.play(
    LaggedStart(*[Create(sub) for sub in svg], lag_ratio=0.12),
    run_time=2.5,
)
# Optionally fade in original brand colors afterward
self.play(svg.animate.set_fill(opacity=1.0), run_time=0.6)
```

---

## 2. Morphing Techniques

### `Transform` vs `ReplacementTransform`

- **`Transform(a, b)`**: Morphs `a`'s geometry/color into `b` in-place. `a` stays in the scene (`b` is never added). Useful when chaining `Transform(a, b)`, `Transform(a, c)`, `Transform(a, d)`.
- **`ReplacementTransform(a, b)`**: Removes `a` from the scene and inserts `b`. Use this when later animations reference `b` directly.

```python
shape = Circle(radius=1.2, color=TEAL_C, fill_opacity=0.35)
square = Square(side_length=2.2, color=PURPLE_B, fill_opacity=0.35)
star = Star(n=5, outer_radius=1.5, color=GOLD_C, fill_opacity=0.45)

self.play(Create(shape))
self.play(Transform(shape, square, path_arc=PI / 3), run_time=1.1)
self.play(Transform(shape, star, path_arc=-PI / 3), run_time=1.1)
```

### `TransformMatchingShapes` & `TransformMatchingTex`

- **`TransformMatchingShapes(mob1, mob2)`**: Automatically pairs matching characters or subpaths (anagrams, rearranged icons, code lines) while fading unmatched parts cleanly:

```python
w1 = Text("LISTEN", font_size=64, weight="BOLD")
w2 = Text("SILENT", font_size=64, weight="BOLD", color=TEAL_C)
self.play(Write(w1))
self.play(TransformMatchingShapes(w1, w2, path_arc=PI / 2), run_time=1.2)
```

- **`TransformMatchingTex(tex1, tex2)`** *(requires LaTeX)*: Breaks equations into matching tokens when isolated with braces (`r"{{a}}^2 + {{b}}^2 = {{c}}^2"` -> `r"{{c}} = \sqrt{{{a}}^2 + {{b}}^2}"`).

### `MoveToTarget` & `Save/Restore`

Ideal for multi-attribute transforms (position + scale + rotation + color) in one clean call:

```python
card = RoundedRectangle(corner_radius=0.2, width=3, height=2, color=BLUE_C)
card.save_state()
card.generate_target()
card.target.shift(RIGHT * 3).scale(0.6).rotate(PI / 8).set_color(PINK)

self.play(MoveToTarget(card), run_time=0.9)
self.play(Restore(card), run_time=0.8)
```

### Non-Linear Warps & Homotopies

Deform entire grids, drawings, or meshes continuously in space and time:

```python
grid = NumberPlane(x_range=[-5, 5, 1], y_range=[-3, 3, 1]).prepare_for_nonlinear_transform()

# Static pointwise warp
self.play(ApplyPointwiseFunction(lambda p: p + np.array([0.4 * np.sin(p[1]), 0.4 * np.cos(p[0]), 0]), grid), run_time=1.6)

# Time-varying homotopy (x, y, z, t) -> (x', y', z')
def wave_homotopy(x, y, z, t):
    return np.array([x, y + 0.5 * np.sin(x + 2 * PI * t) * np.sin(PI * t), z])

self.play(Homotopy(wave_homotopy, grid), run_time=2.0)
```

> **Tip:** Always call `.prepare_for_nonlinear_transform()` on straight-line Mobjects (`Line`, `Square`, `NumberPlane`) before applying `ApplyPointwiseFunction`, `ApplyComplexFunction`, or `Homotopy` so straight segments subdivide into smooth curves!
