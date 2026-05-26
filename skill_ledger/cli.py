from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

from .gui import run_gui
from .reporting import build_report, render_doctor, render_json, render_markdown
from .scanner import scan_skills


def main(argv: Sequence[str] | None = None) -> int:
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return run_scan(args)
    if args.command == "doctor":
        return run_doctor(args)
    if args.command == "gui":
        run_gui(args.host, args.port, open_browser=not args.no_open)
        return 0

    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oh-my-skills",
        description="Inventory local SKILL.md files for Codex and agent skills.",
    )
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan skill folders and render an inventory.")
    add_common_scan_options(scan_parser)
    scan_parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format. Defaults to markdown.",
    )
    scan_parser.add_argument("--out", type=Path, help="Write output to a file instead of stdout.")

    doctor_parser = subparsers.add_parser("doctor", help="Print duplicate and metadata warnings.")
    add_common_scan_options(doctor_parser)

    gui_parser = subparsers.add_parser("gui", help="Start the local browser GUI.")
    gui_parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Defaults to 127.0.0.1.")
    gui_parser.add_argument("--port", type=int, default=8765, help="Port to bind. Auto-increments if busy.")
    gui_parser.add_argument("--no-open", action="store_true", help="Do not open the browser automatically.")

    return parser


def add_common_scan_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Root folder to scan. Can be passed multiple times. Defaults to known Codex/agent roots.",
    )
    parser.add_argument(
        "--full-paths",
        action="store_true",
        help="Show absolute paths instead of replacing the home directory with ~.",
    )


def run_scan(args: argparse.Namespace) -> int:
    records = scan_skills(args.root)
    report = build_report(records, full_paths=args.full_paths)
    output = render_json(report) if args.format == "json" else render_markdown(report)
    write_output(output, args.out)
    return 0


def run_doctor(args: argparse.Namespace) -> int:
    records = scan_skills(args.root)
    report = build_report(records, full_paths=args.full_paths)
    output = render_doctor(report)
    write_output(output, None)
    return 1 if report["duplicate_names"] or report["missing_description"] else 0


def write_output(output: str, out_path: Path | None) -> None:
    if out_path is None:
        try:
            sys.stdout.write(output)
            sys.stdout.flush()
        except (BrokenPipeError, OSError):
            sys.stdout = open(os.devnull, "w", encoding="utf-8")
            return
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
