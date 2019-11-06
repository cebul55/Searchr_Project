from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils.text import slugify

from searchr_app.models import Project


class ProjectTest(TestCase):

    def try_save(self, project):
        try:
            with transaction.atomic():
                project.save()
            self.fail('Project cannot be saved without mandatory fields')
        except IntegrityError:
            pass
        except ValidationError:
            pass

    def test_project_create(self):
        str_project_name = 'Name'
        project = Project(title=str_project_name)
        self.assertEqual(str(project), str_project_name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Project._meta.verbose_name_plural), 'projects')

    def test_slug_added_after_save(self):
        username = 'Username'
        user = User(username=username)
        user.save()
        title = 'Very long title'
        project = Project(title=title, user=user)
        project.save()
        self.assertEqual(project.slug, slugify(title))

    def test_save_mandatory_fields(self):
        str_value = 'Title'
        project = Project()
        # try save empty project
        self.try_save(project)

        # try save project with title
        project.title = str_value
        self.try_save(project)

        # try save project with title, user
        user = User(username='username')
        user.save()
        project.user = user

        # save after adding last mandatory field
        # that is success
        project.save()

    def test_two_projects_cant_have_same_title_and_user(self):
        str_project_title = 'Title'
        username = 'Username'
        user = User(username=username)
        user.save()

        project1 = Project(title=str_project_title, user=user)
        project1.save()
        project2 = Project(title=str_project_title, user=user)
        try:
            project2.validate_unique()
            project2.save()
            self.fail('User cannot have 2 different projects with the same name')
        except IntegrityError:
            pass
        except ValidationError:
            pass

    def test_two_public_project_cannot_have_same_name(self):
        user1 = User(username='Username')
        user1.save()
        user2 = User(username='Username2')
        user2.save()

        str_project_title = 'Title'
        project1 = Project(title=str_project_title, user=user1, is_private=False)
        project1.save()
        project2 = Project(title=str_project_title, user=user2, is_private=False)
        try:
            project2.validate_unique()
            project2.save()
            self.fail('2 Public projects cannot exist with the same name')
        except ValidationError:
            pass