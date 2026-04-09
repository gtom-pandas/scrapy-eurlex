from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicateFilterPipeline:
    """Drop items whose URL has already been seen in the current run."""

    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get("url")
        if url in self.seen_urls:
            spider.logger.debug("Duplicate item dropped: %s", url)
            raise DropItem(f"Duplicate URL: {url}")
        self.seen_urls.add(url)
        return item
