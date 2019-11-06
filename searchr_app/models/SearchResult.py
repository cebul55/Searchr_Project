from datetime import date

from django.db import models
from django.utils.timezone import now
from searchr_app.models import Phrase
from hashlib import sha256


class SearchResult(models.Model):
    SEARCH_RESULT_NAME_MAX_LEN = 128

    title = models.CharField(max_length=SEARCH_RESULT_NAME_MAX_LEN)
    url = models.URLField()
    search_result_hash = models.CharField(max_length=64)
    html_content = models.TextField(editable=False)
    date_found = models.DateTimeField()
    accuracy = models.FloatField(default=0)
#    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)

    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Object Search Result is not editable
        if not self.pk:
            self.date_found = now()
            self.search_result_hash = self.sha256_html_content()
            super(SearchResult, self).save(*args, **kwargs)

    def sha256_html_content(self):
        if self.html_content:
            hashed_html_content = sha256(str(self.html_content).encode('utf-8')).hexdigest()
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