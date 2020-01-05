from django import forms
from django.conf.global_settings import LANGUAGES

from searchr_app.models import Search, Project, Phrase


class AdvancedSearchForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Title'}),
        required=True,
    )

    project = forms.ChoiceField(
        choices=[],
    )

    search_engine = forms.ChoiceField(
        choices=Search.SEARCH_ENGINE_CHOICES,
    )

    number_of_results = forms.IntegerField(
        widget=forms.NumberInput(),
        min_value=0,
        max_value=50,
        initial=int(10),
    )

    language = forms.ChoiceField(
        choices=LANGUAGES,
    )

    choose_phrases = forms.ChoiceField(
    )

    # todo  adding new phrase inside search form
    add_phrase = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add new search phrase'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid', None)
        projectid = kwargs.pop('projectid', None)
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        if userid:
            project_choices = Project.objects.filter(user_id=userid)
            self.fields['project'].choices = [(choice.pk, choice) for choice in project_choices]

        if projectid:
            project = Project.objects.get(id=projectid)
            phrase_choices = Phrase.objects.filter(projects=project)
            self.fields['choose_phrases'].choices = [(choice.pk, choice) for choice in phrase_choices]
