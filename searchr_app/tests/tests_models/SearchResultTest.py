from django.test import TestCase

from searchr_app.models import SearchResult, Phrase
from hashlib import sha256


class SearchResultTest(TestCase):

    def test_str_returns_title(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        self.assertEqual(str(search_result), str_title)

    def test_fields_are_empty_before_save(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        self.assertEqual(search_result.search_result_hash, '','Search Result hash is not empty before save.')
        self.assertIsNone(search_result.date_found, 'Search Result date found is not empty before save.')

    def test_fields_are_not_empty_after_save(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        phrase = Phrase(phrase_value='Search Phrase')
        phrase.save()
        search_result.phrase = phrase
        search_result.save()
        self.assertIsNotNone(search_result.search_result_hash, 'Search Result hash is  empty after save.')
        self.assertIsNotNone(search_result.date_found, 'Search Result date found is empty after save.')

    def test_date_found_does_not_change(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        phrase = Phrase(phrase_value='Search Phrase')
        phrase.save()
        search_result.phrase = phrase
        search_result.save()
        date_1 = search_result.date_found

        search_result.save()
        date_2 = search_result.date_found

        self.assertEqual(date_1, date_2, 'Date was updated after save')

    def test_search_result_hash_uses_sha256(self):
        str_content = '<html><title>Test If sha256 is used?</title></html>'
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title, html_content=str_content)
        phrase = Phrase(phrase_value='Search Phrase')
        phrase.save()
        search_result.phrase = phrase
        search_result.save()
        hashed_value = sha256(str(str_content).encode('utf-8')).hexdigest()
        self.assertEqual(search_result.search_result_hash, hashed_value)
