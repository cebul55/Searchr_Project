from django.shortcuts import render
from django.views import View

from searchr_app.bing_search import run_query
from searchr_app.models import SearchResult, Keyword


class ShowKeywordView(View):
    def add_or_update_search_results(self, query_result, keyword):
        # function that adds new search results to keyword or updates date last searched
        for i in range(0, 4):
            result = query_result[i]
            search_result = SearchResult.objects.get_or_create(keyword=keyword, search_result_title=result['title'],url=result['link'])
            # search_result.save()

    def get(self, request, keyword_language, keyword_slug):
        context_dict = {}
        query = []

        try:
            keyword = Keyword.objects.get(slug=keyword_slug, language=keyword_language)

            # search_res = SearchResult.objects.filter(keyword=keyword).order_by('-views')
            # todo change search results ...
            search_res = SearchResult.objects.all()

            context_dict['keyword'] = keyword
            context_dict['search_res'] = search_res

        except Keyword.DoesNotExist:
            context_dict['keyword'] = None
            context_dict['search_res'] = None

        return render(request, 'searchr_app/keyword.html', context_dict)

    def post(self, request, keyword_language, keyword_slug):
        context_dict = {}
        query = []

        try:
            keyword = Keyword.objects.get(slug=keyword_slug, language=keyword_language)

            keyword.update_date_last_searched()
            query = keyword.keyword

            query_result_list = run_query(query)
            self.add_or_update_search_results(query_result_list, keyword)

            # search_res = SearchResult.objects.filter(keyword=keyword).order_by('-views')
            # todo change search results ...
            search_res = SearchResult.objects.all()

            context_dict['keyword'] = keyword
            context_dict['search_res'] = search_res

        except Keyword.DoesNotExist:
            context_dict['keyword'] = None
            context_dict['search_res'] = None

        return render(request, 'searchr_app/keyword.html', context_dict)

# todo change displaying searh results to phrasees.
# todo remove saerch button ..., keyword view should be read-only