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
        headers = str(response.headers)
        if len(headers) > 100:
            self.i['content-type'] = headers[0:100]#response.headers.get('Content-Type').decode('utf-8')
        else:
            self.i['content-type'] = headers
        yield response.request.replace(callback=self.parse_item, method='GET')

    def parse_item(self, response):
        # i['url'] = response.text

        # if response.headers.get('Content-Type') == 'Unknown':
        #     try:

        # else:

        if response.status == 200:

            self.i['body'] = response.text

        else:
            self.i['body'] = 'Status Code: ' + response.status + '\nPage wasn\'t downloaded.'
        return self.i
