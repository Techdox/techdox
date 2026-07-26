# Phase 5A preflight complete: PASS

The production cutover is ready for a separately approved Phase 5B window.
Phase 5A captured fresh rollback state, reverified both release candidates, and
prepared the permanent redirect data without changing live traffic.

## Release candidates

| Component | Pull request | Candidate | Result |
|---|---|---|---|
| Blog | `Techdox/techdox#3` | `b6d68bf9b7d131933d940a2b79452396ed014f2b` | Open, draft, mergeable; Pages check passed |
| Landing | `Techdox/techdox-landing#1` | `46c44e82452684ebf71643816725042cd9897ca5` | Open, draft, mergeable; local and immutable-preview verification passed |

The blog candidate retained all Phase 2B canonical, Open Graph, alias, feed,
sitemap, route, and preview-indexing guarantees.

The landing candidate rebuilt with 85/85 checks. Its immutable preview passed
10/10 byte-identical asset checks, 14/14 external-link checks, desktop, mobile,
reduced-motion, 404, focus, overflow, metadata, security-header, and automated
accessibility checks with zero violations.

## Fresh rollback baseline

- Existing blog production deployment:
  `22e38982-96e2-43cb-bb0c-021af5e06981`
- Existing blog production commit:
  `5113a615f504351682c2cbf9cd429b3b3232e71e`
- `techdox.nz` and `blog.techdox.nz` still serve byte-identical homepage,
  representative article, and feed responses.
- The full legacy inventory retained its normal disabled-rule shape:
  137 direct `200`, 75 existing slash-normalisation `308`, and 0 migration
  `302` responses.
- All 121 unique blog targets returned directly with `200`.
- `docs.techdox.nz` and `store.techdox.nz` remained healthy.

Exact response hashes are preserved in
`migration/evidence/phase-5a-production-baseline.json`.

## Permanent redirect preparation

Cloudflare now contains an inactive production list:

- Name: `techdox_apex_blog_production_301`
- Items: 212
- Status: inactive
- Associated rule: none
- CSV SHA-256:
  `fe74ba713ae2bb25e8db45e4db62faf64df961641fed4b4c1c4f9e5fa893caa9`

The Phase 4 temporary rule remains disabled. Creating the inactive 301 list did
not alter traffic.

## Cutover constraint

The landing Pages project is a Direct Upload project. Merging its pull request
does not deploy it. Phase 5B must explicitly upload the verified landing
artifact as a production deployment on branch `main`.

## Production-change statement

Phase 5A made no production deployment, domain, DNS, environment-variable,
merge, or live redirect change. Both pull requests remain draft.

## Phase 5B hold

Do not begin the cutover without explicit approval. The coordinated sequence
must retain a working owner for `techdox.nz`, keep `blog.techdox.nz` healthy,
and enable the exact 301 redirect rule only after the landing production
deployment and domain move have been verified.

Evidence:

- `migration/evidence/phase-5a-production-baseline.json`
- `migration/evidence/phase-5a-controls.json`
- `migration/evidence/phase-5a-blog-preview-verification.json`
