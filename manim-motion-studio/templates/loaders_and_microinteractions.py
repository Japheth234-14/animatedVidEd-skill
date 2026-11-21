"""20 UI Loaders & Micro-Interactions Showcase (Browser Spotlight + Checklist + 5x4 Bento Grid)."""

import numpy as np
from manim import *

ACCENT = "#E8FF14"
DARK_BG = "#141518"
LIGHT_BG = "#F7F6F0"
DARK_INK = "#111111"
LIGHT_INK = "#F8FAFC"


def _theme_colors(theme):
    if theme == "light":
        return LIGHT_BG, DARK_INK, "#D9D7CE"
    if theme == "lime":
        return ACCENT, DARK_INK, "#C8DE0A"
    return DARK_BG, LIGHT_INK, "#2A2D35"


def loader_bouncing_ball(t, s=1.0, theme="light"):
    _, ink, muted = _theme_colors(theme)
    ph = (t * 2.4) % 1.0
    h = 4.0 * ph * (1.0 - ph)
    sq = max(0.0, 1.0 - h * 4.5) * 0.24
    y_ball = -0.35 * s + h * 0.85 * s
    sh = Ellipse(width=(0.36 - 0.16 * h) * s, height=0.07 * s, fill_color=muted, fill_opacity=0.85, stroke_width=0).move_to([0, -0.52 * s, 0])
    ball = Ellipse(
        width=0.34 * s * (1.0 + sq),
        height=0.34 * s * (1.0 - sq),
        fill_color=ACCENT if theme != "lime" else DARK_INK,
        fill_opacity=1.0,
        stroke_color=ink,
        stroke_width=3.0 * min(1.0, s),
    ).move_to([0, y_ball, 0])
    return VGroup(sh, ball)


def loader_spinner_arc(t, s=1.0, theme="dark"):
    _, ink, muted = _theme_colors(theme)
    r = 0.42 * s
    track = Circle(radius=r, stroke_color=muted, stroke_width=6.0 * min(1.0, s), stroke_opacity=0.5)
    sweep = 0.45 * np.pi + 0.85 * np.pi * 0.5 * (1.0 + np.sin(t * 3.2))
    arc = Arc(radius=r, start_angle=-t * 4.5, angle=sweep, stroke_color=ACCENT if theme != "lime" else ink, stroke_width=6.5 * min(1.0, s))
    arc.set_cap_style(CapStyleType.ROUND)
    return VGroup(track, arc)


def loader_bouncing_dots(t, s=1.0, theme="light"):
    _, ink, _ = _theme_colors(theme)
    g = VGroup()
    for i, x in enumerate([-0.38 * s, 0.0, 0.38 * s]):
        w = max(0.0, np.sin(t * 5.0 - i * 0.75))
        col = ACCENT if (theme != "lime" and w > 0.68) else ink
        d = Circle(radius=0.11 * s, fill_color=col, fill_opacity=1.0, stroke_color=ink, stroke_width=2.0 * min(1.0, s))
        d.move_to([x, -0.1 * s + 0.30 * s * w, 0])
        g.add(d)
    return g


