#!/usr/bin/env python3
"""Verify the live Techdox landing/blog production cutover."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


CTX = ssl.create_default_context()
OPENER = urllib.request.build_opener(
    NoRedirect(),
    urllib.request.HTTPHandler(),
    urllib.request.HTTPSHandler(context=CTX),
)
USER_AGENT = "Techdox-Phase5B-Production-Verification/1.0"
QUERY_KEY = "phase5b_validation"
QUERY_VALUE = "codex-20260726"
LANDING_INDEX_SHA256 = (
    "19680c94e8919e8c8ffb8b23db6acde6ee5520619278fc1f1bef89e96df079e0"
)
CLOUDFLARE_BEACON = re.compile(
    rb'\n<script type="module" '
    rb'src="https://static\.cloudflareinsights\.com/beacon\.min\.js/[^"]+"'
    rb".*?</script>",
)


def request(url: str, method: str = "HEAD", follow: bool = False) -> dict:
    opener = (
        urllib.request.build_opener(
            urllib.request.HTTPHandler(),
            urllib.request.HTTPSHandler(context=CTX),
        )
        if follow
        else OPENER
    )
    req = urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with opener.open(req, timeout=25) as response:
            body = response.read() if method == "GET" else b""
            return {
                "url": url,
                "status": response.status,
                "final_url": response.geturl(),
                "location": response.headers.get("Location"),
                "sha256": hashlib.sha256(body).hexdigest() if body else None,
                "bytes": len(body) if body else None,
                "content_type": response.headers.get("Content-Type"),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read() if method == "GET" else b""
        return {
            "url": url,
            "status": exc.code,
            "final_url": exc.geturl(),
            "location": exc.headers.get("Location"),
            "sha256": hashlib.sha256(body).hexdigest() if body else None,
            "bytes": len(body) if body else None,
            "content_type": exc.headers.get("Content-Type"),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "url": url,
            "status": None,
            "final_url": None,
            "location": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def append_query(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append((QUERY_KEY, QUERY_VALUE))
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), "")
    )


def expected_location(target: str) -> str:
    return append_query(target)


def normalized_landing_hash(body: bytes) -> str:
    """Ignore the expected zone-level Cloudflare Web Analytics injection."""
    return hashlib.sha256(CLOUDFLARE_BEACON.sub(b"", body)).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    mappings = []
    for entry in manifest["entries"]:
        for scheme in ("https", "http"):
            mappings.append(
                {
                    "scheme": scheme,
                    "source": append_query(f"{scheme}://{entry['source_url']}"),
                    "expected": expected_location(entry["target_url"]),
                }
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        mapping_results = list(
            executor.map(lambda item: request(item["source"]), mappings)
        )

    mapping_errors = []
    for mapping, result in zip(mappings, mapping_results, strict=True):
        if result.get("status") != 301 or result.get("location") != mapping["expected"]:
            mapping_errors.append({"mapping": mapping, "result": result})

    targets = sorted({entry["target_url"] for entry in manifest["entries"]})
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        target_results = list(executor.map(request, targets))
    target_errors = [
        result
        for result in target_results
        if result.get("status") != 200 or result.get("location")
    ]

    protected_expectations = {
        "https://techdox.nz/": 200,
        "https://techdox.nz/robots.txt": 200,
        "https://techdox.nz/sitemap.xml": 200,
        "https://techdox.nz/about/": 404,
        "https://techdox.nz/contact/": 404,
        "https://techdox.nz/projects/": 404,
        "https://techdox.nz/phase5b-nonmanifest-codex": 404,
        "https://blog.techdox.nz/": 200,
        "https://blog.techdox.nz/why-selfhost/": 200,
        "https://blog.techdox.nz/index.xml": 200,
        "https://docs.techdox.nz/": 200,
        "https://store.techdox.nz/": 200,
        "https://techdox-landing.pages.dev/": 200,
    }
    protected_results = {
        url: request(url) for url in protected_expectations
    }
    protected_errors = [
        {
            "url": url,
            "expected_status": expected,
            "result": protected_results[url],
        }
        for url, expected in protected_expectations.items()
        if protected_results[url].get("status") != expected
        or protected_results[url].get("location")
    ]

    landing = request("https://techdox.nz/", method="GET")
    landing_origin = request("https://techdox-landing.pages.dev/", method="GET")
    article = request("https://blog.techdox.nz/why-selfhost/", method="GET")
    feed = request("https://blog.techdox.nz/index.xml", method="GET")

    article_body = b""
    feed_body = b""
    landing_body = b""
    landing_origin_body = b""
    for url, holder in (
        ("https://techdox.nz/", "landing"),
        ("https://techdox-landing.pages.dev/", "landing_origin"),
        ("https://blog.techdox.nz/why-selfhost/", "article"),
        ("https://blog.techdox.nz/index.xml", "feed"),
    ):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=25, context=CTX) as response:
            if holder == "landing":
                landing_body = response.read()
            elif holder == "landing_origin":
                landing_origin_body = response.read()
            elif holder == "article":
                article_body = response.read()
            else:
                feed_body = response.read()

    landing_normalized_hash = normalized_landing_hash(landing_body)
    landing_origin_normalized_hash = normalized_landing_hash(landing_origin_body)
    metadata_checks = {
        "landing_hash_matches_verified_artifact": (
            landing_normalized_hash == LANDING_INDEX_SHA256
        ),
        "landing_matches_pages_origin": (
            landing_normalized_hash == landing_origin_normalized_hash
        ),
        "blog_article_canonical_present": (
            b'<link rel="canonical" href="https://blog.techdox.nz/why-selfhost/">'
            in article_body
        ),
        "blog_article_og_url_present": (
            b'<meta property="og:url"         content="https://blog.techdox.nz/why-selfhost/">'
            in article_body
        ),
        "blog_feed_uses_blog_host": (
            b"https://blog.techdox.nz/" in feed_body
            and b"https://techdox.nz/" not in feed_body
        ),
        "blog_article_status": article.get("status") == 200,
        "blog_feed_status": feed.get("status") == 200,
    }

    errors = {
        "mapping_errors": mapping_errors,
        "target_errors": target_errors,
        "protected_errors": protected_errors,
        "metadata_errors": [
            name for name, passed in metadata_checks.items() if not passed
        ],
    }
    passed = not any(errors.values())
    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "passed": passed,
        "summary": {
            "https_mappings": sum(
                1
                for item, result in zip(mappings, mapping_results, strict=True)
                if item["scheme"] == "https"
                and result.get("status") == 301
                and result.get("location") == item["expected"]
            ),
            "http_mappings": sum(
                1
                for item, result in zip(mappings, mapping_results, strict=True)
                if item["scheme"] == "http"
                and result.get("status") == 301
                and result.get("location") == item["expected"]
            ),
            "mappings_per_scheme": len(manifest["entries"]),
            "unique_targets_200": sum(
                1
                for result in target_results
                if result.get("status") == 200 and not result.get("location")
            ),
            "unique_targets": len(targets),
            "protected_checks": len(protected_expectations),
        },
        "landing": landing,
        "landing_origin": landing_origin,
        "landing_normalized_sha256": landing_normalized_hash,
        "landing_origin_normalized_sha256": landing_origin_normalized_hash,
        "cloudflare_web_analytics_beacon_present": bool(
            CLOUDFLARE_BEACON.search(landing_body)
        ),
        "metadata_checks": metadata_checks,
        "protected_results": protected_results,
        "errors": errors,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
