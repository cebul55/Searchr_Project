from datetime import date

from django.db import models
from django.utils.timezone import now
from searchr_app.models import Search# , SearchHistory
from hashlib import sha256


class SearchResult(models.Model):
    SEARCH_RESULT_NAME_MAX_LEN = 128

    _CREATED = 'created'
    _STARTED = 'started'
    _FINISHED = 'finished'
    _FINISHED_SAVED = 'finished_saved'
    _FINISHED_ANALYZED = 'finished_analyzed'
    SEARCH_STATUS_CHOICES = [
        (_CREATED, 'CREATED'),
        (_STARTED, 'STARTED'),
        (_FINISHED, 'FINISHED'),
        (_FINISHED_SAVED, 'FINISHED_SAVED'),
        (_FINISHED_ANALYZED, 'FINISHED_ANALYZED')
    ]

    title = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    url = models.URLField(null=False, blank=False)
    search_result_hash = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    content_type = models.CharField(max_length=100, null=True)
    html_file = models.TextField(editable=False, null=True)
    date_found = models.DateTimeField()
    accuracy = models.FloatField(default=0)
    status = models.CharField(max_length=30, null=False, choices=SEARCH_STATUS_CHOICES, default=_CREATED)
    scrapy_unique_task_id = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN, editable=False)

    search = models.ForeignKey(Search, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Object Search Result is not editable
        is_new_result = False
        if not self.id:
            self.date_found = now()
            is_new_result = True
        # if self.status == self._FINISHED:
        #     self.status = self._FINISHED_SAVED
        #     self.search.running_results = self.search.running_results - 1
        #     self.search_result_hash = self.sha256_html_content()
        #     self.search.save()
        super(SearchResult, self).save(*args, **kwargs)
        if is_new_result:
            from searchr_app.models.search_models_helper_functions import add_result_to_history
            add_result_to_history(self.search, self)
        if self.status == self._FINISHED:
            # start analyzing result
            from searchr_app.models.search_models_helper_functions import analyze_search_result
            analyze_search_result(self)

    def sha256_html_content(self):
        if self.html_file:
            hashed_html_content = sha256(str(self.html_file).encode('utf-8')).hexdigest()
        else:
            hashed_html_content = -1
        return hashed_html_content

    def set_status_to_analyzed(self):
        if not self.id:
            pass
        self.status = self._FINISHED_ANALYZED
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Search Results'
        verbose_name = 'Search Result'

# todo calculate accuracy
