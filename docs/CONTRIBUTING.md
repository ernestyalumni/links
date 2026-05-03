# CONTRIBUTING.md

Thanks for considering a contribution! This project aims to be the simplest possible open-source Linktree alternative — please keep changes aligned with that goal.

## Philosophy

- **Static-first.** No databases, no server-rendered pages, no runtime JavaScript unless absolutely necessary.
- **Files over UIs.** Configuration lives in JSON files in git, not in admin panels.
- **Agent-friendly.** Every operation should be scriptable. If a human-only workflow exists, expose a CLI for the same thing.
- **Schema-validated.** New config fields ship with schema updates and `validate.py` checks.
- **Minimal dependencies.** Astro + zero npm runtime deps. Python scripts use stdlib only.

## What's welcome

- New themes (PR adding to `src/themes/themes.ts` + schema enum)
- Schema improvements / validation gaps
- Documentation fixes
- New examples in `examples/`
- Bug fixes
- Accessibility improvements
- New CLI commands that compose well (e.g. `bulk-import`, `dedupe`)

## What's not welcome (without prior discussion)

- Adding a backend / database / auth
- Adding a CMS / admin UI
- Bundling tracking / analytics by default
- Switching frameworks (Astro is intentional)
- Heavy JavaScript runtime features
- Vendor lock-in (e.g. Vercel-only features)

## Development workflow

```sh
# 1. Fork, clone, branch
git checkout -b feature/my-thing

# 2. Install
npm install

# 3. Make changes
# 4. Validate
scripts/validate.py
npm run build

# 5. Test with both example profiles
scripts/apply-example.py --name sample-creator
npm run build
scripts/apply-example.py --name ernestyalumni
npm run build

# 6. Commit + push
git commit -m "feat: ..."
git push origin feature/my-thing

# 7. Open PR
```

## Coding conventions

- **Astro:** Keep `index.astro` as the only page until/unless we have a good reason for routes.
- **TypeScript:** `src/themes/themes.ts` is the only TS file. Keep types narrow and exported.
- **Python:** stdlib only. Type hints encouraged. Match the style of existing scripts.
- **JSON:** 2-space indent. Trailing newline. `$schema` references where applicable.
- **CSS:** Use the variables in `src/pages/index.astro`. No new variables without a purpose.

## Commits

Conventional-ish:

- `feat: add pastel theme`
- `fix: validate.py crashes on missing tags array`
- `docs: clarify Vercel deploy steps`
- `chore: bump astro to 4.17`
- `links: add resume, archive wordpress` (for `data/` changes only)

## Tests

There's no test framework yet (intentional — the surface is tiny). `scripts/validate.py` + `npm run build` catches ~all real bugs. If you add a complex script, consider a `tests/` folder with stdlib `unittest`.

## Releases

This project doesn't version itself yet. If we need versions, we'll use git tags + GitHub releases.

## Code of Conduct

Be kind. We're here to make a small thing well.

## Questions

Open an issue. Or, if you're an AI agent: read `docs/AGENTS.md`.
