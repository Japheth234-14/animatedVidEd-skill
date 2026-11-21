#!/usr/bin/env python3
"""
Video editing & AI-assisted post-production CLI powered by ffmpeg + Python ecosystem.
Core subcommands (ffmpeg only): probe, combine, trim, speed, overlay, mux-audio, duck-audio, burn-subtitles, gif
AI / Analysis subcommands (modular pip extras): detect-scenes, auto-captions, smart-reframe, beat-markers
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

PRESETS = {
    "landscape": (1920, 1080),
    "portrait": (1080, 1920),
    "reel34": (1080, 1440),
    "square": (1080, 1080),
}


def get_env() -> dict:
    env = os.environ.copy()
    if not shutil.which("ffmpeg", path=env.get("PATH")):
        try:
            import imageio_ffmpeg

            exe = imageio_ffmpeg.get_ffmpeg_exe()
            shim_dir = "/tmp/bin"
            os.makedirs(shim_dir, exist_ok=True)
            shim = os.path.join(shim_dir, "ffmpeg")
            if not os.path.exists(shim):
                os.symlink(exe, shim)
            env["PATH"] = f"{shim_dir}:{env.get('PATH', '')}"
        except Exception:
            pass
    if not shutil.which("ffmpeg", path=env.get("PATH")):
        raise RuntimeError(
            "ffmpeg binary not found on PATH and imageio-ffmpeg is not installed. "
            "Run: bash scripts/setup_manim.sh core"
        )
    return env


def probe_clip(path: str, env: dict) -> dict:
    res = subprocess.run(["ffmpeg", "-i", path], capture_output=True, text=True, env=env)
    info = res.stderr
    m_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", info)
    if not m_dur:
        raise RuntimeError(f"Could not parse duration for {path}:\n{info}")
    dur = int(m_dur.group(1)) * 3600 + int(m_dur.group(2)) * 60 + float(m_dur.group(3))
    m_res = re.search(r"Video:.*?,\s*(\d+)x(\d+)", info)
    w, h = (int(m_res.group(1)), int(m_res.group(2))) if m_res else (0, 0)
    m_fps = re.search(r"(\d+(?:\.\d+)?)\s*fps", info)
    fps = float(m_fps.group(1)) if m_fps else 30.0
    has_audio = bool(re.search(r"Stream #.*Audio:", info))
    return {"duration": dur, "width": w, "height": h, "fps": fps, "has_audio": has_audio, "raw": info}


def run_ffmpeg(cmd: list, env: dict) -> int:
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, env=env)


def _fmt_srt_time(sec: float) -> str:
    ms = max(0, int(round(sec * 1000)))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cmd_probe(args, env) -> int:
    for path in args.inputs:
        p = probe_clip(path, env)
        print(
            f"{path}: {p['duration']:.2f}s | {p['width']}x{p['height']} | "
            f"{p['fps']:.2f} fps | audio={'yes' if p['has_audio'] else 'no'}"
        )
    return 0


def cmd_combine(args, env) -> int:
    tw, th = PRESETS[args.preset]
    fps = args.fps
    xfade = max(0.0, args.xfade)
    clips = [probe_clip(p, env) for p in args.inputs]
    if len(clips) == 0:
        raise ValueError("Provide at least one input video.")

    cmd = ["ffmpeg", "-y"]
    for p in args.inputs:
        cmd.extend(["-i", p])

    fc = []
    for idx, c in enumerate(clips):
        same_ar = abs((c["width"] / max(1, c["height"])) - (tw / th)) < 0.02
        if same_ar:
            branch = (
                f"[{idx}:v]scale={tw}:{th}:flags=lanczos,"
                f"fps={fps},settb=1/{fps},format=yuv420p[v{idx}]"
            )
        elif args.bg_mode == "blur":
            branch = (
                f"[{idx}:v]fps={fps},settb=1/{fps},format=yuv420p,split[fg{idx}][bg{idx}];"
                f"[bg{idx}]scale={tw}:{th}:force_original_aspect_ratio=increase,"
                f"crop={tw}:{th},gblur=sigma=35,eq=brightness=-0.18:saturation=0.92[bgb{idx}];"
                f"[fg{idx}]scale={tw}:{th}:force_original_aspect_ratio=decrease[fgs{idx}];"
                f"[bgb{idx}][fgs{idx}]overlay=(W-w)/2:(H-h)/2:shortest=1,"
                f"fps={fps},settb=1/{fps},format=yuv420p[v{idx}]"
            )
        else:
            branch = (
                f"[{idx}:v]scale={tw}:{th}:force_original_aspect_ratio=decrease,"
                f"pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2:color={args.bg_color},"
                f"fps={fps},settb=1/{fps},format=yuv420p[v{idx}]"
            )
        fc.append(branch)

    if len(clips) == 1:
        fc.append("[v0]copy[vout]")
    elif xfade <= 0.0:
        ins = "".join(f"[v{i}]" for i in range(len(clips)))
        fc.append(f"{ins}concat=n={len(clips)}:v=1:a=0,format=yuv420p[vout]")
    else:
        prev = "v0"
        cur_dur = clips[0]["duration"]
        for i in range(1, len(clips)):
            eff_fade = min(xfade, cur_dur * 0.4, clips[i]["duration"] * 0.4)
            offset = max(0.0, cur_dur - eff_fade)
            out_lbl = "vout" if i == len(clips) - 1 else f"x{i}"
            fmt = ",format=yuv420p" if i == len(clips) - 1 else ""
            fc.append(
                f"[{prev}][v{i}]xfade=transition={args.transition}:"
                f"duration={eff_fade:.3f}:offset={offset:.3f}{fmt}[{out_lbl}]"
            )
            cur_dur = offset + clips[i]["duration"]
            prev = out_lbl

    cmd.extend([
        "-filter_complex", ";".join(fc),
        "-map", "[vout]",
        "-c:v", "libx264",
        "-preset", args.encode_preset,
        "-crf", str(args.crf),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        args.output,
    ])
    return run_ffmpeg(cmd, env)


def cmd_trim(args, env) -> int:
    cmd = ["ffmpeg", "-y", "-ss", str(args.start), "-i", args.input]
    if args.end is not None:
        cmd.extend(["-to", str(max(0.01, args.end - args.start))])
    elif args.duration is not None:
        cmd.extend(["-t", str(args.duration)])
    cmd.extend(["-c:v", "libx264", "-crf", str(args.crf), "-c:a", "aac", "-movflags", "+faststart", args.output])
    return run_ffmpeg(cmd, env)


def cmd_speed(args, env) -> int:
    if args.factor <= 0:
        raise ValueError("--factor must be > 0.")
    pts = 1.0 / args.factor
    p = probe_clip(args.input, env)
    cmd = ["ffmpeg", "-y", "-i", args.input]
    if p["has_audio"]:
        rem = args.factor
        atempo = []
        while rem > 2.0:
            atempo.append("atempo=2.0")
            rem /= 2.0
        while rem < 0.5:
            atempo.append("atempo=0.5")
            rem /= 0.5
        atempo.append(f"atempo={rem:.4f}")
        cmd.extend([
            "-filter_complex", f"[0:v]setpts={pts:.5f}*PTS[v];[0:a]{','.join(atempo)}[a]",
            "-map", "[v]", "-map", "[a]", "-c:a", "aac",
        ])
    else:
        cmd.extend(["-vf", f"setpts={pts:.5f}*PTS"])
    cmd.extend(["-c:v", "libx264", "-crf", str(args.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", args.output])
    return run_ffmpeg(cmd, env)


def cmd_overlay(args, env) -> int:
    cmd = [
        "ffmpeg", "-y", "-i", args.base, "-i", args.overlay,
        "-filter_complex", f"[0:v][1:v]overlay={args.x}:{args.y}:eof_action=pass,format=yuv420p[v]",
        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", str(args.crf), "-c:a", "copy",
        "-movflags", "+faststart", args.output,
    ]
    return run_ffmpeg(cmd, env)


def cmd_mux_audio(args, env) -> int:
    vp = probe_clip(args.video, env)
    dur = vp["duration"]
    af = [f"volume={args.volume:.3f}"]
    if args.fade_in > 0:
        af.append(f"afade=t=in:st=0:d={args.fade_in:.2f}")
    if args.fade_out > 0 and dur > args.fade_out:
        af.append(f"afade=t=out:st={dur - args.fade_out:.2f}:d={args.fade_out:.2f}")
    afilter = ",".join(af)

    cmd = ["ffmpeg", "-y", "-i", args.video, "-i", args.audio]
    if vp["has_audio"] and not args.replace:
        cmd.extend([
            "-filter_complex", f"[1:a]{afilter}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]",
        ])
    else:
        cmd.extend(["-filter_complex", f"[1:a]{afilter}[aout]", "-map", "0:v", "-map", "[aout]"])
    cmd.extend(["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args.output])
    return run_ffmpeg(cmd, env)


def cmd_duck_audio(args, env) -> int:
    """Mix voiceover onto video while automatically ducking background music beneath speech."""
    cmd = [
        "ffmpeg", "-y",
        "-i", args.video,
        "-i", args.voice,
        "-i", args.music,
        "-filter_complex",
        (
            f"[1:a]aformat=channel_layouts=stereo,volume={args.voice_volume:.2f},asplit[vo][sc];"
            f"[2:a]aformat=channel_layouts=stereo,volume={args.music_volume:.2f}[bgm];"
            f"[bgm][sc]sidechaincompress=threshold={args.threshold:.4f}:ratio={args.ratio:.1f}:"
            f"attack=25:release=350[ducked];"
            f"[vo][ducked]amix=inputs=2:duration=first:normalize=0[aout]"
        ),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        args.output,
    ]
    return run_ffmpeg(cmd, env)


def cmd_burn_subtitles(args, env) -> int:
    """Burn .srt/.ass captions onto video using ffmpeg subtitles filter."""
    srt_escaped = str(Path(args.srt).resolve()).replace("\\", "\\\\").replace(":", "\\:")
    style = (
        f"FontName={args.font},FontSize={args.font_size},"
        f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,"
        f"MarginV={args.margin_v}"
    )
    cmd = [
        "ffmpeg", "-y", "-i", args.input,
        "-vf", f"subtitles='{srt_escaped}':force_style='{style}'",
        "-c:v", "libx264", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", args.output,
    ]
    return run_ffmpeg(cmd, env)


def cmd_detect_scenes(args, env) -> int:
    """Detect shot boundaries using PySceneDetect and optionally split clips."""
    try:
        from scenedetect import SceneManager, open_video
        from scenedetect.detectors import AdaptiveDetector, ContentDetector
    except ImportError as exc:
        raise RuntimeError("scenedetect not installed. Run: bash scripts/setup_manim.sh editing") from exc

    video = open_video(args.input)
    sm = SceneManager()
    if args.detector == "adaptive":
        sm.add_detector(AdaptiveDetector(adaptive_threshold=args.threshold))
    else:
        sm.add_detector(ContentDetector(threshold=args.threshold))
    sm.detect_scenes(video)
    scenes = sm.get_scene_list()

    records = [
        {
            "scene": idx + 1,
            "start": round(start.get_seconds(), 3),
            "end": round(end.get_seconds(), 3),
            "duration": round(end.get_seconds() - start.get_seconds(), 3),
        }
        for idx, (start, end) in enumerate(scenes)
    ]
    out_json = json.dumps(records, indent=2)
    if args.out:
        Path(args.out).write_text(out_json, encoding="utf-8")
        print(f"Saved {len(records)} detected scenes to {args.out}")
    else:
        print(out_json)

    if args.split_dir and records:
        out_dir = Path(args.split_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for r in records:
            clip_out = out_dir / f"scene_{r['scene']:03d}.mp4"
            run_ffmpeg(
                [
                    "ffmpeg", "-y", "-ss", str(r["start"]), "-i", args.input,
                    "-t", str(max(0.05, r["duration"])),
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", str(clip_out),
                ],
                env,
            )
    return 0


def cmd_auto_captions(args, env) -> int:
    """Transcribe video/audio with faster-whisper via pre-decoded 16 kHz mono PCM."""
    try:
        import numpy as np
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "faster-whisper/numpy not installed. Run: bash scripts/setup_manim.sh editing"
        ) from exc

    with tempfile.NamedTemporaryFile(suffix=".f32", delete=False) as tmp:
        raw_path = tmp.name

    try:
        rc = run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", args.input,
                "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", raw_path,
            ],
            env,
        )
        if rc != 0:
            raise RuntimeError("ffmpeg audio decode failed for auto-captions.")
        audio = np.fromfile(raw_path, dtype=np.float32)
    finally:
        if os.path.exists(raw_path):
            os.remove(raw_path)

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(audio, language=args.language, word_timestamps=args.words)

    srt_lines = []
    json_segs = []
    for idx, seg in enumerate(segments, start=1):
        txt = seg.text.strip()
        srt_lines.append(f"{idx}\n{_fmt_srt_time(seg.start)} --> {_fmt_srt_time(seg.end)}\n{txt}\n")
        item = {"id": idx, "start": round(seg.start, 3), "end": round(seg.end, 3), "text": txt}
        if args.words and getattr(seg, "words", None):
            item["words"] = [
                {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
                for w in seg.words
            ]
        json_segs.append(item)

    Path(args.output).write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"Wrote {len(json_segs)} caption segments ({info.language}) to {args.output}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(json_segs, indent=2), encoding="utf-8")
        print(f"Wrote JSON timestamps to {args.json_out}")
    return 0


def cmd_smart_reframe(args, env) -> int:
    """Subject-aware crop/reframe (e.g. 16:9 -> 9:16) using OpenCV face/motion tracking."""
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise RuntimeError(
            "opencv-python-headless/numpy not installed. Run: bash scripts/setup_manim.sh vision"
        ) from exc

    tw, th = PRESETS[args.preset]
    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {args.input}")

    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    dt = 1.0 / max(1.0, fps)

    crop_h = src_h
    crop_w = int(round(crop_h * (tw / th)))
    if crop_w > src_w:
        crop_w = src_w
        crop_h = int(round(crop_w * (th / tw)))

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cx = src_w / 2.0
    cy = src_h / 2.0
    prev_gray = None

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        raw_vid = tmp.name

    writer = cv2.VideoWriter(raw_vid, cv2.VideoWriter_fourcc(*"mp4v"), fps, (tw, th))
    alpha = 1.0 - math.exp(-args.smoothing * dt)

    try:
        frame_idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            target_x, target_y = cx, cy

            if frame_idx % 3 == 0:
                faces = cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4, minSize=(40, 40))
                if len(faces) > 0:
                    fx, fy, fw, fh = max(faces, key=lambda b: b[2] * b[3])
                    target_x = fx + fw / 2.0
                    target_y = fy + fh / 2.0
                elif prev_gray is not None:
                    diff = cv2.absdiff(gray, prev_gray)
                    _, thresh = cv2.threshold(diff, 22, 255, cv2.THRESH_BINARY)
                    m = cv2.moments(thresh)
                    if m["m00"] > 5000:
                        target_x = m["m10"] / m["m00"]
                        target_y = m["m01"] / m["m00"]
                prev_gray = gray

            cx += (target_x - cx) * alpha
            cy += (target_y - cy) * alpha

            x0 = int(max(0, min(src_w - crop_w, round(cx - crop_w / 2.0))))
            y0 = int(max(0, min(src_h - crop_h, round(cy - crop_h / 2.0))))
            cropped = frame[y0 : y0 + crop_h, x0 : x0 + crop_w]
            resized = cv2.resize(cropped, (tw, th), interpolation=cv2.INTER_AREA)
            writer.write(resized)
            frame_idx += 1
    finally:
        cap.release()
        writer.release()

    # Re-encode with H.264 and preserve original audio if present
    vp = probe_clip(args.input, env)
    if vp["has_audio"]:
        cmd = [
            "ffmpeg", "-y", "-i", raw_vid, "-i", args.input,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-movflags", "+faststart", args.output,
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-i", raw_vid,
            "-c:v", "libx264", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", args.output,
        ]
    try:
        return run_ffmpeg(cmd, env)
    finally:
        if os.path.exists(raw_vid):
            os.remove(raw_vid)


def cmd_beat_markers(args, env) -> int:
    """Detect BPM and beat timestamps from audio/video using librosa (or ffmpeg RMS fallback)."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name

    try:
        rc = run_ffmpeg(
            ["ffmpeg", "-y", "-i", args.input, "-vn", "-ac", "1", "-ar", "22050", wav_path],
            env,
        )
        if rc != 0:
            raise RuntimeError("Failed to extract audio for beat-markers.")

        try:
            import librosa
            y, sr = librosa.load(wav_path, sr=22050, mono=True)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = [round(float(t), 3) for t in librosa.frames_to_time(beat_frames, sr=sr)]
            bpm_val = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
            payload = {"bpm": round(bpm_val, 2), "method": "librosa", "beats": beat_times}
        except ImportError:
            import numpy as np
            import wave
            with wave.open(wav_path, "rb") as wf:
                sr = wf.getframerate()
                pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32)
            hop = int(sr * 0.05)
            rms = np.array([np.sqrt(np.mean(pcm[i : i + hop] ** 2)) for i in range(0, len(pcm) - hop, hop)])
            thresh = float(np.mean(rms) + 1.15 * np.std(rms))
            peaks = [round(i * 0.05, 3) for i in range(1, len(rms) - 1) if rms[i] > thresh and rms[i] >= rms[i - 1] and rms[i] > rms[i + 1]]
            payload = {"bpm": None, "method": "rms-onset-fallback", "beats": peaks}

        out_str = json.dumps(payload, indent=2)
        if args.out:
            Path(args.out).write_text(out_str, encoding="utf-8")
            print(f"Saved {len(payload['beats'])} beat markers to {args.out}")
        else:
            print(out_str)
        return 0
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


