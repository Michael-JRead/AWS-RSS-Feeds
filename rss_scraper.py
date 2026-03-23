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

    # Extract "general:products/{service-id}" category tags — AWS's authoritative
    # service identifiers. Each What's New item is tagged with exactly the service(s)
    # an announcement relates to, enabling precise filtering without title guessing.
    #
    # AWS RSS category tags can appear in several formats:
    #   Format A: scheme="general:products", term="amazon-ec2"
    #   Format B: term="general:products/amazon-ec2"  (no scheme)
    #   Format C: term="general:products/amazon-msk,marketing:marchitecture/analytics"
    #             (comma-separated list — multiple namespaces in one tag)
    # We split each term by comma and process every part individually.
    product_ids: list[str] = []
    if hasattr(entry, "tags") and entry.tags:
        for tag in entry.tags:
            raw_term = (getattr(tag, "term",   "") or "").strip()
            scheme   = (getattr(tag, "scheme", "") or "").strip()

            for part in raw_term.split(","):
                part = part.strip()
                if not part:
                    continue

                if scheme == "general:products":
                    # Format A: scheme carries the namespace; part is the product ID
                    # (may include a path component — take the last segment)
                    pid = part.split("/")[-1].lower().strip()
                    if pid and ":" not in pid and pid not in product_ids:
                        product_ids.append(pid)
                elif "general:products/" in part:
                    # Format B/C: full URI in the term, e.g. "general:products/amazon-msk"
                    pid = part.split("general:products/")[-1].lower().strip()
                    # Remove any trailing slash-separated sub-path (defensive)
                    pid = pid.split("/")[0].strip()
                    if pid and ":" not in pid and pid not in product_ids:
                        product_ids.append(pid)

    return {
        "title":       getattr(entry, "title", "No Title").strip(),
        "link":        getattr(entry, "link", ""),
        "published":   published,
        "summary":     summary,
        "guid":        getattr(entry, "id", getattr(entry, "link", "")),
        "source_url":  source_url,
        "product_ids": product_ids,   # AWS-assigned service identifiers from <category> tags
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


def _derive_product_ids(service_name: str) -> list[str]:
    """Generate candidate AWS product-ID strings from a service display name.

    AWS What's New items carry <category>general:products/{service-id}</category>
    tags. We derive likely IDs from the display name so we can match against them
    without requiring every service entry to be hand-annotated.

    Examples
    --------
    "EC2 (Elastic Compute Cloud)"  → ["amazon-ec2", "aws-ec2"]
    "Lambda"                       → ["amazon-lambda", "aws-lambda"]
    "Amazon Aurora"                → ["amazon-aurora"]
    "AWS Config"                   → ["aws-config"]
    "MemoryDB for Redis"           → ["amazon-memorydb-for-redis", "aws-memorydb-for-redis",
                                      "amazon-memorydb", "aws-memorydb"]
    "MQ (Amazon MQ)"               → ["amazon-mq", "aws-mq"]
    """
    candidates: list[str] = []

    def _slugify(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[/\\]", "-", s)
        s = re.sub(r"[._]", "", s)
        s = re.sub(r"\s+", "-", s.strip())
        s = re.sub(r"-+", "-", s).strip("-")
        return s

    def _add(slug: str, prefix: str) -> None:
        if slug:
            pid = f"{prefix}{slug}"
            if pid not in candidates:
                candidates.append(pid)

    # Strip parenthetical content to get the main name
    main = re.sub(r"\s*\(.*", "", service_name).strip()
    main_lower = main.lower()

    if main_lower.startswith("amazon "):
        slug = _slugify(main[7:])
        _add(slug, "amazon-")
        # For "Amazon X for Y" — also try without "for Y" suffix
        if "-for-" in slug:
            _add(slug.split("-for-")[0], "amazon-")
    elif main_lower.startswith("aws "):
        slug = _slugify(main[4:])
        _add(slug, "aws-")
        if "-for-" in slug:
            _add(slug.split("-for-")[0], "aws-")
    else:
        # Bare name (e.g. "Lambda", "EC2", "Route 53") — try both amazon- and aws-
        slug = _slugify(main)
        _add(slug, "amazon-")
        _add(slug, "aws-")
        if "-for-" in slug:
            base = slug.split("-for-")[0]
            _add(base, "amazon-")
            _add(base, "aws-")

    # Check parenthetical content for embedded "Amazon X" / "AWS X" patterns
    # e.g., "MQ (Amazon MQ)" → also derive "amazon-mq"
    for paren in re.findall(r"\(([^)]+)\)", service_name):
        p = paren.strip()
        p_lower = p.lower()
        if p_lower.startswith("amazon "):
            _add(_slugify(p[7:]), "amazon-")
        elif p_lower.startswith("aws "):
            _add(_slugify(p[4:]), "aws-")

    return candidates


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
                # Filter items to those relevant to this service.
                # Two-layer approach for 100% accuracy:
                #   Layer 1 (primary):  match by AWS category product-IDs — exact, authoritative
                #   Layer 2 (fallback): title substring match for any items lacking category tags
                if service["name"] not in ("What's New (All Services)", "AWS News Blog (All)"):
                    # Build the set of product IDs this service should appear under.
                    # Explicit overrides in the registry take priority; auto-derived fill the rest.
                    candidate_ids: set[str] = set(service.get("product_ids", []))
                    candidate_ids.update(_derive_product_ids(service["name"]))

                    # Partition: items AWS has tagged vs those without any product tag
                    tagged   = [i for i in raw if i["product_ids"]]
                    untagged = [i for i in raw if not i["product_ids"]]

                    # Layer 1 — exact category match (zero false positives)
                    matched_tagged = [
                        i for i in tagged
                        if set(i["product_ids"]) & candidate_ids
                    ]

                    # Layer 2 — title match only on untagged items (safe fallback)
                    name_terms = _derive_name_terms(service["name"])
                    matched_untagged = filter_by_keywords(untagged, name_terms)

                    raw = matched_tagged + matched_untagged
            else:
                raw = fetch_feed(feed_url)
                # Blog feeds (e.g. big-data, compute, security) are CATEGORY blogs —
                # they cover many services, not just the one selected. Apply the same
                # two-layer filter so only relevant posts appear.
                # "All Services" / "All" entries are deliberately left unfiltered.
                if service["name"] not in ("What's New (All Services)", "AWS News Blog (All)"):
                    candidate_ids: set[str] = set(service.get("product_ids", []))
                    candidate_ids.update(_derive_product_ids(service["name"]))

                    tagged_b   = [i for i in raw if i["product_ids"]]
                    untagged_b = [i for i in raw if not i["product_ids"]]

                    matched_b_tagged = [
                        i for i in tagged_b
                        if set(i["product_ids"]) & candidate_ids
                    ]
                    name_terms_b = _derive_name_terms(service["name"])
                    matched_b_untagged = filter_by_keywords(untagged_b, name_terms_b)

                    raw = matched_b_tagged + matched_b_untagged

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
