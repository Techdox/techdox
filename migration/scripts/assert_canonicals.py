#!/usr/bin/env python3
"""Assert exact canonical and Open Graph URLs in a generated Hugo site."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


EXPECTED_CASES = (
    ("article", "/why-selfhost/", "https://blog.techdox.nz/why-selfhost/"),
    ("homepage-page-1", "/", "https://blog.techdox.nz/"),
    ("homepage-page-2", "/page/2/", "https://blog.techdox.nz/page/2/"),
    ("posts-page-1", "/posts/", "https://blog.techdox.nz/posts/"),
    ("posts-page-2", "/posts/page/2/", "https://blog.techdox.nz/posts/page/2/"),
    ("tag-page-1", "/tags/selfhosting/", "https://blog.techdox.nz/tags/selfhosting/"),
    ("tag-page-2", "/tags/selfhosting/page/2/", "https://blog.techdox.nz/tags/selfhosting/page/2/"),
)


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.og_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs}
        if tag.lower() == "link":
            rel = (values.get("rel") or "").lower().split()
            href = values.get("href")
            if "canonical" in rel and href:
                self.canonicals.append(href)
        elif tag.lower() == "meta":
            prop = (values.get("property") or "").lower()
            content = values.get("content")
            if prop == "og:url" and content:
                self.og_urls.append(content)


@dataclass
class ExactCheck:
    name: str
    route: str
    generated_file: str
    expected: str
    canonicals: list[str]
    og_urls: list[str]
    passed: bool


def route_file(build_dir: Path, route: str) -> Path:
    if route == "/":
        return build_dir / "index.html"
    return build_dir / route.strip("/") / "index.html"


def parse_metadata(path: Path) -> MetadataParser:
    parser = MetadataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-dir", required=True, type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expected-host", default="blog.techdox.nz")
    args = ap.parse_args()

    checks: list[ExactCheck] = []
    errors: list[str] = []

    for name, route, expected in EXPECTED_CASES:
        generated = route_file(args.build_dir, route)
        if not generated.is_file():
            errors.append(f"missing generated file for {name}: {generated}")
            checks.append(ExactCheck(name, route, str(generated), expected, [], [], False))
            continue
        metadata = parse_metadata(generated)
        passed = metadata.canonicals == [expected] and metadata.og_urls == [expected]
        if not passed:
            errors.append(
                f"{name}: expected canonical and og:url {expected!r}; "
                f"got canonical={metadata.canonicals!r}, og:url={metadata.og_urls!r}"
            )
        checks.append(
            ExactCheck(
                name,
                route,
                str(generated.relative_to(args.build_dir)),
                expected,
                metadata.canonicals,
                metadata.og_urls,
                passed,
            )
        )

    html_files = sorted(args.build_dir.rglob("*.html"))
    missing: list[str] = []
    duplicate: list[dict[str, object]] = []
    wrong_host: list[dict[str, str]] = []
    for path in html_files:
        metadata = parse_metadata(path)
        relative = str(path.relative_to(args.build_dir))
        if not metadata.canonicals:
            missing.append(relative)
        elif len(metadata.canonicals) != 1:
            duplicate.append({"file": relative, "canonicals": metadata.canonicals})
        for canonical in metadata.canonicals:
            if urlsplit(canonical).hostname != args.expected_host:
                wrong_host.append({"file": relative, "canonical": canonical})

    if missing:
        errors.append(f"{len(missing)} generated HTML files have no canonical")
    if duplicate:
        errors.append(f"{len(duplicate)} generated HTML files have duplicate canonicals")
    if wrong_host:
        errors.append(f"{len(wrong_host)} generated HTML files use a non-blog canonical host")

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_branch": "migration/landing-blog-split",
        "expected_host": args.expected_host,
        "exact_checks": [asdict(check) for check in checks],
        "exact_passed": sum(check.passed for check in checks),
        "exact_total": len(checks),
        "site_scan": {
            "html_files": len(html_files),
            "missing_canonical": missing,
            "duplicate_canonical": duplicate,
            "wrong_host_canonical": wrong_host,
        },
        "errors": errors,
        "passed": not errors,
    }

    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
