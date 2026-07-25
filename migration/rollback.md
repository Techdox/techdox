# Rollback plan

This document describes rollback procedures only. No rule, list, Pages project, custom domain, or DNS change is created by committing it.

## Baseline recovery point

- Blog repository: `Techdox/techdox`
- Baseline branch: `main`
- Baseline commit: `5113a615f504351682c2cbf9cd429b3b3232e71e`
- Existing Pages project: `techdox`
- Existing Pages hostname: `techdox.pages.dev`
- Existing apex custom domain: `techdox.nz`
- Existing apex DNS: proxied CNAME to `techdox.pages.dev`

Do not delete the existing `techdox` Pages project during this migration.

## Disabled emergency redirect

Prepare, but do not enable, one Cloudflare **Single Redirect** with these properties:

| Property | Value |
|---|---|
| Name | `techdox-emergency-return-to-blog` |
| Enabled | `false` |
| Match expression | `(http.host eq "techdox.nz")` |
| Target expression | `concat("https://blog.techdox.nz", http.request.uri.path)` |
| Status | `302` |
| Preserve query string | `true` |

This is intentionally broad. It temporarily sends the landing homepage and all landing routes to the equivalent blog paths. It is an emergency availability measure, not the permanent migration rule.

Single Redirects execute before Bulk Redirects, allowing this temporary rule to override the exact permanent list during an incident.

Creating or enabling this rule is a production change and requires explicit approval. Phase 1 only records the proposed configuration.

## Phase 2 rollback: blog hostname and canonical change

Use if `blog.techdox.nz` or the Hugo `baseURL` deployment fails.

1. Keep `techdox.nz` attached to the existing `techdox` Pages project.
2. Roll the Pages production deployment back to baseline commit `5113a615f504351682c2cbf9cd429b3b3232e71e`, or revert the Phase 2 commit on a feature branch and merge after approval.
3. Confirm canonicals, RSS, and sitemap again use `https://techdox.nz/`.
4. Remove `blog.techdox.nz` from the Pages project only if the failed custom domain itself is causing an incident.
5. Verify representative articles, feeds, images, docs, and store.

Expected effect: the original apex blog continues operating exactly as it did before Phase 2.

## Phase 4 rollback: redirect testing

Use if temporary `302` mappings are incorrect.

1. Disable the Bulk Redirect rule that references the migration list.
2. Leave the list itself intact for inspection unless it is corrupt.
3. Confirm old apex article routes return directly from the existing blog again.
4. Correct and regenerate `migration/url-manifest.json` and the test CSV.
5. Do not convert any rule to `301` until the entire `302` matrix passes.

Expected effect: requests stop using the migration list and return to the pre-test routing path.

## Phase 5 rapid rollback

Use if the landing apex is unhealthy but `blog.techdox.nz` remains healthy.

1. Enable the prepared emergency Single Redirect as a `302`.
2. Verify `/`, a representative article, an RSS route, and an image asset reach `blog.techdox.nz`.
3. Keep the exact Bulk Redirect list enabled or disabled as incident conditions require; the Single Redirect takes precedence.
4. Investigate the landing project without exposing visitors to a broken apex.

Expected effect: all apex traffic temporarily returns to the blog hostname, including paths intended for the landing page.

## Phase 5 full rollback

Use if the apex must return to the old Pages project.

1. Enable the emergency `302` first if immediate traffic protection is needed.
2. Remove `techdox.nz` from the new landing Pages project.
3. Reattach `techdox.nz` to the existing `techdox` Pages project.
4. Verify the apex DNS/custom-domain state resolves to `techdox.pages.dev` again.
5. Roll the blog repository back to the baseline commit if the apex must also resume apex canonicals.
6. Disable the permanent Bulk Redirect rule.
7. Disable the emergency Single Redirect after direct apex service is verified.
8. Crawl the Phase 1 route inventory again.
9. Verify `docs.techdox.nz` and `store.techdox.nz` remain unchanged.

Expected effect: the pre-migration Hugo blog again serves directly from `techdox.nz`.

## Verification matrix after any rollback

At minimum verify:

- `https://techdox.nz/`
- `https://techdox.nz/why-selfhost/`
- `https://techdox.nz/why-selfhost?rollback_test=1`
- `https://techdox.nz/posts/`
- `https://techdox.nz/tags/selfhosting/`
- `https://techdox.nz/index.xml`
- One `/content/images/...` asset
- `https://docs.techdox.nz/`
- `https://store.techdox.nz/`

Check status, final URL, redirect count, TLS, canonical URL, and query-string preservation.
