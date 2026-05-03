# ARCHITECTURE.md

Why this project is shaped the way it is.

## Constraints (chosen on purpose)

1. **Static output only.** No SSR, no edge functions. Page must serve from any dumb file host.
2. **No runtime JS by default.** Page renders without executing any script. Themes use CSS variables.
3. **One source of truth per concept.** Branding lives in `config/site.config.json`. Links live in `data/links.json`. Nothing duplicates.
4. **Agent-first ergonomics.** Every read/write operation has a CLI. JSON schemas document the data contract.
5. **Trivially forkable.** A user with no programming experience should be able to fork → edit two JSON files → deploy on Vercel in 10 minutes.

## Data flow

```
config/site.config.json ──┐
                          ├──→  src/pages/index.astro ──→  npm run build  ──→  dist/index.html  ──→  Vercel CDN
data/links.json ──────────┤              │
                          │              ↓
src/themes/themes.ts ─────┘     CSS vars + content
```

- Astro reads JSON imports at build time (`import linksData from '../../data/links.json'`).
- The single page interpolates everything into one HTML file with inlined CSS.
- No fetch at runtime. No database. No auth.

## Why Astro?

Considered:
- **Next.js / React** — overkill, ships a runtime by default.
- **Hugo / Jekyll** — fast, but theming is template-heavy and JSON imports aren't first-class.
- **Pure HTML + a build script** — simplest, but no DX (no live reload, no JSX-style components).
- **11ty** — solid, but Astro's TypeScript-friendly + JSON-import story is cleaner for our schema-driven approach.

Astro wins on:
- JSON imports as TypeScript-typed values (when paired with schemas)
- Zero JS runtime by default (`output: 'static'`, no `<script>` tags emitted unless we add them)
- Single-file `.astro` components (no separate template language to learn)
- Trivial Vercel/Cloudflare/Netlify integration
- Active project, stable API

## Why JSON instead of YAML / TOML?

- JSON has the best agent ergonomics (every language has a parser, no whitespace ambiguity)
- JSON Schema is a mature, tool-supported validation format
- Our config is small enough that JSON readability isn't an issue

If a user prefers YAML, they can convert at edit time and commit JSON; we'd need a build-time transform to switch.

## Why Python for CLI scripts?

- Stdlib only — no `pip install` step
- macOS/Linux preinstalled
- Simpler than Node for sub-process / file ops
- Easier for non-frontend devs to extend

If we ever need cross-platform Windows support without WSL, we'd port to Node (still stdlib-only via `node:fs`).

## Schema-as-docs

`config/site.config.schema.json` and `data/links.schema.json` are JSON Schema Draft 7. They serve dual purposes:

1. Editor autocomplete + validation (when editors honor `$schema` references in JSON)
2. Programmatic validation by `scripts/validate.py`
3. Documentation — `descriptions` are user-facing

If you add a config field, update the schema first.

## Theme system design

Themes are pure data:

```ts
{
  fonts_url: "https://...",       // optional
  font_family: "...",             // CSS font stack
  light: { "--paper": "...", ... },
  dark: { "--paper": "...", ... },
  extra_css: "..."                // optional
}
```

The Astro template inlines the appropriate `:root` block based on `color_scheme` (`light` / `dark` / `auto`). No theme-specific code in the renderer.

This means:
- A theme is ~30 lines of TypeScript
- A theme can be added in a single PR with no architectural changes
- Themes are auditable in one file (`src/themes/themes.ts`)

## What's intentionally absent

- **Click tracking** — privacy-respecting by default. Opt-in to Plausible/Umami if desired.
- **A11y JS** — semantic HTML + focus styles do the work; no JS ARIA helpers needed.
- **i18n** — single-page projects rarely need it. If users want translations, they fork.
- **Multi-page support** — not yet. The product is a *link page*, not a site builder.
- **Drag-drop reordering UI** — defeats the agent-friendly file-driven design. Use the CLI.
- **OG image generation** — punted. Users can drop an OG image in `public/` and reference it.

## What might come later (and what would change)

| Feature | Architectural impact |
|---|---|
| Sections / grouping | New schema field on `Link` (e.g. `section`); template change to render groups |
| Brand-icon support | New `icon_set` config; build-time fetch of `simple-icons` SVGs; cached locally |
| Multiple pages | Refactor `index.astro` → dynamic routes; new top-level config schema for routes |
| RSS/Atom feed of changes | New build step writes feed from git log of `data/` |
| Custom domains as data | Already config; users handle via Vercel UI |

If any of those land, the rules above (one source of truth, schema-validated, agent-CLI parity) still apply.
