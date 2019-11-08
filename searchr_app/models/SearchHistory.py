from django.contrib.auth.models import User
from django.db import models

from searchr_app.models import Search, SearchResult


class SearchHistory(models.Model):
    """
    SearchHistory
    """
    search = models.ForeignKey(Search, on_delete=models.SET_NULL, blank=False, null=True)
    username = models.CharField(max_length=150, null=False)
    date_searched = models.DateTimeField(editable=False)
    query_value = models.CharField(max_length=Search.SEARCH_QUERY_LENGTH)
    number_of_results = models.PositiveIntegerField(default=0)
    search_results = models.ManyToManyField(
        SearchResult,
        db_table='search_history_results',
    )

    def __str__(self):
        return self.search.title + ',' + self.username + ',[' + self.date_searched.strftime('%d/%m/%Y, %H:%M:%S') + ']'

    class Meta:
        verbose_name_plural = 'search history'
