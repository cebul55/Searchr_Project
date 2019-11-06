from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.test import TestCase
from django.utils import timezone

from searchr_app.models import Search, Project


class SearchTest(TestCase):

    def setUp(self) -> None:
        self.user = User(username='username')
        self.user.save()

    def try_save(self, search):
        try:
            with transaction.atomic():
                search.save()
            self.fail('Search cannot be saved without mandatory fields')
        except IntegrityError:
            pass

    def test_search_create(self):
        str_search_title = 'Title'
        search = Search(title=str_search_title)
        self.assertEqual(str(search), str_search_title)

    def test_search_verbose_plural(self):
        self.assertEqual(str(Search._meta.verbose_name_plural), 'searches')

    def test_save_mandatory_fields(self):
        str_val = 'Title'
        search = Search()
        # try save empty search
        self.try_save(search)

        # try save search with title
        search.title = str_val
        self.try_save(search)

        # try save search with title, project
        project = Project(title='Proj', user=self.user)
        project.save()
        search.project = project
        self.try_save(search)

        # try save search with title, project, query
        search.query = 'QUERY'

        # save after adding last mandatory field
        # that is success
        search.save()

    def test_two_projects_cant_have_same_title_project(self):
        str_project_title = 'Project'
        project = Project(title=str_project_title, user=self.user)
        project.save()

        s1 = Search(title=str_project_title, project=project, query='')
        s1.save()
        s2 = Search(title=str_project_title, project=project, query='')
        try:
            s2.validate_unique()
            s2.save()
            self.fail('Two searches in project cant have same title')
        except IntegrityError:
            pass
        except ValidationError:
            pass

    def test_date_created_not_empty_after_save(self):
        str_project_title = 'Project'
        project = Project(title=str_project_title, user=self.user)
        project.save()

        s1 = Search(title=str_project_title, project=project, query='')
        s1.save()
        time_now = timezone.now()
        self.assertNotEqual(s1.date_created, None)
        self.assertAlmostEqual(s1.date_created, time_now, delta=timedelta(seconds=1))
