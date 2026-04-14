#!/usr/bin/env python3
"""Slugify AI MCP — MEOK AI Labs. URL slug generation, text normalization, SEO-friendly transformations."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import re, json, unicodedata, hashlib
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

mcp = FastMCP("slugify-ai", instructions="URL slug generation and text normalization. Slugify, deslugify, batch process, and generate SEO-friendly URLs. By MEOK AI Labs.")

# Common transliterations for non-ASCII
_TRANSLIT = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'à': 'a', 'á': 'a', 'â': 'a',
    'ã': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e',
    'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ñ': 'n', 'ò': 'o',
    'ó': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u',
    'ý': 'y', 'ÿ': 'y', 'ð': 'd', 'þ': 'th', 'œ': 'oe',
}

STOP_WORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'it', 'as'}


def _transliterate(text: str) -> str:
    result = []
    for ch in text:
        if ch in _TRANSLIT:
            result.append(_TRANSLIT[ch])
        else:
            decomposed = unicodedata.normalize('NFD', ch)
            result.append(''.join(c for c in decomposed if unicodedata.category(c) != 'Mn'))
    return ''.join(result)


def _make_slug(text: str, separator: str = "-", max_length: int = 80, remove_stop_words: bool = False, lowercase: bool = True) -> str:
    s = _transliterate(text)
    if lowercase:
        s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s).strip()
    if remove_stop_words:
        words = s.split()
        words = [w for w in words if w not in STOP_WORDS]
        s = ' '.join(words)
    s = re.sub(r'[-\s]+', separator, s)
    if max_length and len(s) > max_length:
        s = s[:max_length].rstrip(separator)
    return s


@mcp.tool()
def slugify(text: str, separator: str = "-", max_length: int = 80, remove_stop_words: bool = False, api_key: str = "") -> str:
    """Convert text to a URL-friendly slug. Handles Unicode, transliteration, stop words."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    slug = _make_slug(text, separator=separator, max_length=max_length, remove_stop_words=remove_stop_words)
    return {
        "original": text,
        "slug": slug,
        "length": len(slug),
        "url_safe": True,
        "separator": separator,
    }


@mcp.tool()
def deslugify(slug: str, api_key: str = "") -> str:
    """Convert a slug back to human-readable text."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    for sep in ['-', '_', '.']:
        slug = slug.replace(sep, ' ')
    text = slug.strip().title()
    return {"slug": slug, "text": text}


@mcp.tool()
def batch_slugify(texts: str, separator: str = "-", remove_stop_words: bool = False, api_key: str = "") -> str:
    """Batch slugify multiple texts (pipe-separated). E.g. 'Hello World|My Article|New Post'."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    items = [t.strip() for t in texts.split('|') if t.strip()]
    results = []
    seen = set()
    for text in items:
        slug = _make_slug(text, separator=separator, remove_stop_words=remove_stop_words)
        # Deduplicate
        base = slug
        counter = 1
        while slug in seen:
            slug = f"{base}{separator}{counter}"
            counter += 1
        seen.add(slug)
        results.append({"original": text, "slug": slug})

    return {"results": results, "total": len(results), "duplicates_resolved": len(results) - len(set(r["slug"] for r in results)) == 0}


@mcp.tool()
def generate_seo_slug(title: str, category: str = "", date_prefix: bool = False, api_key: str = "") -> str:
    """Generate an SEO-optimized slug from a title. Removes stop words, adds optional category/date prefix."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    slug = _make_slug(title, remove_stop_words=True, max_length=60)
    parts = []
    if date_prefix:
        parts.append(datetime.now(timezone.utc).strftime("%Y/%m"))
    if category:
        parts.append(_make_slug(category, max_length=20))
    parts.append(slug)
    full_path = "/".join(parts)

    return {
        "title": title,
        "slug": slug,
        "full_path": f"/{full_path}",
        "seo_tips": [
            f"Length: {len(slug)} chars (optimal: 50-60)",
            "Stop words removed" if len(slug) < len(_make_slug(title)) else "No stop words found",
            "Contains target keywords" if len(slug.split('-')) >= 2 else "Consider adding more keywords",
        ],
        "character_count": len(slug),
    }


if __name__ == "__main__":
    mcp.run()
