from django.db import IntegrityError
from django.test import TestCase

from searchr_app.models import SearchResult, Phrase, Keyword
from searchr_app.models.AnalisysOutcome import AnalisysOutcome


class AnalisysOutcomeTest(TestCase):
    str_fragment = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

    def test_str_returns_text_fragment(self):
        analisys_outcome = AnalisysOutcome(text_fragment=self.str_fragment)
        self.assertEqual(str(analisys_outcome), self.str_fragment)

    def test_analisys_outcome_empty_object_is_not_saved(self):
        analisys_outcome = AnalisysOutcome(text_fragment=self.str_fragment)
        try:
            analisys_outcome.save()
            self.fail('Empty analisys outcome was saved')
        except IntegrityError:
            pass

    def test_verbose_name_plural(self):
        self.assertEqual(str(AnalisysOutcome._meta.verbose_name_plural), 'analisys outcomes')


# todo more models tests !