# AGENTS.md — instructions for sub-agents

You're editing **ernestyalumni/links**, a static Astro site that renders `data/links.json`.

## Rules

1. **Never edit `src/pages/index.astro` rendering of links manually.** Always edit `data/links.json` via `scripts/links.py`. The renderer reads JSON.
2. **Auto-commit mode is ON.** After a successful CLI run:
   ```sh
   git add data/
   git commit -m "links: <verb> <subject>"   # e.g. "links: add groki, archive wordpress-blog"
   git push origin main
   ```
   Use the `linkbot` author if available; otherwise default user.
3. **One logical change per commit** when possible. Bundle reorders/multi-archives into one commit.
4. **Never delete** from `data/links.json` directly — always `archive` so click history is preserved.
5. **Verify URLs are reachable** before adding (HEAD request, expect 2xx/3xx). Skip if it requires auth.
6. **Preserve `id` slugs** once committed — they're stable identifiers. Edit `title`/`url` freely.
7. **Position 1 = top of page.** Lower numbers render higher.
8. **Aesthetic changes** (CSS, layout) require human review — propose via PR or message, do not auto-commit.

## Common tasks

- **"Add this link"** → `scripts/links.py add --title ... --url ... --tags ...` → commit
- **"Move X to top"** → `scripts/links.py move --id <slug> --to 1` → commit
- **"Get rid of the wordpress one"** → `scripts/links.py archive --id wordpress-blog` → commit
- **"Show me my links"** → `scripts/links.py list` (read-only, no commit)

## Validation

Run before committing:

```sh
python3 -c "import json; json.load(open('data/links.json')); json.load(open('data/archive.json'))"
```

Optional full-build smoke test:

```sh
npm install --silent && npm run build --silent
```

## Don't touch

- `package-lock.json` (let npm manage it)
- `.vercel/` (Vercel CLI artifacts)
- `dist/` (build output, gitignored)
