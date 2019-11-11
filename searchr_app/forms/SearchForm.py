from django import forms

from searchr_app.models import Search, Project


class SearchForm(forms.ModelForm):

    def __init__(self, user):
        if user.is_authenticated:
            self.user = user

    user = None

    title = forms.CharField(
        max_length=Search.SEARCH_TITLE_LENGTH,
        help_text='Enter title'
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(user=user),
    )
    attributes = forms.CharField(
        max_length=Search.SEARCH_ATTRIBS_LENGTH,
    )
    query = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    search_engine = forms.ChoiceField(
        choices=Search.SEARCH_ENGINE_CHOICES,
    )
    date_created = forms.DateTimeField(
        widget=forms.HiddenInput(),
        required=False
    )
