---
version: alpha
name: Techdox Blog
description: Practical self-hosting, from my own homelab.
colors:
  primary: "#4D8DFF"
  background: "#090C12"
  raised: "#0D121B"
  panel: "#111824"
  soft: "#151E2C"
  text: "#F4F7FB"
  muted: "#9AA8BC"
  bright: "#79AAFF"
  cyan: "#65DCE9"
  success: "#65E6A7"
  caution: "#FFD166"
  line: "#293445"
  lightBackground: "#F6F5F1"
  lightPanel: "#FFFFFF"
  lightText: "#14181F"
  lightMuted: "#565E6C"
  lightAccent: "#1958D7"
typography:
  h1:
    fontFamily: Fraunces
    fontWeight: 600
  body-md:
    fontFamily: Hanken Grotesk
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: JetBrains Mono
    fontWeight: 500
rounded:
  panel: 18px
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.muted}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.background}"
  page-light:
    backgroundColor: "{colors.lightBackground}"
    textColor: "{colors.lightText}"
  panel-light:
    backgroundColor: "{colors.lightPanel}"
    textColor: "{colors.lightMuted}"
  button-primary-light:
    backgroundColor: "{colors.lightAccent}"
    textColor: "{colors.lightPanel}"
---

## Overview

Blog-only adoption of the supplied Techdox-Brand-Kit. Canonical reference:
`/home/techdox/brand/techdox/DESIGN.md`; original masters and exact token export:
`/home/techdox/brand/techdox/Techdox-Brand-Kit/` (`logos/`, `social/`, `tokens/techdox.css`).
Use Techdox in prose; never typeset a substitute for the supplied lowercase logo.
Keep the personal editorial voice and contextual “Break things, start small,
document everything” headline. Generic site description: “Practical self-hosting,
from my own homelab.” Brand tagline: “Build it. Break it. Understand it.”

## Colors

`assets/css/main.css` maps the kit dark palette to existing semantic names:
`--bg`, `--bg-soft` (raised), `--panel`, `--panel-2` (soft), `--text`,
`--muted`/`--faint`, `--accent`, `--accent-bright`, `--border`/`--border-strong`.
Blue-filled controls use dark `--on-accent` text, never white on #4D8DFF.

The kit has no light palette. Preserve the blog's warm light surfaces, dark body
text and #1958D7 links/buttons; white text on that darker blue passes AA. Light
cyan/success/caution adaptations are #006B78/#187344/#805B00, not kit exports.
Keep existing terminal illustration and syntax colors separate from page tokens;
terminal illustrations remain dark in light mode. Do not use status colors as
arbitrary decorative emphasis. Browser tests check key foreground/background
pairs in both themes; this is not a claim of a complete WCAG audit.

## Typography

Preserve locally hosted Fraunces editorial titles and headings (600), Hanken
Grotesk body/UI, and JetBrains Mono code/metadata. Retain all existing compact
WOFF2 subsets and distribute the kit's corresponding OFL licenses (previously
missing here), rather than copying its larger TTFs.
Outlined logo masters have no font dependency. Theme switching must not replace
the editorial serif with Hanken.

## Layout

Keep article text, permalink rules, navigation destinations, tags, archives,
search, keyboard focus, theme persistence and code-copy behaviour unchanged.
The header wordmark still links to https://techdox.nz/ (“Techdox home”); the
footer wordmark still links to / (“Techdox blog home”).

## Shapes

The kit panel token is 18px (`--radius-panel`). Existing editorial cards and
reading controls retain their fit-for-purpose radii; this alignment does not
redesign the reading layout.

## Components

`layouts/partials/brand.html` uses byte-identical outlined `primary-dark.svg`
(off-white lettering) and `primary-light.svg` (dark lettering), selected by the
existing `data-theme`. Nick explicitly overrides the kit static-cursor rule for techdox.nz, docs.techdox.nz and blog.techdox.nz: blink only the supplied attached cursor at 1.2s with step timing in web-only SVG derivatives. Keep all paths, fills, transforms, canvas geometry, visible size, clearspace, themed variants and accessible link names unchanged. Never add a second cursor or animate the letters. Reduced motion selects the unchanged static artwork via a native picture source; retain the SVG media-query safeguard too. Original masters, icons, favicons and social artwork remain byte-identical and static.

The 960×180 SVG canvas contains surplus transparent space. CSS positions the
unmodified master at 240×45 in a 160×30 crop, offset -12/-7px; only transparent
canvas is hidden. Chromium SVG `getBBox()` verifies the entire artwork remains
inside that box: visible artwork is 143.85×26.32 CSS px, above the 140px minimum.
The link reserves 15px padding on all four sides, at least half the mark box's
height (and more than half the visible artwork height). Never shrink or distort
this wordmark; use the ~/ icon if a future layout cannot accommodate it.

Icons are exact kit copies: avatar.svg → favicon.svg; favicon.ico unchanged;
icon-180.png → apple-touch-icon.png; icon-48.png and icon-512.png for app/browser
icons. `site.webmanifest` explicitly uses browser display, root scope/start URL
and the dark brand colors; no service worker or installability claim is added.

`social/blog-og.png` replaces the generic `/og-default.png` bytes while preserving
that public URL. Metadata precedence remains: generic site fallback → generated
article-specific title card for posts → nonempty `feature_image` override
(absolute external URL or root-relative local image). OG, Twitter and JSON-LD
share the selected image. Do not replace individual post images with the generic
card. `social-image.html` and its existing generated article artwork are preserved.

## Do's and Don'ts

- Do run `HUGO_BIN=/path/to/hugo python3 scripts/test.py` with Python Playwright and
  Chromium installed; `BROWSER_EXECUTABLE` may select a local Chromium binary.
- New `test_reading_brand_*.py` files deliberately match the existing CI discovery
  pattern. `tests/brand-assets.json` records source-kit SHA-256 hashes.
- Set `BLOG_EVIDENCE` to an existing external directory for desktop/mobile,
  dark/light screenshots and measured SVG bounds; omit it in routine CI.
- Evidence/build output belongs outside version control. Local task evidence:
  `/home/techdox/brand/techdox/site-audit/blog-local/`.
- Keep production release unchanged: GitHub **Techdox/techdox → native Cloudflare
  Pages**. Older CLAUDE.md homelab/Gitea deployment notes are stale; this task does
  not edit deployment files, commit, push, or deploy.
