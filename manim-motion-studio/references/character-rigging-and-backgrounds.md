# Articulated Character Rigging & Custom-Background Animation

Build expressive, 60fps 2-joint articulated characters (stick figures, mascots, silhouettes) and composite them cleanly over solid stages, procedural sets, or custom user images/illustrations.

---

## 1. 2-Joint Articulated Character Architecture

A forward-kinematics 2-joint rig computes joints relative to a dynamic `hip` origin so limbs stay connected through leans, squashes, jumps, and full 360°/720° flips:

- **Core state parameters:**
  - Transform: `cx`, `y_floor`, `scale`, `facing` (`+1.0` right / `-1.0` left), `y_jump`, `squash`, `body_lean`, `body_spin`.
  - Legs: `l_hip`, `l_knee`, `r_hip`, `r_knee` + outward/forward foot segments.
  - Arms: `l_sh`, `l_elb`, `r_sh`, `r_elb` + optional multi-finger splayed hands or hand dots.
  - Expression: `head_tilt`, `blink`, `happy_eyes` (`^ ^` arcs), `wide_eyes`, `mouth_open`.
  - Style interpolation (`style_blend`): smoothly morph line widths, stroke color, double-stroke sketch accents, and head fill opacity (e.g., transparent pencil on notebook paper -> opaque cream-filled ink cartoon on a desk).

### Critical Flip & Grounding Rules

1. **Never clamp hip height to `min(l_foot_y, r_foot_y)` while spinning:**
   When `abs(body_spin) > 0.02`, computing `hip_h = -min(l_rel[1], r_rel[1])` drops the hip downward as the legs rotate above the hip (`body_spin ~ PI`), pushing the character's head into the floor!
   ```python
   if abs(body_spin) > 0.02:
       hip_h = (thigh_e + shin_e) * 0.94  # Fixed upright offset + y_jump
   else:
       hip_h = -min(l_rel[1], r_rel[1])   # Ground-anchored standing/walking
   ```
2. **Keep arms clear of wide cartoon heads during cheers/waves:**
   Measure `head_r + neck_len` relative to `upper_arm`. Flare shoulder angles outward (`±1.5–1.8 rad`) and bend elbows upward (`±0.6–0.85 rad`) so raised hands frame the head instead of hiding behind it.
3. **Dynamic ground shadow:**
   Anchor a soft ellipse at `[cx, y_floor - 0.03 * scale, 0]` whose opacity scales inversely with `y_jump` (`max(0.20, 1.0 - 0.18 * y_jump)`), grounding jumps, landings, and elevated props.

---

## 2. Timeline State Machine + Smooth Camera Tracking

Drive multi-act choreography (`10s–60s+`) from a single `t_tracker = ValueTracker(0.0)` and `always_redraw(lambda: make_character(**eval_pose(t_tracker.get_value())))`:

- Use `smoothstep(t0, t1, t)` for clean transitions between idle, wave, walk, jog, hurdle leaps, trampoline flips, moonwalks, juggling, and dance grooves.
- Add `TracedPath(hip_anchor.get_center, stroke_color=..., dissipating_time=0.45)` for kinetic motion trails during jumps and flips.

### `MovingCameraScene` Tracking Rule (CRITICAL)

In `MovingCameraScene`, **`self.camera.frame` is not automatically in the scene's updater loop**. You MUST call `self.add(self.camera.frame)` before attaching `frame.add_updater(...)`, and use **`dt`-based exponential smoothing** so draft (`15fps`) and production (`60fps`) renders produce identical framing:

```python
self.add(self.camera.frame)  # REQUIRED for frame.add_updater to run!

def track_cam(frame, dt):
    p = eval_pose(t_tracker.get_value())
    alpha = 1.0 - float(np.exp(-3.5 * max(dt, 1e-4)))
    cur = frame.get_center()
    frame.set(height=(1.0 - alpha) * frame.height + alpha * target_h)
    frame.move_to([
        (1.0 - alpha) * cur[0] + alpha * target_x,
        (1.0 - alpha) * cur[1] + alpha * target_y,
        0.0,
    ])

self.camera.frame.add_updater(track_cam)
```

---

## 3. Animating on Custom User Backgrounds & Multi-Scene Transitions

When animating a character onto user-provided photos, sketches, or illustrated backgrounds:

1. **Match the background aspect ratio in Manim:**
   For square (`1:1`) or portrait (`3:4`, `9:16`) backgrounds, set `self.camera.frame_width` and `self.camera.frame_height` explicitly inside `construct()` (e.g., `8.0 × 8.0` for `1:1`) and render with `-r 1080,1080 --fps 60` (never `-qh`).
2. **Cleanly remove any static reference character from the background first:**
   - **Flat / ruled / textured paper:** Threshold dark ink inside a tight ROI, dilate slightly, run `cv2.inpaint(..., cv2.INPAINT_TELEA)`, and blend high-frequency paper grain sampled along the same row (`y`) so ruled lines and texture remain unbroken.
   - **Complex illustrated or photo scenes (blurred windows, perspective props):** Use an image-editing/inpainting pass to reconstruct occluded background geometry cleanly before compositing in Manim.
3. **Map scene landmarks to Manim world coordinates:**
   Convert pixel coordinates `(px, py)` in a `W×H` background mapped to `frame_w × frame_h` via:
   `mx = (px / W - 0.5) * frame_w`, `my = (0.5 - py / H) * frame_h`.
   Interpolate both `y_floor` and `scale` when the character walks deeper into the scene or leaps onto elevated props (e.g., books, shelves, steps).
4. **Physical page/scene transitions:**
   Stack `ImageMobject` layers with `set_z_index(-20)` and `set_z_index(-10)`. Slide/rotate the foreground page off-screen (`paper_bg.animate.shift(DOWN * 8.6 + LEFT * 1.4).rotate(0.14)`) simultaneously with a mid-air jump and `style_blend` morph.
