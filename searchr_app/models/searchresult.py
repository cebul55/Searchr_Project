from datetime import date

from django.db import models

from searchr_app.models import Keyword


class SearchResult( models.Model):
    SEARCH_RESULT_NAME_MAX_LEN = 128

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    search_result_title = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    url = models.URLField()
    views = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        now = date.today()
        self.date_last_searched = now
        super(SearchResult, self).save(*args, **kwargs)

    def __str__(self):
        return self.search_result_title

    class Meta:
        verbose_name_plural = 'Search Results'
        verbose_name = 'Search Result'
