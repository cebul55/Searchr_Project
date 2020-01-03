import os
import shutil
from uuid import uuid4

import scrapy
from scrapy.spiders import CrawlSpider
from tika import parser

from searchr_project.settings import MEDIA_DIR


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
                # todo sprawdzić czy pobiera word
                if 'pdf' in self.i['content-type'] or 'word' in self.i['content-type']:
                    self.i['body'] = self.parse_file_to_text(response)
                else:
                    self.i['body'] = error

        else:
            self.i['body'] = 'Status Code: ' + response.status + '\nPage wasn\'t downloaded.'
        return self.i

    def parse_file_to_text(self, response):
        unique_folder_id = str(uuid4())
        file_name = response.url.split('/')[-1]
        # create folder to store document wich will later be extracted
        folder_path = os.path.join(MEDIA_DIR, 'spider', unique_folder_id)
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            pass

        # download file from url
        path = os.path.join(folder_path, file_name)
        with open(path, 'wb') as f:
            f.write(response.body)
            f.close()

        parsed_text = self.tika_parser(path)
        # remove folder with content
        shutil.rmtree(folder_path, ignore_errors=True, onerror=None)
        return parsed_text

    def tika_parser(self, file_path):
        # Extract text from document
        try:
            content = parser.from_file(file_path)
        except:
            import tika
            tika.initVM()
            content = parser.from_file(file_path)

        if 'content' in content:
            text = content['content']
        else:
            return ''
        # Convert to string
        text = str(text)
        return text
