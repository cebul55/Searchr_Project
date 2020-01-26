from django import forms
from django.conf.global_settings import LANGUAGES
from django.core.exceptions import ValidationError

from searchr_app.models import Phrase, Keyword


class PhraseForm(forms.ModelForm):
    value = forms.CharField(
        label='Phrase value',
        max_length=Phrase._PHRASE_MAX_LENGTH,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Phrase value.'}),
        help_text='Enter phrase value',
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
        initial='en',
    )
    projects = forms.MultipleChoiceField(
        widget=forms.HiddenInput(),
        required=False,
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Phrase
        exclude = ['slug']

    def clean_value(self):
        # custom clean of value field to validate if words are not longer than 512 characters
        phrase_value = self.cleaned_data['value']
        words = phrase_value.split()
        for word in words:
            if len(word) > Keyword.KEYWORD_MAX_LENGTH:
                raise ValidationError("Phrase must contain from keywords shorter than " + str(Keyword.KEYWORD_MAX_LENGTH) + ' characters.')
        return phrase_value