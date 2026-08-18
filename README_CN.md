# AutoVideo-Agent

面向 Agent 工作流的本地优先 Markdown 转视频工具。

写一份简短分镜，执行一条命令即可得到确定性的构建目录：结构化 manifest、逐场景画面、静音时间轴，以及在安装 FFmpeg 时生成的 MP4。v0.1.0 不需要 API Key、云账号或私有素材。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
autovideo run examples/demo-script.md
```

打开 `build/demo-script/video.mp4`。同一目录还包含 `manifest.json`、`report.json`、`scenes/` 和 `audio-silence.wav`。

## 分镜格式

每个二级标题 `##` 开始一个场景；`duration` 为秒数，`visual` 和 `narration` 会原样保存到 manifest，供后续素材与 TTS provider 使用。

## FFmpeg 降级

FFmpeg 是可选项。找不到或执行失败时，工具仍会生成全部画面与元数据，输出 `status: degraded`，并在 `report.json` 中写明原因。

## 版本路线

v0.2 计划接入 MiniMax、ComfyUI 和 TTS；第一版先保证一键运行、可测试和可审查。

## 许可证

MIT，见 [LICENSE](LICENSE)。
