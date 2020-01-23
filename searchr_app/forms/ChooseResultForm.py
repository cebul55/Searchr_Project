from django import forms

from searchr_app.models import SearchResult


class ChooseResultForm(forms.Form):

    search_results = forms.ModelChoiceField(
        help_text='Choose Search Result to compare',
        queryset=SearchResult.objects.all(),
        label='Choose Search Result to compare',
    )

    def __init__(self, *args, **kwargs):
        searchid = kwargs.pop('searchid', None)
        current_search_id = kwargs.pop('current_res_id', None)
        super(ChooseResultForm, self).__init__(*args, **kwargs)

        if searchid:
            self.fields['search_results'].queryset = SearchResult.objects.filter(search_id=searchid, status__in=[SearchResult._FINISHED, SearchResult._FINISHED_ANALYZED])
            if current_search_id:
                queryset = SearchResult.objects.filter(search_id=searchid,status__in=[SearchResult._FINISHED,SearchResult._FINISHED_ANALYZED]).exclude(id=current_search_id)
                self.fields['search_results'].queryset = queryset
