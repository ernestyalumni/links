# AGENTS.md

If you are an AI agent in this repository, start with [`docs/AGENTS.md`](docs/AGENTS.md). It contains the operational rules and command reference.

This file exists at the root because many agent harnesses (Claude Code, Codex, OpenClaw, Cursor, etc.) auto-load top-level `AGENTS.md` for context.

## TL;DR

- Edit `data/links.json` via `scripts/links.py`, never directly hardcode in templates
- Edit `config/site.config.json` directly for branding/theme changes
- Validate with `scripts/validate.py` before committing
- Auto-commit mode is **ON** for `data/` changes; PR mode for everything else
- Never delete from links — always `archive`

Full guide: [`docs/AGENTS.md`](docs/AGENTS.md)
Setup guide: [`docs/SETUP.md`](docs/SETUP.md)
Theme docs: [`docs/THEMES.md`](docs/THEMES.md)
Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
