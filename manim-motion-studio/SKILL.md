---
name: manim-motion-studio
description: Create production-quality 2D/3D animations, motion graphics, camera rigs, stroke-by-stroke drawings, shape morphs, UI loaders, articulated character animations on custom backgrounds, data visualizations, code/diagram explainers, physics simulations, AI-assisted Python video editing (scene detection, Whisper auto-captions, subtitle burn-in, smart vertical reframing, beat markers, audio ducking, xfade combining), and Notion-connected production workflows (scripts, storyboards, database-driven charts, render logging) using Manim Community, ffmpeg, and the modular Python motion ecosystem.
---

# Manim Motion Studio

Build crisp, 60fps programmatic animations, run AI-assisted video editing pipelines, and sync video production with Notion using **Manim Community**, **ffmpeg**, and modular Python media packages.

## Modular Setup (`scripts/setup_manim.sh`)

Install only the profile you need so incompatible GUI, CV, or 3D dependencies never collide:

```bash
bash scripts/setup_manim.sh core     # manim + imageio-ffmpeg + pillow + numpy + scipy
bash scripts/setup_manim.sh editing  # + av, moviepy, scenedetect, opencv-headless, faster-whisper, pydub
bash scripts/setup_manim.sh plugins  # + manim-slides, manim-physics, manim-voiceover
bash scripts/setup_manim.sh vision   # + opencv-python-headless, mediapipe, scikit-image
bash scripts/setup_manim.sh audio    # + librosa, pydub, soundfile, faster-whisper
bash scripts/setup_manim.sh notion   # + notion-client
bash scripts/setup_manim.sh full     # full non-conflicting stack (Manim + AI editing + plugins + Notion)
```

If system `ffmpeg` is missing, `scripts/setup_manim.sh` symlinks `imageio_ffmpeg`'s bundled binary to `/tmp/bin/ffmpeg`, and both `scripts/render.py` and `scripts/video_edit.py` automatically inject it into `PATH`.

> **LaTeX-Free Portability Rule:** Minimal `pip install manim` environments do not include `pdflatex`. Always use `Text` / `MarkupText` for labels and pass `label_constructor=Text` inside `Axes`, `BarChart`, and `ThreeDAxes` (`axis_config={"label_constructor": Text}`) unless you have verified `latex` and `dvisvgm` are installed for `MathTex`/`Tex`.

## Workflow

1. **Pull brief, script, or data from Notion** (via connected Notion app or `scripts/notion_sync.py`) when working from a workspace storyboard or KPI table.
2. **Choose the right Scene class & packages** from the capability matrix below (and `references/python-motion-ecosystem.md` for the quick stack, `references/python-animation-library-catalogue.md` for the full 18-section catalogue).
3. **Start from a verified template** in `templates/` or combine patterns from `references/`.
4. **Preview fast at draft quality** (`--quality draft`) to verify timing, layout, camera tracking, and framing before a full 60fps render.
5. **Render at target aspect ratio** using `scripts/render.py` (never combine `-qh` with custom `-r` dimensions).
6. **Edit, caption, reframe, mix & export** with `scripts/video_edit.py` (`combine`, `detect-scenes`, `auto-captions`, `burn-subtitles`, `smart-reframe`, `beat-markers`, `duck-audio`, `mux-audio`, `overlay`, `trim`, `speed`, `gif`, `probe`).
7. **Visually inspect extracted frames** via `ffmpeg` before delivering the final `.mp4` or `.gif`, and log the render back to Notion.

## Capability Matrix

