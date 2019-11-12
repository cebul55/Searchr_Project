from django import forms
from django.conf.global_settings import LANGUAGES

from searchr_app.models import Phrase


class PhraseForm(forms.ModelForm):

    value = forms.CharField(
        max_length=Phrase._PHRASE_MAX_LENGTH,
        required=True,
        widget=forms.Textarea(),
    )
    date_last_searched = forms.DateField(
        widget=forms.HiddenInput(),
        required=False,

    )
    date_created = forms.DateField(
        widget=forms.HiddenInput(),
        required=False,

    )
    number_of_searches = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
        initial=int(0),
    )
    language = forms.ChoiceField(
        choices=LANGUAGES,
    )
    searches = forms.MultipleChoiceField(
        widget=forms.HiddenInput(),
        required = False,
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required = False,
    )

    class Meta:
        model = Phrase
        exclude = ['slug']