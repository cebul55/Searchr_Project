from django.test import TestCase

from searchr_app.models.PhraseDescription import PhraseDescription


class PhraseDescriptionTest(TestCase):

    def test_string_representation(self):
        phrase = PhraseDescription(phrase_value='Phrase value')
        self.assertEqual(str(phrase), PhraseDescription.phrase_value)

    # def test_verbose_name_plural(self):
    #     self.assertEqual(str(Keyword._meta.verbose_name_plural), 'keywords')