| Domain | Core Classes, Animations & Tools | Reference / Template |
|---|---|---|
| **Motion Graphics & Camera** | `MovingCameraScene`, `ZoomedScene`, `self.camera.frame`, `LaggedStart`, `MarkupText`, `rate_functions`, layered glow strokes | `references/motion-graphics-camera.md`<br>`templates/motion_graphics_camera.py` |
| **Stroke Drawing & Morphing** | `Create`, `DrawBorderThenFill`, `Write`, `ShowPassingFlash`, `VMobject` Bezier paths, `SVGMobject`, `TransformMatchingShapes`, `Homotopy` | `references/stroke-drawing-morphing.md`<br>`templates/stroke_drawing_morphing.py` |
| **UI Loaders, Micro-Interactions & Showcase Reels** | 20 UI loaders (bouncing ball, liquid fill, skeleton/text shimmer, orbit, spoke/gradient spinners, chasing squares, battery), macOS browser chrome, progressive checklist, 5×4 simultaneous Bento grid | `references/loaders-and-ui-microinteractions.md`<br>`templates/loaders_and_microinteractions.py` |
| **Articulated Characters & Custom Backgrounds** | 2-joint FK/IK character rigs, squash & stretch, blinks/expressions, multi-act `ValueTracker` timelines, `dt`-safe camera tracking, `ImageMobject` paper/desk scenes, background character removal | `references/character-rigging-and-backgrounds.md`<br>`templates/character_rig_scene.py` |
| **3D Scenes & Surfaces** | `ThreeDScene`, `ThreeDAxes`, `Surface`, `move_camera`, `begin_ambient_camera_rotation`, `add_fixed_in_frame_mobjects` | `references/3d-charts-physics-hybrid.md`<br>`templates/three_d_showcase.py` |
| **Data Viz & Charts** | `Axes`, `BarChart`, `NumberPlane`, `AnnularSector`, `get_riemann_rectangles`, `ValueTracker` + `always_redraw` live counters | `references/3d-charts-physics-hybrid.md`<br>`templates/data_viz_dashboard.py` |
| **Code, Math, Physics & Graphs** | `Code`, `Table`, `Brace`, `SurroundingRectangle`, `apply_matrix`, `ComplexPlane`, `ArrowVectorField`, `StreamLines`, `Graph`/`DiGraph`, `add_updater(mob, dt)` | `references/3d-charts-physics-hybrid.md`<br>`templates/math_code_and_diagrams.py` |
| **Hybrid Photo / CV Video** | `ImageMobject` + OpenCV (`cv2.inpaint`, `cv2.remap` `float32`) + MediaPipe `FaceLandmarker`/`HandLandmarker` | `references/3d-charts-physics-hybrid.md` |
| **Broader Python Motion Ecosystem** | `manim-slides`, `manim-physics`, `manim-voiceover`, `av`, `moviepy`, `lottie`, `cairosvg`, `pytweening`, `pymunk`, `transitions`, `bpy`/`pyvista`, compatibility matrix | `references/python-motion-ecosystem.md` |
| **Full Animation Library Catalogue** | 18-section catalogue: math/explainer, 2D/game, creative coding, vector/SVG, video editing, CV/AI, 3D, physics, charts, GUI, storytelling, easing, audio, adjacent tools, pip index, warnings, goal combos, core stack | `references/python-animation-library-catalogue.md` |
| **Video Editing & AI Post-Production** | `scripts/video_edit.py`, `detect-scenes` (`PySceneDetect`), `auto-captions` (`faster-whisper`), `burn-subtitles`, `smart-reframe` (OpenCV tracking), `beat-markers` (`librosa`), `duck-audio`, `xfade` combine, mixed-aspect blurred padding, transparent `.mov` overlays, GIFs | `references/video-editing-postprod.md`<br>`scripts/video_edit.py` |
| **Notion Production Workflows** | Connected Notion app + `scripts/notion_sync.py`: search, read briefs/storyboards, export DB metrics to JSON for Manim charts, create storyboard pages, update statuses, log rendered MP4 metadata, append blocks & comments | `references/notion-video-workflows.md`<br>`scripts/notion_sync.py` |

## Essential Rendering, Video Editing & Notion Commands

### Render Manim Scenes (`scripts/render.py`)

```bash
# Fast draft preview (half-res 15fps)
python3 scripts/render.py templates/character_rig_scene.py CharacterRigShowcase --quality draft

# Full 1080p60 16:9 render
python3 scripts/render.py templates/stroke_drawing_morphing.py StrokeMorphShowcase --quality high

# Portrait 9:16 (1080x1920), 3:4 (1080x1440), or Square 1:1 (1080x1080) at 60fps
python3 scripts/render.py my_scene.py MyScene --preset portrait --quality high
python3 scripts/render.py my_scene.py MyScene --preset square --quality high

# Transparent overlay (.mov with alpha channel for compositing onto video)
python3 scripts/render.py lower_third.py LowerThird --transparent --quality high
```

### Edit, Caption, Reframe & Assemble Videos (`scripts/video_edit.py`)

