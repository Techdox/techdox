# Production baseline

Captured read-only on 2026-07-25.

## Repository

| Setting | Value |
|---|---|
| GitHub repository | `https://github.com/Techdox/techdox` |
| Default branch | `main` |
| Production/source commit | `5113a615f504351682c2cbf9cd429b3b3232e71e` |
| Migration branch | `migration/landing-blog-split` |
| Viewer permission | `ADMIN` |

The latest Cloudflare production deployment reports the same commit as the GitHub `main` head captured during Phase 1.

## Hugo

| Setting | Value |
|---|---|
| Current `baseURL` | `https://techdox.nz/` |
| Post permalink | `/:slug/` |
| Taxonomy | `tags` |
| Pagination size | `10` |
| Source content | `content/posts/` plus `content/deals.md` |
| Custom theme | `layouts/` and `assets/`; no external Hugo theme |
| Local verification image | `hugomods/hugo:exts-0.148.2` |

A clean verification build produced:

- 73 Hugo pages
- 7 paginator pages
- 17 aliases
- 50 static files
- 148 output files

The repository documentation recommends `hugo --gc --minify`, while the live Cloudflare Pages project currently runs `hugo`. This difference is recorded rather than silently normalised during Phase 1.

## Cloudflare Pages project

| Setting | Value |
|---|---|
| Project | `techdox` |
| Pages hostname | `techdox.pages.dev` |
| Git provider | GitHub |
| Owner/repository | `Techdox/techdox` |
| Production branch | `main` |
| Build command | `hugo` |
| Output directory | `public` |
| Root directory | repository root |
| Production deployments | enabled |
| Preview deployments | all branches enabled |
| Pull-request comments | enabled |
| Build image major version | `3` |
| Compatibility date | `2026-06-01` |
| Environment variables | none returned by API |
| Active custom domain | `techdox.nz` |

The active custom domain was created on 2026-06-01. The most recent production deployment completed successfully on 2026-07-15 and serves commit `5113a615f504351682c2cbf9cd429b3b3232e71e`.

## Routing DNS

Only migration-relevant `A`, `AAAA`, and `CNAME` records were captured.

| Name | Type | Target | Proxied |
|---|---|---|---|
| `techdox.nz` | `CNAME` | `techdox.pages.dev` | yes |
| `blog.techdox.nz` | absent | — | — |
| `www.techdox.nz` | absent | — | — |
| `docs.techdox.nz` | `CNAME` | `techdox-docs.pages.dev` | yes |
| `store.techdox.nz` | `A` | `34.117.223.165` | no |

No DNS records were changed.

## Redirect and rules baseline

The zone ruleset list returned three Cloudflare-managed rulesets only:

1. URL normalisation (`http_request_sanitize`)
2. Cloudflare Managed Free WAF (`http_request_firewall_managed`)
3. DDoS L7 protection (`ddos_l7`)

No zone-level custom Single Redirect ruleset was visible.

The current Cloudflare OAuth scope could not read:

- Legacy Page Rules: API error `9109 Unauthorized`.
- Account Bulk Redirect lists: API error `10000 Authentication error`.
- Account rulesets: API error `10000 Authentication error`.

The browser dashboard and Wrangler 4.114.0 sessions were not authenticated. No credentials were requested or entered.

This limitation must not be interpreted as proof that account-level or legacy redirects are absent. Before Phase 4, the account-level redirect inventory must be rechecked using an OAuth scope or authenticated dashboard session that can read those products.

## Source references requiring Phase 2 updates

Three hard-coded apex references were found:

| File | Line | Current value |
|---|---:|---|
| `hugo.toml` | 1 | `https://techdox.nz/` |
| `HUGO.md` | 3 | `https://techdox.nz` |
| `README.md` | 20 | `https://techdox.nz` |

The `hugo.toml` value controls absolute URLs, sitemap output, RSS output, and the existing Open Graph URL. It must change only after `blog.techdox.nz` is attached and verified in Phase 2.

### Canonical metadata baseline

A direct check of the deployed feature-branch article page found:

- `og:url`: `https://techdox.nz/why-selfhost/`
- `<link rel="canonical">`: absent

Phase 2 must therefore add and verify canonical link tags across articles, indexes, pagination, and taxonomies. Updating `baseURL` alone is not sufficient.

## Deployment files not used as production evidence

The repository also contains:

- `.gitea/workflows/deploy.yml`
- `Dockerfile`
- Kubernetes manifests under `deploy/`
- `wrangler.toml` naming `techdox-blog`

These reflect older or alternate deployment paths. The live Cloudflare API, not these files, is authoritative for current production.

## Production behaviour at capture time

- `techdox.nz` still serves the Hugo blog.
- All 141 generated routes probed by Phase 1 returned HTTP `200`.
- `blog.techdox.nz` is not attached or routed.
- No redirect list or redirect rule was created or activated.
- `docs.techdox.nz` and `store.techdox.nz` were not modified.
