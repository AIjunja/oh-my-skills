from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Iterable


@dataclass(frozen=True)
class ScanRoot:
    label: str
    path: Path


@dataclass(frozen=True)
class SkillRecord:
    name: str
    description: str
    title: str
    source: str
    path: Path
    size_bytes: int
    modified_at: str
    sha256: str

    def to_dict(self, *, home: Path | None = None, full_paths: bool = False) -> dict[str, object]:
        path = str(self.path)
        if home is not None and not full_paths:
            path = home_relative_path(self.path, home)
        return {
            "id": skill_id_for_path(self.path),
            "name": self.name,
            "description": self.description,
            "title": self.title,
            "source": self.source,
            "path": path,
            "size_bytes": self.size_bytes,
            "modified_at": self.modified_at,
            "sha256": self.sha256,
        }


def default_roots(home: Path | None = None) -> list[ScanRoot]:
    home = Path.home() if home is None else Path(home)
    return [
        ScanRoot("codex-skills", home / ".codex" / "skills"),
        ScanRoot("claude-skills", home / ".claude" / "skills"),
        ScanRoot("agents-skills", home / ".agents" / "skills"),
        ScanRoot("codex-plugin-cache", home / ".codex" / "plugins" / "cache"),
    ]


def scan_skills(
    roots: Iterable[ScanRoot | Path | str] | None = None,
    *,
    home: Path | None = None,
) -> list[SkillRecord]:
    home = Path.home() if home is None else Path(home)
    normalized_roots = _normalize_roots(default_roots(home) if roots is None else roots)
    seen_paths: set[Path] = set()
    records: list[SkillRecord] = []

    for root in normalized_roots:
        if not root.path.exists():
            continue
        for skill_path in sorted(root.path.rglob("SKILL.md"), key=lambda item: str(item).lower()):
            resolved = skill_path.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            records.append(read_skill(skill_path, home=home, fallback_source=root.label))

    return sorted(records, key=lambda item: (item.name.lower(), item.source, str(item.path).lower()))


def read_skill(path: Path, *, home: Path | None = None, fallback_source: str = "unknown") -> SkillRecord:
    home = Path.home() if home is None else Path(home)
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    metadata = parse_frontmatter(text)
    stat = path.stat()
    digest = sha256(path.read_bytes()).hexdigest()
    name = str(metadata.get("name") or path.parent.name).strip()
    description = str(metadata.get("description") or "").strip()
    title = first_heading(text)
    modified_at = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()

    return SkillRecord(
        name=name,
        description=description,
        title=title,
        source=classify_source(path, home=home, fallback=fallback_source),
        path=path.resolve(),
        size_bytes=stat.st_size,
        modified_at=modified_at,
        sha256=digest,
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}

    metadata: dict[str, str] = {}
    frontmatter = lines[1:end]
    index = 0
    while index < len(frontmatter):
        line = frontmatter[index]
        if not line.strip() or line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if value in {">", "|"}:
            block: list[str] = []
            index += 1
            while index < len(frontmatter):
                next_line = frontmatter[index]
                if next_line and not next_line.startswith((" ", "\t")) and ":" in next_line:
                    break
                block.append(next_line.strip())
                index += 1
            metadata[key] = "\n".join(block).strip() if value == "|" else " ".join(block).strip()
            continue

        metadata[key] = _strip_quotes(value)
        index += 1

    return metadata


def first_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def classify_source(path: Path, *, home: Path, fallback: str = "unknown") -> str:
    resolved = path.resolve()
    roots = [
        ("codex-system", home / ".codex" / "skills" / ".system"),
        ("plugin-cache", home / ".codex" / "plugins" / "cache"),
        ("claude-user", home / ".claude" / "skills"),
        ("agents-user", home / ".agents" / "skills"),
        ("codex-user", home / ".codex" / "skills"),
    ]
    for label, root in roots:
        if is_relative_to(resolved, root.resolve()):
            return label
    return fallback


def home_relative_path(path: Path, home: Path) -> str:
    resolved = path.resolve()
    home = home.resolve()
    if is_relative_to(resolved, home):
        return "~/" + resolved.relative_to(home).as_posix()
    return str(resolved)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _normalize_roots(roots: Iterable[ScanRoot | Path | str]) -> list[ScanRoot]:
    normalized: list[ScanRoot] = []
    for root in roots:
        if isinstance(root, ScanRoot):
            normalized.append(ScanRoot(root.label, Path(root.path).expanduser()))
        else:
            path = Path(root).expanduser()
            normalized.append(ScanRoot(path.name or "custom-root", path))
    return normalized


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def skill_id_for_path(path: Path) -> str:
    encoded = urlsafe_b64encode(str(path.resolve()).encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")


def path_from_skill_id(skill_id: str) -> Path:
    padding = "=" * (-len(skill_id) % 4)
    decoded = urlsafe_b64decode((skill_id + padding).encode("ascii")).decode("utf-8")
    return Path(decoded)
