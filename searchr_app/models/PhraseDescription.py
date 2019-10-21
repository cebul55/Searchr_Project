from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class PhraseDescription(models.Model):
    _PHRASE_PRIVATE_FIELD_NAME = 'Is Phrase private?'
    _PHRASE_MAX_LENGTH = 1024

    phrase_value = models.CharField(max_length=_PHRASE_MAX_LENGTH,)
    is_private = models.BooleanField(verbose_name=_PHRASE_PRIVATE_FIELD_NAME, default=False)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()
    number_of_searches = models.PositiveIntegerField(default=0)
    user_id = models.ForeignKey(
            User, on_delete=models.CASCADE
        )

    def save(self, *args, **kwargs):
        """ On save update timestamps """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        super(PhraseDescription, self).save(*args, **kwargs)