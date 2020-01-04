from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.models import AnalisysOutcome, AnalisysOutcomePhraseValues


class ShowAnalisysOutcomeView(View):

    @method_decorator(login_required)
    def get(self, request, analisys_outcome_id):
        context_dict = {}
        try:
            analisys_outcome = AnalisysOutcome.objects.get(id=analisys_outcome_id)
            search_result = analisys_outcome.search_result
            search = search_result.search
            username = search.project.user.username
            is_private = search.project.is_private
            project = search.project
            try:
                phrase_values = AnalisysOutcomePhraseValues.objects.get(analisys_outcome=analisys_outcome)
            except AnalisysOutcome.DoesNotExist:
                phrase_values = ''
            context_dict['analisys_outcome'] = analisys_outcome
            context_dict['project'] = project
            context_dict['search'] = search
            context_dict['search_result'] = search_result
            context_dict['username'] = username
            context_dict['is_private'] = is_private
            context_dict['phrase_values'] = str(phrase_values)
        except AnalisysOutcome.DoesNotExist:
            context_dict['analisys_outcome'] = None
            context_dict['project'] = None
            context_dict['search'] = None
            context_dict['search_result'] = None
            context_dict['username'] = None
            context_dict['is_private'] = None
            context_dict['phrase_values'] = None

        return render(request, 'searchr_app/analisys_outcome.html', context_dict)