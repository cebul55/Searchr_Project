import scrapy
from scrapy.spiders import CrawlSpider


class HtmlFileDownloader(CrawlSpider):
    name = 'html_file_downloader'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        super(HtmlFileDownloader, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        i = {}
        i['url'] = response.body
        return i