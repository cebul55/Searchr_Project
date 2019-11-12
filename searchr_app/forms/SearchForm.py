from django import forms

from searchr_app.models import Search, Project, Phrase


class SearchForm(forms.ModelForm):

    title = forms.CharField(
        max_length=Search.SEARCH_TITLE_LENGTH,
        help_text='Enter title',
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
    )
    attributes = forms.CharField(
        max_length=Search.SEARCH_ATTRIBS_LENGTH,
    )
    search_engine = forms.ChoiceField(
        choices=Search.SEARCH_ENGINE_CHOICES,
    )
    phrases = forms.ModelMultipleChoiceField(
        queryset=Phrase.objects.all(),
    )
    query = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    date_created = forms.DateTimeField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Search
        exclude = ['slug']

        # todo filtering projects by user
        # todo proper adding of phrases !