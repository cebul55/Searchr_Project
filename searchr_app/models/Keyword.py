from django.utils.timezone import now
from django.db import models
from django.utils.text import slugify
from django.conf.global_settings import LANGUAGES

'''
    Class Keyword - represents single word, that can be part of search phrase
    
'''
class Keyword(models.Model):
    KEYWORD_MAX_LENGTH = 128
    LANGUAGE_MAX_LENGTH = 7

    keyword = models.CharField(max_length=KEYWORD_MAX_LENGTH)
    language = models.CharField(max_length=LANGUAGE_MAX_LENGTH, choices=LANGUAGES)

    # todo get root form basing on language and keyword
    root_form = models.CharField(max_length=KEYWORD_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    # todo remove date_lase_searched
    date_last_searched = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.keyword)
        super(Keyword, self).save(*args, **kwargs)

    def __str__(self):
        return self.keyword

    def update_date_last_searched(self):
        self.date_last_searched = now()
        self.save()

    class Meta:
        verbose_name_plural = 'keywords'
