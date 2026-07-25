#!/usr/bin/env python3
"""Build Techdox Phase 1 URL evidence and migration manifest.

This script is read-only against production. It inspects a local Hugo build,
fetches the live sitemap, probes generated routes with HEAD requests, and
classifies Internet Archive paths without activating redirects.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener
import xml.etree.ElementTree as ET

APEX = "techdox.nz"
BLOG = "blog.techdox.nz"
USER_AGENT = "Techdox migration inventory/1.0"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
TEXT_SUFFIXES = {".md", ".html", ".toml", ".yaml", ".yml", ".json", ".js", ".css", ".xml", ".txt"}


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonical: str | None = None
        self.assets: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): v for k, v in attrs if v is not None}
        rel = set((values.get("rel") or "").lower().split())
        if tag.lower() == "link" and "canonical" in rel and values.get("href"):
            self.canonical = values["href"]
        if tag.lower() in {"img", "script", "source"}:
            for key in ("src", "srcset"):
                value = values.get(key)
                if value:
                    for candidate in value.split(","):
                        self.assets.add(candidate.strip().split()[0])
        if tag.lower() == "meta" and values.get("property", "").lower() in {
            "og:image",
            "twitter:image",
        } and values.get("content"):
            self.assets.add(values["content"])


def route_for_file(relative: Path) -> str | None:
    value = relative.as_posix()
    if value == "index.html":
        return "/"
    if value.endswith("/index.html"):
        return "/" + value[: -len("index.html")]
    if value in {"index.xml", "robots.txt", "sitemap.xml", "404.html"}:
        return "/" + value
    if value.endswith(".xml"):
        return "/" + value
    if relative.suffix.lower() in IMAGE_SUFFIXES:
        return "/" + value
    return None


def parse_html(path: Path) -> tuple[str | None, set[str]]:
    parser = HeadParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.canonical, parser.assets


def canonical_path(canonical: str | None, fallback: str) -> str:
    if not canonical:
        return fallback
    parsed = urlsplit(canonical)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    return path


def category_for(path: str, suffix: str) -> str:
    if path == "/":
        return "landing-root"
    if path in {"/robots.txt", "/sitemap.xml"}:
        return "landing-owned"
    if path == "/404.html":
        return "not-found-document"
    if suffix.lower() in IMAGE_SUFFIXES:
        return "direct-image-asset"
    if path.endswith(".xml"):
        return "rss-feed"
    if path == "/deals/":
        return "blog-deals"
    if path.startswith("/tags/") or path == "/tags/":
        return "blog-taxonomy"
    if path.startswith("/posts/") or path == "/posts/":
        return "blog-index"
    if path.startswith("/page/"):
        return "blog-pagination"
    return "blog-article"


def fetch_bytes(url: str, timeout: int = 30) -> tuple[int, str, bytes, dict[str, str]]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with build_opener().open(request, timeout=timeout) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            return response.status, response.geturl(), response.read(), headers
    except HTTPError as exc:
        headers = {k.lower(): v for k, v in exc.headers.items()}
        return exc.code, exc.geturl(), exc.read(), headers


def probe_url(url: str) -> dict[str, Any]:
    request = Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with build_opener().open(request, timeout=20) as response:
            return {
                "url": url,
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("Content-Type"),
                "content_length": response.headers.get("Content-Length"),
            }
    except HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "final_url": exc.geturl(),
            "content_type": exc.headers.get("Content-Type"),
            "content_length": exc.headers.get("Content-Length"),
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {"url": url, "status": None, "error": str(exc)}


def normalize_path(value: str) -> str:
    parsed = urlsplit(value)
    path = parsed.path or "/"
    path = re.sub(r"/{2,}", "/", path)
    return path


def source_variants(path: str, category: str) -> list[str]:
    """Return exact path variants for scheme-less Bulk Redirect sources."""
    variants: list[str] = []
    paths = [path]
    if category in {
        "blog-article",
        "blog-deals",
        "blog-index",
        "blog-pagination",
        "blog-taxonomy",
    } and path != "/" and path.endswith("/"):
        paths.append(path.rstrip("/"))
    for candidate in paths:
        variants.append(candidate)
    return variants


def hardcoded_references(repo: Path) -> list[dict[str, Any]]:
    pattern = re.compile(r"https?://(?:www\.)?techdox\.nz(?:[^\s\"'<>)]*)", re.I)
    found: list[dict[str, Any]] = []
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "migration" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            for match in pattern.finditer(line):
                found.append(
                    {
                        "file": path.relative_to(repo).as_posix(),
                        "line": number,
                        "url": match.group(0),
                    }
                )
    return found


def load_wayback(path: Path, current_paths: set[str], current_articles: set[str]) -> dict[str, Any]:
    if not path.exists():
        return {"available": False, "paths": [], "summary": {}}
    rows = json.loads(path.read_text(encoding="utf-8"))
    originals = [row[0] for row in rows[1:] if row]
    grouped: dict[str, set[str]] = defaultdict(set)
    schemes: dict[str, set[str]] = defaultdict(set)
    for original in originals:
        parsed = urlsplit(original)
        host = (parsed.hostname or "").lower()
        if host not in {APEX, "www." + APEX}:
            continue
        normalized = normalize_path(original)
        grouped[normalized].add(host)
        schemes[normalized].add(parsed.scheme.lower())

    article_slugs = {p.strip("/") for p in current_articles}
    classified: list[dict[str, Any]] = []
    for candidate in sorted(grouped):
        normalized = candidate if candidate == "/" or candidate.endswith("/") or Path(candidate).suffix else candidate + "/"
        direct = normalized in current_paths or candidate in current_paths
        dated_match = re.fullmatch(r"/\d{4}/\d{2}/\d{2}/([^/]+)/", normalized)
        mapped_target = None
        if dated_match and dated_match.group(1) in article_slugs:
            mapped_target = "/" + dated_match.group(1) + "/"
        if direct:
            classification = "covered-current-route"
        elif mapped_target:
            classification = "mappable-dated-article"
        elif re.fullmatch(r"/\d{4}/\d{2}/\d{2}/[^/]+/", normalized):
            classification = "historical-article-no-current-destination"
        elif re.fullmatch(r"/\d{4}/\d{2}(?:/page/\d+)?/", normalized):
            classification = "historical-date-archive"
        elif normalized.startswith(("/wp-admin/", "/wp-content/", "/wp-includes/")):
            classification = "wordpress-utility"
        elif any(token in normalized for token in ("/feed/", "/author/", "/category/", "/tag/", "/page/")):
            classification = "historical-index-or-feed"
        else:
            classification = "historical-other"
        classified.append(
            {
                "path": normalized,
                "hosts": sorted(grouped[candidate]),
                "schemes": sorted(schemes[candidate]),
                "classification": classification,
                "mapped_target": mapped_target,
            }
        )
    summary = Counter(row["classification"] for row in classified)
    return {
        "available": True,
        "original_url_count": len(originals),
        "unique_path_count": len(classified),
        "summary": dict(sorted(summary.items())),
        "paths": classified,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--wayback", type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    build_dir = args.build_dir.resolve()
    source_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    source_branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=repo, text=True
    ).strip()
    migration = repo / "migration"
    evidence = migration / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)

    status, final_url, sitemap_body, sitemap_headers = fetch_bytes(f"https://{APEX}/sitemap.xml")
    if status != 200:
        print(f"live sitemap returned {status}", file=sys.stderr)
        return 1
    (evidence / "live-sitemap.xml").write_bytes(sitemap_body)
    sitemap_root = ET.fromstring(sitemap_body)
    sitemap_urls = [node.text.strip() for node in sitemap_root.findall("{*}url/{*}loc") if node.text]
    sitemap_paths = {normalize_path(url) for url in sitemap_urls}

    generated: dict[str, dict[str, Any]] = {}
    referenced_assets: set[str] = set()
    for file_path in sorted(build_dir.rglob("*")):
        if not file_path.is_file():
            continue
        relative = file_path.relative_to(build_dir)
        route = route_for_file(relative)
        if route is None:
            continue
        canonical = None
        assets: set[str] = set()
        if file_path.name.endswith(".html"):
            canonical, assets = parse_html(file_path)
            for asset in assets:
                parsed = urlsplit(urljoin(f"https://{APEX}{route}", asset))
                if parsed.hostname == APEX:
                    referenced_assets.add(parsed.path)
        category = category_for(route, file_path.suffix)
        generated[route] = {
            "path": route,
            "generated_file": relative.as_posix(),
            "category": category,
            "canonical_path": canonical_path(canonical, route),
            "in_live_sitemap": route in sitemap_paths,
        }

    # Ensure sitemap routes are not lost if source/build behavior changes.
    for path in sorted(sitemap_paths):
        generated.setdefault(
            path,
            {
                "path": path,
                "generated_file": None,
                "category": category_for(path, Path(path).suffix),
                "canonical_path": path,
                "in_live_sitemap": True,
            },
        )

    probe_paths = sorted(generated)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        probes = list(executor.map(lambda p: probe_url(f"https://{APEX}{p}"), probe_paths))
    probe_by_path = {normalize_path(row["url"]): row for row in probes}

    current_articles = {
        path
        for path, row in generated.items()
        if row["category"] == "blog-article" and path != "/404.html"
    }
    current_paths = set(generated)
    wayback = load_wayback(args.wayback, current_paths, current_articles) if args.wayback else {
        "available": False,
        "paths": [],
        "summary": {},
    }

    manifest_entries: list[dict[str, Any]] = []
    seen_sources: set[str] = set()
    for path, row in sorted(generated.items()):
        category = row["category"]
        if category in {"landing-root", "landing-owned", "not-found-document"}:
            continue
        target_path = row["canonical_path"]
        if not target_path.startswith("/"):
            target_path = path
        evidence_sources = ["hugo-build"]
        if row["in_live_sitemap"]:
            evidence_sources.append("live-sitemap")
        if path in referenced_assets:
            evidence_sources.append("live-page-reference")
        current_probe = probe_by_path.get(path, {})
        for source_path in source_variants(path, category):
            # Cloudflare matches both HTTP and HTTPS when the source scheme is omitted.
            source_url = APEX + source_path
            if source_url in seen_sources:
                continue
            seen_sources.add(source_url)
            manifest_entries.append(
                {
                    "source_url": source_url,
                    "target_url": urlunsplit(("https", BLOG, target_path, "", "")),
                    "category": category,
                    "test_status": 302,
                    "production_status": 301,
                    "preserve_query_string": True,
                    "subpath_matching": False,
                    "include_subdomains": False,
                    "match_schemes": ["http", "https"],
                    "evidence": evidence_sources,
                    "current_live_status": current_probe.get("status"),
                    "current_live_final_url": current_probe.get("final_url"),
                }
            )

    # Add archived dated URLs only where the destination exists today.
    for archived in wayback.get("paths", []):
        if archived["classification"] != "mappable-dated-article":
            continue
        source_url = APEX + archived["path"]
        if source_url in seen_sources:
            continue
        seen_sources.add(source_url)
        manifest_entries.append(
            {
                "source_url": source_url,
                "target_url": urlunsplit(("https", BLOG, archived["mapped_target"], "", "")),
                "category": "historical-dated-article-alias",
                "test_status": 302,
                "production_status": 301,
                "preserve_query_string": True,
                "subpath_matching": False,
                "include_subdomains": False,
                "match_schemes": ["http", "https"],
                "evidence": ["internet-archive", "current-blog-destination"],
                "current_live_status": None,
                "current_live_final_url": None,
            }
        )

    manifest_entries.sort(key=lambda row: row["source_url"])
    hardcoded = hardcoded_references(repo)
    generated_summary = Counter(row["category"] for row in generated.values())
    probe_summary = Counter(str(row.get("status")) for row in probes)

    source_routes = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_commit": source_commit,
        "source_branch": source_branch,
        "hugo_build_dir": str(build_dir),
        "live_sitemap": {
            "url": f"https://{APEX}/sitemap.xml",
            "status": status,
            "final_url": final_url,
            "content_type": sitemap_headers.get("content-type"),
            "url_count": len(sitemap_urls),
        },
        "generated_summary": dict(sorted(generated_summary.items())),
        "referenced_same_host_assets": sorted(referenced_assets),
        "routes": [generated[path] for path in sorted(generated)],
        "hardcoded_apex_references": hardcoded,
    }
    live_crawl = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "probe_method": "HEAD",
        "summary": dict(sorted(probe_summary.items())),
        "results": probes,
    }
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_host": APEX,
        "destination_host": BLOG,
        "source_commit": source_commit,
        "source_branch": source_branch,
        "default_test_status": 302,
        "default_production_status": 301,
        "query_strings": "preserve",
        "source_scheme_policy": "omitted-source-scheme-matches-http-and-https",
        "activation_state": "not-created-or-enabled",
        "landing_owned_paths": ["/", "/robots.txt", "/sitemap.xml"],
        "reserved_future_landing_paths": ["/about/", "/contact/", "/projects/"],
        "redirect_count": len(manifest_entries),
        "entries": manifest_entries,
    }

    (evidence / "source-routes.json").write_text(json.dumps(source_routes, indent=2, sort_keys=True) + "\n")
    (evidence / "live-route-probes.json").write_text(json.dumps(live_crawl, indent=2, sort_keys=True) + "\n")
    (evidence / "wayback-historical-paths.json").write_text(json.dumps(wayback, indent=2, sort_keys=True) + "\n")
    (migration / "url-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(json.dumps({
        "live_sitemap_urls": len(sitemap_urls),
        "generated_routes": len(generated),
        "generated_summary": dict(sorted(generated_summary.items())),
        "live_probe_summary": dict(sorted(probe_summary.items())),
        "wayback_summary": wayback.get("summary", {}),
        "hardcoded_apex_references": len(hardcoded),
        "manifest_redirects": len(manifest_entries),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
