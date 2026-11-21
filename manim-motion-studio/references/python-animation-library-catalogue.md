# Python Animation, Motion Graphics, Video Editing and Visualisation Library Catalogue

**A broad, practical catalogue of Python tools for animation and visual production**  
**Compiled:** 21 November 2026

> **Scope note:** There is no finite list of “every animation package on PyPI”. PyPI contains thousands of packages, new projects appear, and many tools are plugins, bindings, applications, or libraries that only handle one part of an animation pipeline. This catalogue brings together the tools mentioned in the original lists, adds important related tools, and distinguishes actual Python packages from external applications and non-Python frameworks. It is intended as a broad reference, not a guarantee that every package is equally maintained, production-ready, or compatible with every Python version.

## How to read this catalogue

- **Pip package** means the name shown is normally installable with `python -m pip install ...`.
- **External application / API** means Python can control or integrate with the application, but the complete application is not simply installed as a normal Python package.
- **Legacy / caution** means the project is older, platform-limited, has a changing maintenance situation, or needs compatibility checks before use.
- **Support tool** means it assists an animation workflow but is not, by itself, a complete animation system.
- The **PyPI name**, **Python import name**, and **command-line executable** can be different. The install examples below refer to package names, not necessarily import names.

---

# 1. Mathematical, scientific and explainer animation

These tools are useful for equations, diagrams, geometry, physics demonstrations, graphs, technical explainers and animated teaching material.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Manim Community Edition (ManimCE)** | `manim` — pip | Programmatic 2D/3D mathematical animation, equations, diagrams, graphs, camera movement and explanatory videos. | The community-maintained edition; usually the best starting point for new Manim projects. |
| **ManimGL / 3Blue1Brown Manim** | `manimgl` — pip | The original 3Blue1Brown-oriented OpenGL-based Manim codebase and workflow. | Separate project from ManimCE. Do not mix installation instructions or code examples between the two. |
| **Manim Physics** | `manim-physics` — pip plugin | Physics-themed Manim scenes, such as mechanics, electromagnetism and waves. | Add-on for Manim; check compatibility with the Manim version you install. |
| **Manim Voiceover** | `manim-voiceover` — pip plugin | Adds recorded or generated narration to Manim scenes and can synchronise animation timing with speech. | Supports integrations with selected TTS services; service extras may be installed separately. |
| **Manim Slides** | `manim-slides` — pip plugin | Turns Manim scenes into step-through presentations and lecture slides. | Works with ManimCE or ManimGL; follow the matching installation instructions. |
| **Matplotlib Animation** | `matplotlib` — pip | Animated plots, line charts, scatter plots, bar charts, scientific visualisations and frame sequences. | Includes `matplotlib.animation.FuncAnimation` and writers for exporting animations. |
| **Celluloid** | `celluloid` — pip | Simplifies capturing Matplotlib figures frame by frame and turning them into animations. | A helper around Matplotlib, not a general-purpose animation engine. |
| **AnimPy / animpy** | `animpy` — pip | Terminal-based text, particle, shape and character-like console animations. | Despite the similar name, this is not a lightweight Manim replacement for rendered HD video. Check the specific project's documentation because similarly named projects can exist. |
| **PyMotion Studio** | `pymotion-studio` — pip | A newer Python-oriented framework advertised for video composition, captions, motion graphics, compositing and rendering. | Emerging option. Review its source-available licence, API maturity, dependencies and suitability for your project before adopting it commercially. |
| **VPython** | `vpython` — pip | Simple interactive 3D physics and science demonstrations using objects such as spheres, boxes and arrows. | Good for interactive teaching and simulation; not a full 3D film-production package. |
| **PyQtGraph** | `pyqtgraph` — pip | Fast, interactive, frequently updating plots and scientific graphics. | Useful for live data and simulation displays; commonly used with Qt. |
| **VisPy** | `vispy` — pip | GPU-accelerated scientific visualisation and interactive 2D/3D graphics. | Particularly useful for large visual datasets and real-time displays. |

