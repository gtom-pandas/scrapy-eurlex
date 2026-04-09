"""
Spider: eurlex_regulations
Purpose: Scrape public EUR-Lex regulation pages related to food contaminants.

Seed URLs cover:
  - Regulation (EU) 2023/915  – maximum levels for contaminants in food
  - Regulation (EC) 1881/2006 – original contaminants framework
  - Latest consolidated version of 1881/2006
  - Amendment Regulation (EU) 2021/1527
  - EUR-Lex search for "contaminants food" regulations

The spider stays within eur-lex.europa.eu and follows only legal-content
links that look like regulation documents or search results, keeping the
crawl focused and lightweight.
"""

import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import scrapy

from eurlex.items import RegulationItem

# EUR-Lex domain
EURLEX_DOMAIN = "eur-lex.europa.eu"

# Pattern that matches individual legal-content document pages
LEGAL_CONTENT_RE = re.compile(
    r"https://eur-lex\.europa\.eu/legal-content/[A-Z]{2}/TXT/",
    re.IGNORECASE,
)

# Pattern for EUR-Lex search-result pages (list pages worth following)
SEARCH_RE = re.compile(
    r"https://eur-lex\.europa\.eu/search\.html",
    re.IGNORECASE,
)


class EurlexRegulationsSpider(scrapy.Spider):
    name = "eurlex_regulations"
    allowed_domains = [EURLEX_DOMAIN]

    # Seed list: public EUR-Lex pages on food-contaminant regulations.
    # All URLs are genuine EUR-Lex permalinks – no login required.
    start_urls = [
        # Regulation (EU) 2023/915 – maximum levels for contaminants in food
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023R0915",
        # Regulation (EC) 1881/2006 – original framework for contaminant limits
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006R1881",
        # Consolidated version of 1881/2006 (as amended up to 2023)
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02006R1881-20230701",
        # Amendment: Regulation (EU) 2021/1527
        "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021R1527",
        # EUR-Lex search: contaminants food regulations (list page)
        (
            "https://eur-lex.europa.eu/search.html"
            "?query=contaminants+food"
            "&DB_TYPE_OF_ACT=regulation"
            "&SUBDOM_INIT=ALL_ALL"
            "&DTS_DOM=ALL"
            "&typeOfActStatus=REGULATION"
            "&locale=en"
        ),
    ]

    def parse(self, response):
        """Dispatch to the appropriate parser based on URL type."""
        url = response.url

        if LEGAL_CONTENT_RE.search(url):
            yield from self._parse_document(response)
        elif SEARCH_RE.search(url):
            yield from self._parse_search_results(response)
        else:
            self.logger.debug("Skipping unsupported URL: %s", url)

    # ------------------------------------------------------------------
    # Document page parser
    # ------------------------------------------------------------------

    def _parse_document(self, response):
        """Extract item fields from a single EUR-Lex document page."""
        title = self._extract_title(response)
        text = self._extract_text(response)

        item = RegulationItem(
            url=response.url,
            title=title,
            html=response.text,
            text=text,
            crawl_timestamp=datetime.now(timezone.utc).isoformat(),
            source_domain=EURLEX_DOMAIN,
        )
        yield item

        # Follow internal links to related legal-content pages
        yield from self._follow_related_links(response)

    def _extract_title(self, response):
        """Return the document title, falling back gracefully."""
        # EUR-Lex typically puts the title in <title> or a prominent <h1>/<h2>
        title = (
            response.css("title::text").get()
            or response.css("h1.doc-ti::text").get()
            or response.css("h1::text").get()
            or response.css("h2.doc-ti::text").get()
            or ""
        )
        return title.strip()

    def _extract_text(self, response):
        """Return visible page text with normalised whitespace."""
        raw = " ".join(response.css("body *::text").getall())
        return re.sub(r"\s+", " ", raw).strip()

    def _follow_related_links(self, response):
        """Yield requests for related EUR-Lex legal-content links on the page."""
        for href in response.css("a::attr(href)").getall():
            absolute = response.urljoin(href)
            parsed = urlparse(absolute)
            if parsed.netloc != EURLEX_DOMAIN:
                continue
            if LEGAL_CONTENT_RE.search(absolute):
                yield response.follow(absolute, callback=self.parse)

    # ------------------------------------------------------------------
    # Search results page parser
    # ------------------------------------------------------------------

    def _parse_search_results(self, response):
        """Follow links to individual documents found in a search-results page."""
        found = 0
        for href in response.css("a::attr(href)").getall():
            absolute = response.urljoin(href)
            if LEGAL_CONTENT_RE.search(absolute):
                found += 1
                yield response.follow(absolute, callback=self.parse)

        self.logger.info("Search page %s – found %d document links", response.url, found)

        # Follow the next search-results page if present
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
