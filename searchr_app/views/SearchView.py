from django.shortcuts import render
from django.views import View

from searchr_app.bing_search import run_query


class SearchView(View):

    def get(self, request):
        result_list = []
        query = []
        context_dict = {'result_list': result_list, 'query': query}

        return render(request, 'searchr_app/search.html', context_dict)

    def post(self, request):
        result_list = []
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

        context_dict = {'result_list': result_list, 'query': query}

        return render(request, 'searchr_app/search.html', context_dict)
