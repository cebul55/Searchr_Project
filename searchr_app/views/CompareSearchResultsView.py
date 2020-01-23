from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import ChooseResultForm
from searchr_app.models import SearchResult


class CompareSearchResultsView(View):

    form = ChooseResultForm

    @method_decorator(login_required)
    def get(self, request, search_res_id_1, search_res_id_2):
        context_dict = {}
        try:
            search_res_1 = SearchResult.objects.get(id=search_res_id_1)

            search_res_2 = SearchResult.objects.get(id=search_res_id_2)
            if search_res_1.search != search_res_2.search:
                return redirect('searchr_app:home_view')

            self.form = ChooseResultForm(searchid=search_res_1.search.id, current_res_id=search_res_id_1)

            context_dict['search_result_1'] = search_res_1
            context_dict['search_result_2'] = search_res_2
            context_dict['search'] = search_res_1.search
            context_dict['project'] = search_res_1.search.project
            context_dict['analysis_1'] = search_res_1.analisysoutcome_set.get_queryset()
            context_dict['analysis_2'] = search_res_2.analisysoutcome_set.get_queryset()
            context_dict['form'] = self.form

        except SearchResult.DoesNotExist:
            self.form = None
            context_dict['search_result_1'] = None
            context_dict['search_result_2'] = None
            context_dict['search'] = None
            context_dict['project'] = None
            context_dict['analysis_1'] = None
            context_dict['analysis_2'] = None
            context_dict['form'] = self.form

        return render(request, 'searchr_app/compare_search_results.html', context_dict)
