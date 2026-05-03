# SETUP.md — first-time setup and deployment

This guide takes you from "I cloned the repo" to "my page is live on the internet" in ~10 minutes.

## Prerequisites

- **Node.js 18+** (`brew install node` on macOS, or [nodejs.org](https://nodejs.org))
- **Python 3.9+** (preinstalled on macOS/Linux; for the helper scripts)
- **Git** + a GitHub account
- **Free Vercel account** (or Cloudflare Pages, Netlify — anything that builds Astro)

## Step 1 — Get the code

### Option A: Use this as a template (recommended)

1. Go to https://github.com/ernestyalumni/links
2. Click **"Use this template"** → **"Create a new repository"**
3. Name it (e.g. `<your-handle>-links`), make it public or private
4. `git clone https://github.com/<you>/<your-repo>.git`

### Option B: Fork

`git clone` your fork.

### Option C: Manual

```sh
git clone https://github.com/ernestyalumni/links.git my-links
cd my-links
rm -rf .git && git init -b main   # start fresh history
```

## Step 2 — Install + verify

```sh
cd my-links
npm install
npm run build       # should complete in <1 second
scripts/validate.py # should print "OK"
```

If both pass, the project is healthy.

## Step 3 — Edit your profile

Open `config/site.config.json`:

```json
{
  "site": {
    "title": "Your Name — Links",
    "description": "What you do, in one line.",
    "url": "https://your-project.vercel.app",
    "language": "en"
  },
  "profile": {
    "handle": "yourhandle",
    "display_name": "Your Name",
    "tagline": "what you do · what you make · vibes",
    "avatar": "/avatar-placeholder.svg",
    "show_avatar": true,
    "show_handle": true,
    "show_tagline": true
  },
  "theme": {
    "preset": "academic",
    "color_scheme": "auto"
  }
}
```

**Avatar:** Drop a square image at `public/avatar.jpg` (or `.png`/`.webp`) and set `profile.avatar` to match the filename. Recommended: 256×256px or larger, square crop, under 100 KB. The page renders it at 96×96px CSS with `object-fit: cover`, so any square image works. A placeholder SVG is included — replace it with your own photo or set `"show_avatar": false` to hide it.

**Social sharing image (OG image):** For link previews on Twitter/Slack/etc., add a 1200×630px image to `public/` (e.g. `public/og.png`) and set `social_meta.og_image` in your config to the full URL (e.g. `"https://your-project.vercel.app/og.png"`). Without this, shared links show no preview image.

Pick a theme: `academic`, `minimal`, `terminal`, `dark-space`. See [`THEMES.md`](THEMES.md).

## Step 4 — Add your links

Use the CLI (preferred):

```sh
scripts/links.py add --title "GitHub"  --url "https://github.com/you"        --icon "⬢"  --tags "code"
scripts/links.py add --title "Resume"  --url "https://your-site.com/cv.pdf"  --icon "📄" --position 1
scripts/links.py add --title "Email"   --url "mailto:you@example.com"        --icon "✉"
scripts/links.py list
```

Or edit `data/links.json` directly:

```json
{
  "links": [
    { "id": "resume",   "title": "Resume",   "url": "https://...", "icon": "📄", "position": 1, "added_at": "2026-05-03" },
    { "id": "github",   "title": "GitHub",   "url": "https://github.com/you", "position": 2, "added_at": "2026-05-03" }
  ]
}
```

Validate:

```sh
scripts/validate.py
```

## Step 5 — Preview locally

```sh
npm run dev
# open http://localhost:4321
```

Iterate on profile, links, theme.

## Step 6 — Push to GitHub

```sh
git add -A
git commit -m "Customize profile and links"
git push origin main
```

## Step 7 — Deploy to Vercel (recommended)

1. Go to https://vercel.com/new
2. **Import** your repo
3. Vercel auto-detects **Astro** as the framework
4. Click **Deploy** (no config changes needed)
5. After ~30s, you'll get `<project>.vercel.app`

Update `site.url` in `config/site.config.json` to match the deployed URL, then push again.

### Custom domain (optional)

In Vercel:
- **Settings → Domains** → add e.g. `links.yoursite.com`
- Add the CNAME / A records Vercel shows you in your DNS provider
- Done — TLS is automatic

## Alternative hosts

### Cloudflare Pages

1. Connect repo at https://pages.cloudflare.com
2. Build command: `npm run build`
3. Output directory: `dist`

### Netlify

1. https://app.netlify.com/start → connect repo
2. Build command: `npm run build`
3. Publish directory: `dist`

### GitHub Pages

```sh
# In .github/workflows/pages.yml — see Astro docs:
# https://docs.astro.build/en/guides/deploy/github/
```

You'll need to set `site` and `base` in `astro.config.mjs`. Vercel/Cloudflare are simpler unless you specifically want Pages.

## Step 8 — Update Linktree (or wherever)

If you're migrating away from Linktree, edit your Linktree page to have a single link pointing at your new URL, with text like "👉 New home: links.yoursite.com". Or schedule the cutover and replace the linktr.ee URL in your bios.

## Maintenance

To add a link from the command line:

```sh
scripts/links.py add --title "New thing" --url "https://..."
git commit -am "links: add new thing"
git push
```

Vercel auto-deploys. Done in 30 seconds.

To delegate to an AI agent: see [`AGENTS.md`](AGENTS.md).

## Troubleshooting

| Problem | Fix |
|---|---|
| `npm install` fails | Update Node to 18+. Delete `node_modules/` and `package-lock.json`, retry. |
| Build fails with JSON parse error | Run `scripts/validate.py` to find the bad file. |
| Page renders blank/empty | Likely empty `data/links.json`. Confirm `links` array has entries. |
| Vercel build fails | Check Vercel build logs. Most common: outdated Node version (set to 18+ in Vercel project settings). |
| Theme colors look wrong | Check `theme.preset` spelling. Run `scripts/validate.py`. |
| Avatar not showing | Confirm `public/avatar.jpg` exists and `profile.avatar` matches the path. |
| Custom domain not working | Wait 5 min for DNS propagation. Check Vercel domains panel. |
