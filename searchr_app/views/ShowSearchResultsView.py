from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import SearchResultForm
from searchr_app.models import SearchResult


class ShowSearchResultsView(View):
    form = SearchResultForm

    @method_decorator(login_required)
    def get(self, request, search_res_id):
        context_dict = {}
        try:
            search_result = SearchResult.objects.get(id=search_res_id)
            self.bound_search_result_to_form(search_result)

            context_dict['search_result'] = search_result
            context_dict['search'] = search_result.search
            context_dict['project'] = search_result.search.project
            context_dict['form'] = self.form
            context_dict['analisys_results'] = search_result.analisysoutcome_set.get_queryset()
            # context_dict['outcome_phrases'] = search_result.analisysoutcome_set

        except SearchResult.DoesNotExist:
            context_dict['search_result'] = None
            context_dict['search'] = None
            context_dict['project'] = None
            context_dict['form'] = self.form
            context_dict['analisys_results'] = None

        return render(request, 'searchr_app/show_search_result.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        context_dict = {}

        return render(request, 'searchr_app/show_search_result.html', context_dict)

    def bound_search_result_to_form(self, search_result):
        self.form = SearchResultForm(initial={
            'title': search_result.title,
            'url': search_result.url,
            'search_result_hash': search_result.search_result_hash,
            'html_file': search_result.html_file,
            'date_found': search_result.date_found,
            'accuracy': search_result.accuracy,
            'search': search_result.search,
        })
