# Phase 1 acceptance report

Date: 2026-07-25
Branch: `migration/landing-blog-split`
Baseline commit: `5113a615f504351682c2cbf9cd429b3b3232e71e`

## Checklist

- [x] Repository, branch, commit, Hugo configuration, and build layout recorded.
- [x] Live Cloudflare Pages project and active custom domain recorded.
- [x] Migration-relevant DNS records recorded.
- [x] Zone ruleset summary recorded.
- [x] Live sitemap captured.
- [x] Hugo routes, aliases, pagination, feeds, and direct image assets inventoried.
- [x] Hard-coded apex references inventoried.
- [x] Internet Archive paths classified separately from currently valid routes.
- [x] Exact URL migration manifest generated.
- [x] Temporary `302` and production `301` Bulk Redirect CSVs generated but not uploaded.
- [x] Disabled emergency `302` configuration documented but not created.
- [x] Rollback procedures documented for Phases 2, 4, and 5.
- [x] Production behaviour rechecked after artifact creation.

## Verification results

| Check | Result |
|---|---|
| Hugo container build | Passed with Hugo Extended 0.148.2 |
| Generated output | 148 files, 73 pages, 7 paginator pages, 17 aliases |
| Generated/current routes | 141 |
| Live route probes | 141/141 returned HTTP 200 |
| Live sitemap | HTTP 200, 52 URLs |
| Manifest validation | Passed, no errors or warnings |
| Exact redirect entries | 212 |
| Cloudflare Free-plan allowance | 10,000 |
| Test CSV | 212 valid `302` rows |
| Production CSV | 212 valid `301` rows |
| Query preservation | Enabled on every row |
| Include subdomains | Disabled on every row |
| Subpath matching | Disabled on every row |
| Preserve path suffix | Disabled on every row |
| Landing-owned path collisions | None |
| Missing local blog targets | None |
| Duplicate sources | None |
| Secret scan | No token, bearer credential, password, client secret, or private-key pattern found |
| Identifier scan | Cloudflare account/zone identifiers absent from committed evidence |
| Repository scope | All changes are under `migration/` |

## Production unchanged verification

The following remained HTTP 200 at their original URLs after Phase 1:

- `https://techdox.nz/`
- `https://techdox.nz/why-selfhost/`
- `https://techdox.nz/index.xml`
- `https://docs.techdox.nz/`
- `https://store.techdox.nz/`

`blog.techdox.nz` still has no routing DNS result and is not attached to the Pages project.

No DNS record, Pages project, custom domain, redirect rule, Bulk Redirect list, or production deployment was changed.

## Recorded limitation

The Cloudflare operational OAuth connection can read Pages, DNS, and the zone ruleset list. It cannot currently read legacy Page Rules or account-level Bulk Redirect lists/rulesets. The browser dashboard and Wrangler sessions are not authenticated.

No custom zone redirect ruleset is visible, and all inventoried apex routes currently resolve directly without a redirect. Account-level redirect inventory must still be rechecked before Phase 4 using an OAuth scope or dashboard session that can read those products.

This is a **pre-Phase-4 prerequisite**, not a Phase 2 blocker.

## Gate result

**PASS with one recorded pre-Phase-4 access prerequisite.**

Phase 2 must not begin until its exact production changes, expected effects, and rollback procedure are presented and explicitly approved.
