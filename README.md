# AutoVideo-Agent

Local-first Markdown-to-video automation for agent workflows.

Write a small storyboard, run one command, and get a deterministic build directory containing a machine-readable manifest, scene assets, a silent timeline, and (when FFmpeg is installed) an MP4. No API key, cloud account, or private media is required for the first version.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
python -m pip install -e .
autovideo run examples/demo-script.md
```

Open `build/demo-script/video.mp4`. The same build also contains `manifest.json`, `report.json`, `scenes/`, and `audio-silence.wav`.

## Script format

```markdown
# My video

## Scene 1: Opening
- duration: 3
- visual: A bright studio desk
- narration: A short spoken line for a future voice provider.
```

Each `##` heading starts a scene. `duration` is in seconds; `visual` and `narration` are preserved in the manifest for later media and TTS providers.

## FFmpeg behavior

FFmpeg is optional. When available, AutoVideo-Agent creates an H.264 MP4 with a silent AAC track. If it is missing or fails, the command exits successfully with `status: degraded`, keeps all scene assets and metadata, and explains the warning in `report.json`.

## Development

```bash
python -m pip install -e .
python -m pytest
```

The project intentionally has no runtime dependencies. Provider integrations such as MiniMax, ComfyUI, and TTS are planned for v0.2.

## Security

Credentials belong in environment variables or a local secret manager. `.gitignore` excludes common credential files; review `git diff` before every commit.

## License

MIT. See [LICENSE](LICENSE).
