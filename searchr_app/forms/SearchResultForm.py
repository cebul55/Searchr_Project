from django import forms

from searchr_app.models import SearchResult


class SearchResultForm(forms.ModelForm):

    title = forms.CharField(
        max_length=SearchResult.SEARCH_RESULT_NAME_MAX_LEN,
    )
    url = forms.URLField(
        widget=forms.URLInput(),
    )
    html_file = forms.TextInput(
    )
    date_found = forms.DateTimeField(
        widget=forms.DateTimeInput()
    )
    accuracy = forms.CharField(
        max_length=16,
    )

    class Meta:
        model = SearchResult
        exclude = ['search_result_hash', ]
