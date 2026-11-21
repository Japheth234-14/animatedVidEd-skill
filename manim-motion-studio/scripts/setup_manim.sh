#!/usr/bin/env bash
set -euo pipefail

# Modular bootstrap for Manim Motion Studio + Python Video Editing + Notion Sync.
# Usage: bash scripts/setup_manim.sh [core|editing|plugins|vision|audio|notion|full]
PROFILE="${1:-core}"

echo "Installing core stack (manim + imageio-ffmpeg + pillow + numpy + scipy)..."
pip install --upgrade manim imageio-ffmpeg pillow numpy scipy

case "$PROFILE" in
  core) ;;
  editing)
    echo "Installing AI video-editing stack..."
    pip install --upgrade av moviepy scenedetect opencv-python-headless faster-whisper pydub
    ;;
  plugins)
    echo "Installing Manim plugins (slides, physics, voiceover)..."
    pip install --upgrade manim-slides manim-physics manim-voiceover
    ;;
  vision)
    echo "Installing computer-vision & tracking stack..."
    pip install --upgrade opencv-python-headless mediapipe scikit-image
    ;;
  audio)
    echo "Installing audio analysis & captioning stack..."
    pip install --upgrade librosa pydub soundfile faster-whisper
    ;;
  notion)
    echo "Installing Notion API client..."
    pip install --upgrade notion-client
    ;;
  full)
    echo "Installing full non-conflicting creative + editing + Notion stack..."
    pip install --upgrade \
      av moviepy scenedetect opencv-python-headless mediapipe scikit-image \
      faster-whisper pydub librosa soundfile \
      manim-slides manim-physics manim-voiceover \
      pytweening easing-functions transitions cairosvg lottie \
      notion-client
    ;;
  *)
    echo "Unknown profile: $PROFILE (use: core|editing|plugins|vision|audio|notion|full)" >&2
    exit 1
    ;;
esac

if ! command -v ffmpeg >/dev/null 2>&1; then
  mkdir -p /tmp/bin
  FFMPEG_EXE="$(python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
  ln -sf "$FFMPEG_EXE" /tmp/bin/ffmpeg
  export PATH="/tmp/bin:$PATH"
  echo "Linked bundled ffmpeg at /tmp/bin/ffmpeg"
fi

python3 -c "import manim; print('Ready: Manim', manim.__version__)"
