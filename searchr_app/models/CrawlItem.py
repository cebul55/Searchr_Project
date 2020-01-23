import json

from django.db import models
from django.utils import timezone

from searchr_app.models import SearchResult, Search


class CrawlItem(models.Model):
    """
    Class representing scrapy crawl item with unique_id, extracted data, date and status.
    Only spiders from scrapy framework are inserting data into the table
    """
    unique_id = models.CharField(max_length=100, null=True)
    content_type = models.CharField(max_length=100, null=True)
    data = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='started')

    # Serialisation to return as JSON
    @property
    def to_dictionary(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date,
            'content-type': self.content_type,
        }
        return data

    def __str__(self):
        return self.unique_id

    def save(self, *args, **kwargs):

        if self.status == 'finished':
            scrapy_id = self.unique_id
            search_result = SearchResult.objects.get(scrapy_unique_task_id=scrapy_id)

            if search_result is not None:
                search_result.status = SearchResult._FINISHED
                if self.content_type is not None:
                    search_result.content_type = self.content_type
                else:
                    search_result.content_type = 'SearchR-Unknown'
                if self.data is None or self.data == '':
                    self.data = 'Unable to find content for url: ' + search_result.url + '.'

                search_result.html_file = self.data
                search_result.search_result_hash = search_result.sha256_html_content()
                search_result.save()
                # update number of running searches in search
                search = Search.objects.get(id=search_result.search.id)
                search.running_results = search.running_results - 1
                search.save(force_update=True)

        super(CrawlItem, self).save(*args, **kwargs)
