---
name: oh-my-skills
description: Use when the user wants to install, launch, inspect, inventory, create, edit, archive, deduplicate, or manage local Codex, Claude, or Agent Skills with the oh-my-skills GUI or CLI.
---

# oh-my-skills

oh-my-skills manages local `SKILL.md` folders across Codex, Claude, and generic Agent Skills. It provides a local browser GUI plus CLI reports for skill inventory, duplicate detection, safe editing, creation, and archiving.

## Quick Workflow

1. If this repository is the current workspace, run commands from the repository root.
2. If the user only has the skill installed, use the skill folder as the repository root.
3. Prefer the GUI for interactive management and the CLI for reports or automation.
4. Keep generated inventory files private unless the user explicitly wants to publish them.

## Launch The GUI

From the repository root:

```powershell
python -m skill_ledger gui
```

If the package is installed:

```powershell
oh-my-skills gui
```

The GUI defaults to `http://127.0.0.1:8765/` and auto-increments the port if it is busy. It supports English/Korean UI and light/dark themes.

## CLI Commands

```powershell
python -m skill_ledger scan --format markdown --out inventory\skills.md
python -m skill_ledger scan --format json --out inventory\skills.json
python -m skill_ledger doctor
```

Use forward slashes instead of backslashes on macOS/Linux:

```bash
python -m skill_ledger scan --format markdown --out inventory/skills.md
python -m skill_ledger scan --format json --out inventory/skills.json
python -m skill_ledger doctor
```

## Install As A Skill

Codex:

```bash
git clone https://github.com/AIjunja/-oh-my-skills.git ~/.codex/skills/oh-my-skills
```

Claude:

```bash
git clone https://github.com/AIjunja/-oh-my-skills.git ~/.claude/skills/oh-my-skills
```

Windows PowerShell:

```powershell
git clone https://github.com/AIjunja/-oh-my-skills.git "$env:USERPROFILE\.codex\skills\oh-my-skills"
git clone https://github.com/AIjunja/-oh-my-skills.git "$env:USERPROFILE\.claude\skills\oh-my-skills"
```

## Safety Rules

- Treat `codex-system` and `plugin-cache` skills as read-only.
- Editable user targets are `codex-user`, `claude-user`, and `agents-user`.
- Save operations create a backup under `~/.oh-my-skills/backups`.
- Archive operations move folders to `~/.oh-my-skills/archive`; they do not permanently delete files.
- Keep generated inventory files private unless the user explicitly reviews them for sensitive paths and prompt content.
