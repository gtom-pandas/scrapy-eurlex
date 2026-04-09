import scrapy


class RegulationItem(scrapy.Item):
    """Represents a scraped EUR-Lex regulation page."""

    # Page URL
    url = scrapy.Field()

    # Document title extracted from the page
    title = scrapy.Field()

    # Full HTML source of the page
    html = scrapy.Field()

    # Plain text content (whitespace-normalised)
    text = scrapy.Field()

    # ISO-8601 timestamp when the page was crawled
    crawl_timestamp = scrapy.Field()

    # Source domain (always eur-lex.europa.eu)
    source_domain = scrapy.Field()
