"""Generic 2-joint articulated character rig + dt-safe MovingCameraScene tracking template."""

import numpy as np
from manim import *


def smoothstep(e0, e1, x):
    if e1 == e0:
        return 0.0
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return float(t * t * (3.0 - 2.0 * t))


def lerp(a, b, t):
    return a + (b - a) * t


def make_character(
    cx=0.0,
    y_floor=-2.0,
    scale=1.0,
    facing=1.0,
    body_lean=0.0,
    y_jump=0.0,
    squash=0.0,
    body_spin=0.0,
    l_hip=-0.26,
    l_knee=0.12,
    r_hip=0.26,
    r_knee=-0.12,
    l_sh=-0.85,
    l_elb=-0.10,
    r_sh=0.85,
    r_elb=0.10,
    head_tilt=0.0,
    blink=0.0,
    happy_eyes=0.0,
    stroke_color="#F8FAFC",
    head_fill="#0D1117",
    accent_color="#38B2AC",
    show_fingers=True,
):
    """Build a 2-joint articulated character anchored to y_floor with safe mid-air spin."""
    s = scale
    head_r = 0.42 * s
    neck_len = 0.14 * s
    torso_len = 0.95 * s
    upper_arm = 0.48 * s
    forearm = 0.45 * s
    thigh_len = 0.56 * s
    shin_len = 0.58 * s
    foot_len = 0.22 * s

    sq_y = 1.0 - 0.16 * squash
    sq_x = 1.0 + 0.12 * squash
    thigh_e, shin_e = thigh_len * sq_y, shin_len * sq_y
    torso_e, neck_e = torso_len * sq_y, neck_len * sq_y

    def leg_end(hip_a, knee_a):
        a1 = -np.pi / 2 + hip_a * facing
        kx, ky = thigh_e * np.cos(a1) * sq_x, thigh_e * np.sin(a1)
        a2 = a1 + knee_a * facing
        return np.array([kx + shin_e * np.cos(a2) * sq_x, ky + shin_e * np.sin(a2)])

    l_rel = leg_end(l_hip, l_knee)
    r_rel = leg_end(r_hip, r_knee)
    # Keep upright hip height during 360-degree spins so head never clips floor
    hip_h = (thigh_e + shin_e) * 0.94 if abs(body_spin) > 0.02 else -min(l_rel[1], r_rel[1])
    hip = np.array([cx, y_floor + hip_h + y_jump, 0.0])

    def rot_pt(pt_2d):
        c, sn = np.cos(body_spin), np.sin(body_spin)
        return hip + np.array([c * pt_2d[0] - sn * pt_2d[1], sn * pt_2d[0] + c * pt_2d[1], 0.0])

    t_ang = np.pi / 2 - body_lean * facing
    sh_rel = np.array([torso_e * np.cos(t_ang) * sq_x, torso_e * np.sin(t_ang)])
    nk_rel = sh_rel + np.array([neck_e * np.cos(t_ang) * sq_x, neck_e * np.sin(t_ang)])
    hd_rel = nk_rel + np.array([
        head_r * 0.95 * np.cos(t_ang + head_tilt * 0.35),
        head_r * 0.95 * np.sin(t_ang + head_tilt * 0.35),
    ])

    shoulder_pt = rot_pt(sh_rel)
    neck_top_pt = rot_pt(nk_rel)
    head_pt = rot_pt(hd_rel)

    def build_leg(hip_a, knee_a, foot_dir):
        a1 = -np.pi / 2 + hip_a * facing
        k_rel = np.array([thigh_e * np.cos(a1) * sq_x, thigh_e * np.sin(a1)])
        a2 = a1 + knee_a * facing
        f_rel = k_rel + np.array([shin_e * np.cos(a2) * sq_x, shin_e * np.sin(a2)])
        ftip_rel = f_rel + np.array([foot_len * foot_dir, 0.0])
        return rot_pt(k_rel), rot_pt(f_rel), rot_pt(ftip_rel)

    lk, lf, lft = build_leg(l_hip, l_knee, -1.0 * facing)
    rk, rf, rft = build_leg(r_hip, r_knee, 1.0 * facing)

    def build_arm(sh_a, elb_a):
        a1 = -np.pi / 2 + sh_a
        e_rel = sh_rel + np.array([upper_arm * np.cos(a1), upper_arm * np.sin(a1)])
        a2 = a1 + elb_a
        w_rel = e_rel + np.array([forearm * np.cos(a2), forearm * np.sin(a2)])
        fingers = []
        if show_fingers:
            for deg in (-36.0, -10.0, 16.0, 40.0):
                fa = a2 + np.deg2rad(deg)
                fingers.append((rot_pt(w_rel), rot_pt(w_rel + np.array([0.15 * s * np.cos(fa), 0.15 * s * np.sin(fa)]))))
        return rot_pt(e_rel), rot_pt(w_rel), fingers

    le, lw, l_f = build_arm(l_sh, l_elb)
    re, rw, r_f = build_arm(r_sh, r_elb)

    grp = VGroup()
    h_att = max(0.20, 1.0 - 0.18 * y_jump)
    grp.add(
        Ellipse(width=1.05 * s, height=0.14 * s, stroke_width=0, fill_color=accent_color, fill_opacity=0.25 * h_att)
        .move_to([cx, y_floor - 0.02 * s, 0.0])
    )

    def seg(p0, p1, w=7.0 * s, col=stroke_color):
        ln = Line(p0, p1, color=col, stroke_width=w)
        ln.set_cap_style(CapStyleType.ROUND)
        return ln

    grp.add(seg(hip, lk), seg(lk, lf), seg(lf, lft), seg(hip, rk), seg(rk, rf), seg(rf, rft))
    grp.add(seg(hip, shoulder_pt), seg(shoulder_pt, neck_top_pt))
    grp.add(seg(shoulder_pt, le), seg(le, lw), seg(shoulder_pt, re), seg(re, rw))
    for p0, p1 in l_f + r_f:
        grp.add(seg(p0, p1, w=4.5 * s))

    grp.add(Circle(radius=head_r, color=stroke_color, stroke_width=7.0 * s, fill_color=head_fill, fill_opacity=1.0).move_to(head_pt))

    f_ang = body_spin + head_tilt - body_lean * facing * 0.35
    u_vec = np.array([np.cos(f_ang), np.sin(f_ang), 0.0])
    v_vec = np.array([-np.sin(f_ang), np.cos(f_ang), 0.0])
    for side in (-1.0, 1.0):
        ep = head_pt + u_vec * (side * 0.12 * s + 0.03 * s * facing) + v_vec * (0.07 * s)
        if happy_eyes > 0.5:
            eye = Arc(radius=0.055 * s, start_angle=0.15 * np.pi + f_ang, angle=0.70 * np.pi, color=accent_color, stroke_width=4.5 * s).move_to(ep)
        elif blink > 0.5:
            eye = seg(ep - u_vec * 0.04 * s, ep + u_vec * 0.04 * s, w=4.0 * s, col=accent_color)
        else:
            eye = Dot(ep, radius=0.042 * s, color=accent_color)
        grp.add(eye)

    mouth = Arc(radius=0.11 * s, start_angle=-0.82 * np.pi + f_ang, angle=0.64 * np.pi, color="#F6AD55", stroke_width=4.2 * s).move_to(head_pt - v_vec * 0.05 * s)
    grp.add(mouth)
    return grp