```bash
# Inspect any video clip
python3 scripts/video_edit.py probe clip1.mp4 clip2.mp4

# Combine mixed-aspect clips with 0.5s crossfades & blurred ambient widescreen padding
python3 scripts/video_edit.py combine clip1.mp4 square_clip.mp4 -o Combined.mp4 --preset landscape --xfade 0.5 --bg-mode blur

# AI editing: shot detection, Whisper auto-captions, subtitle burn-in, smart 9:16 reframe, beat sync, ducking
python3 scripts/video_edit.py detect-scenes raw.mp4 --out scenes.json --split-dir shots/
python3 scripts/video_edit.py auto-captions talk.mp4 -o captions.srt --json-out words.json --words
python3 scripts/video_edit.py burn-subtitles talk.mp4 --srt captions.srt -o captioned.mp4
python3 scripts/video_edit.py smart-reframe wide.mp4 -o reel_9x16.mp4 --preset portrait
python3 scripts/video_edit.py beat-markers music.mp3 --out beats.json
python3 scripts/video_edit.py duck-audio video.mp4 --voice narration.mp3 --music bgm.mp3 -o mixed.mp4

# Trim, speed-ramp, composite transparent Manim overlay, mux audio, or export GIF
python3 scripts/video_edit.py trim in.mp4 -o cut.mp4 --start 2.0 --end 14.5
python3 scripts/video_edit.py speed in.mp4 -o fast.mp4 --factor 1.5
python3 scripts/video_edit.py overlay base.mp4 overlay.mov -o out.mp4
python3 scripts/video_edit.py mux-audio video.mp4 music.mp3 -o final.mp4 --volume 0.35 --fade-out 1.5
python3 scripts/video_edit.py gif final.mp4 -o preview.gif --fps 24 --width 720
```

### Sync with Notion (`scripts/notion_sync.py` or Connected Notion App)

```bash
export NOTION_TOKEN="ntn_..."
python3 scripts/notion_sync.py search "Video Roadmap"
python3 scripts/notion_sync.py read-page <PAGE_ID> --out brief.md
python3 scripts/notion_sync.py query-db <DB_ID> --out metrics.json
python3 scripts/notion_sync.py create-page --parent-db <DB_ID> --title "Launch Reel" --status "Draft" --body-file storyboard.md
python3 scripts/notion_sync.py update-status <PAGE_ID> --prop Status --value "Rendered"
python3 scripts/notion_sync.py log-render <PAGE_ID> --video out.mp4 --notes "1080p60 final"
```

## Critical Gotchas

- **`-qh` resets custom dimensions:** Never pass `-qh` when rendering portrait (`1080x1920`, `1080x1440`) or square (`1080x1080`) scenes; use `scripts/render.py --preset ...` or `-r WIDTH,HEIGHT --fps 60`, and match `self.camera.frame_width` / `frame_height` in `construct()` to the target aspect ratio.
- **Non-conflicting installs only:** Never mix `opencv-python` + `opencv-python-headless`, `pygame` + `pygame-ce`, `manim` + `manimgl`, or `pip install ffmpeg` (use `imageio-ffmpeg` / system binary).
- **`faster-whisper` audio decoding:** Always pre-decode audio to 16 kHz mono `float32` via `ffmpeg` before passing to `WhisperModel.transcribe(...)` (`video_edit.py auto-captions` handles this automatically).
- **`MovingCameraScene` camera updaters:** Always call `self.add(self.camera.frame)` before `self.camera.frame.add_updater(track_cam)`, and use `dt`-based smoothing (`1.0 - np.exp(-k * dt)`) so 15fps drafts and 60fps renders track identically.
- **Spinning character hip anchor:** Never compute `hip_h = -min(l_foot_y, r_foot_y)` while `abs(body_spin) > 0.02`; keep a fixed upright `hip_h` during 360°/720° flips so the head does not dip into the floor.
- **`AnnularSector` center placement:** Pass `arc_center=center` directly rather than `.move_to(center)` (which aligns bounding-box center).
- **`ffmpeg` `xfade` timebases:** Place `fps=60,settb=1/60,format=yuv420p` at the end of *every* input branch (especially after `overlay`) before chaining `xfade`.
- **3D HUD & zero-LaTeX axes:** In `ThreeDScene`, call `self.add_fixed_in_frame_mobjects(...)` for 2D HUD elements; pass `axis_config={"label_constructor": Text}` to `Axes`, `BarChart`, and `ThreeDAxes`.
