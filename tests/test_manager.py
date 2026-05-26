from pathlib import Path

import pytest

from skill_ledger.manager import SkillManagerError, archive_skill, create_skill, read_skill_content, write_skill_content
from skill_ledger.scanner import skill_id_for_path


def test_create_and_update_claude_skill(tmp_path: Path) -> None:
    record = create_skill(
        "claude-user",
        "My Claude Skill",
        "Helps Claude do a thing.",
        "# My Claude Skill\n\nUse carefully.",
        home=tmp_path,
    )
    skill_id = skill_id_for_path(record.path)
    details = read_skill_content(skill_id, home=tmp_path)

    assert record.source == "claude-user"
    assert details["editable"] is True
    assert "Helps Claude" in str(details["content"])

    updated = str(details["content"]) + "\nExtra notes.\n"
    write_skill_content(skill_id, updated, home=tmp_path)

    assert (tmp_path / ".oh-my-skills" / "backups").exists()
    assert "Extra notes." in record.path.read_text(encoding="utf-8")


def test_archive_moves_editable_skill(tmp_path: Path) -> None:
    record = create_skill("codex-user", "Archive Me", "Temporary skill.", home=tmp_path)
    skill_dir = record.path.parent

    archived_to = archive_skill(skill_id_for_path(record.path), home=tmp_path)

    assert not skill_dir.exists()
    assert archived_to.exists()
    assert (archived_to / "SKILL.md").exists()


def test_plugin_cache_is_read_only(tmp_path: Path) -> None:
    plugin_skill = tmp_path / ".codex" / "plugins" / "cache" / "bundle" / "skills" / "readonly" / "SKILL.md"
    plugin_skill.parent.mkdir(parents=True)
    plugin_skill.write_text("---\nname: readonly\ndescription: Read-only.\n---\n\n# Read-only\n", encoding="utf-8")

    with pytest.raises(SkillManagerError):
        write_skill_content(skill_id_for_path(plugin_skill), "Nope", home=tmp_path)
