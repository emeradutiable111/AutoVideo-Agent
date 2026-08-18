from __future__ import annotations

import json
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from .models import Project, Scene


DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_FPS = 30


def _hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        return (23, 32, 51)
    return tuple(int(value[offset : offset + 2], 16) for offset in (0, 2, 4))


def _write_ppm(path: Path, scene: Scene, width: int, height: int) -> None:
    """Write a dependency-free scene card that every FFmpeg build can decode."""

    base = _hex_rgb(scene.color)
    accent = tuple(min(255, int(channel * 0.55 + 110)) for channel in base)
    stripe_width = max(1, width // 9)
    with path.open("wb") as handle:
        handle.write(f"P6\n{width} {height}\n255\n".encode("ascii"))
        row = bytearray(width * 3)
        for y in range(height):
            for x in range(width):
                diagonal = ((x + y) // stripe_width) % 2 == 0
                edge = x < width * 0.035 or x > width * 0.965 or y < height * 0.06 or y > height * 0.94
                color = accent if diagonal else base
                if edge:
                    color = tuple(min(255, channel + 24) for channel in color)
                offset = x * 3
                row[offset : offset + 3] = bytes(color)
            handle.write(row)


def _write_silence(path: Path, duration: float, sample_rate: int = 48000) -> None:
    frames = max(1, round(duration * sample_rate))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(b"\x00\x00" * 2 * frames)


def _find_ffmpeg() -> str | None:
    configured = shutil.which("ffmpeg")
    return configured


def _run_ffmpeg(ffmpeg: str, concat_file: Path, audio_file: Path, output_file: Path, fps: int) -> tuple[bool, str]:
    command = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-i",
        str(audio_file),
        "-r",
        str(fps),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode == 0:
        return True, ""
    detail = (result.stderr or result.stdout).strip().splitlines()
    return False, detail[-1] if detail else f"FFmpeg exited with code {result.returncode}"


def render_project(
    project: Project,
    output_dir: str | Path,
    *,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    fps: int = DEFAULT_FPS,
) -> dict[str, Any]:
    """Render a project and return a JSON-serializable build report."""

    if width < 16 or height < 16 or fps < 1:
        raise ValueError("width and height must be at least 16, and fps must be positive")
    output = Path(output_dir)
    scenes_dir = output / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    scene_files: list[Path] = []
    for scene in project.scenes:
        scene_path = scenes_dir / f"scene-{scene.index:03d}.ppm"
        _write_ppm(scene_path, scene, width, height)
        scene_files.append(scene_path)

    manifest = output / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "autovideo_version": "0.1.0",
                "render": {"width": width, "height": height, "fps": fps},
                **project.to_dict(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    concat_file = output / "scenes.txt"
    concat_lines: list[str] = []
    for scene_path, scene in zip(scene_files, project.scenes):
        # concat demuxer paths use forward slashes on all platforms.
        concat_lines.extend([f"file '{scene_path.resolve().as_posix()}'", f"duration {scene.duration:.6f}"])
    concat_lines.append(f"file '{scene_files[-1].resolve().as_posix()}'")
    concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    audio_file = output / "audio-silence.wav"
    _write_silence(audio_file, project.duration)

    video_file = output / "video.mp4"
    ffmpeg = _find_ffmpeg()
    status = "rendered"
    error = None
    if ffmpeg:
        success, error = _run_ffmpeg(ffmpeg, concat_file, audio_file, video_file, fps)
        if not success:
            status = "degraded"
            video_file = None
    else:
        status = "degraded"
        error = "FFmpeg was not found; generated scene assets and manifest only"
        video_file = None
    report: dict[str, Any] = {
        "status": status,
        "title": project.title,
        "duration": project.duration,
        "scene_count": len(project.scenes),
        "output_dir": str(output.resolve()),
        "manifest": str(manifest.resolve()),
        "video": str(video_file.resolve()) if video_file and video_file.exists() else None,
        "audio": str(audio_file.resolve()),
        "ffmpeg": ffmpeg,
        "warning": error,
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
