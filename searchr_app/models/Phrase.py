from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from searchr_app.models import Keyword


class Phrase(models.Model):
    _PHRASE_PRIVATE_FIELD_NAME = 'Is Phrase private?'
    _PHRASE_MAX_LENGTH = 1024

    phrase_value = models.CharField(max_length=_PHRASE_MAX_LENGTH,)
    is_private = models.BooleanField(verbose_name=_PHRASE_PRIVATE_FIELD_NAME, default=False)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()
    number_of_searches = models.PositiveIntegerField(default=0)
    keywords = models.ManyToManyField(Keyword)
    user_id = models.ForeignKey(
            User, on_delete=models.CASCADE, null=True
        )

    def save(self, *args, **kwargs):
        """ On save update timestamps """
        date_saved = timezone.now()
        if not self.id:
            self.date_created = date_saved
        self.date_modified = date_saved
        super(Phrase, self).save(*args, **kwargs)

    def __str__(self):
        return self.phrase_value

    class Meta:
        verbose_name_plural = 'phrases'
