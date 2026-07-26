# Techdox site migration

This directory is the version-controlled control plane for moving the existing Hugo blog from `techdox.nz` to `blog.techdox.nz` and introducing a separate landing site at `techdox.nz`.

## Migration checklist

- [x] Phase 1 — Inventory and rollback preparation
- [x] Phase 2A — `blog.techdox.nz` attached, verified, and accepted
- [x] Phase 2B — Canonical changes prepared and preview-verified; production merge held
- [x] Phase 3 — Build and verify the isolated landing preview
- [x] Phase 4 — Configure, exercise, and disable temporary redirects
- [x] Phase 5A — Production cutover preflight
- [x] Phase 5B — Controlled production cutover

Phase 1 was read-only against production. Phase 2A attached `blog.techdox.nz`
without deploying source or enabling redirects; see `phase-2a-report.md`.
Phase 2B changes only the migration branch and its preview. Phase 3 produced a
verified landing preview in the separate `Techdox/techdox-landing` repository.
Phase 4 proved all exact redirects using a temporary 302 rule and returned that
rule to disabled. Phase 5A preflight is documented but must not be treated as
cutover approval. Phase 5B completed the production split: the landing owns the
apex, the blog owns `blog.techdox.nz`, and the exact permanent redirects are
active.

## Architecture

| Host | Intended owner |
|---|---|
| `techdox.nz` | New landing Pages project |
| `blog.techdox.nz` | Existing `Techdox/techdox` Hugo project |
| `docs.techdox.nz` | Unchanged |
| `store.techdox.nz` | Unchanged |

The migration uses exact Cloudflare Bulk Redirect entries. It does not use a permanent apex wildcard. The apex homepage, sitemap, robots file, and future landing routes remain available to the landing project.

## Phase 1 results

- Live sitemap URLs: **52**
- Hugo-generated and currently reachable routes: **141**
- Root-level articles: **33**
- Direct historical image assets: **44**
- RSS/feed routes: **18**
- Exact redirect entries: **212**
- Production probes: **141/141 successful after expected Pages normalisation**
- Hard-coded apex references in source: **3**
- Cloudflare Free-plan Bulk Redirect allowance: **10,000**

The 212 entries include:

- Both slash and no-slash forms for HTML routes.
- Both HTTP and HTTPS through Cloudflare's scheme-less source matching.
- Pagination aliases with direct canonical targets.
- RSS and tag feeds.
- Direct `/content/images/...` assets.
- Query-string preservation.

All rules are exact. `include_subdomains`, `subpath_matching`, and `preserve_path_suffix` are disabled.

## Phase 2B branch preparation

The migration branch now prepares the blog hostname metadata without changing production:

- `baseURL` is `https://blog.techdox.nz/` on `migration/landing-blog-split` only.
- Every generated HTML document has one canonical URL on `blog.techdox.nz`.
- `og:url` uses the same URL as the canonical link.
- Homepage, posts, and tag page-two canonicals retain `/page/2/`.
- The paginator collection is shared by the head and body templates so metadata cannot create a second or different paginator.
- Hugo Extended `0.147.7` is used for local evidence to match the successful Pages build.

The branch must not be merged until the temporary redirect test list and coordinated launch window are approved. No Pages environment variable or production `HUGO_VERSION` pin is part of Phase 2B.

## Landing-owned and reserved paths

These paths are deliberately absent from the redirect list:

- `/`
- `/robots.txt`
- `/sitemap.xml`
- `/about/`
- `/contact/`
- `/projects/`

`/deals/` currently belongs to the blog and is mapped to `blog.techdox.nz/deals/`. A future landing-page deals section can link to that route or use a different landing route.

## Internet Archive inventory

The Wayback CDX index exposed 1,977 unique historical paths, including an older WordPress-era site dating back to 2017.

- 29 are covered by current routes.
- 117 are dated historical article paths with no current destination.
- 35 are old date archives.
- 126 are old indexes or feeds.
- 1 is a WordPress utility path.
- 1,669 are other historical paths.

No redirect was generated for a route whose proposed blog destination does not exist. Sending an old URL to a new `404` would not preserve it. The full classification remains in `evidence/wayback-historical-paths.json` for future content-restoration decisions.

The archive also shows historical `www.techdox.nz` use. `www` does not currently have a routing DNS record, so restoring it would be a separate, explicitly approved production change.

## Artifacts

