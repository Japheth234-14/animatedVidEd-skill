#!/usr/bin/env python3
"""Preset-aware Manim render wrapper with automatic imageio-ffmpeg PATH injection."""

import argparse
import os
import shutil
import subprocess
import sys

PRESETS = {
    "landscape": (1920, 1080),
    "portrait": (1080, 1920),   # 9:16 Reels / Shorts / TikTok
    "reel34": (1080, 1440),     # 3:4 Social portrait
    "square": (1080, 1080),     # 1:1 Feed square
}

QUALITY_MAP = {
    "draft": (0.5, 15),   # Half resolution, 15 fps
    "medium": (0.67, 30),
    "high": (1.0, 60),
    "4k": (2.0, 60),
}


def ensure_ffmpeg_in_path(env: dict) -> None:
    if shutil.which("ffmpeg", path=env.get("PATH")):
        return
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Manim scene with aspect/quality presets.")
    parser.add_argument("script", help="Path to the Python file containing the Scene.")
    parser.add_argument("scene", help="Scene class name to render.")
    parser.add_argument("--preset", choices=PRESETS.keys(), default="landscape")
    parser.add_argument("--quality", choices=QUALITY_MAP.keys(), default="high")
    parser.add_argument("--transparent", action="store_true", help="Render with alpha channel (.mov/.webm).")
    parser.add_argument("--gif", action="store_true", help="Output an animated GIF.")
    parser.add_argument("--disable-cache", action="store_true", help="Disable Manim partial movie caching.")
    args = parser.parse_args()

    base_w, base_h = PRESETS[args.preset]
    scale, fps = QUALITY_MAP[args.quality]
    w = max(2, int(round(base_w * scale)) // 2 * 2)
    h = max(2, int(round(base_h * scale)) // 2 * 2)

    cmd = [sys.executable, "-m", "manim", "-r", f"{w},{h}", "--fps", str(fps)]
    if args.transparent:
        cmd.append("-t")
    if args.gif:
        cmd.extend(["--format", "gif"])
    if args.disable_cache:
        cmd.append("--disable_caching")
    cmd.extend([args.script, args.scene])

    env = os.environ.copy()
    ensure_ffmpeg_in_path(env)
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
