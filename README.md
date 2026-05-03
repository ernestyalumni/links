# ernestyalumni/links

A static replacement for my Linktree, optimized for **agentic editing**. Sub-agents can read and write `data/links.json`, run a small CLI, commit, and Vercel auto-deploys.

> Live: https://ernestyalumni-links.vercel.app (TBD — deploys on first push)

## Why

- **Single source of truth**: `data/links.json`. No DB, no admin UI, no auth.
- **Sub-agent friendly**: pure files, deterministic CLI, no headless browser, no cookies.
- **Self-hostable**: free Vercel/Cloudflare/GitHub Pages tier.
- **Fast & private**: static HTML, zero JS at runtime, Lighthouse 100, no third-party trackers by default.
- **Aesthetic**: academic / paper-like, EB Garamond serif, light & dark mode.

## Layout

```
data/
  links.json       ← active links (single source of truth)
  archive.json     ← retired links (preserved, never auto-deleted)
public/
  favicon.svg      ← lowercase italic "e" mark
  avatar.jpg       ← (drop your photo here, optional)
src/
  pages/index.astro  ← the only page; pulls data/links.json at build time
scripts/
  links.py         ← agent-safe CLI for add/edit/archive/reorder
astro.config.mjs
package.json
```

## Local dev

```sh
npm install
npm run dev          # http://localhost:4321
npm run build        # → dist/
```

## CLI for editing (agent-friendly)

```sh
# list everything
scripts/links.py list

# add a link (auto-slug from title; appends to end)
scripts/links.py add \
  --title "Groki — AI-native circuit design" \
  --url   "https://groki.cad" \
  --tags  "project,ai,hardware"

# add at a specific position with an icon
scripts/links.py add --title "Resume (PDF)" --url "https://..." --icon "📄" --position 1

# edit
scripts/links.py edit --id resume-pdf --title "Resume (May 2026)"

# move
scripts/links.py move --id resume-pdf --to 3

# reorder by listing ids in desired order
scripts/links.py reorder --order resume-pdf,github-main,linkedin

# archive (preserves entry in data/archive.json)
scripts/links.py archive --id wordpress-blog --reason "Replaced by Substack"
```

## Agent workflow

This repo is set up for **auto-commit mode**. When the user asks to add/edit/reorder a link:

1. Run the appropriate `scripts/links.py` command.
2. `git add data/ && git commit -m "links: <one-line summary>"`
3. `git push` → Vercel auto-deploys in ~30s.
4. Optional: `curl -sf https://ernestyalumni-links.vercel.app | grep -q "<new title>"` to confirm.

For destructive operations (archive multiple, reorder all), prefer one combined commit so revert is easy.

## Deploy

First-time setup (manual, ~2 min):

1. Push this repo to `github.com/ernestyalumni/links`.
2. Go to https://vercel.com/new, import the repo. Framework auto-detects as Astro.
3. Build command: `npm run build`. Output: `dist`. Done.
4. Vercel gives you `<project>.vercel.app`. Add custom domain later if you buy one.

After that, every push to `main` auto-deploys.

## Roadmap

- [ ] Add avatar.jpg (1:1, 256+px)
- [ ] Buy `ernestyalumni.com` and point `links.` subdomain at Vercel
- [ ] Optional: per-link click tracking via Plausible (privacy-friendly)
- [ ] Optional: tag-based filtering / sections
- [ ] Optional: OG image generation per-link

## License

MIT for the code. Content (links, copy) © Ernest Yeung.