| File | Purpose |
|---|---|
| `url-manifest.json` | Canonical machine-readable redirect source |
| `generated/cloudflare-bulk-redirects-test-302.csv` | Inactive test import |
| `generated/cloudflare-bulk-redirects-production-301.csv` | Inactive production import |
| `scripts/inventory_urls.py` | Rebuild source/live/archive inventory |
| `scripts/generate_redirects.py` | Validate manifest and generate CSV files |
| `scripts/assert_canonicals.py` | Assert exact canonical and Open Graph URLs, including pagination |
| `scripts/verify_phase2b_build.py` | Verify the full route, alias, feed, sitemap, and static-asset build |
| `scripts/verify_phase2b_preview.py` | Verify metadata, routes, aliases, feeds, sitemap, and indexing headers over preview HTTPS |
| `production-baseline.md` | GitHub, Hugo, Pages, DNS, and rules baseline |
| `rollback.md` | Disabled emergency redirect and rollback procedures |
| `evidence/live-sitemap.xml` | Production sitemap captured during Phase 1 |
| `evidence/live-route-probes.json` | Production route probe results |
| `evidence/source-routes.json` | Hugo routes, assets, canonicals, and source references |
| `evidence/cloudflare-production.json` | Sanitised Pages/DNS snapshot |
| `evidence/cloudflare-zone-rulesets.json` | Zone ruleset summary |
| `phase-2a-report.md` | Human-readable Phase 2A execution and acceptance report |
| `evidence/phase-2a-controls.md` | Approved Phase 2A scope, alias interpretation, indexing controls, and rollback sequence |
| `evidence/phase-2a-prechange-baseline.json` | Fresh rollback baseline captured immediately before attachment |
| `evidence/phase-2a-route-verification.json` | Full dual-host route, hash, metadata, and alias results |
| `evidence/phase-2a-postchange-state.json` | Final Pages, DNS, TLS, deployment, and staging-deadline evidence |
| `phase-2b-report.md` | Human-readable Phase 2B branch preparation and preview report |
| `evidence/phase-2b-controls.md` | Phase 2B scope, production guardrails, and rollback gate |
| `evidence/phase-2b-hugo-build.txt` | Exact matching-version local Hugo build output |
| `evidence/phase-2b-canonical-verification.json` | Seven exact canonical cases and complete generated-HTML scan |
| `evidence/phase-2b-build-verification.json` | Route, alias, feed, sitemap, origin, and static-asset results |
| `evidence/phase-2b-prepush-production-state.json` | Read-only production state captured before the branch push |
| `evidence/phase-2b-preview-verification.json` | Live HTTPS checks against the exact Phase 2B preview deployment |
| `evidence/phase-2b-postpush-state.json` | Preview build record and read-only production comparison after the branch push |
| `phase-4-report.md` | Temporary 302 redirect activation, full validation, and post-disable report |
| `evidence/phase-4-live-validation.json` | All HTTPS and HTTP exact-mapping results from the temporary rule |
| `evidence/phase-4-post-disable.json` | Full legacy-route verification after the temporary rule was disabled |
| `phase-5a-report.md` | Production cutover readiness report and explicit Phase 5B hold |
| `evidence/phase-5a-production-baseline.json` | Fresh production hashes, route shape, and rollback baseline |
| `evidence/phase-5a-controls.json` | Pull request, Pages, redirect-list, and no-production-change controls |
| `evidence/phase-5a-blog-preview-verification.json` | Live verification of the exact blog release candidate preview |
| `phase-5b-report.md` | Final production cutover, deployment, redirect, verification, and rollback report |
| `evidence/phase-5b-controls.json` | Final GitHub, Pages, domain, redirect-rule, and deferred-follow-up state |
| `evidence/phase-5b-live-verification.json` | Full live HTTPS, HTTP, target, protected-route, service, and metadata verification |
| `scripts/verify_phase5b.py` | Repeatable full production cutover verifier |
| `evidence/wayback-historical-paths.json` | Historical URL classification |

## Rebuild and verify

A pinned Hugo container is used because Hugo is not installed on the host. Phase 1 evidence used Extended `0.148.2`; Phase 2B uses Extended `0.147.7` to match Cloudflare Pages:

```bash
docker run --rm \
  -v /tmp/techdox-build-src:/src \
  -v /tmp/techdox-hugo-public:/output \
  -w /src \
  hugomods/hugo:exts-0.147.7 \
  hugo --gc --minify --destination /output

python3 migration/scripts/assert_canonicals.py \
  --build-dir /tmp/techdox-hugo-public \
  --output migration/evidence/phase-2b-canonical-verification.json

python3 migration/scripts/verify_phase2b_build.py \
  --repo . \
  --build-dir /tmp/techdox-hugo-public \
  --route-evidence migration/evidence/source-routes.json \
  --output migration/evidence/phase-2b-build-verification.json

python3 migration/scripts/inventory_urls.py \
  --repo . \
  --build-dir /tmp/techdox-hugo-public \
  --wayback /tmp/techdox-wayback.json

python3 migration/scripts/generate_redirects.py \
  --manifest migration/url-manifest.json \
  --build-dir /tmp/techdox-hugo-public
```

The source must be copied into `/tmp/techdox-build-src` first so Hugo can create its build lock and resource cache without modifying the feature-branch checkout.
