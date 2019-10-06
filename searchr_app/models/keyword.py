from django.db import models

from searchr_app.models.phrase import Phrase


class Keyword(models.Model):
    KEYWORD_MAX_LENGTH = 128

    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=KEYWORD_MAX_LENGTH)

    def __str__(self):
        return self.keyword

