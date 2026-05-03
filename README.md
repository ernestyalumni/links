# links — open-source Linktree alternative

A static, file-driven, agent-friendly link-in-bio page. Edit one JSON file, push, deploy. No database, no admin UI, no auth, no JavaScript at runtime.

> **Live demo:** https://ernestyalumni-links.vercel.app

## Why this exists

Linktree-style services are great until you want to:

- Have AI agents (Claude Code, Codex, OpenClaw, etc.) maintain your page autonomously
- Self-host with full control over aesthetics
- Stop paying for "Pro" features that should be free
- Own your content as plain files in git

This project gives you all of those at the cost of running `git push`.

## Features

- 📄 **One JSON file = your page.** `data/links.json` is the single source of truth.
- 🎨 **4 built-in themes** — `academic`, `minimal`, `terminal`, `dark-space`. Light + dark mode each.
- 🤖 **Built for agents.** Deterministic CLI (`scripts/links.py`). Schemas for everything. No browser automation needed.
- ⚡ **Static HTML output.** Astro builds once, serves everywhere. Lighthouse 100, ~5KB page weight.
- 🔒 **Privacy-respecting.** Zero trackers by default. Optional Plausible/Umami integration.
- 🆓 **Free hosting.** Deploy to Vercel, Cloudflare Pages, Netlify, or GitHub Pages.

## Quick start (5 minutes)

```sh
# 1. Fork or clone
git clone https://github.com/ernestyalumni/links.git my-links
cd my-links
npm install

# 2. Edit your profile
$EDITOR config/site.config.json

# 3. Add your links
scripts/links.py add --title "GitHub" --url "https://github.com/you" --icon "⬢"
scripts/links.py add --title "Newsletter" --url "https://you.substack.com" --icon "✉"

# 4. Validate + preview
scripts/validate.py
npm run dev   # http://localhost:4321

# 5. Deploy
git push    # Vercel/Cloudflare auto-deploys on push
```

See [`docs/SETUP.md`](docs/SETUP.md) for full deploy instructions.

## Project layout

```
config/
  site.config.json          ← your profile, theme, branding (USER EDIT)
  site.config.schema.json   ← JSON schema for validation
data/
  links.json                ← active links (USER EDIT, or via CLI)
  links.schema.json         ← JSON schema for validation
  archive.json              ← retired links (preserved, never auto-deleted)
public/
  favicon.svg               ← drop your own favicon here
  avatar.jpg                ← (optional) profile photo
src/
  pages/index.astro         ← the only page; reads config + data at build
  themes/themes.ts          ← theme registry (add new ones here)
scripts/
  links.py                  ← CLI: add/edit/archive/reorder/move
  validate.py               ← Lint config + links
  apply-example.py          ← Copy an example profile in
examples/
  ernestyalumni/            ← real-world example
  sample-creator/           ← starter template
docs/
  SETUP.md                  ← full deploy guide
  AGENTS.md                 ← instructions for AI agents
  THEMES.md                 ← theme docs + how to add one
  CONTRIBUTING.md           ← human contributor guide
astro.config.mjs
package.json
```

## CLI reference

```sh
# List
scripts/links.py list

# Add (auto-slugs from title; appends to end)
scripts/links.py add --title "Resume" --url "https://..." --icon "📄" --tags "work,pdf"

# Add at top
scripts/links.py add --title "Featured" --url "https://..." --position 1

# Edit
scripts/links.py edit --id resume --title "Resume (May 2026)"

# Move
scripts/links.py move --id resume --to 3

# Reorder all (any unlisted ids retain trailing order)
scripts/links.py reorder --order resume,github,linkedin

# Archive (preserves entry in data/archive.json — never delete!)
scripts/links.py archive --id wordpress-blog --reason "Replaced by Substack"

# Validate
scripts/validate.py

# Apply an example
scripts/apply-example.py --list
scripts/apply-example.py --name sample-creator
```

## Themes

Pick one in `config/site.config.json` → `theme.preset`:

| Preset | Vibe | Font |
|---|---|---|
| `academic` | Paper-like serif. Researchers, writers, scientists. | EB Garamond |
| `minimal` | Apple-clean sans-serif. | Inter |
| `terminal` | Monospace, hacker green-on-black. | JetBrains Mono |
| `dark-space` | Deep navy with gold accents. Cosmic. | Cormorant Garamond |

All themes support `light`, `dark`, and `auto` color schemes. Add your own in [`docs/THEMES.md`](docs/THEMES.md).

## Working with AI agents

This project is designed for agentic editing. See [`docs/AGENTS.md`](docs/AGENTS.md) for the full workflow.

Quick version: ask any agent (Claude Code, Codex, OpenClaw, etc.) to "read AGENTS.md, then add this link: ..." — it will use the CLI, commit, and push autonomously.

## License

MIT for the code. Your content (links, copy, avatars) is yours.

## Credits

Built on [Astro](https://astro.build/). Inspired by the limitations of Linktree.
