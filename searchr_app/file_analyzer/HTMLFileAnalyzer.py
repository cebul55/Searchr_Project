from searchr_app.file_analyzer import FileAnalyzer
from bs4 import BeautifulSoup

from searchr_app.models import AnalisysOutcome, AnalisysOutcomePhraseValues


class HTMLFileAnalyzer(object):
    list_of_outcomes = []
    search_result = None
    search_phrases_combinations = None
    html_doc = None
    soup_obj = None

    def __init__(self, search_result, search_phrases_combitations, html_doc):
        self.search_result = search_result
        self.search_phrases_combinations = search_phrases_combitations
        self.html_doc = html_doc

    def analyze_html_file(self):
        if self.html_doc is None:
            return
        self.soup_obj = BeautifulSoup(self.html_doc, 'html.parser')

        # searching for occurance of phrase or combination of phrases
        for combination in self.search_phrases_combinations:
            self.find_in_title(combination)
            self.find_in_header(combination)

    def create_outcome(self, phrases_combination, text_fragment, exact_match, website_part):
        outcome = AnalisysOutcome(text_fragment=text_fragment,
                                  exact_match=exact_match,
                                  website_part=website_part,
                                  search_result=self.search_result)
        outcome.save()
        # create phrase values
        phrase_values = AnalisysOutcomePhraseValues(phrase_value=str(phrases_combination), analisys_outcome=outcome)
        phrase_values.save()
        return outcome

    def find_in_title(self, phrases_combination):
        title_list = self.soup_obj.find_all('title')
        for title in title_list:
            if all(phrase.lower() in str(title).lower() for phrase in phrases_combination):
                # element was successfully found
                # based on that information analisys outcome is created
                outcome = self.create_outcome(phrases_combination, title.prettify(), False, 'Title')
                self.list_of_outcomes.append(outcome)

    def find_in_header(self, phrases_combination):
        header_list = self.soup_obj.find_all('header')
        for header in header_list:
            soup_header = BeautifulSoup(str(header), 'html.parser')
            # search in visible elements placed in header:
            # q, code, p, h1...h6, blockquote, dl, pre, span
            tag_list = soup_header.find_all(['q', 'code', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'dl', 'pre', 'span'])
            for tag in tag_list:
                if all(phrase.lower() in str(tag).lower() for phrase in phrases_combination):
                    outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Header')
                    self.list_of_outcomes.append(outcome)
