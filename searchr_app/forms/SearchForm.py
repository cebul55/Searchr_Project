from django import forms

from searchr_app.models import Search, Project, Phrase


class SearchForm(forms.ModelForm):

    title = forms.CharField(
        max_length=Search.SEARCH_TITLE_LENGTH,
        help_text='Enter title',
    )
    project = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
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
        widget=forms.CheckboxSelectMultiple()
    )
    query = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    date_created = forms.DateTimeField(
        widget=forms.HiddenInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid', None)
        projectid = kwargs.pop('projectid', None)
        super(SearchForm, self).__init__(*args, **kwargs)

        if userid:
            self.fields['project'].queryset = Project.objects.filter(user_id=userid)

        if projectid:
            project = Project.objects.get(id=projectid)
            self.fields['phrases'].queryset = Phrase.objects.filter(projects=project)

    class Meta:
        model = Search
        exclude = ['slug', 'phrases_list', 'running_results']

        # todo proper adding of phrases !