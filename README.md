<div align="center">

# Slugify Ai MCP

**MCP server for slugify ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-slugify-ai-mcp)](https://pypi.org/project/meok-slugify-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Slugify Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `slugify` | Convert text to a URL-friendly slug. Handles Unicode, transliteration, stop word |
| `deslugify` | Convert a slug back to human-readable text. |
| `batch_slugify` | Batch slugify multiple texts (pipe-separated). E.g. 'Hello World|My Article|New  |
| `generate_seo_slug` | Generate an SEO-optimized slug from a title. Removes stop words, adds optional c |

## Installation

```bash
pip install meok-slugify-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "slugify-ai": {
      "command": "python",
      "args": ["-m", "meok_slugify_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
