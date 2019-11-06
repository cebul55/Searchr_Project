from django.test import TestCase
from django.urls import reverse


class AddPhraseViewTest(TestCase):
    def test_uses_add_phrase_template(self):
        response = self.client.get(reverse('searchr_app:add_phrase'))
        self.assertTemplateUsed(response, 'searchr_app/add_phrase.html')