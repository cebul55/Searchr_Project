from datetime import date

from django.db import models
from django.utils.timezone import now
from searchr_app.models import Search
from hashlib import sha256


class SearchResult(models.Model):
    SEARCH_RESULT_NAME_MAX_LEN = 128

    _CREATED = 'created'
    _STARTED = 'started'
    _FINISHED = 'finished'
    SEARCH_STATUS_CHOICES = [
        (_CREATED, 'CREATED'),
        (_STARTED, 'STARTED'),
        (_FINISHED, 'FINISHED'),
    ]

    title = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    url = models.URLField(null=False, blank=False)
    search_result_hash = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    html_file = models.TextField(editable=False)
    date_found = models.DateTimeField()
    accuracy = models.FloatField(default=0)
    status = models.CharField(max_length=30, null=False, choices=SEARCH_STATUS_CHOICES, default=_CREATED)
    scrapy_unique_task_id = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN, editable=False)

    search = models.ForeignKey(Search, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Object Search Result is not editable
        if not self.id:
            self.date_found = now()
            self.search_result_hash = self.sha256_html_content()
        super(SearchResult, self).save(*args, **kwargs)

    def sha256_html_content(self):
        if self.html_file:
            hashed_html_content = sha256(str(self.html_file).encode('utf-8')).hexdigest()
        else:
            hashed_html_content = -1
        return hashed_html_content

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Search Results'
        verbose_name = 'Search Result'

# todo calculate accuracy
# todo remove views ?