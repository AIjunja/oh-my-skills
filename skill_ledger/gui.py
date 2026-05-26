from __future__ import annotations

import json
import mimetypes
import os
import socket
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .manager import (
    SkillManagerError,
    archive_skill,
    create_skill,
    editable_targets,
    read_skill_content,
    write_skill_content,
)
from .reporting import build_report, render_json, render_markdown
from .scanner import scan_skills


WEB_ROOT = Path(__file__).with_name("web")
DEFAULT_CREATOR_LINKS = [
    {"label": "Threads", "url": "https://www.threads.com/@ai_jjuun"},
    {"label": "Instagram", "url": "https://www.instagram.com/ai_jjuun/"},
    {"label": "YouTube", "url": "https://www.youtube.com/@AI%EC%AD%8C"},
    {"label": "GitHub", "url": "https://github.com/AIjunja"},
]


def run_gui(host: str = "127.0.0.1", port: int = 8765, *, open_browser: bool = True) -> tuple[str, int]:
    chosen_port = find_available_port(host, port)
    server = ThreadingHTTPServer((host, chosen_port), SkillLedgerHandler)
    url = f"http://{host}:{chosen_port}/"
    if open_browser:
        webbrowser.open(url)
    print(f"oh-my-skills GUI running at {url}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\noh-my-skills GUI stopped.")
    finally:
        server.server_close()
    return host, chosen_port


def find_available_port(host: str, start_port: int) -> int:
    if start_port == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, 0))
            return int(sock.getsockname()[1])

    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise OSError(f"No available port found from {start_port} to {start_port + 49}.")


class SkillLedgerHandler(BaseHTTPRequestHandler):
    server_version = "OhMySkills/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/state":
            self.send_json(build_state())
            return
        if parsed.path == "/api/skill":
            query = parse_qs(parsed.query)
            skill_id = first(query.get("id"))
            if not skill_id:
                self.send_error_json(HTTPStatus.BAD_REQUEST, "Missing skill id.")
                return
            try:
                self.send_json(read_skill_content(skill_id))
            except SkillManagerError as error:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(error))
            return
        if parsed.path == "/api/export":
            query = parse_qs(parsed.query)
            export_format = first(query.get("format")) or "markdown"
            report = build_report(scan_skills())
            if export_format == "json":
                self.send_text(render_json(report), "application/json; charset=utf-8")
            else:
                self.send_text(render_markdown(report), "text/markdown; charset=utf-8")
            return
        if parsed.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return
        self.serve_static(parsed.path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/skills":
            try:
                payload = self.read_json_body()
                record = create_skill(
                    str(payload.get("target", "")),
                    str(payload.get("name", "")),
                    str(payload.get("description", "")),
                    str(payload.get("body", "")),
                )
                self.send_json({"skill": record.to_dict()})
            except (SkillManagerError, ValueError) as error:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(error))
            return
        if parsed.path == "/api/skill/archive":
            try:
                payload = self.read_json_body()
                archived_to = archive_skill(str(payload.get("id", "")))
                self.send_json({"archived_to": str(archived_to)})
            except (SkillManagerError, ValueError) as error:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(error))
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "Unknown endpoint.")

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/skill":
            self.send_error_json(HTTPStatus.NOT_FOUND, "Unknown endpoint.")
            return
        query = parse_qs(parsed.query)
        skill_id = first(query.get("id"))
        if not skill_id:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "Missing skill id.")
            return
        try:
            payload = self.read_json_body()
            record = write_skill_content(skill_id, str(payload.get("content", "")))
            self.send_json({"skill": record.to_dict()})
        except (SkillManagerError, ValueError) as error:
            self.send_error_json(HTTPStatus.BAD_REQUEST, str(error))

    def serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in {"/", ""} else request_path.lstrip("/")
        file_path = (WEB_ROOT / relative).resolve()
        if not is_relative_to(file_path, WEB_ROOT.resolve()) or not file_path.exists() or not file_path.is_file():
            self.send_error_json(HTTPStatus.NOT_FOUND, "Not found.")
            return
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        data = self.rfile.read(length).decode("utf-8")
        parsed = json.loads(data)
        if not isinstance(parsed, dict):
            raise ValueError("JSON body must be an object.")
        return parsed

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text: str, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"error": message}, status)

    def log_message(self, format: str, *args: object) -> None:
        return


def build_state() -> dict[str, object]:
    records = scan_skills()
    report = build_report(records)
    report["editable_targets"] = editable_targets()
    cta_url = os.environ.get("OH_MY_SKILLS_CTA_URL") or os.environ.get("SKILL_LEDGER_CTA_URL")
    report["cta"] = {
        "label": os.environ.get("OH_MY_SKILLS_CTA_LABEL")
        or os.environ.get("SKILL_LEDGER_CTA_LABEL", "제작자 구독하기"),
        "url": cta_url or DEFAULT_CREATOR_LINKS[0]["url"],
        "links": DEFAULT_CREATOR_LINKS,
        "note": os.environ.get(
            "OH_MY_SKILLS_CTA_NOTE",
            os.environ.get(
                "SKILL_LEDGER_CTA_NOTE",
                "Follow the creator on Threads, Instagram, YouTube, or GitHub.",
            ),
        ),
    }
    return report


def first(values: list[str] | None) -> str | None:
    if not values:
        return None
    return values[0]


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
