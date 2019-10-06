from django.shortcuts import render

from searchr_app.bing_search import run_query


def search(request):
    result_list = []
    query = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    context_dict = {'result_list': result_list, 'query': query}

    return render(request, 'searchr_app/search.html', context_dict)