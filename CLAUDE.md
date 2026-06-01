# CLAUDE.md — techdox blog

Context handoff from a claude.ai session. Read this first.

## What this is
A markdown-based rebuild of techdox.nz (currently Ghost) as a **Hugo** static site
with a custom "terminal" theme. Goal: git-based workflow, no CMS/database, served
from a homelab k8s cluster.

## Stack & layout
- Hugo (extended). Custom theme lives in `layouts/` + `assets/css/main.css` — no external theme.
- Aesthetic: dark terminal feel. Fraunces (display) + Hanken Grotesk (body) + JetBrains Mono (meta).
  Accent #4d8dff dark / #1958d7 light. Light/dark toggle persists via localStorage.
- `content/posts/` holds posts. Frontmatter: `title, date, tags[] (first = chip), featured (bool), draft`.
- Taxonomy: `tags`. RSS + Chroma syntax highlighting enabled in `hugo.toml`.

## Commands
    hugo server -D          # local preview at :1313
    hugo --gc --minify      # production build -> public/
    hugo new posts/x.md     # new post from archetype

## Deploy (homelab)
`git push` -> Gitea Actions (`.gitea/workflows/deploy.yml`) builds the multi-stage
`Dockerfile` (Hugo build -> nginx:alpine), pushes to the Gitea registry, k8s pulls it.
`deploy/` has Deployment + Service + Ingress (annotated for the `letsencrypt-dns`
cert-manager ClusterIssuer, ingressClassName `nginx`). Set workflow vars/secrets:
`REGISTRY_HOST`, `REGISTRY_REPO`, `REGISTRY_USER`, `REGISTRY_TOKEN`.

## OPEN ITEMS (pick up here)
1. Newsletter — Ghost's subscribe portal does not survive the move to static.
   Decide: self-hosted listmonk vs hosted Buttondown, then wire it to the
   Subscribe link in layouts/partials/nav.html.
2. Content migration — the 6 posts in content/posts/ are STUBS with real
   titles/dates/tags but placeholder bodies. Import the real content:
   Ghost admin -> Settings -> Export (JSON), then `ghostToHugo --hugo . export.json`,
   verify frontmatter maps (title/date/tags), set featured on the pinned post,
   move images from Ghost's export zip into static/.

## Preferences
Terse, command-focused answers with a short "why" for each step.
