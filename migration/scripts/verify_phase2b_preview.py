#!/usr/bin/env python3
"""Verify Phase 2B metadata and representative routes on a Pages preview."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET


EXPECTED_CASES = (
    ("article", "/why-selfhost/", "https://blog.techdox.nz/why-selfhost/"),
    ("homepage-page-1", "/", "https://blog.techdox.nz/"),
    ("homepage-page-2", "/page/2/", "https://blog.techdox.nz/page/2/"),
    ("posts-page-1", "/posts/", "https://blog.techdox.nz/posts/"),
    ("posts-page-2", "/posts/page/2/", "https://blog.techdox.nz/posts/page/2/"),
    ("tag-page-1", "/tags/selfhosting/", "https://blog.techdox.nz/tags/selfhosting/"),
    ("tag-page-2", "/tags/selfhosting/page/2/", "https://blog.techdox.nz/tags/selfhosting/page/2/"),
)

REPRESENTATIVE_ROUTES = (
    ("root", "/", 200),
    ("article", "/why-selfhost/", 200),
    ("homepage-page-2", "/page/2/", 200),
    ("posts", "/posts/", 200),
    ("posts-page-2", "/posts/page/2/", 200),
    ("tag", "/tags/selfhosting/", 200),
    ("tag-page-2", "/tags/selfhosting/page/2/", 200),
    ("main-feed", "/index.xml", 200),
    ("tag-feed", "/tags/selfhosting/index.xml", 200),
    ("image", "/content/images/2023/03/IMG_2009-Small.png", 200),
    ("sitemap", "/sitemap.xml", 200),
    ("robots", "/robots.txt", 200),
    ("evidence-not-served", "/migration/phase-2b-report.md", 404),
    ("unknown-route", "/definitely-not-a-real-route-phase2b/", 404),
)

ALIASES = (
    ("/page/1/", "https://blog.techdox.nz/"),
    ("/posts/page/1/", "https://blog.techdox.nz/posts/"),
    ("/tags/ai/page/1/", "https://blog.techdox.nz/tags/ai/"),
    ("/tags/selfhosting/page/1/", "https://blog.techdox.nz/tags/selfhosting/"),
)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.og_urls: list[str] = []
        self.refreshes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs}
        if tag.lower() == "link":
            rel = (values.get("rel") or "").lower().split()
            href = values.get("href")
            if "canonical" in rel and href:
                self.canonicals.append(href)
        elif tag.lower() == "meta":
            prop = (values.get("property") or "").lower()
            content = values.get("content") or ""
            if prop == "og:url" and content:
                self.og_urls.append(content)
            if (values.get("http-equiv") or "").lower() == "refresh":
                match = re.search(r"url\s*=\s*['\"]?([^'\";]+)", content, re.I)
                if match:
                    self.refreshes.append(match.group(1).strip())


def fetch(opener, base_url: str, path: str) -> dict[str, object]:  # noqa: ANN001
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    request = Request(url, headers={"User-Agent": "Techdox Phase 2B preview verifier/1.0"})
    try:
        with opener.open(request, timeout=30) as response:
            return {
                "url": url,
                "status": response.status,
                "headers": {key.lower(): value for key, value in response.headers.items()},
                "body": response.read(),
            }
    except HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "headers": {key.lower(): value for key, value in exc.headers.items()},
            "body": exc.read(),
        }


def parse_html(body: bytes) -> MetadataParser:
    parser = MetadataParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    return parser


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--deployment-id", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--hugo-version", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    opener = build_opener(NoRedirect())
    errors: list[str] = []

    route_checks = []
    response_cache: dict[str, dict[str, object]] = {}
    for name, path, expected_status in REPRESENTATIVE_ROUTES:
        response = fetch(opener, args.base_url, path)
        response_cache[path] = response
        location = response["headers"].get("location")
        passed = response["status"] == expected_status and location is None
        if not passed:
            errors.append(
                f"{name}: expected status {expected_status} with no HTTP redirect; "
                f"got status={response['status']}, location={location!r}"
            )
        route_checks.append(
            {
                "name": name,
                "path": path,
                "expected_status": expected_status,
                "status": response["status"],
                "location": location,
                "passed": passed,
            }
        )

    exact_checks = []
    for name, path, expected in EXPECTED_CASES:
        response = response_cache.get(path) or fetch(opener, args.base_url, path)
        metadata = parse_html(response["body"])
        passed = (
            response["status"] == 200
            and metadata.canonicals == [expected]
            and metadata.og_urls == [expected]
        )
        if not passed:
            errors.append(
                f"{name}: expected canonical and og:url {expected!r}; "
                f"got status={response['status']}, canonical={metadata.canonicals!r}, "
                f"og:url={metadata.og_urls!r}"
            )
        exact_checks.append(
            {
                "name": name,
                "path": path,
                "expected": expected,
                "canonicals": metadata.canonicals,
                "og_urls": metadata.og_urls,
                "passed": passed,
            }
        )

    alias_checks = []
    for path, expected in ALIASES:
        response = fetch(opener, args.base_url, path)
        metadata = parse_html(response["body"])
        passed = (
            response["status"] == 200
            and metadata.canonicals == [expected]
            and metadata.refreshes == [expected]
        )
        if not passed:
            errors.append(
                f"alias {path}: expected canonical and refresh {expected!r}; "
                f"got status={response['status']}, canonical={metadata.canonicals!r}, "
                f"refresh={metadata.refreshes!r}"
            )
        alias_checks.append(
            {
                "path": path,
                "expected": expected,
                "status": response["status"],
                "canonicals": metadata.canonicals,
                "refreshes": metadata.refreshes,
                "passed": passed,
            }
        )

    sitemap_response = response_cache["/sitemap.xml"]
    sitemap_urls: list[str] = []
    if sitemap_response["status"] == 200:
        root = ET.fromstring(sitemap_response["body"])
        sitemap_urls = [node.text or "" for node in root.findall("{*}url/{*}loc")]
    sitemap_passed = (
        len(sitemap_urls) == 52
        and all(urlsplit(url).hostname == "blog.techdox.nz" for url in sitemap_urls)
    )
    if not sitemap_passed:
        errors.append("preview sitemap does not contain exactly 52 blog-host URLs")

    feed_checks = []
    for path in ("/index.xml", "/tags/selfhosting/index.xml"):
        body = response_cache[path]["body"].decode("utf-8", errors="replace")
        blog_count = body.count("https://blog.techdox.nz")
        apex_count = body.count("https://techdox.nz")
        passed = response_cache[path]["status"] == 200 and blog_count > 0 and apex_count == 0
        if not passed:
            errors.append(f"feed {path}: blog_count={blog_count}, apex_count={apex_count}")
        feed_checks.append(
            {"path": path, "blog_reference_count": blog_count, "apex_reference_count": apex_count, "passed": passed}
        )

    root_headers = response_cache["/"]["headers"]
    robots_header = root_headers.get("x-robots-tag", "")
    preview_noindex = "noindex" in robots_header.lower()
    if not preview_noindex:
        errors.append("preview root does not send X-Robots-Tag: noindex")

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "deployment": {
            "id": args.deployment_id,
            "commit": args.commit,
            "url": args.base_url,
            "environment": "preview",
            "hugo_version": args.hugo_version,
        },
        "route_checks": route_checks,
        "exact_canonical_checks": exact_checks,
        "alias_checks": alias_checks,
        "sitemap": {"url_count": len(sitemap_urls), "all_blog_host": sitemap_passed},
        "feed_checks": feed_checks,
        "preview_indexing": {"x_robots_tag": robots_header, "noindex": preview_noindex},
        "errors": errors,
        "passed": not errors,
    }

    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(output)
    print(output, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
