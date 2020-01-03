import itertools

class FileAnalyzer:
    search_result = None
    search_phrases_combination = None

    def __init__(self, search_result):
        self.search_result = search_result
        self.search_phrases_combination = self.generate_phrase_combinations_as_text(search_result.search.phrases_list)

    def start_analyzing(self):
        pass

    def generate_phrase_combinations_as_text(self, phrases_list):
        combinations = []
        for L in range(1, len(phrases_list) + 1):
            for subset in itertools.combinations(phrases_list, L):
                combinations.append(subset)

        # for combination in combinations:
        #     print(combination)
        #     for i in combination:
        #         print(i)
        return combinations
