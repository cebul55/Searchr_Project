from django.db import models
from django.utils import timezone
from django.utils.text import slugify

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

    _CREATED = 'created'
    _SAVED = 'saved'
    _SEARCHED = 'searched'
    SEARCH_STATUS_CHOICES = [
        (_CREATED, 'CREATED'),
        (_SAVED, 'SAVED'),
        (_SEARCHED, 'SEARCHED'),
    ]

    title = models.CharField(max_length=SEARCH_TITLE_LENGTH, null=False, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    attributes = models.CharField(max_length=SEARCH_ATTRIBS_LENGTH, null=True)
    query = models.CharField(max_length=SEARCH_QUERY_LENGTH, null=False, default=None)
    search_engine = models.CharField(max_length=64, choices=SEARCH_ENGINE_CHOICES, default=_BING)
    date_created = models.DateTimeField(editable=False)
    status = models.CharField(max_length=64, null=False, blank=False, editable=False, default=_CREATED)
    # todo show status in view
    slug = models.SlugField(max_length=SEARCH_TITLE_LENGTH, null=False, unique=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.slug = slugify(self.title.strip())
        super(Search, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'searches'
        unique_together = ('title', 'project')
