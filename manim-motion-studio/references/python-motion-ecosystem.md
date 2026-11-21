# Python Animation, Video Editing & Visualisation Ecosystem

A practical map of verified `pip` packages and external tools for building automated video creation, motion graphics, and editing pipelines—alongside critical compatibility rules so dependency trees never collide.

---

## 1. Recommended Core Stack for an AI Video-Production Agent

| Pipeline Responsibility | Primary `pip` / Tool | Role |
|---|---|---|
| **Explainers, Motion Graphics & UI** | `manim` (ManimCE) | Vector strokes, camera rigs, 2D/3D math, loaders, articulated characters |
| **Manim Add-ons** | `manim-slides`, `manim-physics`, `manim-voiceover` | Interactive slide decks, rigid-body/EM physics, TTS-synced scenes |
| **Fast Cuts, Scaling & Final Encode** | `ffmpeg` + `imageio-ffmpeg` | Cutting, `xfade` transitions, mixed-aspect padding, subtitles, audio ducking |
| **Frame-Exact Media & Timeline** | `av` (PyAV) · `moviepy` (v2+) | Packet/frame access, high-level compositing, dynamic text/image overlays |
| **Shot / Scene Detection** | `scenedetect` (PySceneDetect) | Automatic shot boundary detection & multi-clip splitting |
| **Speech-to-Text & Captions** | `faster-whisper` | Word/segment timestamps for `.srt` captions & edit alignment |
| **Computer Vision & Tracking** | `opencv-python-headless` · `mediapipe` · `scikit-image` | Face/hand/pose tracking, smart vertical reframing, optical flow, inpainting |
| **Audio Analysis & Mixing** | `librosa` · `pydub` · `soundfile` · `pedalboard` | Beat/onset/BPM markers, fades, EQ, compression |
| **Vector, SVG, Lottie & Raster** | `pillow` · `cairosvg` · `svgpathtools` · `lottie` (`python-lottie`) | Thumbnails, captions, SVG rasterisation, Lottie motion conversion |
| **Timing, Easing & State Machines** | `pytweening` · `easing-functions` · `transitions` · `scipy` | Smooth easing curves, splines, character state coordination |
| **Charts & Scientific Animation** | `matplotlib` · `celluloid` · `plotly` · `seaborn` | Data-driven plots & statistical video sequences |
| **2D Sprites & Physics Engines** | `pygame-ce` / `arcade` · `pymunk` · `py5` | Real-time 2D characters, rigid-body collisions, generative sketches |
| **3D Scenes & Meshes** | `bpy` / Blender · `panda3d` · `ursina` · `pyvista` · `trimesh` | Full 3D character rigs, lighting, meshes, point clouds |

---

## 2. Production Combinations by Goal

- **Math / Code / Technical Explainers:** `manim` + `manim-voiceover` (or `manim-slides`) + `ffmpeg`
- **Automated Short-Form / Social Repurposing:** `ffmpeg` + `scenedetect` + `faster-whisper` + `opencv-python-headless` / `mediapipe` + `pillow`
- **UI Loaders, Lottie & Brand Motion:** `manim` + `lottie` + `cairosvg` + `pillow`
- **2D Physics & Character Worlds:** `manim` (or `pygame-ce` + `pymunk`) + `transitions` + `scipy`
- **Data-Driven Stories (from Notion / CSV / APIs):** `manim` or `matplotlib` + `celluloid` + `ffmpeg`
- **3D Product / Architectural Renders:** Blender (`bpy`) or `pyvista` + `ffmpeg`

---

## 3. Critical Compatibility & Installation Rules

1. **Install modularly, never all at once:** GUI (`PySide6`/`PyQt6`), heavy ML (`torch`), and 3D stacks have conflicting transitive dependencies. Use `scripts/setup_manim.sh [core|editing|plugins|vision|audio|notion|full]`.
2. **Choose ONE OpenCV wheel per environment:** Pick `opencv-python-headless` (recommended on servers/containers) — never stack `opencv-python`, `opencv-contrib-python`, and headless wheels together.
3. **Do not mix `manim` and `manimgl`:** Manim Community (`manim`) and 3Blue1Brown's `manimgl` have incompatible imports and APIs.
4. **Do not mix `pygame` and `pygame-ce`:** Both import as `pygame`; pick `pygame-ce` for modern Python 3 builds.
5. **`pip install ffmpeg` is NOT the FFmpeg binary:** Always ensure the `ffmpeg` executable is on `PATH` (via system install or `imageio-ffmpeg` symlink).
6. **`faster-whisper` path-open quirk:** When transcribing extracted audio, pre-decode to a 16 kHz mono `float32` NumPy array via `ffmpeg` and pass the array to `model.transcribe(audio, ...)` to avoid `TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
7. **MoviePy 2.x API changes:** MoviePy 2.x moved/renamed several `moviepy.editor` imports (`from moviepy import VideoFileClip, ...` instead of `moviepy.editor`); prefer direct `ffmpeg` filtergraphs (`scripts/video_edit.py`) for deterministic rendering and multi-clip `xfade`.
8. **`py5` requires Java 17+:** Avoid legacy `Processing.py` (Python 2/Jython); use `py5` with JDK 17+.
