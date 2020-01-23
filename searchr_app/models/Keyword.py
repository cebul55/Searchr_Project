from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.conf.global_settings import LANGUAGES

from searchr_app.models import Phrase


class Keyword(models.Model):
    """
        Class Keyword - represents single word, that can be part of search phrase

    """
    KEYWORD_MAX_LENGTH = 512
    LANGUAGE_MAX_LENGTH = 7

    keyword = models.CharField(max_length=KEYWORD_MAX_LENGTH, unique=False, null=False)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH, choices=LANGUAGES)
    primary_form = models.CharField(max_length=KEYWORD_MAX_LENGTH)
    slug = models.SlugField(unique=False)
    phrases = models.ManyToManyField(
        Phrase,
        db_table='phrase_consists_of_keywords'
    )

    def save(self, *args, **kwargs):
        if self.keyword == '':
            raise ValidationError('Keyword value can not be empty.')
        self.slug = slugify(self.keyword + ' ' + self.language)

        super(Keyword, self).save(*args, **kwargs)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name_plural = 'keywords'
        unique_together = ('keyword', 'language')
