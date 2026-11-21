# UI Loaders, Micro-Interactions & Showcase Reel Layouts

Build crisp, 60fps UI loading animations, micro-interactions, and high-retention developer/design showcase reels (macOS browser window spotlight, progressive 2-column checklist, and simultaneous 5×4 Bento recap grid) using pure Manim geometry (`0` LaTeX required).

---

## 1. High-Retention Showcase Reel Layout Pattern

A proven visual grammar for technical/UI motion reels (`9:16` portrait or `16:9` widescreen):

- **Color Palette (High-Contrast Kinetic Theme):**
  - Canvas: `#0A0B0D` with subtle radial accent glow (`#E8FF14` at `0.06` opacity)
  - Alternating Stage Themes inside window: Warm Cream (`#F7F6F0`, ink `#111111`), Charcoal Dark (`#141518`, ink `#F8FAFC`), Electric Lime (`#E8FF14`, ink `#111111`)
  - Title Bar Chrome: `#16181D` with macOS dots (`#FF5F56`, `#FFBD2E`, `#27C93F`) and centered pill slug badge (`loader/liquid-fill`)
- **3-Act Reel Structure:**
  1. **Spotlight Window + Active Slug:** Each pattern plays inside the browser window for `1.0s–1.8s` while the slug pill updates cleanly.
  2. **Progressive 2-Column Checklist:** Numbered slots (`1..20`) stay visible; completed items settle in white, the currently playing item highlights in `#E8FF14`, and upcoming slots show only their index number until reached.
  3. **Simultaneous Bento Recap Grid:** Transition to a `5×4` (or `4×5`) grid inside a wide browser frame where **all patterns animate concurrently** driven by one shared `ValueTracker`.

---

## 2. The 20 Core Loader & Micro-Interaction Primitives

All 20 patterns can be implemented as pure stateless functions `draw_loader(t, w, h, theme)` driven by `t_tracker = ValueTracker(0.0)` + `always_redraw`, making them effortless to preview solo OR run simultaneously inside a Bento grid:

| # | Pattern | Motion & Math Mechanic |
|---|---|---|
| 1 | **Bouncing Ball** | Vertical `abs(sin(w*t))` arc; squash `(1+0.25*sq, 1-0.25*sq)` on impact; shadow ellipse scales inversely with height. |
| 2 | **Spinner Arc** | `Arc` rotating at `omega * t` while `angle` breathes between `0.15*PI` and `1.45*PI`. |
| 3 | **Bouncing Dots** | 3–4 dots with phase offsets `i * 0.55`; active crest dot swaps to accent `#E8FF14`. |
| 4 | **Pulse Rings** | 3 concentric `Circle`s with phase `u = (t * rate + i / 3) % 1.0`, `radius = lerp(r0, r1, u)`, `stroke_opacity = 1 - u`. |
| 5 | **Indeterminate Bar** | Pill track (`RoundedRectangle`) + sliding inner capsule whose `x` and `width` sweep smoothly via `smoothstep`/`sin`. |
| 6 | **Skeleton Shimmer** | Avatar `Circle` + rounded text bars with a traveling brighter highlight pill clipped/masked across their X span. |
| 7 | **Orbit** | 2–3 elliptical guide rings (`Ellipse`) + orbiting dots at `(a*cos(w*t + p), b*sin(w*t + p))`. |
| 8 | **Equalizer Bars** | 5–9 vertical capsules (`RoundedRectangle`) pulsing symmetrically with `0.3 + 0.7 * abs(sin(w*t + i*0.6))`. |
| 9 | **Square Morph** | `RoundedRectangle` rotating `0 -> PI/2` per beat while `corner_radius` oscillates between crisp square and circle (`w/2`). |
| 10 | **Liquid Fill** | Circular frame + rising clipped sine-wave fill (`Intersection(circle, wave_poly)`) + centered live integer `%` `Text`. |
| 11 | **Dot Grid Wave** | `4×4` grid of dots where `scale = 0.35 + 0.65 * 0.5*(1 + sin(4*t - 0.7*(row + col)))`. |
| 12 | **Infinity Trail** | Lemniscate curve `x = a*cos(u)/(1+sin(u)^2)`, `y = a*sin(u)*cos(u)/(1+sin(u)^2)` sampled across trailing window `[t-0.9, t]` with fading stroke segments. |
| 13 | **Flipping Square** | Pseudo-3D card flip: alternate X-flip (`height * max(0.08, |cos(theta)|)`) and Y-flip (`width * max(0.08, |cos(theta)|)`). |
| 14 | **Gradient Ring** | Multi-segment `Arc` chain (`16–24` sub-arcs) interpolating color `#E8FF14 -> #38B2AC -> #1E293B` rotating continuously. |
| 15 | **Typing Dots** | Rounded chat-bubble pill containing 3 phase-staggered bouncing dots. |
| 16 | **Spoke Spinner** | 12 radial `Line` spokes at `k * 30°` where opacity cascades clockwise: `0.15 + 0.85 * ((1 - ((k/12 - t*1.2) % 1.0)) ** 2)`. |
| 17 | **Percent Bar** | Caption (`"Exporting video"`), right-aligned live `%` `Text`, and smooth rounded fill bar `width = max(h, frac * track_w)`. |
| 18 | **Chasing Squares** | 3 squares inside a `2×2` lattice sliding into the single empty slot one corner per beat (`t % 4`). |
| 19 | **Text Shimmer** | Muted base `Text("Loading")` overlaid with per-glyph brightness pulse `0.25 + 0.75 * exp(-((idx - sweep_pos)^2) / 1.4)`. |
| 20 | **Battery Charge** | Battery shell + terminal nub + lightning bolt polygon + 3 inner charge blocks lighting sequentially (`1 -> 2 -> 3`). |

---

## 3. Clipping & Masking Recipes Without Shaders

- **Liquid Fill inside a Circle (`Intersection`):**
  Build a closed polygon covering `y = bottom` up to a sine wave `y_top(x) = y_level + amp * sin(k*x + phase)` and intersect it with `Circle(radius=r)`:
  ```python
  liquid = Intersection(container_circle.copy(), wave_poly, fill_color=accent, fill_opacity=0.95, stroke_width=0)
  ```
- **Shimmer Sweep Without Frag Shaders:**
  Split text into individual glyphs (`Text("Loading")[:]`) and modulate each glyph's opacity/color with a Gaussian window centered on `sweep_x = (t * 2.5) % (len(glyphs) + 3) - 1.5`. Zero clipping artifacts and crisp 60fps rendering!
