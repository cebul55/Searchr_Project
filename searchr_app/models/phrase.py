from django.db import models
from django.utils.text import slugify


class Phrase(models.Model):
    PHRASE_MAX_LENGTH = 1200

    phrase_name = models.CharField(max_length=PHRASE_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.phrase_name)
        super(Phrase, self).save(*args, **kwargs)

    def __str__(self):
        return self.phrase_name

    class Meta:
        verbose_name_plural = 'Phrases'
