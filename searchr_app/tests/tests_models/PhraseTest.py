from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.test import TestCase

from searchr_app.models import Phrase


class PhraseTest(TestCase):

    def try_save(self, phrase):
        try:
            with transaction.atomic():
                phrase.save()
            self.fail('Phrase cannot be saved without mandatory fields')
        except IntegrityError:
            pass
        except ValidationError:
            pass

    def test_string_representation(self):
        str_value = 'Phrase value'
        phrase = Phrase(value=str_value)
        self.assertEqual(str(phrase), str_value)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Phrase._meta.verbose_name_plural), 'phrases')

    def test_dates_empty_before_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(value=str_value)
        self.assertEqual(phrase.date_created, None)
        self.assertEqual(phrase.date_last_searched, None)

    def test_date_created_lsetsearched_equal_after_first_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(value=str_value)
        phrase.save()
        self.assertEqual(phrase.date_created, phrase.date_last_searched, 'Dates aren\'t equal')

    def test_dates_arent_equal_after_second_save(self):
        str_value = 'Phrase value'
        phrase = Phrase(value=str_value)
        phrase.save()
        phrase.save()
        self.assertNotEqual(phrase.date_created, phrase.date_last_searched, 'Dates are equal after second save')

    def test_save_mandatory_fields(self):
        str_value = 'Phrase that will be searched'
        phrase = Phrase()
        # try save empty phrase
        self.try_save(phrase)

        # try save phrase with value
        phrase.value = str_value

        # save after adding last mandatory field
        # that is success
        phrase.save()
