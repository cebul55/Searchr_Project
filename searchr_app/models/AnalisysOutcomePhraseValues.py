from django.db import models

from searchr_app.models import AnalisysOutcome


class AnalisysOutcomePhraseValues(models.Model):
    phrase_value = models.TextField()
    analisys_outcome = models.ForeignKey(AnalisysOutcome, on_delete=models.CASCADE, null=False)
    number_of_phrases = models.IntegerField(default=0)

    def __str__(self):
        return self.phrase_value