def loader_pulse_rings(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    g = VGroup(Dot([0, 0, 0], radius=0.09 * s, color=col))
    for i in range(3):
        u = (t * 0.75 + i / 3.0) % 1.0
        r = (0.10 + 0.48 * u) * s
        c = Circle(radius=r, stroke_color=col, stroke_width=3.5 * min(1.0, s), stroke_opacity=max(0.0, 1.0 - u))
        g.add(c)
    return g


def loader_indeterminate_bar(t, s=1.0, theme="light"):
    _, ink, muted = _theme_colors(theme)
    tw, th = 1.65 * s, 0.14 * s
    track = RoundedRectangle(width=tw, height=th, corner_radius=th / 2, fill_color=muted, fill_opacity=0.65, stroke_width=0)
    u = (t * 0.85) % 1.0
    pill_w = (0.35 + 0.30 * np.sin(np.pi * u)) * tw
    x_pos = (-tw / 2 + pill_w / 2) + (tw - pill_w) * (0.5 - 0.5 * np.cos(np.pi * u))
    pill = RoundedRectangle(width=pill_w, height=th, corner_radius=th / 2, fill_color=ink, fill_opacity=1.0, stroke_width=0).move_to([x_pos, 0, 0])
    return VGroup(track, pill)


def loader_skeleton_shimmer(t, s=1.0, theme="light"):
    _, _, muted = _theme_colors(theme)
    hi = "#FFFFFF" if theme != "dark" else "#4A4E5A"
    sweep = (t * 1.4) % 1.6 - 0.8
    bars = [
        Circle(radius=0.18 * s).move_to([-0.58 * s, 0.22 * s, 0]),
        RoundedRectangle(width=0.88 * s, height=0.13 * s, corner_radius=0.06 * s).move_to([0.14 * s, 0.30 * s, 0]),
        RoundedRectangle(width=0.62 * s, height=0.11 * s, corner_radius=0.05 * s).move_to([0.01 * s, 0.12 * s, 0]),
        RoundedRectangle(width=1.45 * s, height=0.11 * s, corner_radius=0.05 * s).move_to([0.0, -0.15 * s, 0]),
        RoundedRectangle(width=1.10 * s, height=0.11 * s, corner_radius=0.05 * s).move_to([-0.17 * s, -0.34 * s, 0]),
    ]
    g = VGroup()
    for b in bars:
        dist = abs(b.get_center()[0] / max(1e-4, s) - sweep)
        lum = np.exp(-dist * dist * 4.5)
        col = interpolate_color(ManimColor(muted), ManimColor(hi), float(lum))
        b.set_fill(col, opacity=0.95).set_stroke(width=0)
        g.add(b)
    return g


def loader_orbit(t, s=1.0, theme="dark"):
    _, ink, muted = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    ring1 = Circle(radius=0.45 * s, stroke_color=muted, stroke_width=1.8 * min(1.0, s), stroke_opacity=0.6)
    ring2 = Ellipse(width=1.15 * s, height=0.48 * s, stroke_color=muted, stroke_width=1.8 * min(1.0, s), stroke_opacity=0.6).rotate(0.45)
    core = Dot([0, 0, 0], radius=0.09 * s, color=col)
    d1 = Dot([0.45 * s * np.cos(t * 3.0), 0.45 * s * np.sin(t * 3.0), 0], radius=0.065 * s, color=ink)
    p2 = np.array([0.575 * s * np.cos(-t * 4.2 + 1.0), 0.24 * s * np.sin(-t * 4.2 + 1.0), 0])
    c, sn = np.cos(0.45), np.sin(0.45)
    d2 = Dot([c * p2[0] - sn * p2[1], sn * p2[0] + c * p2[1], 0], radius=0.055 * s, color=col)
    return VGroup(ring1, ring2, core, d1, d2)


def loader_equalizer_bars(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    g = VGroup()
    for i in range(7):
        x = (i - 3) * 0.19 * s
        amp = 0.22 + 0.78 * abs(np.sin(t * 4.8 + i * 0.65))
        h = 0.85 * s * amp
        bar = RoundedRectangle(width=0.11 * s, height=h, corner_radius=0.055 * s, fill_color=col if i % 2 == 0 else ink, fill_opacity=0.95, stroke_width=0).move_to([x, 0, 0])
        g.add(bar)
    return g


def loader_square_morph(t, s=1.0, theme="lime"):
    _, ink, _ = _theme_colors(theme)
    u = 0.5 * (1.0 - np.cos(t * 3.2))
    side = (0.58 + 0.10 * np.sin(t * 3.2)) * s
    sq = RoundedRectangle(width=side, height=side, corner_radius=(0.06 + 0.23 * u) * s, fill_color=ink, fill_opacity=1.0, stroke_width=0)
    sq.rotate(t * 1.6)
    return sq


def loader_liquid_fill(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    r = 0.48 * s
    frac = 0.12 + 0.86 * (0.5 - 0.5 * np.cos(t * 1.15))
    y_lvl = -r + 2.0 * r * frac
    pts = [[-r * 1.1, -r * 1.15, 0]]
    xs = np.linspace(-r * 1.1, r * 1.1, 18)
    for x in xs:
        pts.append([x, y_lvl + 0.05 * s * np.sin(x / max(1e-4, s) * 6.0 + t * 5.0), 0])
    pts.append([r * 1.1, -r * 1.15, 0])
    wave = Polygon(*pts, stroke_width=0, fill_opacity=1.0)
    ring = Circle(radius=r, stroke_color=ink, stroke_width=4.0 * min(1.0, s))
    liq = Intersection(Circle(radius=r * 0.96), wave, fill_color=col, fill_opacity=0.9, stroke_width=0)
    pct = Text(f"{int(round(frac * 100))}%", font_size=max(14, int(24 * s)), weight="BOLD", color=ink if frac < 0.55 else DARK_INK)
    return VGroup(liq, ring, pct)


def loader_dot_grid_wave(t, s=1.0, theme="light"):
    _, ink, _ = _theme_colors(theme)
    g = VGroup()
    for r in range(4):
        for c in range(4):
            w = 0.5 * (1.0 + np.sin(t * 4.5 - 0.7 * (r + c)))
            d = Dot([(c - 1.5) * 0.24 * s, (1.5 - r) * 0.24 * s, 0], radius=(0.035 + 0.055 * w) * s, color=ink)
            d.set_opacity(0.30 + 0.70 * w)
            g.add(d)
    return g


def loader_infinity_trail(t, s=1.0, theme="dark"):
    _, ink, muted = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    a = 0.68 * s

    def lem(u):
        den = 1.0 + np.sin(u) ** 2
        return np.array([a * np.cos(u) / den, a * np.sin(u) * np.cos(u) / den, 0.0])

    guide = ParametricFunction(lem, t_range=[0, 2 * np.pi], stroke_color=muted, stroke_width=2.5 * min(1.0, s), stroke_opacity=0.45)
    g = VGroup(guide)
    n_seg = 16
    span = 1.35
    for k in range(n_seg):
        u0 = t * 3.0 - span * (1.0 - k / n_seg)
        u1 = t * 3.0 - span * (1.0 - (k + 1) / n_seg)
        ln = Line(lem(u0), lem(u1), stroke_color=col, stroke_width=5.0 * min(1.0, s), stroke_opacity=(k + 1) / n_seg)
        ln.set_cap_style(CapStyleType.ROUND)
        g.add(ln)
    g.add(Dot(lem(t * 3.0), radius=0.065 * s, color=ink))
    return g


def loader_flipping_square(t, s=1.0, theme="light"):
    _, ink, _ = _theme_colors(theme)
    phase = (t * 2.2) % 2.0
    ang = (phase % 1.0) * np.pi
    scale_ax = max(0.10, abs(np.cos(ang)))
    w = 0.64 * s * (scale_ax if phase < 1.0 else 1.0)
    h = 0.64 * s * (scale_ax if phase >= 1.0 else 1.0)
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.08 * s,
        fill_color=ACCENT if theme != "lime" else ink,
        fill_opacity=1.0, stroke_color=ink, stroke_width=3.5 * min(1.0, s),
    )


def loader_gradient_ring(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    r = 0.42 * s
    n = 18
    g = VGroup()
    c_start = ManimColor(ACCENT if theme != "lime" else ink)
    c_end = ManimColor("#1F2937" if theme != "dark" else "#23262E")
    for k in range(n):
        frac = k / (n - 1)
        a0 = -t * 4.2 + frac * 1.55 * np.pi
        seg = Arc(
            radius=r, start_angle=a0, angle=1.55 * np.pi / n * 1.15,
            stroke_color=interpolate_color(c_end, c_start, frac),
            stroke_width=6.5 * min(1.0, s),
        )
        seg.set_cap_style(CapStyleType.ROUND)
        g.add(seg)
    return g


def loader_typing_dots(t, s=1.0, theme="light"):
    _, ink, muted = _theme_colors(theme)
    pill = RoundedRectangle(width=1.18 * s, height=0.52 * s, corner_radius=0.26 * s, fill_color=muted, fill_opacity=0.85, stroke_color=ink, stroke_width=2.0 * min(1.0, s))
    g = VGroup(pill)
    for i, x in enumerate([-0.26 * s, 0.0, 0.26 * s]):
        w = 0.5 * (1.0 + np.sin(t * 6.0 - i * 0.9))
        d = Dot([x, 0.04 * s * (w - 0.5), 0], radius=0.068 * s, color=ink)
        d.set_opacity(0.35 + 0.65 * w)
        g.add(d)
    return g


def loader_spoke_spinner(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    n = 12
    g = VGroup()
    for k in range(n):
        ang = -k * 2 * np.pi / n
        phase = (k / n - t * 1.15) % 1.0
        op = 0.15 + 0.85 * ((1.0 - phase) ** 2.2)
        p0 = np.array([0.22 * s * np.cos(ang), 0.22 * s * np.sin(ang), 0])
        p1 = np.array([0.46 * s * np.cos(ang), 0.46 * s * np.sin(ang), 0])
        ln = Line(p0, p1, stroke_color=col, stroke_width=5.0 * min(1.0, s), stroke_opacity=op)
        ln.set_cap_style(CapStyleType.ROUND)
        g.add(ln)
    return g


def loader_percent_bar(t, s=1.0, theme="dark"):
    _, ink, muted = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    frac = 0.08 + 0.90 * (0.5 - 0.5 * np.cos(t * 1.2))
    tw, th = 1.65 * s, 0.14 * s
    track = RoundedRectangle(width=tw, height=th, corner_radius=th / 2, fill_color=muted, fill_opacity=0.8, stroke_width=0).move_to([0, -0.06 * s, 0])
    fw = max(th, tw * frac)
    fill = RoundedRectangle(width=fw, height=th, corner_radius=th / 2, fill_color=col, fill_opacity=1.0, stroke_width=0).move_to([(-tw + fw) / 2, -0.06 * s, 0])
    lbl = Text("Exporting", font_size=max(8, int(16 * s)), color=ink).next_to(track, UP, buff=0.08 * s).align_to(track, LEFT)
    pct = Text(f"{int(round(frac * 100))}%", font_size=max(8, int(17 * s)), weight="BOLD", color=ink).next_to(track, UP, buff=0.08 * s).align_to(track, RIGHT)
    return VGroup(lbl, pct, track, fill)


def loader_chasing_squares(t, s=1.0, theme="dark"):
    _, ink, _ = _theme_colors(theme)
    col = ACCENT if theme != "lime" else ink
    step = (t * 2.0) % 4.0
    idx_step = int(step)
    u = step - idx_step
    u_ease = u * u * (3.0 - 2.0 * u)
    off = 0.22 * s
    corners = [(-off, off), (off, off), (off, -off), (-off, -off)]
    g = VGroup()
    for i in range(3):
        c0 = (i + idx_step) % 4
        c1 = (c0 + 1) % 4 if i == 2 else c0
        x = corners[c0][0] + (corners[c1][0] - corners[c0][0]) * u_ease
        y = corners[c0][1] + (corners[c1][1] - corners[c0][1]) * u_ease
        sq = RoundedRectangle(width=0.34 * s, height=0.34 * s, corner_radius=0.05 * s, fill_color=col if i == 2 else ink, fill_opacity=1.0, stroke_width=0).move_to([x, y, 0])
        g.add(sq)
    return g


def loader_text_shimmer(t, s=1.0, theme="dark"):
    _, ink, muted = _theme_colors(theme)
    word = Text("Loading", font_size=max(16, int(36 * s)), weight="BOLD", color=muted)
    sweep = (t * 4.5) % (len(word) + 4) - 2.0
    for idx, ch in enumerate(word):
        lum = float(np.exp(-((idx - sweep) ** 2) / 1.8))
        ch.set_color(interpolate_color(ManimColor(muted), ManimColor(ink), lum))
    return word


def loader_battery_charge(t, s=1.0, theme="lime"):
    _, ink, _ = _theme_colors(theme)
    bw, bh = 1.25 * s, 0.62 * s
    shell = RoundedRectangle(width=bw, height=bh, corner_radius=0.09 * s, stroke_color=ink, stroke_width=4.0 * min(1.0, s), fill_opacity=0)
    nub = RoundedRectangle(width=0.09 * s, height=0.26 * s, corner_radius=0.03 * s, fill_color=ink, fill_opacity=1.0, stroke_width=0).move_to([bw / 2 + 0.06 * s, 0, 0])
    level = int((t * 1.8) % 4)
    g = VGroup(shell, nub)
    for i in range(3):
        bx = (-0.36 + i * 0.36) * s
        blk = RoundedRectangle(
            width=0.29 * s, height=0.44 * s, corner_radius=0.04 * s,
            fill_color=ink, fill_opacity=1.0 if i < level else 0.18, stroke_width=0,
        ).move_to([bx, 0, 0])
        g.add(blk)
    bolt = Polygon(
        [0.05 * s, 0.17 * s, 0], [-0.08 * s, 0.01 * s, 0], [0.01 * s, 0.01 * s, 0],
        [-0.05 * s, -0.17 * s, 0], [0.08 * s, -0.01 * s, 0], [-0.01 * s, -0.01 * s, 0],
        fill_color=ACCENT if theme != "dark" else LIGHT_INK, fill_opacity=1.0, stroke_color=ink, stroke_width=1.5 * min(1.0, s),
    )
    g.add(bolt)
    return g


LOADERS = [
    ("loader/bouncing-ball", "Bouncing Ball", "light", loader_bouncing_ball),
    ("loader/spinner-arc", "Spinner Arc", "dark", loader_spinner_arc),
    ("loader/bouncing-dots", "Bouncing Dots", "light", loader_bouncing_dots),
    ("loader/pulse-rings", "Pulse Rings", "dark", loader_pulse_rings),
    ("loader/indeterminate-bar", "Indeterminate Bar", "light", loader_indeterminate_bar),
    ("loader/skeleton-shimmer", "Skeleton Shimmer", "light", loader_skeleton_shimmer),
    ("loader/orbit", "Orbit", "dark", loader_orbit),
    ("loader/equalizer-bars", "Equalizer Bars", "dark", loader_equalizer_bars),
    ("loader/square-morph", "Square Morph", "lime", loader_square_morph),
    ("loader/liquid-fill", "Liquid Fill", "dark", loader_liquid_fill),
    ("loader/dot-grid-wave", "Dot Grid Wave", "light", loader_dot_grid_wave),
    ("loader/infinity-trail", "Infinity Trail", "dark", loader_infinity_trail),
    ("loader/flipping-square", "Flipping Square", "light", loader_flipping_square),
    ("loader/gradient-ring", "Gradient Ring", "dark", loader_gradient_ring),
    ("loader/typing-dots", "Typing Dots", "light", loader_typing_dots),
    ("loader/spoke-spinner", "Spoke Spinner", "dark", loader_spoke_spinner),
    ("loader/percent-bar", "Percent Bar", "dark", loader_percent_bar),
    ("loader/chasing-squares", "Chasing Squares", "dark", loader_chasing_squares),
    ("loader/text-shimmer", "Text Shimmer", "dark", loader_text_shimmer),
    ("loader/battery-charge", "Battery Charge", "lime", loader_battery_charge),
]


def make_browser_chrome(win_w, win_h, slug="20 loading animations", body_color=DARK_BG):
    outer = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.22, fill_color=body_color, fill_opacity=1.0, stroke_color="#2A2D36", stroke_width=2.0)
    bar_h = 0.48
    bar = Rectangle(width=win_w - 0.04, height=bar_h, fill_color="#16181D", fill_opacity=1.0, stroke_width=0).align_to(outer, UP).shift(DOWN * 0.02)
    dots = VGroup(*[
        Dot(radius=0.07, color=c).move_to(bar.get_left() + RIGHT * (0.28 + i * 0.24))
        for i, c in enumerate(["#FF5F56", "#FFBD2E", "#27C93F"])
    ])
    pill = RoundedRectangle(width=min(3.4, win_w * 0.45), height=0.28, corner_radius=0.14, fill_color="#22252D", fill_opacity=1.0, stroke_width=0).move_to(bar.get_center())
    pill_txt = Text(slug, font_size=14, color="#CBD5E1").move_to(pill.get_center())
    return VGroup(outer, bar, dots, pill, pill_txt)


class LoadersShowcase(Scene):
    def construct(self):
        self.camera.background_color = "#0A0B0D"

        title = Text("20 Loading Animations", font_size=40, weight="BOLD", color=WHITE).to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)

        # 1. Spotlight Showcase Window + Progressive Checklist (samples 4 iconic loaders)
        spotlight_indices = [0, 9, 16, 19]  # Bouncing Ball, Liquid Fill, Percent Bar, Battery Charge
        win_w, win_h = 6.8, 4.4
        win_center = LEFT * 2.7 + DOWN * 0.3

        # Build checklist on right
        list_items = VGroup()
        for idx, (_, label, _, _) in enumerate(LOADERS):
            num = Text(f"{idx + 1}.", font_size=15, weight="BOLD", color=ACCENT)
            name = Text(label, font_size=15, color="#475569")
            row = VGroup(num, name).arrange(RIGHT, buff=0.12)
            col_i, row_i = idx // 10, idx % 10
            row.move_to(RIGHT * (1.85 + col_i * 2.75) + UP * (2.05 - row_i * 0.46))
            row.align_to(RIGHT * (0.8 + col_i * 2.75), LEFT)
            list_items.add(row)

        self.play(FadeIn(list_items, lag_ratio=0.02), run_time=0.6)

        t_tracker = ValueTracker(0.0)
        for spot_i, loader_idx in enumerate(spotlight_indices):
            slug, label, theme, fn = LOADERS[loader_idx]
            bg_col, _, _ = _theme_colors(theme)
            chrome = make_browser_chrome(win_w, win_h, slug=slug, body_color=bg_col).move_to(win_center)
            # Highlight checklist row
            list_items[loader_idx][1].set_color(ACCENT)

            anim_mob = always_redraw(lambda f=fn, th=theme: f(t_tracker.get_value(), s=1.45, theme=th).move_to(win_center + DOWN * 0.2))
            self.add(chrome, anim_mob)
            self.play(t_tracker.animate.set_value((spot_i + 1) * 1.4), run_time=1.4, rate_func=linear)
            self.remove(chrome, anim_mob)
            list_items[loader_idx][1].set_color(WHITE)

        self.play(FadeOut(list_items), run_time=0.35)

        # 2. Simultaneous 5x4 Bento Recap Grid inside full-width browser window!
        bento_w, bento_h = 11.8, 5.9
        bento_center = DOWN * 0.38
        bento_chrome = make_browser_chrome(bento_w, bento_h, slug="20 loading animations", body_color="#111317").move_to(bento_center)
        self.play(FadeIn(bento_chrome), run_time=0.4)

        cols, rows = 5, 4
        cell_w = (bento_w - 0.16) / cols
        cell_h = (bento_h - 0.62) / rows

        def build_bento():
            t = t_tracker.get_value()
            grid = VGroup()
            for idx, (_, _, theme, fn) in enumerate(LOADERS):
                r, c = divmod(idx, cols)
                cx = bento_center[0] - (bento_w - 0.16) / 2 + (c + 0.5) * cell_w
                cy = bento_center[1] + (bento_h - 0.56) / 2 - 0.24 - (r + 0.5) * cell_h
                bg_col, _, _ = _theme_colors(theme)
                tile = Rectangle(width=cell_w - 0.04, height=cell_h - 0.04, fill_color=bg_col, fill_opacity=1.0, stroke_color="#23262F", stroke_width=1.0).move_to([cx, cy, 0])
                icon = fn(t, s=0.68, theme=theme).move_to([cx, cy, 0])
                grid.add(tile, icon)
            return grid

        bento_live = always_redraw(build_bento)
        self.add(bento_live)
        self.play(t_tracker.animate.set_value(t_tracker.get_value() + 3.2), run_time=3.2, rate_func=linear)
