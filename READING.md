# Reading experience

## Build and regression checks

Production remains on Cloudflare Pages' existing GitHub integration. The new GitHub Actions workflow is **test-only**, not a second deployment path.

```sh
hugo --gc --minify
python -m venv .venv
.venv/bin/pip install -r tests/requirements.txt
.venv/bin/python -m playwright install --with-deps chromium
.venv/bin/python scripts/test.py
```

Tests use Hugo 0.147.7 extended in CI. `HUGO_BIN` can select another installed binary; `BROWSER_EXECUTABLE` can select an existing Chromium binary. The runner creates a temporary build and loopback-only server and cleans both up afterwards.

Static tests check article titles, editorial cards, archive pagination, favicons, related-reading labels and generated social assets. Browser tests exercise 320/375/390px overflow (including clipped featured content), beginner ordering, search match/empty states and real clipboard success/denial. Browser regression tests deliberately block analytics; public deployment verification must check those requests separately.

## Editorial conventions

- The layout owns the article H1. Do not repeat the title as a first Markdown heading.
- Use a real `description` in front matter where the automatic summary repeats the title. Do not invent tested versions or verification dates.
- “Start here” explicitly orders Why Selfhost → Linux → Raspberry Pi. KubeSolo is labelled an optional next step.
- Ordinary cards prioritize category, title, summary and publication metadata. Terminal illustrations remain on the front-page hero and featured story only.
- “Related reading” describes tag-based recommendations without claiming an exact topic match.

## Static reading tools

`/search/` builds a fingerprinted JSON index of published posts using Hugo resources. Search executes locally with plain DOM text nodes, with a no-JavaScript archive fallback. No hosted search account, browser tracking or database was added.

Code-copy buttons are progressive enhancement on existing preformatted blocks. Clipboard denial leaves the original code selectable and reports a useful message.

Posts without an explicit `feature_image` receive title-specific 1200×630 PNG social cards from the checked-in background and native Hugo image processing. Existing explicit artwork takes precedence. No external image-generation service or build-time network request is needed.

## Release and rollback

Use feature branches and Cloudflare branch previews, then merge only after tests and preview checks pass. Revert the refresh PR through GitHub for rollback. Do not change the existing Pages project, canonical domain, redirects or production approval/signing conventions.
