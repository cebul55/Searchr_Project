from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from searchr_app.models import SearchResult


class GoToUrlView(View):
    def get(self, request):
        search_result_id = request.GET.get('search_result_id')

        try:

            search_result = SearchResult.objects.get(id=search_result_id)

            search_result.views = search_result.views + 1
            search_result.save()

            return redirect(search_result.url)

        except SearchResult.DoesNotExist:
            return redirect(reverse('searchr_app:home'))

    def post(self, request):
        return redirect(reverse('searchr_app:home:index'))
