from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .parser import ScriptParseError, parse_script_file
from .render import DEFAULT_FPS, DEFAULT_HEIGHT, DEFAULT_WIDTH, render_project


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="autovideo", description="Build a local video from a Markdown storyboard.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="parse a Markdown script and render it")
    run.add_argument("script", type=Path, help="path to a Markdown storyboard")
    run.add_argument("-o", "--output", type=Path, help="build directory (default: build/<script-name>)")
    run.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    run.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    run.add_argument("--fps", type=int, default=DEFAULT_FPS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "run":
        output = args.output or Path("build") / args.script.stem
        try:
            project = parse_script_file(args.script)
            report = render_project(project, output, width=args.width, height=args.height, fps=args.fps)
        except (FileNotFoundError, ScriptParseError, ValueError, OSError) as exc:
            print(f"autovideo: error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(report, indent=2))
        if report["status"] == "degraded":
            print(f"autovideo: warning: {report['warning']}", file=sys.stderr)
        return 0
    return 2