def cmd_gif(args, env) -> int:
    vf = f"fps={args.fps},scale={args.width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    return run_ffmpeg(["ffmpeg", "-y", "-i", args.input, "-vf", vf, args.output], env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Video editing & AI post-production toolkit.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_probe = sub.add_parser("probe", help="Inspect video duration, resolution, fps, and audio.")
    p_probe.add_argument("inputs", nargs="+")

    p_comb = sub.add_parser("combine", help="Combine clips with transitions and mixed-aspect framing.")
    p_comb.add_argument("inputs", nargs="+")
    p_comb.add_argument("-o", "--output", required=True)
    p_comb.add_argument("--preset", choices=PRESETS.keys(), default="landscape")
    p_comb.add_argument("--fps", type=int, default=60)
    p_comb.add_argument("--xfade", type=float, default=0.5, help="Crossfade seconds (0 for hard cuts).")
    p_comb.add_argument("--transition", default="fade", help="ffmpeg xfade transition name.")
    p_comb.add_argument("--bg-mode", choices=["blur", "solid"], default="blur")
    p_comb.add_argument("--bg-color", default="#0D1117")
    p_comb.add_argument("--crf", type=int, default=18)
    p_comb.add_argument("--encode-preset", default="medium")

    p_trim = sub.add_parser("trim", help="Trim a clip by timestamps.")
    p_trim.add_argument("input")
    p_trim.add_argument("-o", "--output", required=True)
    p_trim.add_argument("--start", type=float, default=0.0)
    p_trim.add_argument("--end", type=float, default=None)
    p_trim.add_argument("--duration", type=float, default=None)
    p_trim.add_argument("--crf", type=int, default=18)

    p_spd = sub.add_parser("speed", help="Change video playback speed.")
    p_spd.add_argument("input")
    p_spd.add_argument("-o", "--output", required=True)
    p_spd.add_argument("--factor", type=float, required=True)
    p_spd.add_argument("--crf", type=int, default=18)

    p_ov = sub.add_parser("overlay", help="Composite transparent overlay (.mov/.webm) onto base video.")
    p_ov.add_argument("base")
    p_ov.add_argument("overlay")
    p_ov.add_argument("-o", "--output", required=True)
    p_ov.add_argument("--x", default="0")
    p_ov.add_argument("--y", default="0")
    p_ov.add_argument("--crf", type=int, default=18)

    p_mux = sub.add_parser("mux-audio", help="Add or mix audio track with fades.")
    p_mux.add_argument("video")
    p_mux.add_argument("audio")
    p_mux.add_argument("-o", "--output", required=True)
    p_mux.add_argument("--volume", type=float, default=1.0)
    p_mux.add_argument("--fade-in", type=float, default=0.0)
    p_mux.add_argument("--fade-out", type=float, default=0.0)
    p_mux.add_argument("--replace", action="store_true")

    p_duck = sub.add_parser("duck-audio", help="Sidechain-duck background music under voiceover.")
    p_duck.add_argument("video")
    p_duck.add_argument("--voice", required=True)
    p_duck.add_argument("--music", required=True)
    p_duck.add_argument("-o", "--output", required=True)
    p_duck.add_argument("--voice-volume", type=float, default=1.0)
    p_duck.add_argument("--music-volume", type=float, default=0.45)
    p_duck.add_argument("--threshold", type=float, default=0.02)
    p_duck.add_argument("--ratio", type=float, default=6.0)

    p_sub = sub.add_parser("burn-subtitles", help="Burn an .srt subtitle file into video.")
    p_sub.add_argument("input")
    p_sub.add_argument("--srt", required=True)
    p_sub.add_argument("-o", "--output", required=True)
    p_sub.add_argument("--font", default="DejaVu Sans")
    p_sub.add_argument("--font-size", type=int, default=18)
    p_sub.add_argument("--margin-v", type=int, default=36)
    p_sub.add_argument("--crf", type=int, default=18)

    p_sc = sub.add_parser("detect-scenes", help="Detect shot boundaries via PySceneDetect.")
    p_sc.add_argument("input")
    p_sc.add_argument("--detector", choices=["adaptive", "content"], default="adaptive")
    p_sc.add_argument("--threshold", type=float, default=3.0)
    p_sc.add_argument("--out", help="Optional JSON output file")
    p_sc.add_argument("--split-dir", help="Optional directory to split detected scenes into MP4s")

    p_cap = sub.add_parser("auto-captions", help="Generate SRT + JSON timestamps via faster-whisper.")
    p_cap.add_argument("input")
    p_cap.add_argument("-o", "--output", required=True, help="Output .srt file")
    p_cap.add_argument("--json-out", help="Optional .json file with timestamps")
    p_cap.add_argument("--model", default="base")
    p_cap.add_argument("--language", default=None)
    p_cap.add_argument("--device", default="cpu")
    p_cap.add_argument("--compute-type", default="int8")
    p_cap.add_argument("--words", action="store_true")

    p_ref = sub.add_parser("smart-reframe", help="Subject-aware crop/reframe (e.g. 16:9 -> 9:16).")
    p_ref.add_argument("input")
    p_ref.add_argument("-o", "--output", required=True)
    p_ref.add_argument("--preset", choices=PRESETS.keys(), default="portrait")
    p_ref.add_argument("--smoothing", type=float, default=4.0)
    p_ref.add_argument("--crf", type=int, default=18)

    p_beat = sub.add_parser("beat-markers", help="Detect BPM & beat timestamps from audio/video.")
    p_beat.add_argument("input")
    p_beat.add_argument("--out", help="Optional JSON output file")

    p_gif = sub.add_parser("gif", help="Export palette-optimized looping GIF.")
    p_gif.add_argument("input")
    p_gif.add_argument("-o", "--output", required=True)
    p_gif.add_argument("--fps", type=int, default=24)
    p_gif.add_argument("--width", type=int, default=720)

    args = parser.parse_args()
    env = get_env()
    dispatch = {
        "probe": cmd_probe,
        "combine": cmd_combine,
        "trim": cmd_trim,
        "speed": cmd_speed,
        "overlay": cmd_overlay,
        "mux-audio": cmd_mux_audio,
        "duck-audio": cmd_duck_audio,
        "burn-subtitles": cmd_burn_subtitles,
        "detect-scenes": cmd_detect_scenes,
        "auto-captions": cmd_auto_captions,
        "smart-reframe": cmd_smart_reframe,
        "beat-markers": cmd_beat_markers,
        "gif": cmd_gif,
    }
    return dispatch[args.cmd](args, env)


if __name__ == "__main__":
    raise SystemExit(main())
