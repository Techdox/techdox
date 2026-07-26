# Phase 4 complete: PASS

Phase 4 created and exercised the temporary Cloudflare Bulk Redirect
configuration. The test rule is disabled, production behavior is back at the
pre-test baseline, and no permanent redirect has been enabled.

## Cloudflare configuration

- List: `techdox_apex_blog_phase4_302`
- List items: 212
- Redirect status: 302
- Query strings: preserved
- Include subdomains: disabled
- Subpath matching: disabled
- Preserve path suffix: disabled
- Rule: `Techdox apex blog migration — temporary 302 validation`
- Expression: `http.host eq "techdox.nz"`
- Final rule state: disabled

## Live validation

| Check | Result |
|---|---:|
| HTTPS mappings | 212/212 |
| HTTP mappings | 212/212 |
| Total scheme checks | 424/424 |
| Protected-route captures | 0 |
| Subdomain captures | 0 |
| Redirect chains | 0 |
| Redirect loops | 0 |
| Unexpected redirects | 0 |
| Unique blog targets returning directly with 200 | 121/121 |

The emergency disable watchdog was armed before activation and removed after
the rule was disabled and propagation had completed.

## Post-disable verification

The Cloudflare dashboard showed the rule disabled. A fresh 212-source probe
returned the original production shape:

- 137 direct `200` responses
- 75 existing trailing-slash `308` responses
- 0 temporary migration `302` responses

The protected apex routes were not captured. `blog.techdox.nz`,
`docs.techdox.nz`, and `store.techdox.nz` remained outside the rule.

## Evidence

- `migration/evidence/phase-4-live-validation.json`
- `migration/evidence/phase-4-post-disable.json`

Phase 5 remains blocked until the coordinated production cutover is explicitly
approved. The Phase 4 list and disabled rule can be reused for that cutover
after changing the redirect status to the approved permanent value.
