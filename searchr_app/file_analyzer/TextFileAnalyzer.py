from searchr_app.models import AnalisysOutcome, AnalisysOutcomePhraseValues


class TextFileAnalyzer(object):
    list_of_outcomes = []
    search_result = None
    search_phrases_combinations = None
    text_doc = None
    
    def __init__(self, search_result, search_phrases_combinations, text_doc):
        self.search_result = search_result
        self.search_phrases_combinations = search_phrases_combinations
        self.text_doc = text_doc
        
    def analyze_text_file(self):
        if self.text_doc is None:
            return
        
        # search for occurances of phrase or combinations
        for combination in self.search_phrases_combinations:
            self.find_in_text(combination)

    def find_in_text(self, combination):
        if len(combination) == 1:
            # count how many times single phrase occurs in text
            flag = True
            string_text = str(self.text_doc).lower()
            for phrase in combination:
                while flag:
                    index = string_text.find(phrase)

                    if index == -1:
                        flag = False
                    else:
                        outcome_text = string_text[index-100:(index+len(phrase)+100)]
                        outcome = self.create_outcome(combination, outcome_text, False, '(1)Index: ' + str(index))
                        self.list_of_outcomes.append(outcome)
                        string_text = string_text[index+1:]

        else:
            # find occuring of more than one phrase in text
            min_pos_index = None
            max_pos_index = None
            if all(phrase.lower() in str(self.text_doc).lower() for phrase in combination):
                for phrase in combination:
                    index = str(self.text_doc).lower().find(phrase)
                    if min_pos_index is None or max_pos_index is None:
                        min_pos_index = index
                        max_pos_index = index + len(phrase)
                    else:
                        if min_pos_index > index:
                            min_pos_index = index
                        if max_pos_index < index:
                            max_pos_index = index + len(phrase)
                outcome_text = str(self.text_doc)[min_pos_index:max_pos_index]
                outcome = self.create_outcome(combination, outcome_text, False, '('+ str(len(combination)) + ')Index:' + str(min_pos_index))
                self.list_of_outcomes.append(outcome)

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

    def count_result_accuracy(self):
        return len(self.list_of_outcomes)
