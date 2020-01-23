# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from searchr_app.models import CrawlItem


class Scrapy4SearchrAppPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.items = []
        self.html_content = None
        self.content_type = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        item = CrawlItem()
        item.unique_id = self.unique_id
        # save html file
        item.content_type = self.content_type
        if self.html_content:
            self.html_content = self.html_content.replace('\x00', '')

        item.data = self.html_content
        item.status = 'finished'
        item.save()

    def process_item(self, item, spider):
        self.items.append(item['body'])
        self.html_content = item['body']
        self.content_type = item['content-type']
        return item
