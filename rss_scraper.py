"""
RSS scraping logic for AWS service feeds.

Responsibilities:
  - Fetch and parse RSS/Atom feeds via feedparser
  - Filter What's New items by service keywords
  - Deduplicate items across multiple feeds for the same service
  - Return structured FeedItem dicts ready for email rendering
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone, timedelta
from typing import Any

import feedparser

from aws_services import WHATS_NEW_FEED, SERVICES_BY_NAME


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------

def _make_item(entry: Any, source_url: str) -> dict:
    """Normalise a feedparser entry into a plain dict."""
    # Parse published date — feedparser gives us a time.struct_time
    published = None
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
        published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

    summary = ""
    if hasattr(entry, "summary"):
        # Strip basic HTML tags from summary
        import re
        summary = re.sub(r"<[^>]+>", "", entry.summary).strip()
        summary = " ".join(summary.split())  # collapse whitespace
        if len(summary) > 400:
            summary = summary[:397] + "..."

    return {
        "title": getattr(entry, "title", "No Title").strip(),
        "link": getattr(entry, "link", ""),
        "published": published,
        "summary": summary,
        "guid": getattr(entry, "id", getattr(entry, "link", "")),
        "source_url": source_url,
    }


# ---------------------------------------------------------------------------
# Core fetch helpers
# ---------------------------------------------------------------------------

def fetch_feed(url: str, timeout: int = 15) -> list[dict]:
    """Fetch and parse a single RSS/Atom feed. Returns list of item dicts."""
    try:
        parsed = feedparser.parse(url, request_headers={"User-Agent": "aws-rss-digest/1.0"})
        if parsed.bozo and not parsed.entries:
            return []
        return [_make_item(e, url) for e in parsed.entries]
    except Exception:
        return []


def _derive_name_terms(service_name: str) -> list[str]:
    """Derive title-match terms from a service's display name.

    Parses the name field into the meaningful parts a feed title would contain.
    AWS What's New titles always lead with the service name, so we match only
    against the name itself — not broad descriptive keywords.

    Examples
    --------
    "EC2 (Elastic Compute Cloud)"          → ["ec2", "elastic compute cloud"]
    "Lambda"                                → ["lambda"]
    "S3 (Simple Storage Service)"           → ["s3", "simple storage service"]
    "AWS Config"                            → ["aws config", "config"]
    "IAM (Identity & Access Management)"    → ["iam", "identity & access management",
                                               "identity and access management"]
    "MQ (Amazon MQ)"                        → ["mq", "amazon mq"]
    "IoT Core"                              → ["iot core"]
    """
    terms: set[str] = set()

    # --- Text inside parentheses becomes its own term ---
    for paren_content in re.findall(r'\(([^)]+)\)', service_name):
        t = paren_content.strip().lower()
        terms.add(t)
        if "&" in t:
            terms.add(t.replace("&", "and"))  # "identity and access management"

    # --- Main name = everything before the first '(' ---
    main = re.sub(r'\s*\(.*', "", service_name).strip()
    if main:
        m = main.lower()
        terms.add(m)
        # If prefixed with "amazon " or "aws ", also add the bare name
        for prefix in ("amazon ", "aws "):
            if m.startswith(prefix):
                terms.add(m[len(prefix):])
                break

    return [t for t in sorted(terms) if t]


def filter_by_keywords(items: list[dict], keywords: list[str]) -> list[dict]:
    """Keep only items whose title contains at least one of the given terms.

    Called with name-derived terms (from _derive_name_terms) so that matches
    reflect the actual service name appearing in the title, not loose keywords.
    AWS What's New titles always name the primary service
    (e.g. "AWS Lambda now supports..."), so this gives precise, relevant results.
    """
    lower_kw = [kw.lower() for kw in keywords]

    def matches(item: dict) -> bool:
        haystack = item["title"].lower()
        return any(kw in haystack for kw in lower_kw)

    return [i for i in items if matches(i)]


def _cutoff_date(days_back: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days_back)


def _within_window(item: dict, cutoff: datetime) -> bool:
    if item["published"] is None:
        return True  # include items with unknown dates
    return item["published"] >= cutoff


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def scrape_services(
    selected_service_names: list[str],
    custom_feed_urls: list[str] | None = None,
    days_back: int = 7,
) -> dict[str, list[dict]]:
    """
    Scrape RSS feeds for the given service names.

    Returns a dict:  { service_name: [item, ...], ... }
    Items are sorted newest-first, deduplicated by GUID, and filtered to
    `days_back` days.
    """
    cutoff = _cutoff_date(days_back)
    results: dict[str, list[dict]] = {}

    # Cache the What's New feed so we only fetch it once
    whats_new_cache: list[dict] | None = None

    for name in selected_service_names:
        service = SERVICES_BY_NAME.get(name)
        if not service:
            continue

        seen_guids: set[str] = set()
        items: list[dict] = []

        for feed_url in service["feeds"]:
            if feed_url == WHATS_NEW_FEED:
                if whats_new_cache is None:
                    whats_new_cache = fetch_feed(WHATS_NEW_FEED)
                raw = whats_new_cache
                # Filter by service name terms unless the service covers all feeds
                if service["name"] not in ("What's New (All Services)", "AWS News Blog (All)"):
                    name_terms = _derive_name_terms(service["name"])
                    raw = filter_by_keywords(raw, name_terms)
            else:
                raw = fetch_feed(feed_url)

            for item in raw:
                if item["guid"] not in seen_guids and _within_window(item, cutoff):
                    seen_guids.add(item["guid"])
                    items.append(item)

        # Sort newest-first
        items.sort(
            key=lambda i: i["published"] or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        results[name] = items

    # Handle custom feed URLs (grouped under a single "Custom Feeds" key)
    if custom_feed_urls:
        seen_guids: set[str] = set()
        custom_items: list[dict] = []
        for url in custom_feed_urls:
            url = url.strip()
            if not url:
                continue
            for item in fetch_feed(url):
                if item["guid"] not in seen_guids and _within_window(item, cutoff):
                    seen_guids.add(item["guid"])
                    custom_items.append(item)
        if custom_items:
            custom_items.sort(
                key=lambda i: i["published"] or datetime.min.replace(tzinfo=timezone.utc),
                reverse=True,
            )
            results["Custom Feeds"] = custom_items

    return results


def total_item_count(results: dict[str, list[dict]]) -> int:
    return sum(len(v) for v in results.values())
