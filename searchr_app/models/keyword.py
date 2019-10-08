from django.db import models
from django.utils.text import slugify

# from searchr_app.models.phrase import Phrase


class Keyword(models.Model):
    KEYWORD_MAX_LENGTH = 128

    # phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=KEYWORD_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    date_last_searched = models.DateTimeField(default=None)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.keyword)
        super(Keyword, self).save(*args, **kwargs)

    def __str__(self):
        return self.keyword

