from django.db import models

''' 
    Class AnalisysOutcome - represents fragment of a webpage, which contains fragment of searched phrase
'''
class AnalisysOutcome(models.Model):

    text_fagment = models.TextField()
    exact_match = models.BooleanField(verbose_name='Does fragment contain whole searched phrase ?', default=False)
    # var website_part 
