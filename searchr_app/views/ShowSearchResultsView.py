from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import SearchResultForm, ChooseResultForm
from searchr_app.models import SearchResult


class ShowSearchResultsView(View):
    form = ChooseResultForm

    @method_decorator(login_required)
    def get(self, request, search_res_id):
        context_dict = {}
        try:
            search_result = SearchResult.objects.get(id=search_res_id)
            # self.bound_search_result_to_form(search_result)

            context_dict['search_result'] = search_result
            context_dict['search'] = search_result.search
            context_dict['project'] = search_result.search.project
            # context_dict['form'] = self.form
            context_dict['analisys_results'] = search_result.analisysoutcome_set.get_queryset()
            self.form = ChooseResultForm(searchid=search_result.search.id, current_res_id=search_res_id)
            context_dict['form'] = self.form

        except SearchResult.DoesNotExist:
            context_dict['search_result'] = None
            context_dict['search'] = None
            context_dict['project'] = None
            # context_dict['form'] = self.form
            context_dict['analisys_results'] = None
            self.form = None
            context_dict['form'] = self.form

        return render(request, 'searchr_app/show_search_result.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, search_res_id):
        context_dict = {}
        if 'compare' in request.POST:
            try:
                # get search object by id
                search_res_1 = SearchResult.objects.get(id=search_res_id)
                self.form = ChooseResultForm(request.POST, searchid=search_res_1.search.id)
                if self.form.is_valid():
                    search_res_2 = self.form.cleaned_data['search_results']
                    return redirect('searchr_app:compare_results', search_res_1.id, search_res_2.id)

                else:
                    self.get(search_res_id)

            except SearchResult.DoesNotExist:
                self.get(request, search_res_id)

        else:
            return render(request, 'searchr_app/show_search_result.html', context_dict)

    # def bound_search_result_to_form(self, search_result):
    #     self.form = SearchResultForm(initial={
    #         'title': search_result.title,
    #         'url': search_result.url,
    #         'search_result_hash': search_result.search_result_hash,
    #         'html_file': search_result.html_file,
    #         'date_found': search_result.date_found,
    #         'accuracy': search_result.accuracy,
    #         'search': search_result.search,
    #     })
