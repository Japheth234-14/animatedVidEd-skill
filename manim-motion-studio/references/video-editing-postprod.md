# Video Editing & Post-Production (`ffmpeg` + AI Pipeline)

Use `scripts/video_edit.py` (or direct `ffmpeg` filtergraphs) to assemble, trim, resize, transition, overlay, transcribe, detect scenes, smart-reframe, sync to beats, and mix rendered Manim clips and external videos into polished final deliverables.

---

## 1. Unified CLI (`scripts/video_edit.py`)

`scripts/video_edit.py` automatically resolves `imageio-ffmpeg` when system `ffmpeg` is absent and handles mixed resolutions/framerates safely.

```bash
# Combine multiple clips with 0.5s crossfades into 1920x1080 60fps
# (automatically wraps square/portrait clips in a blurred ambient backdrop)
python3 scripts/video_edit.py combine clip1.mp4 clip2.mp4 clip3.mp4 \
  -o Combined.mp4 --preset landscape --xfade 0.5 --bg-mode blur

# Trim a clip from 4.5s to 18.0s
python3 scripts/video_edit.py trim input.mp4 -o trimmed.mp4 --start 4.5 --end 18.0

# Speed ramp (2.0 = 2x faster, 0.5 = 2x slow motion)
python3 scripts/video_edit.py speed input.mp4 -o fast.mp4 --factor 1.5

# Composite a transparent Manim overlay (.mov from render.py --transparent) onto footage
python3 scripts/video_edit.py overlay base.mp4 hud_overlay.mov -o composited.mp4

# Mix background music or voiceover with fade-in/out
python3 scripts/video_edit.py mux-audio video.mp4 music.mp3 -o final.mp4 --volume 0.35 --fade-out 1.5

# Auto-duck background music beneath voiceover narration
python3 scripts/video_edit.py duck-audio video.mp4 --voice narration.mp3 --music bgm.mp3 -o mixed.mp4

# Auto-transcribe speech -> .srt + word-level JSON (via faster-whisper)
python3 scripts/video_edit.py auto-captions talk.mp4 -o captions.srt --json-out words.json --words

# Burn stylized .srt subtitles directly onto video
python3 scripts/video_edit.py burn-subtitles talk.mp4 --srt captions.srt -o captioned.mp4

# Detect shot cuts (PySceneDetect) and optionally split into separate shot files
python3 scripts/video_edit.py detect-scenes raw.mp4 --out scenes.json --split-dir shots/

# Subject-aware 16:9 -> 9:16 vertical reframe (OpenCV face + motion centroid tracking)
python3 scripts/video_edit.py smart-reframe wide.mp4 -o reel_9x16.mp4 --preset portrait

# Extract BPM + beat timestamps (librosa or RMS fallback) to drive cut/animation timing
python3 scripts/video_edit.py beat-markers music.mp3 --out beats.json

# Export high-quality palette-optimized GIF
python3 scripts/video_edit.py gif input.mp4 -o preview.gif --fps 24 --width 720

# Inspect duration, resolution, fps, and streams
python3 scripts/video_edit.py probe input.mp4
```

---

## 2. Mixing Aspect Ratios Without Harsh Bars

When placing a `1:1` (`1080×1080`) or `9:16` (`1080×1920`) clip inside a `16:9` (`1920×1080`) timeline, generate a blurred, gently darkened ambient extension from the clip itself:

```bash
ffmpeg -i square.mp4 -filter_complex "\
[0:v]fps=60,settb=1/60,format=yuv420p,split[fg][bg]; \
[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=35,eq=brightness=-0.18:saturation=0.92[bgb]; \
[fg]scale=1920:1080:force_original_aspect_ratio=decrease[fgs]; \
[bgb][fgs]overlay=(W-w)/2:(H-h)/2:shortest=1,fps=60,settb=1/60,format=yuv420p" \
-c:v libx264 -crf 18 -movflags +faststart out_16x9.mp4
```

> **Critical `xfade` Rule:** Always place `fps=60,settb=1/60,format=yuv420p` at the **end** of every input branch (especially *after* `overlay`, which outputs timebase `1/1000000`) before chaining `xfade`. Mismatched timebases cause `xfade` to fail with `Invalid argument`.

---

## 3. Multi-Clip Crossfades (`xfade`)

For `N` clips with durations `d_0, d_1, ...` and crossfade duration `D` (e.g. `0.5s`):
- `offset_1 = d_0 - D`
- `offset_k = offset_{k-1} + d_{k-1} - D`
- Total output duration = `sum(d_i) - (N - 1) * D`

Useful `xfade` transitions: `fade`, `wipeleft`, `wiperight`, `slideleft`, `smoothleft`, `circleopen`, `dissolve`.

---

## 4. Transparent Manim Overlays (Lower Thirds, Callouts, Subtitles)

Render titles, animated pointers, or data badges in Manim with alpha transparency, then composite over any live-action or screen-recording video:

```bash
# 1. Render transparent Manim overlay (.mov qtrle / rgba)
python3 scripts/render.py lower_third.py LowerThird --transparent --quality high

# 2. Composite over base footage
python3 scripts/video_edit.py overlay footage.mp4 media/videos/lower_third/1080p60/LowerThird.mov -o final.mp4
```

---

## 5. Audio Mixing, Voiceover Ducking & Social Export

- **Duck music automatically under voiceover (`sidechaincompress`):**
  ```bash
  ffmpeg -i video.mp4 -i voice.mp3 -i music.mp3 -filter_complex "\
  [2:a]volume=0.35,afade=t=in:d=1,afade=t=out:st=58:d=2[bg]; \
  [bg][1:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=250[ducked]; \
  [ducked][1:a]amix=inputs=2:duration=longest[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
  ```
- **Burn-in `.srt` subtitles:**
  ```bash
  ffmpeg -i input.mp4 -vf "subtitles=captions.srt:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'" -c:a copy captioned.mp4
  ```
- **Frame extraction for visual QA:**
  ```bash
  ffmpeg -y -i out.mp4 -ss 12.5 -vframes 1 /tmp/check.jpg
  ```
