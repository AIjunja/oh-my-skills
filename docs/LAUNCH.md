# Open Source Launch Notes

Use this when publishing oh-my-skills publicly.

## One-Sentence Pitch

oh-my-skills is a local GUI for seeing, editing, creating, and deduplicating
your Codex, Claude, and Agent Skills.

## Short Pitch

If you use multiple AI coding agents, your `SKILL.md` folders can quickly get
scattered across `~/.codex`, `~/.claude`, `.agents`, and plugin caches.
oh-my-skills gives you one local dashboard to search them, inspect them, detect
duplicates, safely edit user skills, and archive the ones you no longer want.

## Suggested GitHub Topics

- agent-skills
- codex
- claude
- skill-manager
- ai-agents
- developer-tools
- local-first
- python

## Release Checklist

- Confirm the GitHub repository exists at `https://github.com/AIjunja/oh-my-skills`.
- Add screenshots or a short GIF to the README.
- Run `python -m pytest`.
- Run `python -m skill_ledger gui` and verify the GUI.
- Confirm `inventory/` is not committed.
- Create a first release tag, for example `v0.1.0`.

## Social Post Draft

I kept forgetting which AI agent skills were installed on my machine, so I made
oh-my-skills.

It is a local GUI for Codex, Claude, and Agent Skills:

- scans `~/.codex/skills`, `~/.claude/skills`, `~/.agents/skills`
- finds duplicates
- edits user-owned `SKILL.md` files with backups
- keeps system/plugin skills read-only
- archives instead of deleting
- no server, no account, no telemetry

Run it:

```bash
python -m skill_ledger gui
```

Open source: https://github.com/AIjunja/oh-my-skills

Creator channels:

- Threads: https://www.threads.com/@ai_jjuun
- Instagram: https://www.instagram.com/ai_jjuun/
- YouTube: https://www.youtube.com/@AI%EC%AD%8C
- GitHub: https://github.com/AIjunja
