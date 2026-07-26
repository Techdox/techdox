# Phase 5B production cutover complete: PASS

`techdox.nz` now serves the new Techdox landing page.
`blog.techdox.nz` serves the Hugo blog, and every approved historical apex blog
URL redirects permanently to its exact blog-host destination.

## Production ownership

| Host | Production owner | Result |
|---|---|---|
| `techdox.nz` | Pages project `techdox-landing` | Active, SSL enabled |
| `blog.techdox.nz` | Pages project `techdox` | Active, SSL enabled |
| `docs.techdox.nz` | Unchanged | Healthy |
| `store.techdox.nz` | Unchanged | Healthy |

## GitHub and Pages deployments

The blog PR was merged first. Its Git-connected Pages production deployment
completed before any apex routing change:

- PR: `Techdox/techdox#3`
- Merge commit: `45f4e8ea96037d82886aba0ccbafae6301599b73`
- Pages deployment: `91b2c659-2621-4413-9a5f-62d544840786`
- Immutable URL: `https://91b2c659.techdox.pages.dev`

The landing PR was then merged and rebuilt from the exact `main` merge commit:

- PR: `Techdox/techdox-landing#1`
- Merge commit: `2145fe0f1a04ccb8130a5de27f44dd1601844f37`
- Local build: 85/85 checks passed
- Artifact: 11 files, 167,521 bytes
- Artifact ZIP SHA-256:
  `18566a3e87f02b6bb3fad68d27219b817382ed8a8bb4d8146bcba38b84fb34f6`
- Pages deployment: `f97a22b9-b22b-4459-aa81-b172e77f2bb2`
- Immutable URL: `https://f97a22b9.techdox-landing.pages.dev`

The landing Pages project is still configured as Direct Upload. Automatic
GitHub deployment for that project is deliberately deferred until after the
completed cutover.

## Permanent redirect rule

- Rule: `Techdox apex blog migration — permanent 301 redirects`
- Rule ID: `bba8c7249541473cba78b9af75342ab6`
- List: `techdox_apex_blog_production_301`
- Entries: 212
- Expression: `http.host eq "techdox.nz"`
- Lookup key: `http.request.full_uri`
- Query strings: preserved
- Final state: enabled

The Phase 4 temporary 302 rule remains disabled.

## Live acceptance results

| Check | Result |
|---|---:|
| HTTPS exact mappings | 212/212 |
| HTTP exact mappings | 212/212 |
| Unique blog targets returning directly with 200 | 121/121 |
| Protected landing and service checks | 13/13 |
| Redirect mapping errors | 0 |
| Target errors | 0 |
| Metadata errors | 0 |

The apex landing response includes the account's expected Cloudflare Web
Analytics beacon. After removing only that known injected script, its SHA-256
is byte-identical to the verified Pages artifact:

`19680c94e8919e8c8ffb8b23db6acde6ee5520619278fc1f1bef89e96df079e0`

The blog article canonical and Open Graph URL use `blog.techdox.nz`. Blog feeds
contain blog-host URLs and no apex-host references.

## Rollback points retained

- Disable the permanent 301 rule to stop migration redirects.
- Remove `techdox.nz` from `techdox-landing` and reattach it to `techdox`.
- Roll the blog project back to deployment
  `22e38982-96e2-43cb-bb0c-021af5e06981` if canonical metadata must also be
  reverted.
- The landing production deployment remains independently available at
  `techdox-landing.pages.dev`.

## Evidence

- `migration/evidence/phase-5b-controls.json`
- `migration/evidence/phase-5b-live-verification.json`
- `migration/scripts/verify_phase5b.py`
