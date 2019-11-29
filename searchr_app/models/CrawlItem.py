import json

from django.db import models
from django.utils import timezone


class CrawlItem(models.Model):
    """
    Class representing scrapy crawl item with unique_id, extracted data, date and status.
    Only spiders from scrapy framework are inserting data into the table
    """
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='started')

    # Serialisation to return as JSON
    @property
    def to_dictionary(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date,
        }
        return data

    def __str__(self):
        return self.unique_id
    #
    # def save(self, *args, **kwargs):
    #     # todo update search result if cralwItem is saved
    #     super(CrawlItem, self).save(*args, **kwargs)