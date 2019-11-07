import datetime

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.test import TestCase
from django.utils.text import slugify
from django.utils.timezone import now

from searchr_app.models import Keyword


class KeywordTest(TestCase):

    def try_save(self, keyword):
        try:
            with transaction.atomic():
                keyword.save()
            self.fail('Keyword can not be saved without mandatory fields')
        except ValidationError:
            pass
        except IntegrityError:
            pass

    def test_string_representation(self):
        keyword = Keyword(keyword='Keyword')
        self.assertEqual(str(keyword), keyword.keyword)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Keyword._meta.verbose_name_plural), 'keywords')

    def test_slug_is_empty_before_save(self):
        keyword_text = 'Keyword text'
        keyword = Keyword(keyword=keyword_text)
        self.assertEqual(keyword.slug, '')

    def test_slug_is_created_after_save(self):
        keyword_text = 'Keyword text'
        keyword_slug = slugify(keyword_text)
        keyword = Keyword(keyword=keyword_text)
        keyword.save()
        self.assertEqual(keyword.slug, keyword_slug)

    def test_save_mandatory_fields(self):
        keyword = Keyword()

        # try save empty keyword
        self.try_save(keyword)

        # try save keyword with keyword
        keyword.keyword = 'KEYWORD'

        # save with all mandatory fields
        # success
        keyword.save()
