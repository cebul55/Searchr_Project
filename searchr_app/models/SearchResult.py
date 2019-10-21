from datetime import date

from django.db import models
from django.utils.timezone import now
from searchr_app.models import Keyword


class SearchResult(models.Model):
    SEARCH_RESULT_NAME_MAX_LEN = 128

    url = models.URLField()
    search_result_hash = models.IntegerField()
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    title = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)

    views = models.IntegerField(default=0)
    first_searched_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.first_searched_date = now()
        super(SearchResult, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Search Results'
        verbose_name = 'Search Result'
