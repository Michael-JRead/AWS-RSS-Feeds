"""
RSS scraping logic for AWS service feeds.

Responsibilities:
  - Fetch and parse RSS/Atom feeds via feedparser
  - Filter What's New items by service keywords
  - Deduplicate items across multiple feeds for the same service
  - Return structured FeedItem dicts ready for email rendering
"""

from __future__ import annotations

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


def filter_by_keywords(items: list[dict], keywords: list[str]) -> list[dict]:
    """Keep only items whose title or summary contains at least one keyword."""
    lower_kw = [kw.lower() for kw in keywords]

    def matches(item: dict) -> bool:
        haystack = (item["title"] + " " + item["summary"]).lower()
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
                # Filter by keywords unless the service explicitly covers all
                if service["name"] not in ("What's New (All Services)", "AWS News Blog (All)"):
                    raw = filter_by_keywords(raw, service["keywords"])
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
