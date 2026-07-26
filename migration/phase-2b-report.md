# Phase 2B report

Status: **branch preparation and preview verification passed; production merge held**

Prepared on 2026-07-26 from branch parent `06adbf59706c7edad20954e8d1f9ffbad7d752f2`.

## Scope result

Phase 2B prepares the blog-host metadata on `migration/landing-blog-split` only:

- `baseURL` changes from `https://techdox.nz/` to `https://blog.techdox.nz/`.
- Every generated HTML document receives one explicit canonical link.
- `og:url` uses the same value as the canonical link.
- Article JSON-LD uses the same canonical value for `url` and `mainEntityOfPage`.
- Paginated home, posts, and tag pages keep their own page-number URLs.
- Documentation and repeatable validation scripts are included.

No production merge, Pages environment-variable change, production deployment, custom-domain change, DNS change, redirect activation, sitemap submission, or landing-site deployment is part of Phase 2B.

## Pagination implementation

The existing site intentionally uses different paginator collections:

- homepage: posts excluding the featured article;
- posts section: section pages ordered newest first;
- tag terms: term pages ordered newest first.

An initial disposable test using `.Paginator` unconditionally in the head passed the seven URL assertions but changed the generated site from 7 to 11 paginator pages and from 17 to 19 aliases. That implementation was rejected.

The accepted implementation centralises the existing collections in `layouts/partials/paginator.html`. The head, homepage, and list templates reuse that partial, so metadata and page content operate on the same paginator.

The original generated-site shape is preserved:

| Hugo output | Result |
|---|---:|
| Pages | 73 |
| Paginator pages | 7 |
| Static files | 50 |
| Aliases | 17 |

## Hugo version

Local verification used:

```text
hugo v0.147.7-189453612e4bedc4f27495a7b1145321c8d89807+extended
```

This matches the successful Cloudflare Pages version observed during Phase 2A. No production `HUGO_VERSION` variable was added or changed.

## Exact canonical assertions

All required cases contain exactly one canonical link and one matching `og:url`:

| Case | Expected and observed URL | Result |
|---|---|---|
| Article | `https://blog.techdox.nz/why-selfhost/` | pass |
| Homepage page 1 | `https://blog.techdox.nz/` | pass |
| Homepage page 2 | `https://blog.techdox.nz/page/2/` | pass |
| Posts page 1 | `https://blog.techdox.nz/posts/` | pass |
| Posts page 2 | `https://blog.techdox.nz/posts/page/2/` | pass |
| Tag page 1 | `https://blog.techdox.nz/tags/selfhosting/` | pass |
| Tag page 2 | `https://blog.techdox.nz/tags/selfhosting/page/2/` | pass |

Result: **7/7 passed**. No page-two canonical collapses onto page one.

The complete generated-HTML scan found:

- HTML files: 77;
- missing canonicals: 0;
- duplicate canonicals: 0;
- non-blog canonical hosts: 0.

Exact evidence is in `evidence/phase-2b-canonical-verification.json`.

## Full local build verification

| Check | Result |
|---|---:|
| Inventoried generated routes | 141/141 |
| Static source files copied byte-for-byte | 50/50 |
| Page-one alias canonical and meta-refresh targets | 17/17 |
| Inventoried feeds present | 18/18 |
| Sitemap URLs on `blog.techdox.nz` | 52/52 |
| Rendered files referencing the apex origin | 0 |
| Redirect manifest validation | 212/212, still inactive |

Every generated page-one alias now points to its equivalent blog-host page-one URL. Examples:

| Alias | Target |
|---|---|
| `/page/1/` | `https://blog.techdox.nz/` |
| `/posts/page/1/` | `https://blog.techdox.nz/posts/` |
| `/tags/ai/page/1/` | `https://blog.techdox.nz/tags/ai/` |
| `/tags/selfhosting/page/1/` | `https://blog.techdox.nz/tags/selfhosting/` |

Broader evidence is in `evidence/phase-2b-build-verification.json`. The exact Hugo output is in `evidence/phase-2b-hugo-build.txt`.

## Pre-push production state

Captured read-only at `2026-07-25T22:50:42.361156Z`:

| Item | Value |
|---|---|
| GitHub `main` | `5113a615f504351682c2cbf9cd429b3b3232e71e` |
| Successful production deployment | `22e38982-96e2-43cb-bb0c-021af5e06981` |
| Production deployment commit | `5113a615f504351682c2cbf9cd429b3b3232e71e` |
| Production branch | `main` |
| Production environment variables | none |
| `techdox.nz` Pages domain | active |
| `blog.techdox.nz` Pages domain | active |
| Apex homepage, article, and feed | `200` |
| Docs and store | `200` |

Exact state and response hashes are in `evidence/phase-2b-prepush-production-state.json`.

## Branch preview gate

Cloudflare Pages deployed the exact Phase 2B implementation commit successfully:

| Item | Value |
|---|---|
| Commit | `5ff3988afe18dea236ab3fd6621fa243827ec4be` |
| Deployment | `34883c84-d725-4ae2-aa4e-a7f7daa80161` |
| Environment | preview |
| Immutable URL | `https://34883c84.techdox.pages.dev` |
| Branch alias | `https://migration-landing-blog-split.techdox.pages.dev` |
| Status | success |
| Cloudflare build Hugo | Extended `0.147.7` |

The Pages build log contains:

```text
Executing user command: hugo
hugo v0.147.7-189453612e4bedc4f27495a7b1145321c8d89807+extended linux/amd64 BuildDate=2025-05-31T12:41:12Z VendorInfo=gohugoio
```

Live HTTPS verification passed:

| Check | Result |
|---|---:|
| Representative routes | 14/14 |
| Exact canonical and `og:url` cases | 7/7 |
| Representative page-one aliases | 4/4 |
| Representative feeds | 2/2 |
| Sitemap URLs on the blog host | 52/52 |
| Preview `X-Robots-Tag` | `noindex` |
| Migration evidence URL | `404` |
| Unknown route | `404` |

No tested content route performed an HTTP hostname redirect. Generated page-one aliases use their expected HTML meta refresh and canonical target on `blog.techdox.nz`.

Exact preview evidence is in `evidence/phase-2b-preview-verification.json`.

## Post-push production state

The read-only post-push comparison passed:

- GitHub `main` remains `5113a615f504351682c2cbf9cd429b3b3232e71e`.
- Successful production deployment remains `22e38982-96e2-43cb-bb0c-021af5e06981`.
- Production deployment commit remains `5113a615f504351682c2cbf9cd429b3b3232e71e`.
- Production environment variables remain empty.
- `techdox.nz` and `blog.techdox.nz` remain active and validated.
- Apex homepage, article, and feed response hashes match the pre-push state.
- Docs and store response hashes match the pre-push state.
- Live `blog.techdox.nz` still has apex `og:url` and no explicit canonical link, confirming that the Phase 2B branch was not deployed to production.

Exact state is in `evidence/phase-2b-postpush-state.json`.

## Merge gate

Phase 2B remains unmerged. A production merge is blocked until:

1. temporary redirect mappings are ready for the same controlled launch window;
2. a fresh production rollback baseline is captured;
3. the landing and redirect sequence is approved;
4. any proposed production `HUGO_VERSION` pin is separately approved;
5. the duplicate-host deadline remains satisfied or an approved hostname-specific indexing control is in place.

## Rollback

Before merge, rollback is a revert of the Phase 2B branch commit. No Cloudflare production rollback is required.

The Phase 2A custom-domain rollback remains separate and must remove only `blog.techdox.nz` and its exact DNS record if required. It must not touch the apex custom domain or DNS record.
