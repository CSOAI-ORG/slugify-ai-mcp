#!/usr/bin/env python3
"""Convert text to URL-safe slugs. — MEOK AI Labs."""
import json, os, re, hashlib, uuid as _uuid, random
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit/day"})
    _usage[c].append(now); return None

mcp = FastMCP("slugify", instructions="MEOK AI Labs — Convert text to URL-safe slugs.")


@mcp.tool()
def slugify(text: str, separator: str = "-") -> str:
    """Convert text to URL-safe slug."""
    if err := _rl(): return err
    slug = re.sub(r'[^\w\s-]', '', text.lower().strip())
    slug = re.sub(r'[\s_]+', separator, slug)
    slug = re.sub(f'{separator}+', separator, slug).strip(separator)
    return json.dumps({"original": text, "slug": slug, "length": len(slug)}, indent=2)

if __name__ == "__main__":
    mcp.run()
