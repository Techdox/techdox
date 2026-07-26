# Phase 2A controls and interpretation

Approved on 2026-07-25. This evidence file defines how Phase 2A must be executed and interpreted before `blog.techdox.nz` is attached.

## Scope

Phase 2A may only:

- Capture a fresh pre-change production baseline.
- Attach `blog.techdox.nz` to the existing `techdox` project through the Cloudflare Pages Custom Domains workflow.
- Establish the exact required `blog.techdox.nz` CNAME only after the Pages custom-domain object exists; never substitute a DNS-only attachment.
- Verify Pages hostname validation, DNS, TLS, and the resulting hostname.

Phase 2A must not:

- Change Hugo `baseURL`.
- Add or alter canonical markup.
- Merge any source or documentation changes to `main`.
- Enable a redirect.
- Remove or modify the `techdox.nz` Pages custom domain.
- Modify `docs.techdox.nz` or `store.techdox.nz`.
- Prepare or begin Phase 2B.

## Hugo alias interpretation

The production `baseURL` remains `https://techdox.nz/` throughout Phase 2A. Hugo-generated alias documents may therefore intentionally contain an HTTP redirect, meta refresh, JavaScript redirect, or canonical target that sends a request from `blog.techdox.nz` to the equivalent canonical page on `techdox.nz`.

Known generated page-one aliases include:

- `/page/1/` → `/`
- `/posts/page/1/` → `/posts/`
- `/tags/<tag>/page/1/` → `/tags/<tag>/`

Verification must record the actual response status, final HTTP URL, meta-refresh target, JavaScript redirect target, and canonical target for every generated alias. A hostname return to the equivalent apex URL is not a Phase 2A failure when it is emitted by the unchanged Hugo alias document. A redirect to an unrelated path, loop, missing page, or non-equivalent destination is a failure.

Non-alias content is expected to serve directly from `blog.techdox.nz` without an unexpected hostname redirect.

## Temporary duplicate-host controls

During Phase 2A:

- Do not add a navigation link, source link, redirect, social link, or other discoverable link to `blog.techdox.nz`.
- Do not submit `https://blog.techdox.nz/sitemap.xml` to Google, Bing, or any other indexer.
- Do not advertise the temporary hostname.
- Record the exact time the Pages custom domain becomes active.
- Set a review deadline exactly seven days later.

If the duplicate-host staging period is expected to exceed seven days, stop before continuing and propose a temporary host-specific `X-Robots-Tag: noindex` control. That control requires separate approval. It must affect only `blog.techdox.nz`, not the apex.

## Build-version evidence

The successful Cloudflare Pages preview for migration commit `2b64f6d85da30b379422ae482a74a472568abdb4` used:

```text
hugo v0.147.7-189453612e4bedc4f27495a7b1145321c8d89807+extended linux/amd64
```

The Phase 1 local build used Hugo Extended `0.148.2`, so the builds are not currently version-aligned. Phase 2A does not change build configuration. Phase 2B local validation must use Hugo Extended `0.147.7` unless a separately approved `HUGO_VERSION` production configuration change establishes another pinned version.

## Fresh rollback baseline

Immediately before the Pages custom-domain request, record:

- Current GitHub `main` commit.
- Current successful Pages production deployment ID and commit.
- Current production deployment status and aliases.
- Current Pages custom domains and statuses.
- Relevant DNS records.
- Existing apex HTTP and TLS behaviour.
- Hugo version from the current successful deployment log.

Do not permanently rely on the Phase 1 commit or deployment as the rollback baseline.

## Supported Phase 2A removal sequence

If rollback is required, follow Cloudflare Pages' supported custom-domain removal sequence:

1. Identify the exact Pages-managed `blog.techdox.nz` DNS record captured after creation.
2. Delete only that exact DNS record if required by the Pages removal workflow.
3. In Workers & Pages → `techdox` → Custom domains, remove only `blog.techdox.nz`.
4. Verify `techdox.nz` remains attached, active, and unchanged.

Never delete, alter, detach, or recreate the apex `techdox.nz` record or custom domain during Phase 2A rollback.

## Result fields

The completed Phase 2A report must include:

- Fresh pre-change baseline file.
- Pages custom-domain status and timestamps.
- Exact managed DNS record type, target, proxy state, and captured record identifier in private execution evidence.
- TLS issuer, validity, and hostname verification.
- Full route-crawl totals.
- Alias behaviour table.
- Feed, tag, pagination, and image results.
- Apex unchanged verification.
- Duplicate-host activation time and seven-day review deadline.
- Confirmation that the hostname remains unlinked and its sitemap was not submitted.

## Observed Phase 2A values

- Fresh baseline: `evidence/phase-2a-prechange-baseline.json`
- Custom domain created: `2026-07-25T11:53:47.285907Z`
- Pages active: `2026-07-25T12:09:34.586452Z`
- Seven-day review deadline: `2026-08-01T11:53:47.285907Z`
- Route verification: 141/141 passed
- Generated aliases: 17/17 contained equivalent apex meta-refresh and canonical targets
- Rendered absolute links to `blog.techdox.nz`: zero
- Sitemap submission: not performed
- Final state: `evidence/phase-2a-postchange-state.json`
- Human report: `phase-2a-report.md`
