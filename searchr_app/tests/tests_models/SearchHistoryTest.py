from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from searchr_app.models import SearchHistory, Project, Search


class SearchHistoryTest(TestCase):
    def test_str_value(self):
        user = User(username='admin')
        user.save()
        project = Project(title='Proj', user=user)
        project.save()

        search = Search(title='title', query='query')
        search.project = project
        search.save()

        history = SearchHistory()
        history.username = user.username
        date = timezone.now()
        history.date_searched = date
        history.search = search
        str_val = search.title + ',' + history.username + ',[' + search.date_created.strftime('%d/%m/%Y, %H:%M:%S') + ']'
        self.assertEqual(str(history), str_val)