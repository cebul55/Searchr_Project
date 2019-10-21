from django.test import TestCase

from searchr_app.models import SearchResult


class SearchResultTest(TestCase):

    def test_str_returns_title(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        self.assertEqual(str(search_result), str_title)