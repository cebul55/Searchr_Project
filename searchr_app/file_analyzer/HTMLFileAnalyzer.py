from searchr_app.file_analyzer import FileAnalyzer
from bs4 import BeautifulSoup

from searchr_app.models import AnalisysOutcome


class HTMLFileAnalyzer(object):
    list_of_outcomes = []
    search_result = None
    search_phrases_combination = None
    html_doc = None

    def __init__(self, search_result, search_phrases_combitation, html_doc):
        self.search_result = search_result
        self.search_phrases_combination = search_phrases_combitation
        self.html_doc = html_doc

    def analyze_html_file(self):
        if self.html_doc is None:
            return
        outcome = AnalisysOutcome(text_fragment=self.search_phrases_combination, exact_match=False, search_result=self.search_result)
        outcome.save()
