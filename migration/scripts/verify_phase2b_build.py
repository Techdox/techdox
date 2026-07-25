#!/usr/bin/env python3
"""Verify Phase 2B generated routes, aliases, feeds, and static assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


BLOG_ORIGIN = "https://blog.techdox.nz"
APEX_ORIGIN = "https://techdox.nz"


class AliasParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.refreshes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs}
        if tag.lower() == "link":
            rel = (values.get("rel") or "").lower().split()
            href = values.get("href")
            if "canonical" in rel and href:
                self.canonicals.append(href)
        if tag.lower() == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            content = values.get("content") or ""
            match = re.search(r"url\s*=\s*['\"]?([^'\";]+)", content, re.I)
            if match:
                self.refreshes.append(match.group(1).strip())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_alias_target(relative: Path) -> str:
    marker = "/page/1/index.html"
    value = "/" + relative.as_posix()
    if not value.endswith(marker):
        raise ValueError(f"not a page-one alias: {relative}")
    prefix = value[: -len(marker)]
    route = (prefix + "/") if prefix else "/"
    return BLOG_ORIGIN + route


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--build-dir", required=True, type=Path)
    ap.add_argument("--route-evidence", required=True, type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    repo = args.repo.resolve()
    build_dir = args.build_dir.resolve()
    baseline = json.loads(args.route_evidence.read_text(encoding="utf-8"))
    routes = baseline["routes"]
    errors: list[str] = []

    missing_routes = [
        {"path": row["path"], "category": row["category"], "generated_file": row["generated_file"]}
        for row in routes
        if not (build_dir / row["generated_file"]).is_file()
    ]
    if missing_routes:
        errors.append(f"{len(missing_routes)} inventoried route files are missing")

    expected_categories = Counter(row["category"] for row in routes)
    expected_summary = baseline["generated_summary"]
    if dict(sorted(expected_categories.items())) != dict(sorted(expected_summary.items())):
        errors.append("route category totals no longer match the Phase 1 inventory summary")

    static_source = sorted(path for path in (repo / "static").rglob("*") if path.is_file())
    static_checks = []
    for source in static_source:
        relative = source.relative_to(repo / "static")
        generated = build_dir / relative
        source_hash = sha256(source)
        generated_hash = sha256(generated) if generated.is_file() else None
        static_checks.append(
            {
                "file": relative.as_posix(),
                "source_sha256": source_hash,
                "generated_sha256": generated_hash,
                "passed": source_hash == generated_hash,
            }
        )
    failed_static = [row for row in static_checks if not row["passed"]]
    if len(static_source) != 50:
        errors.append(f"expected 50 source static files, found {len(static_source)}")
    if failed_static:
        errors.append(f"{len(failed_static)} static files are missing or changed in output")

    alias_files = sorted(build_dir.rglob("page/1/index.html"))
    alias_checks = []
    for path in alias_files:
        relative = path.relative_to(build_dir)
        parser = AliasParser()
        parser.feed(path.read_text(encoding="utf-8"))
        expected = expected_alias_target(relative)
        passed = parser.canonicals == [expected] and parser.refreshes == [expected]
        alias_checks.append(
            {
                "file": relative.as_posix(),
                "expected": expected,
                "canonicals": parser.canonicals,
                "refreshes": parser.refreshes,
                "passed": passed,
            }
        )
    failed_aliases = [row for row in alias_checks if not row["passed"]]
    if len(alias_checks) != 17:
        errors.append(f"expected 17 page-one aliases, found {len(alias_checks)}")
    if failed_aliases:
        errors.append(f"{len(failed_aliases)} page-one aliases have an incorrect target")

    feed_rows = [row for row in routes if row["category"] == "rss-feed"]
    missing_feeds = [row["generated_file"] for row in feed_rows if not (build_dir / row["generated_file"]).is_file()]
    if len(feed_rows) != 18:
        errors.append(f"expected 18 inventoried feeds, found {len(feed_rows)}")
    if missing_feeds:
        errors.append(f"{len(missing_feeds)} inventoried feeds are missing")

    sitemap = build_dir / "sitemap.xml"
    sitemap_urls: list[str] = []
    if not sitemap.is_file():
        errors.append("sitemap.xml is missing")
    else:
        root = ET.parse(sitemap).getroot()
        sitemap_urls = [node.text or "" for node in root.findall("{*}url/{*}loc")]
        wrong_sitemap_hosts = [url for url in sitemap_urls if urlsplit(url).hostname != "blog.techdox.nz"]
        if len(sitemap_urls) != 52:
            errors.append(f"expected 52 sitemap URLs, found {len(sitemap_urls)}")
        if wrong_sitemap_hosts:
            errors.append(f"{len(wrong_sitemap_hosts)} sitemap URLs use a non-blog host")

    rendered_apex_references = []
    rendered_blog_references = 0
    for path in sorted(build_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        count = text.count(BLOG_ORIGIN)
        rendered_blog_references += count
        if APEX_ORIGIN in text:
            rendered_apex_references.append(
                {"file": path.relative_to(build_dir).as_posix(), "count": text.count(APEX_ORIGIN)}
            )
    if rendered_apex_references:
        errors.append(f"{len(rendered_apex_references)} rendered files still reference the apex origin")
    if rendered_blog_references == 0:
        errors.append("no rendered blog-origin references were found")

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_branch": "migration/landing-blog-split",
        "expected_origin": BLOG_ORIGIN + "/",
        "route_inventory": {
            "total": len(routes),
            "categories": dict(sorted(expected_categories.items())),
            "missing": missing_routes,
            "passed": not missing_routes,
        },
        "static_assets": {
            "total": len(static_checks),
            "failed": failed_static,
            "passed": len(static_checks) == 50 and not failed_static,
        },
        "aliases": {
            "total": len(alias_checks),
            "failed": failed_aliases,
            "checks": alias_checks,
            "passed": len(alias_checks) == 17 and not failed_aliases,
        },
        "feeds": {
            "total": len(feed_rows),
            "missing": missing_feeds,
            "passed": len(feed_rows) == 18 and not missing_feeds,
        },
        "sitemap": {
            "url_count": len(sitemap_urls),
            "all_blog_host": bool(sitemap_urls) and all(urlsplit(url).hostname == "blog.techdox.nz" for url in sitemap_urls),
        },
        "rendered_origins": {
            "blog_reference_count": rendered_blog_references,
            "apex_references": rendered_apex_references,
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
