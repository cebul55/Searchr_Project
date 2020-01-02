from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.test import TestCase

from searchr_app.models import SearchResult, Phrase, Search
from hashlib import sha256


class SearchResultTest(TestCase):

    def setUp(self) -> None:
        self.prepared_search_result = self._create_search_result_object('username')

    def try_save(self, search_result):
        try:
            with transaction.atomic():
                search_result.save()
            self.fail('Can not sabe search result without all mandatory fields')
        except IntegrityError:
            pass
        except ValidationError:
            pass

    def _create_project_object(self, username='admin'):
        from django.contrib.auth.models import User
        user = User(username=username)
        user.save()
        from searchr_app.models import Project
        project = Project(title='Proj', user=user)
        project.save()
        return project

    def _create_search_object(self, username='admin'):
        search = Search(title='title', project=self._create_project_object(username), query='QUERY')
        search.save()
        return search

    def _create_search_result_object(self, username):
        str_content = '<html><title>Test If sha256 is used?</title></html>'
        str_title = 'Search Result Title'
        str_url = 'https://google.com'
        res = SearchResult(title=str_title, url=str_url, html_file=str_content,search=self._create_search_object(username))
        res.save()
        return res


    def test_str_returns_title(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        self.assertEqual(str(search_result), str_title)

    def test_fields_are_empty_before_save(self):
        str_title = 'Search Result Title'
        search_result = SearchResult(title=str_title)
        self.assertEqual(search_result.search_result_hash, '', 'Search Result hash is not empty before save.')
        self.assertIsNone(search_result.date_found, 'Search Result date found is not empty before save.')

    def test_fields_are_not_empty_after_save(self):
        self.assertIsNotNone(self.prepared_search_result.search_result_hash, 'Search Result hash is  empty after save.')
        self.assertIsNotNone(self.prepared_search_result.date_found, 'Search Result date found is empty after save.')

    def test_date_found_does_not_change(self):
        search_result = self._create_search_result_object('test_date_found')
        search_result.save()
        date_1 = search_result.date_found

        search_result.save()
        date_2 = search_result.date_found

        self.assertEqual(date_1, date_2, 'Date was updated after save')

    # def test_search_result_hash_uses_sha256(self):
    #     search_result = self._create_search_result_object('shaTest')
    #
    #     str_content = search_result.html_file
    #     search_result.save()
    #     hashed_value = sha256(str(str_content).encode('utf-8')).hexdigest()
    #     self.assertEqual(search_result.search_result_hash, hashed_value)

    def test_mandatory_fiedls(self):
        str_content = '<html><title>Test If sha256 is used?</title></html>'
        str_title = 'Search Result Title'
        str_url = 'https://google.com'

        search_result = SearchResult()
        # try save empty result
        self.try_save(search_result)

        # try save result with title,
        search_result.title = str_title
        self.try_save(search_result)

        # try save result with title, url
        search_result.url = str_url
        self.try_save(search_result)

        # try save with title, url, html_file
        search_result.html_file = str_content
        self.try_save(search_result)

        # try save with title, url, file, search reference
        search_result.search = self._create_search_object()

        # save after adding all required fields
        # should result in success
        search_result.save()

