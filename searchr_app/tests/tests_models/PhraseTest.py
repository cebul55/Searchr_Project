from django.test import TestCase

from searchr_app.models.Phrase import Phrase


class PhraseTest(TestCase):
    pass

    def test_string_representation(self):
        str_value = 'Phrase value'
        phrase = Phrase(phrase_value=str_value)
        self.assertEqual(str(phrase), str_value)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Phrase._meta.verbose_name_plural), 'phrases')

    def test_dates_empty_before_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(phrase_value=str_value)
        self.assertEqual(phrase.date_created, None)
        self.assertEqual(phrase.date_modified, None)

    def test_date_created_modified_equal_after_first_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(phrase_value=str_value)
        phrase.save()
        self.assertEqual(phrase.date_created, phrase.date_modified, 'Dates aren\'t equal')

    def test_dates_arent_equal_after_second_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(phrase_value=str_value)
        phrase.save()
        phrase.save()
        self.assertNotEqual(phrase.date_created, phrase.date_modified, 'Dates are equal after second save')