# Slugify Ai

> By [MEOK AI Labs](https://meok.ai) — URL slug generation and text normalization. Slugify, deslugify, batch process, and generate SEO-friendly URLs. By MEOK AI Labs.

Slugify AI MCP — MEOK AI Labs. URL slug generation, text normalization, SEO-friendly transformations.

## Installation

```bash
pip install slugify-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install slugify-ai-mcp
```

## Tools

### `slugify`
Convert text to a URL-friendly slug. Handles Unicode, transliteration, stop words.

**Parameters:**
- `text` (str)
- `separator` (str)
- `max_length` (int)
- `remove_stop_words` (bool)

### `deslugify`
Convert a slug back to human-readable text.

**Parameters:**
- `slug` (str)

### `batch_slugify`
Batch slugify multiple texts (pipe-separated). E.g. 'Hello World|My Article|New Post'.

**Parameters:**
- `texts` (str)
- `separator` (str)
- `remove_stop_words` (bool)

### `generate_seo_slug`
Generate an SEO-optimized slug from a title. Removes stop words, adds optional category/date prefix.

**Parameters:**
- `title` (str)
- `category` (str)
- `date_prefix` (bool)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/slugify-ai-mcp](https://github.com/CSOAI-ORG/slugify-ai-mcp)
- **PyPI**: [pypi.org/project/slugify-ai-mcp](https://pypi.org/project/slugify-ai-mcp/)

## License

MIT — MEOK AI Labs
