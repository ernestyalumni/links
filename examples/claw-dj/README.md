# claw-dj links example

Link-in-bio profile for the **claw-dj** hip-hop / R&B anthology + short-form
project. Pair with image assets described in the claw-dj repo:

`repos/claw-dj/docs/IMAGE_PROMPTS_ANTHOLOGY_VISUALS.md` → section **Brand
identity assets** (avatar, OG banner, favicon).

## Channels this page points at

| Surface | URL |
|---|---|
| YouTube | https://www.youtube.com/@claw-dj |
| TikTok | https://www.tiktok.com/@claw__dj |
| GitHub | https://github.com/InServiceOfX/claw-dj |

## Production branch (already set up in git)

Active deploy branch: **`deploy/claw-dj`** (pushed to `origin`).

- Config/data on that branch are the claw-dj profile.
- Personal Ernest page stays on **`deploy/ernestyalumni`**.
- Full Vercel second-project wiring: [`docs/DEPLOY_CLAW_DJ.md`](../../docs/DEPLOY_CLAW_DJ.md).

```sh
git checkout deploy/claw-dj
git pull
npm install
python3 scripts/validate.py
npm run dev   # http://localhost:4321
```

### Second Vercel project (required for a public production URL)

Same GitHub repo, **new** Vercel project named e.g. `claw-dj-links`, with
**Production Branch = `deploy/claw-dj`**. Do not retarget the personal project’s
production branch. See `docs/DEPLOY_CLAW_DJ.md` for dashboard + CLI steps.

After deploy, set `site.url` (and later `social_meta.og_image`) to the real host.

### Assets after you generate brand art

```text
public/avatar.jpg   # square, ≥512px, <150 KB ideal
public/og.png       # 1200×630
# optional: public/favicon.svg
```

Then set `profile.avatar` to `"/avatar.jpg"` and push.

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
