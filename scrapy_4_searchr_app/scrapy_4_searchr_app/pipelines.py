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

    @classmethod
    def from_crawled(cls, crawler):
        return cls(
            # unique id passed from searchr_app
            unique_id=crawler.settings.get('unique_id')
        )

    def close_spider(self, spider):
        # at the end of living cycle, spider saves crawled data into database
        item = CrawlItem()
        item.unique_id = self.unique_id
        item.data = json.dumps(self.items)
        item.status = 'finished'
        item.save()


    def process_item(self, item, spider):
        self.items.append(item['url'])
        return item
