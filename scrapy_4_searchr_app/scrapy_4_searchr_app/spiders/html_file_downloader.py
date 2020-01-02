import scrapy
from scrapy.spiders import CrawlSpider


class HtmlFileDownloader(CrawlSpider):
    name = 'html_file_downloader'
    i = {}

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

        super(HtmlFileDownloader, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_headers, method='HEAD')

    def parse_headers(self, response):
        if response.status == 200:
            self.i['content-type'] = response.headers.get('Content-Type').decode('utf-8')
            yield response.request.replace(callback=self.parse_item, method='GET')
        else:
            self.i['content-type'] = ''
            self.i['body'] = 'Status Code: ' + response.status + '\nPage wasn\'t downloaded.'
            return self.i

    def parse_item(self, response):
        if response.status == 200:

            try:
                self.i['body'] = response.text
            except AttributeError as error:
                self.i['body'] = error

        else:
            self.i['body'] = 'Status Code: ' + response.status + '\nPage wasn\'t downloaded.'
        return self.i
