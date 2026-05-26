# oh-my-skills

[한국어 README](README.ko.md)

Local GUI and CLI for managing `SKILL.md` folders across Codex, Claude, and
generic Agent Skills.

oh-my-skills answers a very simple question:

> "What skills are installed on this machine, and which ones can I safely edit?"

It scans local skill directories, shows duplicates, lets you inspect and edit
user-owned skills, and keeps system/plugin skills read-only.

## Features

- Local browser GUI: search, filter, inspect, edit, create, and archive skills.
- English/Korean GUI toggle.
- Light/dark GUI theme toggle with the same mono README-style interface.
- CLI inventory: export Markdown or JSON reports.
- Duplicate detection across Codex, Claude, Agents, and plugin cache skills.
- Safe editing: backs up `SKILL.md` before saving.
- Safe cleanup: archives user skills instead of permanently deleting them.
- Local-first: runs on `127.0.0.1`; no account, cloud sync, database, or telemetry.
- Dependency-light: Python standard library only.

## What It Scans

By default, oh-my-skills scans:

| Source | Path | Edit Mode |
| --- | --- | --- |
| `codex-user` | `~/.codex/skills` | Editable |
| `claude-user` | `~/.claude/skills` | Editable |
| `agents-user` | `~/.agents/skills` | Editable |
| `codex-system` | `~/.codex/skills/.system` | Read-only |
| `plugin-cache` | `~/.codex/plugins/cache` | Read-only |

## Quick Start

### Run From Source

```bash
git clone https://github.com/AIjunja/oh-my-skills.git
cd oh-my-skills
python -m skill_ledger gui
```

Open the printed local URL. By default:

```text
http://127.0.0.1:8765/
```

If port `8765` is busy, oh-my-skills automatically tries the next available
port.

### Install From GitHub

After this repository is public, users can install it directly:

```bash
pipx install git+https://github.com/AIjunja/oh-my-skills.git
oh-my-skills gui
```

The legacy `skill-ledger` command is kept as a compatibility alias.

Without `pipx`:

```bash
python -m pip install git+https://github.com/AIjunja/oh-my-skills.git
oh-my-skills gui
```

### Editable Development Install

```bash
git clone https://github.com/AIjunja/oh-my-skills.git
cd oh-my-skills
python -m pip install -e .
oh-my-skills gui
```

## CLI Usage

Generate a Markdown inventory:

```bash
python -m skill_ledger scan --format markdown --out inventory/skills.md
```

Generate JSON:

```bash
python -m skill_ledger scan --format json --out inventory/skills.json
```

Print duplicate and metadata warnings:

```bash
python -m skill_ledger doctor
```

Scan specific folders:

```bash
python -m skill_ledger scan \
  --root ~/.codex/skills \
  --root ~/.claude/skills \
  --format markdown
```

## GUI Usage

```bash
python -m skill_ledger gui
```

The GUI lets users:

- browse all discovered skills;
- search by name, description, path, or source;
- filter by source;
- inspect `SKILL.md`;
- edit user-owned skills;
- create new skills for Codex, Claude, or Agents;
- archive unwanted user skills;
- export inventory reports;
- switch between English/Korean and light/dark themes.

### Browser CTA

oh-my-skills shows a creator CTA in the header and sidebar. The default label is
`제작자 구독하기`, and the sidebar includes these creator channels:

- [Threads](https://www.threads.com/@ai_jjuun)
- [Instagram](https://www.instagram.com/ai_jjuun/)
- [YouTube](https://www.youtube.com/@AI%EC%AD%8C)
- [GitHub](https://github.com/AIjunja)

You can override the primary CTA text or URL with environment variables:

```bash
OH_MY_SKILLS_CTA_LABEL="제작자 구독하기" \
OH_MY_SKILLS_CTA_URL="https://www.threads.com/@ai_jjuun" \
OH_MY_SKILLS_CTA_NOTE="Follow the creator on Threads, Instagram, YouTube, or GitHub." \
python -m skill_ledger gui
```

Windows PowerShell:

```powershell
$env:OH_MY_SKILLS_CTA_LABEL = "제작자 구독하기"
$env:OH_MY_SKILLS_CTA_URL = "https://www.threads.com/@ai_jjuun"
$env:OH_MY_SKILLS_CTA_NOTE = "Follow the creator on Threads, Instagram, YouTube, or GitHub."
python -m skill_ledger gui
```

## Safety Model

oh-my-skills is intentionally conservative.

- `codex-system` and `plugin-cache` skills are read-only.
- User skills are editable only under known user skill roots.
- Save operations create backups under `~/.oh-my-skills/backups`.
- Archive operations move skill folders to `~/.oh-my-skills/archive`.
- Generated inventory files can contain local paths and prompt content, so
  `inventory/` is ignored by Git by default.

## Use As An Agent Skill

This repository includes a root `SKILL.md`, so it can also be installed as an
Agent Skill. Once installed, an agent can learn how to run oh-my-skills for
tasks like:

- "Show me all my local Codex and Claude skills."
- "Find duplicate skills."
- "Open the skill manager GUI."
- "Create a new Codex skill."

Install for Codex:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.codex/skills/oh-my-skills
```

Install for Claude:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.claude/skills/oh-my-skills
```

On Windows PowerShell, use:

```powershell
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.codex\skills\oh-my-skills"
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.claude\skills\oh-my-skills"
```

## Related Projects

- [`openai/skills`](https://github.com/openai/skills): official Codex skills catalog.
- [`luongnv89/asm`](https://github.com/luongnv89/asm): universal skill manager CLI/TUI.
- [`siddhantparadox/codexmanager`](https://github.com/siddhantparadox/codexmanager): Codex desktop manager.

oh-my-skills is smaller and more focused: a local-first inventory and editor
for the skills already installed on your machine.

## License

MIT
