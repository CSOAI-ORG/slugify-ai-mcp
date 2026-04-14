#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import re, json
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("slugify-ai-mcp")
@mcp.tool(name="slugify")
async def slugify(text: str, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    s = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return {"slug": re.sub(r'[-\s]+', '-', s)}
@mcp.tool(name="deslugify")
async def deslugify(slug: str, api_key: str = "") -> str:
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    return {"text": slug.replace('-', ' ').title()}
    return {"text": slug.replace('-', ' ').title()}
if __name__ == "__main__":
    mcp.run()
