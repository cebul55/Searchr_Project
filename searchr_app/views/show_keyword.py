from django.shortcuts import render

from searchr_app.models import SearchResult, Keyword


def show_keyword(request, keyword_name_slug):
    context_dict = {}

    try:
        keyword = Keyword.objects.get(slug=keyword_name_slug)

        search_res = SearchResult.objects.filter(keyword=keyword)

        context_dict['keyword'] = keyword
        context_dict['search_res'] = search_res

    except Keyword.DoesNotExist:
        context_dict['keyword'] = None
        context_dict['search_res'] = None

    return render(request, 'searchr_app/keyword.html', context_dict)
