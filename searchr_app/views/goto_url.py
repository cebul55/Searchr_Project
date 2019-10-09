from django.shortcuts import redirect
from django.urls import reverse

from searchr_app.models import SearchResult


def goto_url(request):
    # View that counts clicks on pages and redirects to coresponding page-url
    search_result_id = None

    if request.method == 'GET':
        search_result_id = request.GET.get('search_result_id')

        try:

            search_result = SearchResult.objects.get(id=search_result_id)

            search_result.views = search_result.views + 1
            search_result.save()

            return redirect(search_result.url)

        except SearchResult.DoesNotExist:
            return redirect(reverse('searchr_app:home'))

    return redirect(reverse('searchr_app:home:index'))
