# Deploy claw-dj links (second Vercel project)

This repo already has a personal deploy on **`deploy/ernestyalumni`**.
The claw-dj link-in-bio lives on **`deploy/claw-dj`** and should be a
**separate Vercel project** so the two production URLs never overwrite each other.

## Status (repo)

| Item | Value |
|---|---|
| Branch | `deploy/claw-dj` |
| Example template | `examples/claw-dj/` |
| Active config on that branch | claw-dj profile (YouTube, TikTok, GitHub) |
| Theme | `dark-space` / dark |
| Avatar | `/avatar-placeholder.svg` until brand art is added |

## 1. Create the second Vercel project (dashboard)

You only need this once.

1. Open [vercel.com/new](https://vercel.com/new).
2. **Import** `ernestyalumni/links` (same GitHub repo as the personal page).
3. **Project name:** `claw-dj-links` (suggested).
4. Framework: Astro (auto from `vercel.json`).
5. Root directory: `.` (repo root).
6. Before deploy → **Settings → Git → Production Branch** → set to  
   **`deploy/claw-dj`** (not `main`, not `deploy/ernestyalumni`).
7. Deploy.

You should get a production URL like:

```text
https://claw-dj-links.vercel.app
```

(or a team-prefixed variant — copy whatever Vercel shows).

### Protect the personal project

In the **existing** project that serves Ernest’s personal links:

- Production Branch must stay **`deploy/ernestyalumni`** (or whatever it uses today).
- Do **not** point that project’s production branch at `deploy/claw-dj`.

## 2. Or create via CLI (after login)

```sh
cd /path/to/links
git checkout deploy/claw-dj
git pull

# one-time interactive login in your terminal
npx vercel login

# create/link a NEW project (do not reuse the personal "links" project)
npx vercel link --yes --project claw-dj-links
# If prompted: set up and deploy? link only is fine first.

# production deploy from this branch
npx vercel deploy --prod --yes
```

Record the printed production URL.

## 3. Point `site.url` at the real host

```sh
# edit config/site.config.json → site.url = "https://YOUR-REAL-URL"
# after you add public/og.png:
#   social_meta.og_image = "https://YOUR-REAL-URL/og.png"

python3 scripts/validate.py
npm run build
git add config/site.config.json
git commit -m "deploy(claw-dj): set production site.url"
git push origin deploy/claw-dj
```

Vercel will redeploy production from `deploy/claw-dj` automatically if Git is connected.

## 4. Brand assets

Generate from claw-dj’s image prompt doc (§10), then:

```sh
# on deploy/claw-dj
cp /path/to/avatar.jpg public/avatar.jpg
cp /path/to/og.png public/og.png
# set profile.avatar to "/avatar.jpg" in config/site.config.json
# set social_meta.og_image to absolute https URL of og.png
git add public/avatar.jpg public/og.png config/site.config.json
git commit -m "deploy(claw-dj): add avatar and OG image"
git push origin deploy/claw-dj
```

## 5. Wire social bios

| Platform | Field | Value |
|---|---|---|
| TikTok `@clawdj6` | Website | production links URL |
| YouTube `@claw-dj` | Links / website | production links URL |
| Links page | buttons | YouTube, TikTok, GitHub (already in `data/links.json`) |

## 6. Day-to-day updates

```sh
git checkout deploy/claw-dj
scripts/links.py add --title "★ Latest mix" --url "https://youtu.be/…" --icon "★" --position 1
python3 scripts/validate.py
git commit -am "links(claw-dj): feature latest mix"
git push origin deploy/claw-dj
```

## Note on preview deployments

The existing GitHub↔Vercel integration may already build **Preview** deployments
for every push to `deploy/claw-dj`. Those previews can be SSO-gated on a team
account. The **second project** above is what gives you a stable public
production hostname for bios.
