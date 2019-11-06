from django.db import models
from django.utils import timezone

from searchr_app.models import Project


class Search(models.Model):
    """
    Search model represents single search object which has search parameters defined
    @:param str title: title of search. Has to be unique together in project
    """
    SEARCH_TITLE_LENGTH = 128
    SEARCH_ATTRIBS_LENGTH = 256
    SEARCH_QUERY_LENGTH = 1024

    _GOOGLE = 'go'
    _BING = 'bg'
    _YAHOO = 'yh'
    SEARCH_ENGINE_CHOICES = [
        (_GOOGLE, 'GOOGLE'),
        (_BING, 'BING'),
        (_YAHOO, 'YAHOO'),
    ]

    title = models.CharField(max_length=SEARCH_TITLE_LENGTH, null=False, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    attributes = models.CharField(max_length=SEARCH_ATTRIBS_LENGTH, null=True)
    query = models.CharField(max_length=SEARCH_QUERY_LENGTH, null=False, default=None)
    search_engine = models.CharField(max_length=64, choices=SEARCH_ENGINE_CHOICES, default=_BING)
    date_created = models.DateTimeField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        super(Search, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'searches'
        unique_together = ('title', 'project')
