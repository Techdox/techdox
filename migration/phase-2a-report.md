# Phase 2A report

Status: **accepted**

Executed and verified on 2026-07-25. Phase 2B branch-only preparation was authorised on 2026-07-26.

## Scope result

`blog.techdox.nz` is attached to the existing Cloudflare Pages `techdox` project and serves the unchanged successful production deployment. The original `techdox.nz` custom domain remains attached and active.

No production source deployment, `baseURL` change, canonical change, redirect activation, documentation change, `HUGO_VERSION` change, sitemap submission, or apex removal occurred.

## Fresh rollback baseline

Captured at `2026-07-25T11:53:24.326020Z`, immediately before the Pages custom-domain action.

| Item | Value |
|---|---|
| GitHub `main` | `5113a615f504351682c2cbf9cd429b3b3232e71e` |
| Successful production deployment | `22e38982-96e2-43cb-bb0c-021af5e06981` |
| Production deployment commit | `5113a615f504351682c2cbf9cd429b3b3232e71e` |
| Existing Pages domain | `techdox.nz`, active |
| `blog.techdox.nz` Pages domain | absent |
| `blog.techdox.nz` routing DNS | absent |
| Production Hugo | Extended `0.147.7` |

The exact snapshot is in `evidence/phase-2a-prechange-baseline.json`.

## Production action

At `2026-07-25T11:53:47.285907Z`, the Pages Custom Domains API created:

| Field | Value |
|---|---|
| Pages project | `techdox` |
| Domain | `blog.techdox.nz` |
| Pages domain ID | `d9fc2d29-fe83-4cc3-b04d-6962f49cbf82` |
| Certificate authority | Google |

The Pages API created the custom-domain object first but did not perform the dashboard's DNS-confirmation write. It remained pending with `CNAME record not set`. No standalone DNS-only attachment was substituted: the Pages custom-domain object already existed and owned the hostname before DNS was added.

To complete the supported Pages attachment sequence, the exact required record was created at `2026-07-25T12:02:32.964005Z`:

| Field | Value |
|---|---|
| DNS record ID | `09f8e592625ddd419c3642dd811d78f0` |
| Name | `blog.techdox.nz` |
| Type | `CNAME` |
| Target | `techdox.pages.dev` |
| Proxied | yes |
| TTL | automatic |

The apex DNS record was read before and after this action and was not altered.

Pages first reported both hostname verification and certificate validation active at `2026-07-25T12:09:34.586452Z`.

## Pages, DNS, and TLS

Both Pages domains are active:

- `techdox.nz`
- `blog.techdox.nz`

Public Cloudflare and Google resolvers return Cloudflare anycast addresses for `blog.techdox.nz`. The proxied CNAME is flattened in public responses, which is expected. The workstation's default resolver temporarily retained the pre-creation NXDOMAIN response; testing used public resolver results and direct SNI while that negative cache expired.

HTTPS verification passed:

- TLS validation result: `0`
- Certificate subject: `CN=techdox.nz`
- Issuer: Google Trust Services `WE1`
- SANs: `techdox.nz`, `*.techdox.nz`
- Valid from: 2026-07-04
- Valid until: 2026-10-02
- `https://blog.techdox.nz/`: `200`, no hostname redirect
- HTTP is redirected to HTTPS by Cloudflare

## Full route verification

The Phase 1 inventory was tested on both the apex and blog host. Blog requests used the public Cloudflare address with correct TLS SNI while the local NXDOMAIN cache remained warm.

| Category | Tested | Passed |
|---|---:|---:|
| Articles | 33 | 33 |
| Deals | 1 | 1 |
| Blog indexes | 5 | 5 |
| Pagination | 4 | 4 |
| Taxonomies and tag pagination | 32 | 32 |
| RSS feeds | 18 | 18 |
| Direct image assets | 44 | 44 |
| Landing-owned baseline files | 2 | 2 |
| Root | 1 | 1 |
| Not-found document | 1 | 1 |
| **Total** | **141** | **141** |

All 141 initial response bodies were byte-identical between `techdox.nz` and `blog.techdox.nz`.

Cloudflare normalises `/404.html` identically on both hosts:

```text
/404.html → 308 /404 → 200
```

A genuinely unknown route returns `404` on both hosts with the same response body.

Representative `200` checks included:

- `/`
- `/why-selfhost/`
- `/page/2/`
- `/posts/`
- `/posts/page/2/`
- `/tags/selfhosting/`
- `/tags/selfhosting/page/2/`
- `/index.xml`
- `/tags/selfhosting/index.xml`
- `/content/images/2023/03/IMG_2009-Small.png`
- `/robots.txt`
- `/sitemap.xml`

