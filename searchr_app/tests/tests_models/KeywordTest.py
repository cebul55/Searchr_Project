import datetime

from django.test import TestCase
from django.utils.text import slugify
from django.utils.timezone import now

from searchr_app.models import Keyword


class KeywordTest(TestCase):

    def test_string_representation(self):
        keyword = Keyword(keyword='Keyword')
        self.assertEqual(str(keyword), keyword.keyword)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Keyword._meta.verbose_name_plural), 'keywords')

    def test_slug_is_empty_before_save(self):
        keyword_text = 'Keyword text'
        keyword = Keyword(keyword=keyword_text)
        self.assertEqual(keyword.slug, '')

    def test_date_last_searched_is_initially_empty(self):
        keyword_text = 'Keyword text'
        keyword = Keyword(keyword=keyword_text)
        self.assertEqual(keyword.date_last_searched, None)

    def test_slug_is_created_after_save(self):
        keyword_text = 'Keyword text'
        keyword_slug = slugify(keyword_text)
        keyword = Keyword(keyword=keyword_text)
        keyword.save()
        self.assertEqual(keyword.slug, keyword_slug)

    def test_date_last_searched_updates(self):
        keyword_text = 'Keyword text'
        date = now()
        keyword = Keyword(keyword=keyword_text)
        keyword.update_date_last_searched()
        # assertion ignores miliseconds
        self.assertTrue(abs(date - keyword.date_last_searched) < datetime.timedelta(seconds=1))
