# scrapy-eurlex

A minimal, clean Scrapy project for scraping public **EUR-Lex** regulation pages
related to **food-contaminant legislation** (e.g. Regulation (EU) 2023/915).  
The project is ready to run locally **and** to deploy directly to
[Zyte / Scrapy Cloud](https://www.zyte.com/scrapy-cloud/).

---

## Project structure

```
scrapy-eurlex/
├── scrapy.cfg                   # Scrapy / Zyte deployment configuration
├── requirements.txt             # Python dependencies
├── eurlex/
│   ├── __init__.py
│   ├── items.py                 # Item definition (fields produced by the spider)
│   ├── pipelines.py             # Duplicate-URL filter pipeline
│   ├── settings.py              # Scrapy settings (JSONL output, AutoThrottle, …)
│   └── spiders/
│       └── eurlex_regulations.py  # Main spider
└── output/                      # Created automatically at crawl time
    └── regulations.jsonl        # JSONL output (one regulation per line)
```

---

## Fields produced

| Field | Description |
|---|---|
| `url` | URL of the scraped page |
| `title` | Document title extracted from the page |
| `html` | Full HTML source |
| `text` | Visible page text (whitespace-normalised) |
| `crawl_timestamp` | ISO-8601 UTC timestamp of the crawl |
| `source_domain` | Always `eur-lex.europa.eu` |

---

## Seed URLs

The spider starts from a focused list of public EUR-Lex pages:

| Document | URL |
|---|---|
| Regulation (EU) 2023/915 | `CELEX:32023R0915` |
| Regulation (EC) 1881/2006 | `CELEX:32006R1881` |
| Consolidated 1881/2006 (2023) | `CELEX:02006R1881-20230701` |
| Amendment (EU) 2021/1527 | `CELEX:32021R1527` |
| EUR-Lex search: contaminants food | search page |

From each document page the spider also follows links to related
`/legal-content/` pages on `eur-lex.europa.eu`, keeping the crawl within scope.

---

## Run locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the spider

```bash
scrapy crawl eurlex_regulations
```

Output is written to `output/regulations.jsonl` (JSONL, UTF-8).

### 3. Export to other formats

```bash
# CSV
scrapy crawl eurlex_regulations -o output/regulations.csv

# JSON array
scrapy crawl eurlex_regulations -o output/regulations.json
```

> **Tip:** the `-o` flag overrides the default JSONL feed defined in `settings.py`.

---

## Deploy to Zyte / Scrapy Cloud

### Prerequisites

```bash
pip install shub        # Zyte command-line tool
shub login              # authenticate with your Zyte API key
```

### Configure the project

Edit `scrapy.cfg` and fill in your Zyte project ID:

```ini
[deploy]
url     = https://app.zyte.com/api/scrapyd/
project = <YOUR_ZYTE_PROJECT_ID>
```

### Deploy

```bash
shub deploy
```

### Run the spider from the Zyte UI

1. Open your project in [app.zyte.com](https://app.zyte.com).
2. Go to **Spiders** → select `eurlex_regulations`.
3. Click **Run**.
4. Download the output from the **Jobs** tab once the run completes.

---

## Notes

* **No authentication required** – all scraped pages are publicly accessible.
* **Polite crawling** – `DOWNLOAD_DELAY = 1.5 s` and AutoThrottle are enabled
  to avoid overloading the EUR-Lex servers.
* `ROBOTSTXT_OBEY = True` – the spider respects `robots.txt`.