The complete result set is in `evidence/phase-2a-route-verification.json`.

## Observed Hugo alias behaviour

All 17 generated page-one aliases returned `200` HTML on `blog.techdox.nz`. Each document contained both a meta refresh and alias canonical pointing to the equivalent apex route because production `baseURL` remains `https://techdox.nz/`.

Examples:

| Requested on blog host | Observed generated target |
|---|---|
| `/page/1/` | `https://techdox.nz/` |
| `/posts/page/1/` | `https://techdox.nz/posts/` |
| `/tags/ai/page/1/` | `https://techdox.nz/tags/ai/` |
| `/tags/selfhosting/page/1/` | `https://techdox.nz/tags/selfhosting/` |

Result: **17/17 equivalent apex targets observed**. This is the approved transitional Hugo behaviour, not a routing failure. Non-alias routes served directly from the blog hostname without a hostname redirect.

## Metadata, feeds, and duplicate-host controls

Production behaviour remains unchanged:

- Repository `baseURL`: `https://techdox.nz/`
- Homepage `og:url`: `https://techdox.nz/`
- Article `og:url`: `https://techdox.nz/why-selfhost/`
- Explicit canonical link on ordinary pages: absent
- Sitemap: 52 apex URL occurrences, zero blog URL occurrences
- Main feed: 42 apex URL occurrences, zero blog URL occurrences
- Selfhosting tag feed: 34 apex URL occurrences, zero blog URL occurrences
- Production `HUGO_VERSION` environment variable: absent
- Production build log: Hugo Extended `0.147.7`

No absolute rendered link to `blog.techdox.nz` was found across the 141 checked outputs. No source or navigation link was added. The blog sitemap was **not submitted**, and the temporary hostname was not advertised.

No `X-Robots-Tag` has been added during the initial seven-day window. This is intentional and is not approval to continue duplicate-host staging beyond the deadline.

## Unchanged production and unrelated hosts

Post-change assertions passed:

- GitHub `main` is unchanged.
- Successful production deployment ID is unchanged.
- Production deployment commit is unchanged.
- `techdox.nz` remains active.
- Apex homepage, article, and feed response hashes match the immediate pre-change baseline.
- `docs.techdox.nz` response hash matches the pre-change baseline.
- `store.techdox.nz` response hash matches the pre-change baseline.
- No source files differ from `main` under `hugo.toml`, `config.toml`, `content/`, `layouts/`, or `static/`.

## Duplicate-host deadline

A conservative seven-day clock starts from custom-domain creation, earlier than first confirmed public activation:

```text
Start:    2026-07-25T11:53:47.285907Z
Deadline: 2026-08-01T11:53:47.285907Z
```

If the duplicate-host staging period may continue beyond that deadline, stop and propose a temporary host-specific:

```text
X-Robots-Tag: noindex
```

That proposal requires separate approval and must affect only `blog.techdox.nz`.

## Rollback identifiers and sequence

If rollback is required, follow Cloudflare's supported Pages removal order:

1. Reconfirm that DNS record ID `09f8e592625ddd419c3642dd811d78f0` is still exactly the proxied `blog.techdox.nz CNAME techdox.pages.dev` record.
2. Delete only that exact blog DNS record.
3. Remove only Pages custom domain `blog.techdox.nz`, ID `d9fc2d29-fe83-4cc3-b04d-6962f49cbf82`, from project `techdox`.
4. Verify `techdox.nz` remains attached and active.
5. Verify production deployment `22e38982-96e2-43cb-bb0c-021af5e06981` and commit `5113a615f504351682c2cbf9cd429b3b3232e71e` still serve the apex.
6. Recheck apex, article, feed, image, docs, and store routes.

Do not modify, delete, detach, or recreate the apex DNS record or custom domain.

## Acceptance gate

- [x] Clarifications recorded before execution
- [x] Fresh rollback baseline captured
- [x] Pages Custom Domain created before routing DNS
- [x] Exact blog DNS record captured
- [x] Pages hostname verification active
- [x] TLS validation active
- [x] Existing apex custom domain still active
- [x] 141/141 route checks passed
- [x] 17/17 alias targets observed and classified correctly
- [x] Articles, images, feeds, tags, and pagination passed
- [x] Metadata and `baseURL` unchanged
- [x] Blog hostname remains unlinked
- [x] Blog sitemap not submitted
- [x] Seven-day review deadline recorded
- [x] Production deployment unchanged
- [x] Docs and store unchanged
- [x] Phase 2B not started

**Phase 2A verification passed and was accepted before Phase 2B branch preparation began.**