def eval_demo_pose(t):
    p = {
        "cx": -3.0, "y_floor": -2.0, "scale": 1.0, "facing": 1.0, "body_lean": 0.0,
        "y_jump": 0.0, "squash": 0.0, "body_spin": 0.0,
        "l_hip": -0.26, "l_knee": 0.12, "r_hip": 0.26, "r_knee": -0.12,
        "l_sh": -0.85, "l_elb": -0.10, "r_sh": 0.85, "r_elb": 0.10,
        "head_tilt": 0.0, "blink": 1.0 if 1.6 <= t <= 1.76 else 0.0, "happy_eyes": 0.0,
    }
    if t < 1.8:
        w = smoothstep(0.2, 0.6, t) * (1.0 - smoothstep(1.3, 1.7, t))
        p["r_sh"] = lerp(0.85, 1.75, w)
        p["r_elb"] = lerp(0.10, 0.65 + 0.35 * np.sin(9.0 * t), w)
    elif t < 4.4:
        u = smoothstep(1.8, 4.4, t)
        p["cx"] = lerp(-3.0, 2.2, u)
        phase = 9.0 * (t - 1.8)
        fade = np.sin(np.pi * u)
        s1 = np.sin(phase) * fade
        p["body_lean"] = 0.15 * fade
        p["l_hip"] = 0.45 * s1 - 0.26 * (1.0 - fade)
        p["r_hip"] = -0.45 * s1 + 0.26 * (1.0 - fade)
        p["l_sh"] = -0.85 - 0.50 * s1
        p["r_sh"] = 0.85 - 0.50 * s1
        p["y_jump"] = 0.08 * abs(np.sin(phase)) * fade
    elif t < 5.7:
        p["cx"] = 2.2
        u = (t - 4.4) / 1.3
        p["y_jump"] = 2.2 * np.sin(np.pi * u)
        p["body_spin"] = 2 * np.pi * smoothstep(4.5, 5.55, t)
        tuck = np.sin(np.pi * u)
        p["l_knee"] = lerp(0.12, -1.2, tuck)
        p["r_knee"] = lerp(-0.12, -1.2, tuck)
        p["l_sh"] = lerp(-0.85, -1.9, tuck)
        p["r_sh"] = lerp(0.85, 1.9, tuck)
        p["happy_eyes"] = 1.0 if tuck > 0.35 else 0.0
    else:
        p["cx"] = 2.2
        p["squash"] = 0.35 * np.sin(np.pi * smoothstep(5.7, 6.2, t))
    return p


class CharacterRigShowcase(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0D1117"
        floor = Line([-8, -2.0, 0], [8, -2.0, 0], color="#38B2AC", stroke_width=3)
        self.add(floor, self.camera.frame)  # Add camera.frame so updater executes!

        t_tracker = ValueTracker(0.0)
        character = always_redraw(lambda: make_character(**eval_demo_pose(t_tracker.get_value())))
        self.add(character)

        def track_cam(frame, dt):
            pose = eval_demo_pose(t_tracker.get_value())
            alpha = 1.0 - float(np.exp(-3.5 * max(dt, 1e-4)))
            cur = frame.get_center()
            frame.move_to([
                (1.0 - alpha) * cur[0] + alpha * pose["cx"],
                (1.0 - alpha) * cur[1] + alpha * (0.35 * pose["y_jump"]),
                0.0,
            ])

        self.camera.frame.add_updater(track_cam)
        self.play(t_tracker.animate.set_value(6.5), run_time=6.5, rate_func=linear)
