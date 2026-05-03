# THEMES.md

This project ships with 4 built-in themes. Each is a CSS variable set + optional Google Fonts import. Themes are 100% data — no per-theme rendering logic — so adding a new one is purely additive.

## Built-in themes

### `academic` (default)
Paper-like serif. Suits researchers, writers, scientists. EB Garamond. Cream paper / dark ink in light mode, deep brown / cream in dark mode. Subtle gold accent.

### `minimal`
Apple-clean sans-serif. Inter. Pure white / pure black palette. The "I want it to look expensive" choice.

### `terminal`
Hacker/builder aesthetic. JetBrains Mono. Green-on-black in dark mode, dark-green-on-cream in light mode. For developers who lean into it.

### `dark-space`
Cosmic / cinematic. Cormorant Garamond serif. Deep navy with gold accents. Designed for dark mode primarily.

## Switching themes

Edit `config/site.config.json`:

```json
{
  "theme": {
    "preset": "minimal",
    "color_scheme": "auto"
  }
}
```

`color_scheme`:
- `light` — always light
- `dark` — always dark
- `auto` — follow user's OS preference (default, recommended)

Run `npm run build` to preview, push to deploy.

## Adding a new theme

1. Open `src/themes/themes.ts`.
2. Add an entry to the `themes` map. Provide:
   - `name`, `description` (for self-documentation)
   - `fonts_url` (optional Google Fonts URL)
   - `font_family` (CSS font stack)
   - `light` and `dark` CSS variable maps (define all of: `--paper`, `--ink`, `--ink-soft`, `--ink-muted`, `--rule`, `--link-bg`, `--link-bg-hover`, `--accent`)
   - `extra_css` (optional, for animations etc.)
3. Add the new preset name to `config/site.config.schema.json` under `theme.preset.enum` (and `scripts/validate.py` `valid_presets`).
4. Set `theme.preset` in `config/site.config.json` to your new theme.
5. `npm run build` to verify.

### Example: a `pastel` theme

```ts
pastel: {
  name: "Pastel",
  description: "Soft, candy-shop palette. Pinks, mints, lavenders.",
  fonts_url: "https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600&display=swap",
  font_family: "'Quicksand', system-ui, sans-serif",
  light: {
    "--paper": "#fef6f9",
    "--ink": "#3a2540",
    "--ink-soft": "#5d4470",
    "--ink-muted": "#a08aab",
    "--rule": "#f0d6e2",
    "--link-bg": "#ffffff",
    "--link-bg-hover": "#fce4ec",
    "--accent": "#d97aaf",
  },
  dark: {
    "--paper": "#1a1220",
    "--ink": "#f7e6f1",
    "--ink-soft": "#d0bcd9",
    "--ink-muted": "#7a6585",
    "--rule": "#3a2540",
    "--link-bg": "#241830",
    "--link-bg-hover": "#2f1f3f",
    "--accent": "#e8a0c8",
  },
},
```

## CSS variable contract

The Astro template in `src/pages/index.astro` only uses these variables. If your theme provides them all, your theme will work — no template changes needed.

| Variable | Used for |
|---|---|
| `--paper` | Page background |
| `--ink` | Primary text color |
| `--ink-soft` | Secondary text (tagline) |
| `--ink-muted` | Tertiary text (handle, footer) |
| `--rule` | Hairlines, borders |
| `--link-bg` | Link card background |
| `--link-bg-hover` | Link card hover state |
| `--accent` | Highlights, footer links, focus ring |

## Tips for designing new themes

- **Test in both light and dark.** `color_scheme: auto` is the default; users will see both.
- **Contrast matters.** Aim for WCAG AA (4.5:1 for body text). Use https://webaim.org/resources/contrastchecker/.
- **Pick a font that loads fast.** Google Fonts with a single weight + `&display=swap` is ideal.
- **Keep `--accent` distinctive.** It's the only "color" most users will see — make it count.
- **Avoid runtime JavaScript.** Themes should be pure CSS variables. The site has no JS by design.

## Future ideas (not implemented)

- Per-link icon themes (replace emoji with [simple-icons](https://simpleicons.org) brand SVGs)
- Animated transitions on theme change
- User-uploaded background images
- "Brutalist" theme with sharp grid lines and raw HTML
- "Vaporwave" theme

PRs welcome.
