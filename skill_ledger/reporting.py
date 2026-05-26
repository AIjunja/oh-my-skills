from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .scanner import SkillRecord


def build_report(
    records: list[SkillRecord],
    *,
    home: Path | None = None,
    full_paths: bool = False,
) -> dict[str, object]:
    home = Path.home() if home is None else Path(home)
    by_source = dict(sorted(Counter(record.source for record in records).items()))
    by_name: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        by_name[record.name].append(record)

    duplicates = {
        name: [record.to_dict(home=home, full_paths=full_paths) for record in grouped]
        for name, grouped in sorted(by_name.items(), key=lambda item: item[0].lower())
        if len(grouped) > 1
    }
    missing_description = [
        record.to_dict(home=home, full_paths=full_paths)
        for record in records
        if not record.description
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_skills": len(records),
        "by_source": by_source,
        "duplicate_names": duplicates,
        "missing_description": missing_description,
        "skills": [record.to_dict(home=home, full_paths=full_paths) for record in records],
    }


def render_json(report: dict[str, object]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2) + "\n"


def render_markdown(report: dict[str, object]) -> str:
    lines: list[str] = [
        "# oh-my-skills Inventory",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Total skills: `{report['total_skills']}`",
        "",
        "## By Source",
        "",
        "| Source | Count |",
        "| --- | ---: |",
    ]

    by_source = report.get("by_source", {})
    if isinstance(by_source, dict):
        for source, count in by_source.items():
            lines.append(f"| `{escape_markdown(source)}` | {count} |")

    duplicate_names = report.get("duplicate_names", {})
    lines.extend(["", "## Duplicate Names", ""])
    if isinstance(duplicate_names, dict) and duplicate_names:
        lines.extend(["| Name | Copies | Sources |", "| --- | ---: | --- |"])
        for name, copies in duplicate_names.items():
            sources = sorted({str(copy.get("source", "")) for copy in copies if isinstance(copy, dict)})
            lines.append(
                f"| `{escape_markdown(name)}` | {len(copies)} | {escape_markdown(', '.join(sources))} |"
            )
    else:
        lines.append("No duplicate skill names found.")

    missing_description = report.get("missing_description", [])
    lines.extend(["", "## Missing Descriptions", ""])
    if isinstance(missing_description, list) and missing_description:
        lines.extend(["| Name | Source | Path |", "| --- | --- | --- |"])
        for item in missing_description:
            if not isinstance(item, dict):
                continue
            lines.append(
                "| "
                f"`{escape_markdown(str(item.get('name', '')))}"
                " | "
                f"`{escape_markdown(str(item.get('source', '')))}"
                " | "
                f"`{escape_markdown(str(item.get('path', '')))}"
                " |"
            )
    else:
        lines.append("Every scanned skill has a description.")

    lines.extend(
        [
            "",
            "## Skills",
            "",
            "| Name | Source | Description | Path |",
            "| --- | --- | --- | --- |",
        ]
    )
    skills = report.get("skills", [])
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, dict):
                continue
            lines.append(
                "| "
                f"`{escape_markdown(str(item.get('name', '')))}"
                " | "
                f"`{escape_markdown(str(item.get('source', '')))}"
                " | "
                f"{escape_markdown(str(item.get('description', '')))}"
                " | "
                f"`{escape_markdown(str(item.get('path', '')))}"
                " |"
            )

    return "\n".join(lines) + "\n"


def render_doctor(report: dict[str, object]) -> str:
    duplicate_names = report.get("duplicate_names", {})
    missing_description = report.get("missing_description", [])
    duplicate_count = len(duplicate_names) if isinstance(duplicate_names, dict) else 0
    missing_count = len(missing_description) if isinstance(missing_description, list) else 0

    lines = [
        "oh-my-skills Doctor",
        f"- Total skills: {report['total_skills']}",
        f"- Duplicate names: {duplicate_count}",
        f"- Missing descriptions: {missing_count}",
    ]

    if duplicate_count:
        lines.append("")
        lines.append("Duplicate skill names:")
        assert isinstance(duplicate_names, dict)
        for name, copies in duplicate_names.items():
            sources = sorted({str(copy.get("source", "")) for copy in copies if isinstance(copy, dict)})
            lines.append(f"- {name}: {len(copies)} copies ({', '.join(sources)})")

    if missing_count:
        lines.append("")
        lines.append("Skills missing descriptions:")
        assert isinstance(missing_description, list)
        for item in missing_description:
            if isinstance(item, dict):
                lines.append(f"- {item.get('name', '')} ({item.get('source', '')})")

    return "\n".join(lines) + "\n"


def escape_markdown(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
