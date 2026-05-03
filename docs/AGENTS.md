# AGENTS.md — guide for AI agents working on this repo

> If you are an AI agent (Claude Code, Codex, OpenClaw, Cursor, Aider, etc.) reading this file: **read it fully before making changes.** It tells you exactly how to operate safely and efficiently in this codebase.

## What this repo is

A static link-in-bio page (Linktree alternative). The only thing that matters at runtime is `data/links.json` and `config/site.config.json`. The Astro renderer reads them at build time and produces a single HTML file.

## Hard rules (do not violate)

1. **Never edit `src/pages/index.astro` to hardcode a link.** Always go through `data/links.json` — either edit the JSON directly or use `scripts/links.py`.
2. **Never delete from `data/links.json`.** Always *archive* via `scripts/links.py archive --id <slug>`. This preserves click history.
3. **Never change a link's `id` once committed.** It's a stable slug. Edit `title`, `url`, `icon` freely; treat `id` as immutable.
4. **Never commit secrets.** No API keys, no `.env` values. Analytics IDs in `site.config.json` are fine (they're public anyway).
5. **Validate before committing.** Run `scripts/validate.py` and `npm run build` (or at least `python3 -c "import json; json.load(open('data/links.json'))"`).
6. **One logical change per commit.** Bundle related edits (e.g. "archive 3 stale links") into one commit, but don't mix unrelated changes.
7. **For aesthetic / structural changes** (CSS, theme additions, schema changes, new scripts): propose via PR or message the user, do NOT auto-commit.

## Auto-commit mode

This repo runs in **auto-commit mode**. After a successful CLI run that edits `data/`:

```sh
git add data/
git commit -m "links: <verb> <subject>"
git push origin main
```

Vercel auto-deploys in ~30 seconds. Confirm with `curl -sf <site-url> | grep -q "<expected text>"` if needed.

For changes outside `data/` (CSS, scripts, docs), prefer a feature branch + PR unless the user explicitly says auto-commit.

## Common tasks → exact commands

| Task | Command |
|---|---|
| Add a link | `scripts/links.py add --title "..." --url "..." [--icon "..."] [--tags a,b]` |
| Add at top | `scripts/links.py add --title "..." --url "..." --position 1` |
| Edit title/URL | `scripts/links.py edit --id <slug> --title "..." --url "..."` |
| Move position | `scripts/links.py move --id <slug> --to <n>` |
| Reorder all | `scripts/links.py reorder --order id1,id2,id3` |
| Archive | `scripts/links.py archive --id <slug> --reason "..."` |
| Show current state | `scripts/links.py list` |
| Validate | `scripts/validate.py` |
| Build (smoke test) | `npm run build` |
| Apply example | `scripts/apply-example.py --name <name>` |

## Decision tree

When the user asks you to do something:

```
Is the change to data/links.json or data/archive.json?
├── Yes → Use scripts/links.py, validate, auto-commit, push.
└── No
    ├── Is it config/site.config.json? (theme, profile name, etc.)
    │   ├── Yes → Edit JSON directly, validate, auto-commit OK if obvious change.
    │   └── No
    │       ├── Is it a theme tweak (colors, fonts)?
    │       │   ├── Edit src/themes/themes.ts. Build to verify. PR or ask user.
    │       └── Is it new functionality (scripts, components)?
    │           └── Propose plan first; create feature branch; do NOT auto-commit to main.
```

## Verifying URLs before adding

When adding a link, sanity-check the URL is reachable:

```sh
curl -sI -L --max-time 5 -o /dev/null -w "%{http_code}\n" "https://example.com"
```

Accept `200`-`399`. If `4xx`/`5xx` or timeout, ask the user before adding.

## Common pitfalls

- **JSON trailing commas:** Python's `json` module rejects them. Use `scripts/links.py` and you'll never hit this.
- **Position conflicts:** `scripts/links.py` handles renumbering automatically. Don't manually set positions in JSON unless you also renumber others.
- **Slug collisions:** If `slugify("My Cool Site")` produces an existing id, add `--id my-cool-site-2` explicitly.
- **`src/pages/index.astro` set:html:** The big style block uses Astro's `set:html` directive — keep template-string interpolation correct or build will fail silently with empty CSS.
- **Vercel build:** It runs `npm run build`. If `node_modules/` is gitignored (it is), Vercel installs fresh. Don't commit `node_modules/`.

## When to push back

If the user asks for something that:

- Adds tracking/fingerprinting code → push back, suggest Plausible/Umami if they want analytics.
- Adds runtime JavaScript for non-essential UX → push back, the site is intentionally zero-JS.
- Hardcodes a link in the Astro template → push back, use `data/links.json`.
- Removes the schema files → push back, schemas are docs-as-code.
- Stores credentials in the repo → refuse.

## How to know you're done

Before declaring a task complete:

1. `scripts/validate.py` exits 0
2. `npm run build` succeeds
3. Git working tree is clean (`git status` shows nothing, or only intentional uncommitted files)
4. `git log --oneline -3` shows your commit(s)
5. (If pushed) `git status` shows "Your branch is up to date with 'origin/main'"

## Repo metadata for context

- **Default branch:** `main`
- **Build tool:** Astro 4.x
- **Package manager:** npm (lockfile committed)
- **Python:** scripts use stdlib only, run with `python3` (3.9+)
- **License:** MIT
- **Hosting:** Vercel (recommended), but works on any static host
- **Domain:** `<project>.vercel.app` by default

## Escalation

If you're unsure, prefer:

1. **Read** the file first (`AGENTS.md`, `docs/SETUP.md`, `docs/THEMES.md`)
2. **Validate** rather than assume (`scripts/validate.py`, `npm run build`)
3. **Ask** the user rather than make destructive changes
4. **Branch** rather than push to `main` for non-trivial changes
