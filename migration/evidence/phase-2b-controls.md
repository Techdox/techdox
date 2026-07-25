# Phase 2B controls

Status: **branch-only preparation authorised**

Authorised on 2026-07-26 for `migration/landing-blog-split` only.

## Allowed scope

- Change the branch `baseURL` to `https://blog.techdox.nz/`.
- Add explicit canonical metadata and keep Open Graph URLs consistent with it.
- Preserve page-number canonicals for paginated home, posts, and tag pages.
- Add tests, evidence, and documentation.
- Build locally with Hugo Extended `0.147.7`.
- Push the migration branch and inspect its Cloudflare Pages preview.

## Production guardrails

Phase 2B does not authorise:

- merging or pushing to `main`;
- changing a production Pages deployment;
- changing Pages environment variables;
- adding a production `HUGO_VERSION` pin;
- activating temporary or permanent redirects;
- changing Pages custom domains or DNS;
- submitting the blog sitemap;
- linking the temporary duplicate hostname from the production site;
- creating or deploying the landing site.

The production merge remains blocked until the temporary redirect test list and coordinated launch window are ready and separately approved.

## Hugo version

Local evidence uses `hugomods/hugo:exts-0.147.7`, matching the successful Cloudflare Pages build observed during Phase 2A. Phase 1 local evidence used Extended `0.148.2` and remains historical.

No Pages environment variable was changed. A future production `HUGO_VERSION=0.147.7` pin, if proposed, is a separate production configuration change with its own effect and rollback.

## Pagination control

Calling `.Paginator` unconditionally from the head template creates paginators for pages that did not previously paginate. The accepted implementation centralises the existing intentional paginator collections in `layouts/partials/paginator.html` and reuses that partial from the head and body templates.

The generated-site shape must remain:

- pages: 73;
- paginator pages: 7;
- aliases: 17;
- static files: 50.

## Required exact assertions

Each route must contain exactly one canonical link and one matching `og:url`:

| Case | Expected URL |
|---|---|
| Article | `https://blog.techdox.nz/why-selfhost/` |
| Homepage page 1 | `https://blog.techdox.nz/` |
| Homepage page 2 | `https://blog.techdox.nz/page/2/` |
| Posts page 1 | `https://blog.techdox.nz/posts/` |
| Posts page 2 | `https://blog.techdox.nz/posts/page/2/` |
| Tag page 1 | `https://blog.techdox.nz/tags/selfhosting/` |
| Tag page 2 | `https://blog.techdox.nz/tags/selfhosting/page/2/` |

Page-two URLs must not collapse onto page one.

The broader build gate also requires:

- 141/141 inventoried generated route files;
- 50/50 static files copied byte-for-byte;
- 17/17 page-one alias canonicals and meta-refresh targets on the blog host;
- 18/18 feeds present;
- 52/52 sitemap URLs on the blog host;
- one canonical on every generated HTML file;
- no rendered apex-origin references.

## Rollback

Before merge, rollback is a revert of the Phase 2B migration-branch commit. No Cloudflare production rollback is required because Phase 2B does not change production.

If a production merge is later approved, capture a fresh `main` commit, successful Pages production deployment ID, Pages environment state, custom domains, and relevant DNS immediately before that operation. Document its deployment-specific rollback separately.

## Duplicate-host deadline

Phase 2A's conservative staging deadline remains `2026-08-01T11:53:47.285907Z`. If duplicate-host staging may continue beyond that point, stop and propose a temporary hostname-specific `X-Robots-Tag: noindex` control before continuing.
