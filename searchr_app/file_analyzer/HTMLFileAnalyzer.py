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

    def find_in_title(self, phrases_combination):
        title_list = self.soup_obj.find_all('title')
        for title in title_list:
            try:
                print(str(title) + '___' + str(phrases_combination))
            except:
                print('fail:' + str(title))
            if all(phrase.lower() in str(title).lower() for phrase in phrases_combination):
                # element was successfully found
                # based on that information analisys outcome is created
                outcome = AnalisysOutcome(text_fragment=str(title),
                                          exact_match=False,
                                          website_part='Title',
                                          search_result=self.search_result)
                outcome.save()
                # create phrase values
                phrase_values = AnalisysOutcomePhraseValues(phrase_value=str(phrases_combination), analisys_outcome=outcome)
                phrase_values.save()
                self.list_of_outcomes.append(outcome)

