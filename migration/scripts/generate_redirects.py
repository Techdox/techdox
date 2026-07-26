#!/usr/bin/env python3
"""Validate the Techdox URL manifest and generate inactive Cloudflare CSVs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

MAX_FREE_BULK_REDIRECTS = 10_000
PAGE_CATEGORIES = {
    "blog-article",
    "blog-deals",
    "blog-index",
    "blog-pagination",
    "blog-taxonomy",
}
LANDING_OWNED = {"/", "/robots.txt", "/sitemap.xml", "/about/", "/contact/", "/projects/"}


def target_file(build_dir: Path, target_url: str) -> Path:
    parsed = urlsplit(target_url)
    path = parsed.path or "/"
    if path == "/":
        return build_dir / "index.html"
    relative = path.lstrip("/")
    if path.endswith("/"):
        return build_dir / relative / "index.html"
    return build_dir / relative


def write_csv(path: Path, entries: list[dict], status_key: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        for row in entries:
            writer.writerow(
                [
                    row["source_url"],
                    row["target_url"],
                    row[status_key],
                    "TRUE" if row["preserve_query_string"] else "FALSE",
                    "TRUE" if row["include_subdomains"] else "FALSE",
                    "TRUE" if row["subpath_matching"] else "FALSE",
                    "FALSE",  # preserve path suffix; exact rules do not use it
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("migration/url-manifest.json"))
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("migration/generated"))
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    entries = manifest["entries"]
    errors: list[str] = []
    warnings: list[str] = []

    if manifest.get("activation_state") != "not-created-or-enabled":
        errors.append("manifest activation_state must remain not-created-or-enabled in Phase 1")
    if len(entries) != manifest.get("redirect_count"):
        errors.append("redirect_count does not match entries length")
    if len(entries) > MAX_FREE_BULK_REDIRECTS:
        errors.append(f"manifest exceeds Free-plan Bulk Redirect limit of {MAX_FREE_BULK_REDIRECTS}")

    sources = [row.get("source_url") for row in entries]
    duplicate_sources = [source for source, count in Counter(sources).items() if count > 1]
    if duplicate_sources:
        errors.append(f"duplicate source URLs: {duplicate_sources[:10]}")

    source_set = set(sources)
    target_missing: list[str] = []
    for number, row in enumerate(entries, start=1):
        label = f"entry {number} ({row.get('source_url')})"
        source = row.get("source_url", "")
        target = row.get("target_url", "")
        if source.startswith(("http://", "https://")):
            errors.append(f"{label}: source scheme must be omitted to match HTTP and HTTPS")
        if not source.startswith("techdox.nz/"):
            errors.append(f"{label}: source must be scoped to techdox.nz")
        source_path = "/" + source.split("/", 1)[1] if "/" in source else "/"
        if source_path in LANDING_OWNED:
            errors.append(f"{label}: landing-owned path must not redirect")
        target_parts = urlsplit(target)
        if target_parts.scheme != "https" or target_parts.netloc != "blog.techdox.nz":
            errors.append(f"{label}: target must be an HTTPS blog.techdox.nz URL")
        if target_parts.query or target_parts.fragment:
            errors.append(f"{label}: target must not hard-code a query string or fragment")
        if row.get("test_status") != 302 or row.get("production_status") != 301:
            errors.append(f"{label}: status policy must be test=302 and production=301")
        if row.get("preserve_query_string") is not True:
            errors.append(f"{label}: preserve_query_string must be true")
        if row.get("include_subdomains") is not False:
            errors.append(f"{label}: include_subdomains must be false")
        if row.get("subpath_matching") is not False:
            errors.append(f"{label}: subpath_matching must be false")
        if sorted(row.get("match_schemes", [])) != ["http", "https"]:
            errors.append(f"{label}: match_schemes must contain HTTP and HTTPS")
        if not target_file(args.build_dir, target).is_file():
            target_missing.append(target)

        if row.get("category") in PAGE_CATEGORIES and source_path.endswith("/"):
            no_slash = source.rstrip("/")
            if no_slash not in source_set:
                errors.append(f"{label}: missing no-trailing-slash variant {no_slash}")

    if target_missing:
        errors.append(f"targets absent from Hugo build: {sorted(set(target_missing))[:20]}")

    expected = {
        "techdox.nz/why-selfhost/": "https://blog.techdox.nz/why-selfhost/",
        "techdox.nz/why-selfhost": "https://blog.techdox.nz/why-selfhost/",
        "techdox.nz/index.xml": "https://blog.techdox.nz/index.xml",
    }
    actual = {row["source_url"]: row["target_url"] for row in entries}
    for source, target in expected.items():
        if actual.get(source) != target:
            errors.append(f"required mapping missing or wrong: {source} -> {target}")

    test_csv = args.output_dir / "cloudflare-bulk-redirects-test-302.csv"
    production_csv = args.output_dir / "cloudflare-bulk-redirects-production-301.csv"
    if not errors:
        write_csv(test_csv, entries, "test_status")
        write_csv(production_csv, entries, "production_status")

        for csv_path, expected_status in ((test_csv, "302"), (production_csv, "301")):
            with csv_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
            if len(rows) != len(entries):
                errors.append(f"{csv_path}: row count does not match manifest")
            if any(len(row) != 7 for row in rows):
                errors.append(f"{csv_path}: each row must contain seven Cloudflare fields")
            if any(row[2] != expected_status for row in rows):
                errors.append(f"{csv_path}: unexpected status code")
            if any(row[3:] != ["TRUE", "FALSE", "FALSE", "FALSE"] for row in rows):
                errors.append(f"{csv_path}: unexpected redirect parameters")

    report = {
        "valid": not errors,
        "redirect_count": len(entries),
        "free_plan_limit": MAX_FREE_BULK_REDIRECTS,
        "category_counts": dict(sorted(Counter(row["category"] for row in entries).items())),
        "errors": errors,
        "warnings": warnings,
        "test_csv": str(test_csv),
        "production_csv": str(production_csv),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
