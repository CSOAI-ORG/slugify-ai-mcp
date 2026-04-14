#!/usr/bin/env python3
import re, json
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("slugify-ai-mcp")
@mcp.tool(name="slugify")
async def slugify(text: str) -> str:
    s = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return json.dumps({"slug": re.sub(r'[-\s]+', '-', s)})
@mcp.tool(name="deslugify")
async def deslugify(slug: str) -> str:
    return json.dumps({"text": slug.replace('-', ' ').title()})
if __name__ == "__main__":
    mcp.run()
