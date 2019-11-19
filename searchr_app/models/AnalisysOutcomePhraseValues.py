from django.db import models

from searchr_app.models import AnalisysOutcome


class AnalisysOutcomePhraseValues(models.Model):
    phrase_value = models.TextField()
    analisys_outcome = models.ForeignKey(AnalisysOutcome, on_delete=models.CASCADE, null=False)
