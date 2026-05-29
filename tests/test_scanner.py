from pathlib import Path

from skill_ledger.reporting import build_report, render_markdown
from skill_ledger.scanner import default_roots, parse_frontmatter, scan_skills


def write_skill(path: Path, *, name: str, description: str = "Useful skill.") -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n\nBody\n",
        encoding="utf-8",
    )


def test_scan_default_roots_classifies_sources(tmp_path: Path) -> None:
    home = tmp_path
    write_skill(home / ".codex" / "skills" / "alpha", name="alpha")
    write_skill(home / ".codex" / "skills" / ".system" / "sys", name="sys")
    write_skill(home / ".agents" / "skills" / "alpha", name="alpha")
    write_skill(home / ".codex" / "plugins" / "cache" / "plugin" / "skills" / "beta", name="beta")

    records = scan_skills(default_roots(home), home=home)
    sources = {(record.name, record.source) for record in records}

    assert ("alpha", "codex-user") in sources
    assert ("alpha", "agents-user") in sources
    assert ("sys", "codex-system") in sources
    assert ("beta", "plugin-cache") in sources


def test_report_finds_duplicates(tmp_path: Path) -> None:
    home = tmp_path
    write_skill(home / ".codex" / "skills" / "same", name="same")
    write_skill(home / ".agents" / "skills" / "same", name="same")

    records = scan_skills(default_roots(home), home=home)
    report = build_report(records, home=home)
    markdown = render_markdown(report)

    assert report["total_skills"] == 2
    assert "same" in report["duplicate_names"]
    assert "~/." in markdown


def test_scan_treats_skill_folder_as_leaf(tmp_path: Path) -> None:
    home = tmp_path
    skills_root = home / ".claude" / "skills"

    # A normal, top-level skill.
    write_skill(skills_root / "autoplan", name="autoplan")

    # A skill that is itself a checkout vendoring per-agent mirrors and a
    # nested copy of every skill (this is exactly how the gstack plugin ships).
    write_skill(skills_root / "gstack", name="gstack")
    write_skill(skills_root / "gstack" / "autoplan", name="autoplan")
    write_skill(
        skills_root / "gstack" / ".cursor" / "skills" / "gstack-autoplan",
        name="autoplan",
    )
    write_skill(
        skills_root / "gstack" / "node_modules" / "pkg" / "skills" / "dep",
        name="dep",
    )

    records = scan_skills(default_roots(home), home=home)
    names = sorted(record.name for record in records)

    # gstack is counted once; nothing nested below a SKILL.md leaks in.
    assert names == ["autoplan", "gstack"]


def test_parse_frontmatter_supports_folded_descriptions() -> None:
    metadata = parse_frontmatter(
        "---\n"
        "name: folded\n"
        "description: >\n"
        "  First line\n"
        "  second line\n"
        "---\n"
        "# Body\n"
    )

    assert metadata["name"] == "folded"
    assert metadata["description"] == "First line second line"
