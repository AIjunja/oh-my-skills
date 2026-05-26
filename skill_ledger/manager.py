from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .scanner import SkillRecord, classify_source, default_roots, is_relative_to, path_from_skill_id, read_skill


EDITABLE_TARGETS = {
    "codex-user": ".codex/skills",
    "claude-user": ".claude/skills",
    "agents-user": ".agents/skills",
}

APP_STATE_DIR = ".oh-my-skills"


class SkillManagerError(ValueError):
    pass


def editable_targets(home: Path | None = None) -> dict[str, str]:
    home = Path.home() if home is None else Path(home)
    return {label: str((home / relative).resolve()) for label, relative in EDITABLE_TARGETS.items()}


def resolve_skill_path(skill_id: str, *, home: Path | None = None) -> Path:
    home = Path.home() if home is None else Path(home)
    path = path_from_skill_id(skill_id).resolve()
    if path.name != "SKILL.md":
        raise SkillManagerError("Only SKILL.md files can be managed.")
    allowed_roots = [root.path.resolve() for root in default_roots(home)]
    if not any(is_relative_to(path, root) for root in allowed_roots):
        raise SkillManagerError("Skill path is outside known skill roots.")
    if not path.exists():
        raise SkillManagerError("Skill file does not exist.")
    return path


def read_skill_content(skill_id: str, *, home: Path | None = None) -> dict[str, object]:
    path = resolve_skill_path(skill_id, home=home)
    record = read_skill(path, home=home)
    return {
        "skill": record.to_dict(home=Path.home() if home is None else Path(home)),
        "content": path.read_text(encoding="utf-8-sig", errors="replace"),
        "editable": is_editable(record, home=home),
    }


def write_skill_content(skill_id: str, content: str, *, home: Path | None = None) -> SkillRecord:
    home = Path.home() if home is None else Path(home)
    path = resolve_skill_path(skill_id, home=home)
    record = read_skill(path, home=home)
    if not is_editable(record, home=home):
        raise SkillManagerError("This skill is read-only.")
    if not content.strip():
        raise SkillManagerError("SKILL.md cannot be empty.")
    backup_file(path, home=home)
    path.write_text(content, encoding="utf-8")
    return read_skill(path, home=home)


def create_skill(
    target: str,
    name: str,
    description: str,
    body: str = "",
    *,
    home: Path | None = None,
) -> SkillRecord:
    home = Path.home() if home is None else Path(home)
    if target not in EDITABLE_TARGETS:
        raise SkillManagerError("Unknown editable target.")
    name = name.strip()
    description = description.strip()
    if not name:
        raise SkillManagerError("Skill name is required.")
    if not description:
        raise SkillManagerError("Skill description is required.")

    root = (home / EDITABLE_TARGETS[target]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    skill_dir = root / slugify(name)
    if skill_dir.exists():
        raise SkillManagerError(f"Skill folder already exists: {skill_dir}")
    skill_dir.mkdir(parents=True)
    skill_path = skill_dir / "SKILL.md"
    skill_path.write_text(render_skill_markdown(name, description, body), encoding="utf-8")
    return read_skill(skill_path, home=home)


def archive_skill(skill_id: str, *, home: Path | None = None) -> Path:
    home = Path.home() if home is None else Path(home)
    path = resolve_skill_path(skill_id, home=home)
    record = read_skill(path, home=home)
    if not is_editable(record, home=home):
        raise SkillManagerError("This skill is read-only.")

    skill_dir = path.parent
    archive_root = home / APP_STATE_DIR / "archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_dir = archive_root / f"{timestamp}-{skill_dir.name}"
    counter = 2
    while archive_dir.exists():
        archive_dir = archive_root / f"{timestamp}-{skill_dir.name}-{counter}"
        counter += 1
    shutil.move(str(skill_dir), str(archive_dir))
    return archive_dir


def backup_file(path: Path, *, home: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = home / APP_STATE_DIR / "backups" / timestamp
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_path = backup_root / path.parent.name / path.name
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)
    return backup_path


def is_editable(record: SkillRecord, *, home: Path | None = None) -> bool:
    home = Path.home() if home is None else Path(home)
    if record.source not in EDITABLE_TARGETS:
        return False
    root = (home / EDITABLE_TARGETS[record.source]).resolve()
    return is_relative_to(record.path.resolve(), root)


def slugify(name: str) -> str:
    lowered = name.strip().lower()
    slug = re.sub(r"[^a-z0-9가-힣._-]+", "-", lowered)
    slug = re.sub(r"-{2,}", "-", slug).strip("-._")
    return slug or "skill"


def render_skill_markdown(name: str, description: str, body: str) -> str:
    body = body.strip() or f"# {name}\n\nDescribe when and how this skill should be used.\n"
    if not body.startswith("#"):
        body = f"# {name}\n\n{body}"
    return (
        "---\n"
        f"name: {yaml_quote(name)}\n"
        f"description: {yaml_quote(description)}\n"
        "---\n\n"
        f"{body.rstrip()}\n"
    )


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
