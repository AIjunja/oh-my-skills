# oh-my-skills User Guide

This guide is written for people who just want to run oh-my-skills and manage
their local skills.

## 1. Start The GUI

From the repository folder:

```bash
python -m skill_ledger gui
```

Then open the local URL shown in the terminal:

```text
http://127.0.0.1:8765/
```

The app runs locally on your machine. It does not upload your skills anywhere.
Use the `EN` / `KR` toggle in the header to switch the GUI language, and the
`Dark` / `Light` button to switch themes.

## Install As A Skill

Codex:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.codex/skills/oh-my-skills
```

Claude:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.claude/skills/oh-my-skills
```

Windows PowerShell:

```powershell
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.codex\skills\oh-my-skills"
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.claude\skills\oh-my-skills"
```

## 2. Read The Dashboard

The left sidebar shows:

- total discovered skills;
- duplicate skill names;
- source filters;
- editable target folders.

The middle list shows all discovered skills. Click any skill to inspect it.

The right editor shows the selected `SKILL.md`.

## Add A Channel CTA

The GUI includes a creator subscription CTA. The default label is
`제작자 구독하기`, with links to:

- Threads: https://www.threads.com/@ai_jjuun
- Instagram: https://www.instagram.com/ai_jjuun/
- YouTube: https://www.youtube.com/@AI%EC%AD%8C
- GitHub: https://github.com/AIjunja

To override the primary CTA:

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

## 3. Understand Sources

| Source | Meaning |
| --- | --- |
| `codex-user` | Your personal Codex skills |
| `claude-user` | Your personal Claude skills |
| `agents-user` | Generic Agent Skills |
| `codex-system` | Built-in Codex skills |
| `plugin-cache` | Plugin-provided skills |

Only user sources are editable.

## 4. Edit A Skill

1. Select a skill from `codex-user`, `claude-user`, or `agents-user`.
2. Edit the `SKILL.md` content.
3. Click `Save`.

Before saving, oh-my-skills creates a backup:

```text
~/.oh-my-skills/backups
```

## 5. Create A Skill

1. Click `New Skill`.
2. Choose a target:
   - `codex-user`
   - `claude-user`
   - `agents-user`
3. Enter a name and description.
4. Optionally add body content.
5. Click `Create`.

oh-my-skills creates a folder with a valid `SKILL.md`.

## 6. Archive A Skill

For editable user skills, click `Archive`.

This moves the skill folder to:

```text
~/.oh-my-skills/archive
```

It does not permanently delete the skill.

## 7. Export Inventory

Use the GUI export link, or run:

```bash
python -m skill_ledger scan --format markdown --out inventory/skills.md
python -m skill_ledger scan --format json --out inventory/skills.json
```

The `inventory/` folder is ignored by Git because reports can include private
paths and prompt content.

## 8. Check Duplicates

```bash
python -m skill_ledger doctor
```

This prints duplicate skill names and missing metadata.
