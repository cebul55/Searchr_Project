

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class AddKeywordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword!2')
        self.user.save()

    def test_login(self):
        self.client.login(username='john', password='johnpassword!2')
        response = self.client.get(reverse('searchr_app:add_keyword'))
        self.assertEqual(response.status_code, 200,)

    def test_response_doesnt_use_templete_if_not_logged_in(self):
        response = self.client.get(reverse('searchr_app:add_keyword'))
        self.assertTemplateNotUsed(response, 'searchr_app/add_keyword.html')

    def test_uses_add_keyword_template(self):
        self.client.login(username='john', password='johnpassword!2')
        response = self.client.get(reverse('searchr_app:add_keyword'))
        self.assertTemplateUsed(response, 'searchr_app/add_keyword.html')