Useful references: [Manim Community](https://www.manim.community/), [Manim documentation](https://docs.manim.community/), [ManimGL](https://github.com/3b1b/manim), [Manim Slides](https://www.manim.community/plugin/manim-slides/), [Manim Voiceover](https://www.manim.community/plugin/manim-voiceover/), [Matplotlib animation](https://matplotlib.org/stable/api/animation_api.html).

# 2. 2D animation, sprites, interactive scenes and game-style animation

Use this group for moving characters, sprite sheets, stick figures, game scenes, interactive environments, simple 2D effects and animation controlled by user input.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Pygame** | `pygame` — pip | 2D graphics, sprites, frame loops, keyboard input, sound and game-style animation. | Mature, widely used and flexible. |
| **Pygame-CE** | `pygame-ce` — pip | Community Edition of Pygame with ongoing community development. | Imports as `pygame`. Avoid installing both `pygame` and `pygame-ce` into the same environment unless you know how their files will interact. |
| **Arcade** | `arcade` — pip | Modern 2D game and animation framework with sprites, cameras, tile maps and physics integrations. | Built on modern graphics technology and pyglet. |
| **Pyglet** | `pyglet` — pip | Windowing, sprites, graphics, audio, video playback and OpenGL-based interactive applications. | Useful for visually rich apps and custom real-time animation. |
| **Kivy** | `kivy` — pip | 2D graphics, touch interfaces, animated widgets and cross-platform applications. | Useful when the animation is part of a desktop or mobile application. |
| **KivyMD** | `kivymd` — pip | Material Design widgets for Kivy applications. | UI toolkit built on Kivy, not a separate animation renderer. |
| **py5** | `py5` — pip | Creative coding, drawing, generative visuals, particles and Processing-style animation using modern Python. | Requires Java 17 or newer as well as Python. Stronger choice for new Python creative-coding projects than the old Processing.py mode. |
| **Turtle** | Python standard library | Beginner-friendly drawing and simple movement/animation. | Normally included with Python; do not install it from PyPI. |
| **Tkinter Canvas** | Python standard library | Simple 2D drawings, moving shapes, educational demos and GUI animations. | Normally included with many Python distributions; not designed for complex rendered video. |
| **Asciimatics** | `asciimatics` — pip | Animated terminal interfaces, text effects, console scenes and character-based visuals. | Terminal output rather than normal video graphics. |
| **Pygame-GUI** | `pygame-gui` — pip | Buttons, menus, text boxes and interface elements for Pygame applications. | UI toolkit for Pygame. |
| **Pygame Visual Novel** | Usually custom Pygame code | Dialogue boxes, character sprites, backgrounds and branching story scenes. | This is a development approach, not one single standard package named “Pygame Visual Novel”. |

Useful references: [Pygame](https://www.pygame.org/docs/), [Pygame-CE](https://pyga.me/), [Arcade](https://api.arcade.academy/), [Pyglet](https://docs.pyglet.org/), [Kivy](https://kivy.org/), [py5](https://py5coding.org/).

# 3. Creative coding, generative art and procedural graphics

These tools are useful for abstract motion, particles, patterns, visual experiments, procedural shapes, typography and art generated from code.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **py5** | `py5` — pip | Processing-inspired creative coding in Python 3. | See Section 2; requires Java. |
| **p5 / p5py** | Project name / package: `p5` — pip | A Python port of the Processing API for sketch-based graphics and creative coding. | Do not confuse the Python `p5` project with JavaScript `p5.js`. Check the current project's compatibility and maintenance before choosing it over py5. |
| **Processing.py / Processing Python Mode** | External Processing IDE mode | Older Python-syntax mode for the Processing IDE. | **Legacy / caution:** based on Jython/Python 2-era tooling; reported as unmaintained and incompatible with modern Processing 4 workflows. Prefer py5 for a new Python 3 project. |
| **PyCairo** | `pycairo` — pip | High-quality 2D vector drawing, paths, shapes and text via Cairo. | System Cairo libraries or build dependencies may be required depending on the OS. |
| **cairocffi** | `cairocffi` — pip | Python CFFI bindings for Cairo vector graphics. | Alternative Cairo binding; useful for libraries built around Cairo. |
| **Gizeh** | `gizeh` — pip | A higher-level, simple vector drawing interface built on Cairo. | Often paired with MoviePy to create animated vector scenes. |
| **DrawBot** | External macOS application / Python scripting environment | Vector graphics, typography, posters, layouts and scripted graphic output including movie export. | **Platform-specific:** primarily a macOS application, not a general cross-platform Python animation package. |
| **Noise** | `noise` — pip | Perlin/simplex-style noise values for procedural textures, terrain, clouds, fluid-like movement and organic motion. | A helper for procedural generation, not an animation editor. |
| **NumPy** | `numpy` — pip | Fast arrays and numerical calculations for positions, transforms, pixel operations and simulations. | A foundational dependency used by many animation systems. |
| **SciPy** | `scipy` — pip | Interpolation, signal processing, numerical integration and scientific calculations for motion and simulation. | Support library rather than an animation engine. |

Useful references: [py5](https://py5coding.org/), [p5 Python project](https://github.com/p5py/p5), [PyCairo](https://pycairo.readthedocs.io/), [Gizeh](https://pypi.org/project/gizeh/), [DrawBot](https://drawbot.com/).

# 4. Vector graphics, SVG, typography, drawing and image composition

These packages create or manipulate the artwork that can become animation frames, overlays, titles, lower thirds, logos, icons and visual effects.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Pillow (PIL)** | `pillow` — pip | Drawing text and shapes, compositing images, resizing, masks, filters, thumbnails and frame generation. | One of the most useful general-purpose image tools in a Python video pipeline. |
| **Aggdraw** | `aggdraw` — pip | Antialiased vector-style paths and shapes drawn onto Pillow images. | Useful when Pillow's basic drawing primitives are insufficient. |
| **PyCairo** | `pycairo` — pip | Vector paths, curves, gradients, text and 2D rendering. | Also listed in creative coding. |
| **CairoSVG** | `cairosvg` — pip | Converts SVG files into PNG, PDF, PS and other supported formats. | It is primarily an SVG converter/rasteriser, not a timeline animation system. |
| **svgwrite** | `svgwrite` — pip | Creates SVG vector documents using Python. | Writes SVG; use an SVG renderer or animation technology to produce animated output. |
| **svgpathtools** | `svgpathtools` — pip | Reads, analyses and manipulates SVG paths and Bézier curves. | Useful for path-based motion and geometry. |
| **drawsvg** | `drawsvg` — pip | Creates SVG drawings with Python and can support animated SVG workflows. | Confirm current API and browser/rendering support for the output format you need. |
| **Skia / skia-python** | `skia-python` — pip | High-performance 2D vector and raster graphics, text and compositing. | Useful for advanced drawing and rendering pipelines. |
| **Wand** | `Wand` — pip | Python interface to ImageMagick for image manipulation, effects and conversions. | Requires ImageMagick to be installed separately. |
| **pyvips** | `pyvips` — pip | High-performance image processing for large images and image sequences. | Requires the libvips system library. |
| **python-lottie** | `lottie` — pip | Reads, writes, converts and renders Lottie vector animation files and related sticker formats. | Useful when creating or converting Lottie assets; check licensing before redistributing it in a product. |

Useful references: [Pillow](https://pillow.readthedocs.io/), [CairoSVG](https://cairosvg.org/documentation/), [svgwrite](https://svgwrite.readthedocs.io/), [python-lottie](https://pypi.org/project/lottie/), [Skia Python](https://github.com/kyamagu/skia-python).

# 5. Video editing, compositing, encoding and rendering

These are core tools for cutting long videos into clips, joining footage, adding captions, adding voiceovers, layering graphics, rendering transitions, resizing for social platforms and exporting final MP4 files.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **FFmpeg** | External command-line application | Video/audio encoding, cutting, joining, resizing, cropping, filters, subtitles, overlays, transitions, audio mixing and final rendering. | **Essential external tool.** Install the FFmpeg executable separately; `pip install ffmpeg` is not the same thing. |
| **MoviePy** | `moviepy` — pip | Python-based clip editing, concatenation, text/image overlays, audio mixing, effects and video export. | Convenient high-level API; MoviePy 2.x introduced breaking changes compared with 1.x. |
| **ffmpeg-python** | `ffmpeg-python` — pip | Builds FFmpeg command graphs from Python code. | A wrapper; it still requires the FFmpeg executable. |
| **python-ffmpeg** | `python-ffmpeg` — pip | Another Python interface for constructing and running FFmpeg commands. | Different project from `ffmpeg-python`; choose one wrapper rather than assuming they are interchangeable. |
| **FFmpegIO** | `ffmpegio` — pip | Python interface for FFmpeg media I/O and command execution. | Advanced wrapper; still uses FFmpeg. |
| **PyAV** | `av` — pip | Direct access to media containers, streams, codecs, packets and video/audio frames through FFmpeg libraries. | Better when precise frame- or stream-level control is required. |
| **imageio** | `imageio` — pip | Reads and writes image sequences, GIFs and video through available backends. | General I/O layer, not a full editor. |
| **imageio-ffmpeg** | `imageio-ffmpeg` — pip | FFmpeg binary integration used by imageio and other packages. | Often installed as a dependency; can also be used directly. |
| **OpenCV** | `opencv-python` or `opencv-python-headless` — pip | Frame extraction, image processing, tracking, transformations, detection and computer-vision-based editing. | Use the headless package on servers without a GUI. Do not install multiple OpenCV wheel variants in one environment. |
| **OpenCV Contrib** | `opencv-contrib-python` or `opencv-contrib-python-headless` — pip | OpenCV plus additional/contributed modules. | Choose one OpenCV wheel variant; do not stack the standard and contrib wheels. |
| **scikit-video** | `scikit-video` — pip / GitHub | Video I/O and analysis utilities. | The PyPI release history and GitHub releases can differ; verify the current install route and compatibility before relying on it. |
| **PySceneDetect** | `scenedetect` — pip | Detects scene changes and splits long videos at shot boundaries. | Very useful for automatically finding clip boundaries; supports OpenCV and PyAV backends. |
| **VidGear** | `vidgear` — pip | High-performance video capture, processing and streaming components. | Useful for real-time or threaded video pipelines. |
| **VapourSynth** | `vapoursynth` — pip plus plugins | Scriptable, frame-based video processing, filtering, restoration and rendering. | Powerful specialist video-processing framework; plugin ecosystem and external encoders may be involved. |
| **Decord** | `decord` — pip | Efficient video decoding and random frame access, often for machine-learning workflows. | Useful for loading selected frames from long clips. |
| **MoviePy + Pillow + FFmpeg** | Combination | Programmatic social clips with text, animated captions, images, sound and export. | A practical combination for many automated short-form editing jobs. |

Useful references: [FFmpeg](https://ffmpeg.org/), [MoviePy](https://zulko.github.io/moviepy/), [PyAV](https://pyav.org/docs/), [PySceneDetect](https://www.scenedetect.com/), [VapourSynth](https://www.vapoursynth.com/doc/), [VidGear](https://abhitronix.github.io/vidgear/).

# 6. Computer vision, tracking and visual effects support

These libraries help an AI agent understand video frames and decide what to crop, follow, blur, highlight or transform.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **OpenCV** | `opencv-python` — pip | Object/face detection integrations, feature tracking, optical flow, motion analysis, stabilisation and frame manipulation. | One of the main building blocks for intelligent video editing. |
| **MediaPipe** | `mediapipe` — pip | Face, hand, pose and landmark tracking. | Useful for reframing around a speaker or tracking body movement; available model/task support varies by release. |
| **scikit-image** | `scikit-image` — pip | Image segmentation, filters, morphology, transforms and computer vision. | Complements OpenCV for image analysis. |
| **Kornia** | `kornia` — pip | Differentiable computer vision and image/video transformations built around PyTorch. | Useful in machine-learning-based visual processing. |
| **dlib** | `dlib` — pip where compatible | Face landmarks, detection and traditional computer vision. | Installation can be difficult on some platforms; check wheel availability. |
| **Ultralytics** | `ultralytics` — pip | YOLO-based object detection, segmentation and tracking workflows. | An AI vision framework rather than a general animation library. Check model and licence terms. |
| **PyTorch** | `torch` — pip | Neural-network computation for image/video understanding and generative workflows. | Infrastructure for AI models, not a video editor. |
| **Hugging Face Diffusers** | `diffusers` — pip | Diffusion-model pipelines, including image and selected video-generation workflows. | Model availability, GPU/VRAM needs and licences vary. Not a general-purpose animation editor. |

# 7. 3D modelling, animation, rendering and real-time graphics

This section covers 3D scenes, objects, cameras, materials, lighting, rigs, characters, simulations, rendering and interactive environments.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Blender** | External application; Python API is `bpy` | Full 3D modelling, rigging, character animation, cameras, lighting, materials, particles, simulations, compositing and rendering. | **Most versatile all-round 3D choice.** Blender itself is an application; its Python API controls the application. A PyPI `bpy` distribution is also available for supported versions, but it is version/platform-specific and is not a substitute for understanding Blender's installation requirements. |
| **Panda3D** | `panda3d` — pip | 3D game engine with scene graphs, cameras, animation, models, physics integrations and real-time rendering. | A mature engine usable from Python. |
| **Ursina Engine** | `ursina` — pip | Higher-level 3D engine for interactive worlds, simple games and rapid prototypes. | Built on Panda3D; easier entry point, but not equivalent to Blender's offline film-production tools. |
| **VPython** | `vpython` — pip | Interactive 3D objects and physics demonstrations. | Particularly accessible for teaching and scientific visualisation. |
| **PyOpenGL** | `PyOpenGL` — pip | Python bindings for low-level OpenGL graphics programming. | Powerful but requires more graphics programming knowledge. |
| **ModernGL** | `moderngl` — pip | Modern OpenGL rendering and shader programming from Python. | Often paired with `moderngl-window`. |
| **ModernGL Window** | `moderngl-window` — pip | Window/context and event helpers for ModernGL applications. | Companion package rather than a standalone rendering engine. |
| **VisPy** | `vispy` — pip | GPU-accelerated visualisation and interactive 2D/3D rendering. | Useful for scientific and large-scale visualisation. |
| **Trimesh** | `trimesh` — pip | 3D mesh loading, inspection, transformations, geometry processing and scene handling. | Primarily 3D geometry tooling; pair with a renderer for rendered output. |
| **Pyrender** | `pyrender` — pip | Rendering 3D scenes and meshes, including off-screen rendering. | Often paired with Trimesh. |
| **Open3D** | `open3d` — pip | 3D data processing, point clouds, meshes, reconstruction and visualisation. | Strong for robotics, scanning and 3D computer vision. |
| **VTK** | `vtk` — pip | Advanced 3D scientific visualisation and rendering. | Large, powerful visualisation toolkit. |
| **PyVista** | `pyvista` — pip | Pythonic 3D plotting and mesh visualisation built on VTK. | Convenient interface for engineering and scientific scenes. |
| **Mayavi** | `mayavi` — pip / Conda options | 3D scientific data visualisation and animations. | Installation and GUI/backend compatibility can be more involved than simpler packages. |
| **Vedo** | `vedo` — pip | 3D scientific visualisation, meshes, volumes and animation utilities built around VTK. | Useful for scientific/engineering 3D output. |
| **Harfang3D** | `harfang` — pip / engine distribution | 3D engine and real-time rendering framework with Python bindings. | Smaller ecosystem than Blender or Panda3D; check current package and platform support. |
| **Vapory** | `vapory` — pip plus POV-Ray | Creates POV-Ray scene descriptions from Python and renders them. | Requires POV-Ray separately; a niche route for ray-traced scenes. |
| **PyMOL** | External application; Python API; package availability varies | Molecular visualisation, molecular scenes and scientific animations. | Specialist tool, not a general-purpose 3D animation suite. |
| **pythreejs** | `pythreejs` — pip | Three.js-based 3D visualisation embedded in Jupyter notebooks. | Browser/notebook-oriented and depends on the JavaScript Three.js ecosystem. |
| **ipyvolume** | `ipyvolume` — pip | Interactive 3D plots and volume visualisation inside Jupyter. | Notebook-focused. |

Useful references: [Blender Python API](https://docs.blender.org/api/current/), [Panda3D](https://docs.panda3d.org/), [Ursina](https://www.ursinaengine.org/), [ModernGL](https://moderngl.readthedocs.io/), [Trimesh](https://trimesh.org/), [PyVista](https://pyvista.org/), [Open3D](https://www.open3d.org/).

# 8. Physics engines, simulation and procedural movement

Use these when animation should obey physical rules or be driven by a simulated world rather than manually keyframed positions.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Pymunk** | `pymunk` — pip | 2D rigid-body physics: collisions, gravity, friction, joints and bouncing objects. | Pairs well with Pygame or Arcade. |
| **Box2D / pybox2d** | Often `box2d-py` — pip; bindings vary | 2D physics simulation for games and interactive scenes. | Package and binding variants exist; verify the maintained fork and Python version before installing. |
| **PyBullet** | `pybullet` — pip | 3D rigid-body physics, robotics simulation and articulated bodies. | Useful for physical character/object simulation and robotics. |
| **MuJoCo** | `mujoco` — pip | Fast physics simulation for articulated bodies, robotics and motion research. | More specialised than a simple 2D game physics library. |
| **Taichi** | `taichi` — pip | Parallel/GPU computation for particle systems, fluids, cloth and physical simulations. | Useful for custom high-performance procedural effects and simulations. |
| **Manim Physics** | `manim-physics` — pip plugin | Physics visuals integrated with Manim. | See Section 1. |
| **Noise** | `noise` — pip | Procedural motion, terrain, clouds and organic variation. | Not a physics solver, but helpful for natural-looking movement. |

# 9. Data visualisation and animated charts

These are most useful for business explainers, statistics, dashboards, research videos and data-driven animations.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Matplotlib** | `matplotlib` — pip | Static and animated charts; export as GIF/video or embed in notebooks. | `matplotlib.animation` is the animation module. |
| **Seaborn** | `seaborn` — pip | Statistical plotting; use with Matplotlib to render changing frames. | Not an animation engine itself. |
| **Plotly** | `plotly` — pip | Interactive plots and animations with frame-based chart updates. | Good for browser-based data stories and dashboards. |
| **Bokeh** | `bokeh` — pip | Interactive browser-based data visualisation and streaming plots. | More dashboard-oriented than film-style animation. |
| **Altair** | `altair` — pip | Declarative statistical graphics with interactive/animated chart workflows. | Often used with Vega/Vega-Lite rendering. |
| **Plotnine** | `plotnine` — pip | Grammar-of-graphics plotting inspired by ggplot2. | Typically combine with Matplotlib or frame-generation tools for animation. |
| **PyQtGraph** | `pyqtgraph` — pip | Fast real-time charts and scientific GUI plots. | Best for live data or desktop scientific interfaces. |
| **HoloViews** | `holoviews` — pip | High-level composable visualisations and time-dependent data views. | Often used with Bokeh or Matplotlib backends. |
| **hvPlot** | `hvplot` — pip | High-level interactive plotting for Pandas, Xarray and related data. | Built on HoloViews ecosystem. |
| **bqplot** | `bqplot` — pip | Interactive plotting for Jupyter notebooks. | Notebook-oriented. |

# 10. GUI and application-interface animation

These frameworks are for animated interfaces, controls, menus, transitions and interactive tools. They are not substitutes for a video editor, but they can be used to build the control panel for an AI animation or editing agent.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **PySide6** | `PySide6` — pip | Official Qt for Python bindings; desktop applications, custom graphics and property animations. | Strong choice for professional desktop tooling. |
| **PyQt6** | `PyQt6` — pip | Python bindings for Qt; desktop interfaces and animation via Qt's animation framework. | Review GPL/commercial licensing before building a proprietary app. |
| **Kivy** | `kivy` — pip | Cross-platform touch interfaces and animated widgets. | Also listed in Section 2. |
| **Dear PyGui** | `dearpygui` — pip | GPU-accelerated application interfaces, plots, drawing and interactive tools. | Useful for an internal desktop control panel. |
| **Tkinter** | Python standard library | Basic desktop windows, Canvas drawings and simple transitions. | Included with many Python installations; not normally installed with pip. |
| **CustomTkinter** | `customtkinter` — pip | Modern-looking Tkinter interfaces. | A UI layer, not a full motion-graphics renderer. |
| **Flet** | `flet` — pip | Build cross-platform interfaces in Python with Flutter-backed rendering. | Useful for app interfaces and interactive UI experiences. |
| **PySimpleGUI** | `PySimpleGUI` — pip | Simplified GUI wrapper for Tkinter and related backends. | **Caution:** project licensing and distribution changed over time; verify the current v6 terms and support status before using it in a commercial tool. |
| **wxPython** | `wxPython` — pip | Cross-platform desktop GUI framework. | Can host custom drawing and animated controls. |
| **PyGObject / GTK** | `PyGObject` — pip or OS packages | Python bindings for GTK and related GNOME technologies. | Installation may depend on native system libraries. |
| **Toga** | `toga` — pip | Python-native, OS-native GUI toolkit. | Better for application UI than rendered animation. |
| **NiceGUI** | `nicegui` — pip | Browser-based interfaces built from Python. | Useful for web dashboards and agent controls. |
| **pywebview** | `pywebview` — pip | Embeds a web interface inside a desktop window. | Lets you use HTML/CSS/JavaScript animations in a Python desktop shell. |

# 11. Storytelling, visual novels and character/dialogue animation

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **Ren'Py** | External visual-novel engine with Python scripting | Character sprites, dialogue, scene changes, menus, branching stories and visual-novel effects. | Install Ren'Py as an application/SDK; it is not just a normal pip package. |
| **Pygame** | `pygame` — pip | Build a custom visual novel with sprite animation, dialogue boxes and scene transitions. | Requires you to implement the visual-novel system or use a compatible project framework. |
| **Arcade** | `arcade` — pip | Character and sprite-based story/game scenes. | Better suited to interactive games than conventional visual-novel authoring. |
| **Panda3D / Ursina** | `panda3d` / `ursina` — pip | 3D character scenes and interactive story environments. | Useful when the story needs 3D worlds. |

# 12. Easing, tweening, interpolation and animation timing

These small packages help motion look smooth. They are normally used inside a larger engine rather than producing a complete video by themselves.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **PyTweening** | `pytweening` — pip | Easing curves such as ease-in, ease-out, bounce and elastic movement. | Useful for motion in Pygame, custom renderers and UI systems. |
| **easing-functions** | `easing-functions` — pip | Common mathematical easing functions for interpolating values. | Similar purpose to PyTweening; compare APIs before choosing. |
| **SciPy interpolation** | `scipy` — pip | Interpolation, splines and smooth motion paths. | Useful for precise paths and time-based values. |
| **NumPy** | `numpy` — pip | Vector arithmetic, transforms and per-frame calculations. | Foundational support package. |
| **transitions** | `transitions` — pip | State-machine transitions and callbacks. | Not a tweening library; useful for coordinating animation states such as idle, walking, attacking and jumping. |

# 13. Audio, narration, timing and sound design support

Audio packages are not animation engines, but they are important for synchronising narration, sound effects and music with visuals.

| Tool | Install / type | What it is useful for | Notes |
|---|---|---|---|
| **librosa** | `librosa` — pip | Audio analysis, beats, tempo, onset detection and audio features. | Useful for music-reactive animation and edit timing. |
| **pydub** | `pydub` — pip | Simple audio cutting, joining, fades and format handling. | Usually relies on FFmpeg or avlib for many formats. |
| **soundfile** | `soundfile` — pip | Read and write audio files. | Low-level audio I/O support. |
| **aubio** | `aubio` — pip | Beat, pitch and onset detection. | Useful for syncing visual events to audio. |
| **sounddevice** | `sounddevice` — pip | Audio recording and playback from Python. | Useful for live capture and preview. |
| **pyttsx3** | `pyttsx3` — pip | Offline text-to-speech using available system voices. | Voice quality depends on the operating system and installed voices. |
| **gTTS** | `gTTS` — pip | Text-to-speech using Google Translate's speech service. | Requires network access; review service terms and availability. |
| **Whisper / faster-whisper** | `openai-whisper` or `faster-whisper` — pip | Speech-to-text and word/segment timing for captions. | Not a TTS library; useful for transcription and subtitle alignment. |
| **Coqui TTS ecosystem** | Project/package names and installation route have changed over time | Neural text-to-speech. | Check the current Coqui-maintained project and its installation instructions rather than assuming the older `TTS` package name is the correct current install target. |
| **Pedalboard** | `pedalboard` — pip | Audio effects such as EQ, compression, reverb and filters. | Useful for polishing narration and sound. |

# 14. Adjacent tools that are useful but are not Python animation libraries

These are included because they appeared in the supplied lists or are commonly considered when building an automated production system. They should not be mistaken for native Python animation packages.

| Tool | What it actually is | How it relates to Python |
|---|---|---|
| **Remotion** | React / JavaScript framework for programmatic video creation. | Not a Python library and there is no standard official “Remotion Python port via PyScript”. A Python agent can call a separate Remotion project or service. |
| **Blender** | Full 3D creation application. | Controlled through its Python API (`bpy`) and background-rendering interface. |
| **FFmpeg** | External multimedia command-line framework. | Python can call it directly or through wrappers such as `ffmpeg-python`, `python-ffmpeg` and PyAV. |
| **POV-Ray** | External ray-tracing renderer. | Vapory can generate POV-Ray scenes from Python; POV-Ray itself must be installed. |
| **Processing / Processing.py** | Creative coding IDE and old Python-mode environment. | Processing.py is legacy; use py5 or another current Python graphics framework for a new Python 3 project. |
| **Godot** | Game engine primarily using GDScript, C# and other integrations. | Not a Python animation library. Python integrations/plugins exist but are not the standard workflow. |
| **After Effects** | Commercial motion-graphics and compositing application. | Can be integrated through scripts, plugins, watch folders or external automation; not a Python library. |
| **DaVinci Resolve** | Video editing, colour, audio and compositing application. | Has scripting APIs in supported configurations; not a Python package that replaces the application. |
| **Premiere Pro** | Commercial non-linear video editor. | Can be controlled through supported automation/integration routes, but is not a Python animation library. |

# 15. Quick pip package-name index

The entries below collect the package names in one place. They are **alternatives and components**, not a single environment to install wholesale. Some entries are platform-specific or may need system dependencies. The pip name can differ from the Python import name.

| Area | Pip package names / install identifiers |
|---|---|
| Math / explainer | `manim`, `manimgl`, `manim-physics`, `manim-voiceover`, `manim-slides`, `celluloid`, `animpy`, `pymotion-studio` |
| 2D / game / creative coding | `pygame` **or** `pygame-ce`, `arcade`, `pyglet`, `kivy`, `kivymd`, `py5`, `p5`, `pygame-gui`, `asciimatics`, `noise` |
| Drawing / vector / images | `pillow`, `aggdraw`, `pycairo`, `cairocffi`, `gizeh`, `cairosvg`, `svgwrite`, `svgpathtools`, `drawsvg`, `skia-python`, `Wand`, `pyvips`, `lottie` |
| Video / frame I/O | `moviepy`, `ffmpeg-python`, `python-ffmpeg`, `ffmpegio`, `av`, `imageio`, `imageio-ffmpeg`, `scenedetect`, `vidgear`, `decord`, `scikit-video`, `vapoursynth` |
| Computer vision / AI | Choose one OpenCV wheel: `opencv-python`, `opencv-contrib-python`, `opencv-python-headless` **or** `opencv-contrib-python-headless`; plus `mediapipe`, `scikit-image`, `kornia`, `dlib`, `ultralytics`, `torch`, `diffusers` |
| 3D / rendering | `bpy` (version/platform dependent), `panda3d`, `ursina`, `vpython`, `PyOpenGL`, `moderngl`, `moderngl-window`, `vispy`, `trimesh`, `pyrender`, `open3d`, `vtk`, `pyvista`, `mayavi`, `vedo`, `harfang`, `vapory`, `pythreejs`, `ipyvolume` |
| Physics / simulation | `pymunk`, `box2d-py`, `pybullet`, `mujoco`, `taichi` |
| Charts / data visualisation | `matplotlib`, `plotly`, `bokeh`, `altair`, `plotnine`, `seaborn`, `pyqtgraph`, `holoviews`, `hvplot`, `bqplot` |
| GUI / app interface | `PySide6` **or** `PyQt6`, `dearpygui`, `customtkinter`, `flet`, `PySimpleGUI`, `wxPython`, `PyGObject`, `toga`, `nicegui`, `pywebview` |
| Easing / motion timing | `pytweening`, `easing-functions`, `transitions`, `numpy`, `scipy` |
| Audio / voice / transcription | `librosa`, `pydub`, `soundfile`, `aubio`, `sounddevice`, `pyttsx3`, `gTTS`, `openai-whisper`, `faster-whisper`, `pedalboard` |

Some items above are **not pip packages**: FFmpeg itself, Blender as an application, DrawBot as its macOS app, Processing.py, Ren'Py, Remotion, POV-Ray and Godot. Python standard-library tools such as `tkinter` and `turtle` are also not installed with pip. See the relevant sections above for details.

### Example: install a small starter environment

For a simple automated clipping/editing project, start with a focused environment rather than the entire catalogue:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install av moviepy imageio pillow scenedetect opencv-python faster-whisper
```

Install FFmpeg separately and make sure the executable is accessible on your system PATH. Add Manim, Blender, GUI packages or GPU frameworks only when your workflow needs them.

## 16. Important installation and compatibility warnings

1. **Do not install everything at once.** These projects have different dependency trees. Large GUI, scientific, GPU and video stacks can conflict.
2. **Use a virtual environment.** For example:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
3. **FFmpeg is separate from FFmpeg wrappers.** Install the FFmpeg executable and ensure it is available on PATH, or configure the relevant library to locate it.
4. **Blender is an application.** `bpy` can be installed as a Python distribution for some supported versions, but scripts that use the full application API may need to run using Blender's own Python environment or Blender in background mode.
5. **ManimCE and ManimGL are separate implementations.** Choose one first and follow its own installation and examples.
6. **Pygame and Pygame-CE overlap.** Choose one per environment.
7. **OpenCV wheel variants overlap.** Choose one of `opencv-python`, `opencv-contrib-python`, `opencv-python-headless` or `opencv-contrib-python-headless` for an environment.
8. **py5 needs Java.** Installing the Python package alone is not enough; py5 currently documents Java 17+ as a requirement.
9. **Processing.py is legacy.** Do not choose it for a new Python 3 animation system; look at py5 instead.
10. **Check commercial licensing.** This matters especially for PyQt, PyMotion Studio, AI models, model weights, fonts, stock media and some specialised frameworks.
11. **Confirm current support before deployment.** Check the project's official documentation, release history, supported Python versions and operating-system wheels before making it a production dependency.

## 17. Suggested combinations by production goal

| Production goal | Suggested starting combination |
|---|---|
| Mathematical explainers | ManimCE + Manim Voiceover + FFmpeg |
| Scientific plots and animated charts | Matplotlib + Celluloid + FFmpeg |
| 2D animated characters / stick figures | Pygame-CE or Arcade + Pymunk + Pillow + FFmpeg |
| Abstract generative motion graphics | py5 or Pygame + NumPy + Pillow / Cairo + FFmpeg |
| Professional 3D animation and visual effects | Blender + `bpy` + FFmpeg |
| Interactive 3D simulations | Panda3D or Ursina + PyBullet / MuJoCo |
| Automated short-form video editing | FFmpeg + MoviePy or PyAV + OpenCV + PySceneDetect + Pillow |
| Animated captions and typography | MoviePy or FFmpeg + Pillow / SVG tools + Whisper transcription |
| Lottie assets and vector motion | python-lottie + SVG tools + CairoSVG / browser renderer |
| AI-assisted video understanding | OpenCV + PySceneDetect + MediaPipe / Ultralytics + PyAV |
| Desktop interface for a video agent | PySide6 or Dear PyGui + FFmpeg / MoviePy backend |
| Browser-based programmatic video | Remotion (JavaScript) called by a Python orchestration service |

## 18. Recommended core stack for an AI video-production agent

For an agent that needs to inspect long videos, find interesting moments, extract clips, crop/reframe, create captions, add narration, generate graphics and render final versions, a practical core stack is:

| Pipeline responsibility | Recommended tool | Why |
|---|---|---|
| Media decoding and exact frame/time access | **PyAV** | Fine-grained access to streams, timestamps and frames. |
| Fast media operations and final encoding | **FFmpeg** | Reliable cutting, filters, audio mixing, subtitles, scaling and export. |
| Shot/scene boundary detection | **PySceneDetect** | Finds scene changes that can support automatic clip segmentation. |
| Visual analysis and tracking | **OpenCV** | Face/object tracking, optical flow, cropping and frame analysis. |
| Speech transcription and timestamps | **Whisper / faster-whisper** | Produces transcript segments for captions and content analysis. |
| Caption and graphic asset creation | **Pillow + SVG tools** | Builds branded captions, labels, logos and overlays. |
| Timeline/composition logic | **MoviePy** or a custom FFmpeg graph | High-level composition or more precise low-level control. |
| Animated explainer inserts | **ManimCE** | Creates diagrams, equations and technical animations. |
| 3D scenes and effects | **Blender** | Handles advanced 3D, compositing and rendering. |
| Audio processing | **pydub / librosa / FFmpeg** | Trimming, fades, mixing, beat detection and timing. |

The best architecture is usually **not one giant Python package**. Let the AI agent plan the edit and call specialised tools through clear interfaces. Use FFmpeg for the final media operations, and reserve Manim or Blender for the scenes they are particularly good at creating.

---

# Reference links and verification notes

The links below point to project documentation, package pages or official project material. They are a starting point for checking current installation requirements and supported versions.

- [Manim Community documentation](https://docs.manim.community/)
- [Manim Community on PyPI](https://pypi.org/project/manim/)
- [ManimGL on PyPI](https://pypi.org/project/manimgl/)
- [Manim Slides](https://www.manim.community/plugin/manim-slides/)
- [Manim Voiceover](https://www.manim.community/plugin/manim-voiceover/)
- [Matplotlib animation documentation](https://matplotlib.org/stable/api/animation_api.html)
- [MoviePy documentation](https://zulko.github.io/moviepy/)
- [FFmpeg documentation](https://ffmpeg.org/documentation.html)
- [PyAV documentation](https://pyav.org/docs/)
- [PySceneDetect documentation](https://www.scenedetect.com/docs/)
- [VapourSynth documentation](https://www.vapoursynth.com/doc/)
- [Pygame documentation](https://www.pygame.org/docs/)
- [Pyglet documentation](https://docs.pyglet.org/)
- [Arcade documentation](https://api.arcade.academy/)
- [Kivy documentation](https://kivy.org/doc/stable/)
- [py5 documentation](https://py5coding.org/)
- [p5 Python project](https://github.com/p5py/p5)
- [Blender Python API](https://docs.blender.org/api/current/)
- [Panda3D documentation](https://docs.panda3d.org/)
- [ModernGL documentation](https://moderngl.readthedocs.io/)
- [Trimesh documentation](https://trimesh.org/)
- [PyVista documentation](https://pyvista.org/)
- [Open3D documentation](https://www.open3d.org/docs/)
- [Dear PyGui documentation](https://dearpygui.readthedocs.io/)
- [Qt for Python / PySide6](https://doc.qt.io/qtforpython-6/)
- [PyQt6 on PyPI](https://pypi.org/project/PyQt6/)
- [CairoSVG documentation](https://cairosvg.org/documentation/)
- [python-lottie on PyPI](https://pypi.org/project/lottie/)
- [PyMotion Studio on PyPI](https://pypi.org/project/pymotion-studio/)
- [DrawBot documentation](https://drawbot.com/)

**Final reminder:** Treat this as a curated ecosystem map. Before installing a package, inspect its current official docs, PyPI release history, licence, supported Python versions and platform requirements. A package being available on PyPI does not automatically make it a good choice for production.
