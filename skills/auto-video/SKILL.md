---
name: auto-video
description: Run the repository's local Markdown-to-video workflow when Codex needs to turn a storyboard such as examples/demo-script.md into inspectable scene assets, a manifest, a silent WAV timeline, an optional FFmpeg MP4, and a QA report. Use for requests to build, validate, or iterate on AutoVideo-Agent video pipelines; v0.1 is deterministic and offline, with MiniMax, ComfyUI, TTS, subtitle alignment, and real media providers planned rather than implemented.
---

# AutoVideo Pipeline

Use this skill to operate the AutoVideo-Agent repository honestly and reproducibly.

## Workflow

1. Read AGENTS.md and inspect the target Markdown script before running anything.
2. Confirm the script has a top-level '#' title and one or more '##' scene headings. Scene fields may include duration, visual, and narration.
3. Run autovideo run <script.md> from the repository root. Use --output <dir> when the build must be isolated.
4. Inspect the JSON printed by the CLI and then read <output>/report.json and <output>/manifest.json.
5. Treat status: rendered and a non-null video path as an MP4 success. Treat status: degraded as an intentional partial result: scene PPM assets, the silent WAV, manifest, and report remain useful, but do not claim a video was rendered.
6. When changing core behavior, run python -m pytest and git diff --check before reporting completion.

## v0.1 Boundaries

The shipped renderer creates deterministic placeholder PPM scene cards from scene metadata, a silent WAV timeline, and an H.264/AAC MP4 when FFmpeg is available. It does not call an AI video API, generate speech, align subtitles, or connect to MiniMax, ComfyUI, or real media libraries. Keep those capabilities marked Planned in documentation and issue discussions until code and tests land.

## Agent Request Example

For a request such as:

> Turn examples/demo-script.md into a video and run QA.

execute the CLI, verify the report and manifest, and summarize the actual status, output paths, duration, scene count, and any FFmpeg warning. Do not infer media quality from the visual text; v0.1 does not render that text into an AI-generated scene.
