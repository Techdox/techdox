# Techdox — Hugo

The terminal-styled, markdown-based rebuild of [techdox.nz](https://techdox.nz). No CMS, no database — just markdown in git, built to static HTML.

## Stack

- **Hugo** (extended) — static site generator, single binary, sub-second builds
- Custom theme baked into `layouts/` + `assets/css/main.css` (no external theme dependency)
- Syntax-highlighted code, tags, RSS, light/dark toggle

## Run it locally

```bash
hugo server -D          # -D includes drafts; live-reloads on save
# → http://localhost:1313
```

`hugo` (no args) does a production build into `public/`. That's what the Dockerfile runs.

## Write a post

```bash
hugo new posts/my-new-post.md
```

Frontmatter that the templates read:

```toml
title    = "Post title"
date     = 2026-06-01T09:00:00+12:00
tags     = ["kubernetes", "homelab"]   # first tag shows as the chip
featured = true                        # one post → big hero card on the homepage
draft    = true                        # flip to false / remove to publish
```

Why it matters: `featured` controls the homepage hero (falls back to newest post if none set); the first tag drives the chip and links to `/tags/<tag>/`; `date` orders everything.

## Migrating from Ghost

1. Ghost admin → **Settings → Export** → downloads a JSON of all posts.
2. Convert to Hugo markdown. The community tool `ghostToHugo` handles this:
   ```bash
   ghostToHugo --hugo . your-ghost-export.json
   ```
   It writes markdown + frontmatter into `content/`. Check that `title`, `date`, and `tags` map across (they line up with the fields above) and set `featured` on whichever post you want pinned.
3. Images: Ghost's full export zip includes `/content/images/` — drop them into `static/` and fix the paths.

The six posts currently in `content/posts/` are starter stubs with your real titles/tags/dates — replace their bodies with the imported content.

## Deploy (wired for your lab)

The flow: `git push` → Gitea Actions builds a tiny nginx image → pushes to your Gitea registry → k8s pulls it.

1. **CI** — `.gitea/workflows/deploy.yml`. Set repo variables `REGISTRY_HOST`, `REGISTRY_REPO` and secrets `REGISTRY_USER`, `REGISTRY_TOKEN`. The runner needs Docker.
2. **Image** — `Dockerfile` is multi-stage: builds Hugo, then serves `public/` from `nginx:alpine` (`deploy/nginx.conf` handles gzip + immutable caching on the fingerprinted CSS).
3. **Kubernetes** — `deploy/` has Deployment, Service, and an Ingress annotated for your `letsencrypt-dns` ClusterIssuer on `ingressClassName: nginx`. Edit the image ref + apply:
   ```bash
   kubectl apply -f deploy/
   ```

Since builds are static and tiny (~30 ms Hugo, small image), the long-build Cloudflare proxy timeout isn't a factor here — but the registry push still goes through Cloudflare, so keep that DNS record grey-clouded if you hit it.

## Newsletter / members

Static sites have no server, so Ghost's subscribe portal doesn't carry over. Replace with:

- **listmonk** — self-hosted, fits the lab; embed its subscribe form behind the `/subscribe/` link in the nav.
- **Buttondown** — hosted, zero maintenance, generous free tier.

Wire whichever to the `Subscribe` button in `layouts/partials/nav.html`.
