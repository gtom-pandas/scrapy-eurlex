BOT_NAME = "eurlex"

SPIDER_MODULES = ["eurlex.spiders"]
NEWSPIDER_MODULE = "eurlex.spiders"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Polite crawl rate – EUR-Lex is a public service, be considerate
DOWNLOAD_DELAY = 1.5
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Default encoding
FEED_EXPORT_ENCODING = "utf-8"

# Output format: JSONL (one JSON object per line, easy to stream/load)
FEEDS = {
    "output/regulations.jsonl": {
        "format": "jsonlines",
        "encoding": "utf8",
        "overwrite": False,
    }
}

# Enable the duplicate-URL pipeline
ITEM_PIPELINES = {
    "eurlex.pipelines.DuplicateFilterPipeline": 300,
}

# Scrapy Cloud / Zyte compatibility
# AutoThrottle adapts the crawl speed automatically
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Keep cookies disabled – no login needed
COOKIES_ENABLED = False

# Retry on transient errors
RETRY_ENABLED = True
RETRY_TIMES = 3

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Telnet console (disable in production if desired)
TELNETCONSOLE_ENABLED = False

# Log level
LOG_LEVEL = "INFO"
