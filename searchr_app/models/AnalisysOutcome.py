from django.db import models

from searchr_app.models import SearchResult, Keyword


class AnalisysOutcome(models.Model):
    """
        Class AnalisysOutcome - represents fragment of a webpage, which contains fragment of searched phrase
        Object cannot exist without relation to Search Result and to existink Keyword/s
    """

    text_fragment = models.TextField()
    exact_match = models.BooleanField(verbose_name='Does fragment contain whole searched phrase ?', default=False)
    """ website_part - variable representing part of website, where searched text was found, uses dictionary... """
    website_part = models.CharField(max_length=64, default='')
    search_result = models.ForeignKey(SearchResult, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.text_fragment

    class Meta:
        verbose_name_plural = 'analisys outcomes'