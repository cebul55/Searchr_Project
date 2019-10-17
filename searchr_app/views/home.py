from django.http import HttpResponse
from django.shortcuts import render

from searchr_app.models import Keyword, SearchResult


def home(request):
    keyword_list = Keyword.objects.exclude(date_last_searched=None)
    keyword_list = keyword_list.order_by('-date_last_searched')[:5]
    search_results_list = SearchResult.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['keywords'] = keyword_list
    context_dict['search_results'] = search_results_list

    response = render(request, 'searchr_app/home.html', context_dict)
    return response
