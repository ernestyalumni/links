# Deploy claw-dj links (second Vercel project)

This repo already has a personal deploy on **`deploy/ernestyalumni`**.
The claw-dj link-in-bio lives on **`deploy/claw-dj`** and should be a
**separate Vercel project** so the two production URLs never overwrite each other.

## Status (2026-08-05)

| Item | Status |
|---|---|
| Branch | `deploy/claw-dj` (pushed to `origin`) |
| Profile | claw-dj · dark-space · sample-lineage tagline |
| Links | YouTube `@claw-dj`, TikTok `@clawdj6`, GitHub `InServiceOfX/claw-dj` |
| Avatar / OG | `public/avatar.jpg`, `public/og.png` (from All Night Long art) |
| Validate + build | Passes locally (`python3 scripts/validate.py && npm run build`) |
| Preview on Vercel | Builds on push, but **team SSO-gated** — not usable as a public bio link |
| Public production URL | **Needs one-time second Vercel project** (below) |

**Suggested public URL:** `https://claw-dj-links.vercel.app`  
(config `site.url` and `social_meta.og_image` already assume this)

---

## Why a second project?

| Git branch | Audience | Vercel project |
|---|---|---|
| `deploy/ernestyalumni` | Ernest personal | existing `links` / ernestyalumni-links |
| `deploy/claw-dj` | DJ brand | **new** `claw-dj-links` |

Previews of `deploy/claw-dj` on the *personal* project go to SSO login pages — useless for TikTok Website field.

---

## One-time: create production (you run this)

Vercel CLI must be logged in on your machine (agents cannot complete browser login).

```sh
cd /Users/ernestyeung/.openclaw/workspace/repos/links
git checkout deploy/claw-dj
git pull

# interactive once
npx vercel login

# create a NEW project — do not select the personal "links" project
npx vercel link --yes --project claw-dj-links
# Set: scope = your account, link to existing? no → create claw-dj-links
# Production branch in dashboard: deploy/claw-dj

npx vercel deploy --prod --yes
```

Or use the dashboard:

1. [vercel.com/new](https://vercel.com/new) → Import **`ernestyalumni/links`**
2. Project name: **`claw-dj-links`**
3. Framework: Astro
4. **Settings → Git → Production Branch** → **`deploy/claw-dj`**
5. Deploy

Copy the production URL. If it is **not** `https://claw-dj-links.vercel.app`, update:

```sh
# config/site.config.json → site.url and social_meta.og_image
python3 scripts/validate.py && npm run build
git add config/site.config.json examples/claw-dj/site.config.json
git commit -m "deploy(claw-dj): set production site.url"
git push origin deploy/claw-dj
```

### Protect the personal project

In the **existing** personal links project:

- Production Branch stays **`deploy/ernestyalumni`**
- Never point it at `deploy/claw-dj`

---

## Wire social bios (after public URL works)

| Platform | Field | Value |
|---|---|---|
| TikTok `@clawdj6` | Website | `https://claw-dj-links.vercel.app` (or your real prod URL) |
| YouTube `@claw-dj` | Website / links | same |
| Instagram / X | Bio link | same |

Then captions can say: **“full mix + all links in bio”**.

---

## Day-to-day content updates

```sh
git checkout deploy/claw-dj

# feature a new mix at the top
scripts/links.py add \
  --title "★ Latest: All Night Long sample mix" \
  --url "https://youtu.be/YOUR_VIDEO_ID" \
  --icon "★" \
  --position 1

python3 scripts/validate.py
git add data/links.json
git commit -m "links(claw-dj): feature latest mix"
git push origin deploy/claw-dj
```

---

## Local preview

```sh
cd /Users/ernestyeung/.openclaw/workspace/repos/links
git checkout deploy/claw-dj
npm run dev   # http://localhost:4321
```

---

## Note on package-lock / vercel CLI

`vercel` is optional as a **devDependency** for local deploys. Git-connected Vercel projects redeploy on `git push` without the CLI.
