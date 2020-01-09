import itertools
from bs4 import BeautifulSoup

from searchr_app.file_analyzer.HTMLFileAnalyzer import HTMLFileAnalyzer
from searchr_app.file_analyzer.TextFileAnalyzer import TextFileAnalyzer


class FileAnalyzer(object):
    search_result = None
    search_phrases_combination = None
    html_doc = None
    text_doc = None
    accuracy = 0.0

    def __init__(self, search_result):
        self.search_result = search_result
        phrases_list = str(search_result.search.phrases_list)
        self.search_phrases_combination = self.generate_phrase_combinations_as_text(phrases_list)
        if 'pdf' in search_result.content_type or 'word' in search_result.content_type:
            self.text_doc = search_result.html_file
        elif search_result.html_file is not None:
            self.html_doc = search_result.html_file
        self.start_analyzing()

    # def __init__(self, search_result, phrases_combitation=None, html_doc=None, text_doc=None):
    #     if phrases_combitation is None:
    #         self.search_result = search_result
    #         phrases_list = str(search_result.search.phrases_list)
    #         self.search_phrases_combination = self.generate_phrase_combinations_as_text(phrases_list)
    #         if 'pdf' in search_result.content_type or 'word' in search_result.content_type:
    #             self.text_doc = search_result.html_file
    #         elif search_result.html_file is not None:
    #             self.html_doc = search_result.html_file
    #         self.start_analyzing()
    #     else:
    #         self.search_result = search_result
    #         self.search_phrases_combination = phrases_combitation
    #         self.html_doc = html_doc
    #         self.text_doc = text_doc

    def start_analyzing(self):
        if self.text_doc is not None:
            print('startin doc analisys')
            self.analyze_text()
        elif self.html_doc is not None:
            self.analyze_html()
        # set status to 'analyzed' after end of analisys
        # self.search_result.set_status_to_analyzed()

    def generate_phrase_combinations_as_text(self, phrases_list):
        phrases_list = self.convert_literal_list_to_list(phrases_list)
        combinations = []
        for L in range(1, len(phrases_list) + 1):
            for subset in itertools.combinations(phrases_list, L):
                combinations.append(subset)

        return combinations

    @staticmethod
    def convert_literal_list_to_list(literal_list):
        import ast
        x = u'' + literal_list
        x = ast.literal_eval(x)
        return_list = x
        return_list = [n.strip() for n in return_list]
        return return_list

    def analyze_text(self):
        print('startin doc analisys')
        text_analyzer = TextFileAnalyzer(self.search_result, self.search_phrases_combination, self.text_doc)
        text_analyzer.analyze_text_file()
        self.accuracy = text_analyzer.count_result_accuracy()
        pass

    def analyze_html(self):
        html_analyzer = HTMLFileAnalyzer(self.search_result, self.search_phrases_combination, self.html_doc)
        html_analyzer.analyze_html_file()
        self.accuracy = html_analyzer.count_result_accuracy()

    def get_accuracy(self):
        return self.accuracy
