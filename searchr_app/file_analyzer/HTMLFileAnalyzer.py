import json

from searchr_app.file_analyzer import FileAnalyzer
from bs4 import BeautifulSoup

from searchr_app.models import AnalisysOutcome, AnalisysOutcomePhraseValues


class HTMLFileAnalyzer(object):
    list_of_outcomes = []
    search_result = None
    search_phrases_combinations = None
    html_doc = None
    soup_obj = None
    _SEARCH_TAG_LIST = ['q', 'code', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'dl', 'pre', 'span', 'table']
    _META_TAG_LIST = ['base', 'link', 'meta', 'style']

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
            self.find_in_main(combination)
            self.find_in_footer(combination)
            self.find_in_link(combination)
            self.find_in_head(combination)
            # todo find for occurences in other elements...

            # accuracy = self.count_result_accuracy()
            # print(accuracy)
            # self.search_result.accuracy = accuracy
            # self.search_result.save()

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
            # q, code, p, h1...h6, blockquote, dl, pre, span, table
            tag_list = soup_header.find_all(self._SEARCH_TAG_LIST)
            for tag in tag_list:
                if all(phrase.lower() in str(tag).lower() for phrase in phrases_combination):
                    if tag.parent.name.lower() != 'a':
                        outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Header')
                        self.list_of_outcomes.append(outcome)

    def find_in_main(self, phrases_combination):
        main_list = self.soup_obj.find_all('main')
        # if main element does not exist try to find next element between </header>...<<footer> elements
        if len(main_list) == 0:
            body_tag = self.soup_obj.find('body')
            body_soup = BeautifulSoup(str(body_tag), 'html.parser')
            try:
                for child in body_soup.children:
                    soup_child = BeautifulSoup(str(child), 'html.parser')
                    if str(child.name).lower() != 'header' and str(child.name).lower() != 'footer':
                        tag_list = soup_child.find_all(self._SEARCH_TAG_LIST)
                        for tag in tag_list:
                            if all(phrase.lower() in str(tag).lower() for phrase in phrases_combination):
                                if tag.parent.name.lower() != 'a' and tag.name.lower != 'a':
                                    outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Main')
                                    self.list_of_outcomes.append(outcome)
            except AttributeError:
                if all(phrase.lower() in str(body_tag).lower() for phrase in phrases_combination):
                    outcome = self.create_outcome(phrases_combination, body_tag.prettify(), False, 'Main')
                    self.list_of_outcomes.append(outcome)
        else:
        # main element exist in html file
            for main in main_list:
                soup_main = BeautifulSoup(str(main), 'html.parser')
                # search in visible elements placed in main:
                # q, code, p, h1...h6, blockquote, dl, pre, span, table
                tag_list = soup_main.find_all(self._SEARCH_TAG_LIST)
                for tag in tag_list:
                    if all(phrase.lower() in str(tag).lower() for phrase in phrases_combination):
                        if tag.parent.name.lower() != 'a' and tag.name.lower != 'a':
                            outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Main')
                            self.list_of_outcomes.append(outcome)

    def find_in_footer(self, phrases_combination):
        footer_list = self.soup_obj.find_all('footer')
        for footer in footer_list:
            soup_footer = BeautifulSoup(str(footer), 'html.parser')
            # search in visible elements placed in footer:
            # q, code, p, h1...h6, blockquote, dl, pre, span, table
            tag_list = soup_footer.find_all(self._SEARCH_TAG_LIST)
            for tag in tag_list:
                if all(phrase.lower() in str(tag).lower() for phrase in phrases_combination):
                    if tag.parent.name.lower() != 'a':
                        outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Footer')
                        self.list_of_outcomes.append(outcome)

    def find_in_link(self, phrases_combination):
        link_list = self.soup_obj.find_all('a')
        for link in link_list:
            if all(phrase.lower() in str(link).lower() for phrase in phrases_combination):
                try:
                    # try to find link's parent
                    tag = link.parent
                    outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Link')
                    self.list_of_outcomes.append(outcome)
                except TypeError:
                    outcome = self.create_outcome(phrases_combination, link.prettify(), False, 'Link')
                    self.list_of_outcomes.append(outcome)

    def find_in_head(self, phrases_combination):
        head_list = self.soup_obj.find_all('head')
        for head in head_list:
            soup_head = BeautifulSoup(str(head), 'html.parser')
            tag_list = soup_head.find_all(self._META_TAG_LIST)
            for tag in tag_list:
                if all(phrase.lower() in str(tag) for phrase in phrases_combination):
                    outcome = self.create_outcome(phrases_combination, tag.prettify(), False, 'Meta')
                    self.list_of_outcomes.append(outcome)

    def count_result_accuracy(self):
        project = self.search_result.search.project
        if project:
            tags_weight = json.loads(project.tag_weights)
            title_weight = tags_weight['Title']
            header_weight = tags_weight['Header']
            footer_weight = tags_weight['Footer']
            main_weight = tags_weight['Main']
            link_weight = tags_weight['Link']
            meta_weight = tags_weight['Meta']
            other_weight = tags_weight['Other']
        else:
            title_weight = 3
            header_weight = 4
            footer_weight = 4
            main_weight = 5
            link_weight = 2
            meta_weight = 1
            other_weight = 1
        sum_of_weights = title_weight + header_weight + footer_weight + main_weight + link_weight + meta_weight + other_weight
        sum_of_occurences = 0
        for outcome in self.list_of_outcomes:
            if outcome.website_part == 'Title':
                sum_of_occurences = sum_of_occurences + title_weight
            elif outcome.website_part =='Header':
                sum_of_occurences = sum_of_occurences + header_weight
            elif outcome.website_part == 'Footer':
                sum_of_occurences = sum_of_occurences + footer_weight
            elif outcome.website_part == 'Main':
                sum_of_occurences = sum_of_occurences + main_weight
            elif outcome.website_part == 'Link':
                sum_of_occurences = sum_of_occurences + link_weight
            elif outcome.website_part == 'Meta':
                sum_of_occurences = sum_of_occurences + meta_weight
            elif outcome.website_part == 'Other':
                sum_of_occurences = sum_of_occurences + other_weight

        return sum_of_occurences / sum_of_weights

