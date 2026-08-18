import json
from pathlib import Path

from autovideo.parser import parse_script
from autovideo.render import render_project


def test_render_writes_assets_and_report(tmp_path: Path, monkeypatch):
    project = parse_script("# Test\n## Scene\n- duration: 0.1\n- visual: test")
    monkeypatch.setattr("autovideo.render._find_ffmpeg", lambda: None)
    report = render_project(project, tmp_path / "build", width=32, height=24, fps=2)
    build = tmp_path / "build"
    assert report["status"] == "degraded"
    assert report["video"] is None
    assert (build / "scenes" / "scene-001.ppm").stat().st_size > 32 * 24
    assert (build / "audio-silence.wav").exists()
    manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["scene_count"] == 1


def test_render_with_ffmpeg_creates_video(tmp_path: Path):
    project = parse_script("# Test\n## Scene\n- duration: 0.2\n- visual: test")
    report = render_project(project, tmp_path / "build", width=64, height=48, fps=4)
    if report["ffmpeg"]:
        assert report["status"] == "rendered"
        assert report["video"] and Path(report["video"]).stat().st_size > 0
