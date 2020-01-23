from django.conf.global_settings import LANGUAGES
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.utils.text import slugify

from searchr_app.models import Project


class Phrase(models.Model):
    _PHRASE_PRIVATE_FIELD_NAME = 'Is Phrase private?'
    _PHRASE_MAX_LENGTH = 1024
    LANGUAGE_MAX_LENGTH = 7

    value = models.TextField(null=False, )
    date_created = models.DateTimeField(editable=False)
    date_last_searched = models.DateTimeField()
    number_of_searches = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH, choices=LANGUAGES)
    # searches = models.ManyToManyField(
    #     Search,
    #     db_table='search_contains_phrase',
    # )
    projects = models.ManyToManyField(
        Project,
        db_table='project_contains_phrases',
    )
    slug = models.SlugField(max_length=_PHRASE_MAX_LENGTH, null=False, unique=False)

    def save(self, *args, **kwargs):
        if self.value == '':
            raise ValidationError('Value of phrase can not be empty')
        self.slug = slugify(self.value.strip())
        """ On save update timestamps """
        date_saved = timezone.now()
        if not self.id:
            self.date_created = date_saved
        self.date_last_searched = date_saved
        super(Phrase, self).save(*args, **kwargs)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name_plural = 'phrases'
        unique_together = ('value', 'language')
