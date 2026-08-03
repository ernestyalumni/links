# claw-dj links example

Link-in-bio profile for the **claw-dj** hip-hop / R&B anthology + short-form
project. Pair with image assets described in the claw-dj repo:

`repos/claw-dj/docs/IMAGE_PROMPTS_ANTHOLOGY_VISUALS.md` → section **Brand
identity assets** (avatar, OG banner, favicon).

## Channels this page points at

| Surface | URL |
|---|---|
| YouTube | https://www.youtube.com/@claw-dj |
| TikTok | https://www.tiktok.com/@clawdj6 |
| GitHub | https://github.com/InServiceOfX/claw-dj |

## Do **not** overwrite the personal `ernestyalumni` deploy by accident

This monorepo’s active `config/` + `data/` may already power
`ernestyalumni-links`. For claw-dj, prefer a **separate Vercel project** (or a
dedicated branch/worktree) so both pages stay live.

### Option A — separate clone (recommended)

```sh
git clone https://github.com/ernestyalumni/links.git claw-dj-links
cd claw-dj-links
npm install
python3 scripts/apply-example.py --name claw-dj

# After you generate art on the 3060 box:
#   public/avatar.jpg   (square, ≥512px, <150 KB ideal)
#   public/og.png       (1200×630)
# optional: public/favicon.svg

python3 scripts/validate.py
npm run build
npm run dev   # http://localhost:4321
```

Then create a new Vercel project from `claw-dj-links`, set production domain
idea: `claw-dj-links.vercel.app` (or a custom domain). Update
`site.url` and `social_meta.og_image` in `config/site.config.json` to the real
URL after first deploy.

### Option B — apply inside this repo on a feature branch

```sh
git checkout -b deploy/claw-dj
python3 scripts/apply-example.py --name claw-dj
# add public/avatar.jpg + public/og.png
python3 scripts/validate.py && npm run build
# deploy that branch to a *second* Vercel project, not the ernestyalumni one
```

## After assets land

1. Drop `avatar.jpg` and `og.png` into `public/`.
2. Confirm `profile.avatar` is `"/avatar.jpg"`.
3. Set `social_meta.og_image` to the **absolute** HTTPS URL of `og.png`.
4. Rebuild and redeploy.
5. Paste the live links URL into TikTok + YouTube “Website / Links” fields.

## Suggested later links (add when ready)

```sh
scripts/links.py add --title "Latest mix on YouTube" --url "https://youtu.be/…" --icon "★" --position 1
scripts/links.py add --title "Anthology: West Coast Chronic era" --url "https://…" --icon "🌴"
```

Keep the list short: primary discovery (YouTube, TikTok), then GitHub, then
one “current featured mix” at the top when you have a hero upload.
