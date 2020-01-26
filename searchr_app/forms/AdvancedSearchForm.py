from django import forms
from django.conf.global_settings import LANGUAGES
from django.core.exceptions import ValidationError

from searchr_app.models import Search, Project, Phrase

"""
    Bing languages codes = https://docs.microsoft.com/pl-pl/rest/api/cognitiveservices-bingsearch/bing-web-api-v7-reference#bing-supported-languages
"""
_Arabic = 'ar'
_Basque = 'eu'
_Bengali = 'bn'
_Bulgarian = 'bg'
_Catalan = 'ca'
_Chinese_Simplified = 'zh-hans'
_Chinese_Traditional = 'zh-hant'
_Croatian = 'hr'
_Czech = 'cs'
_Danish = 'da'
_Dutch = 'nl'
_English = 'en'
_English_United_Kingdom = 'en-gb'
_Estonian = 'et'
_Finnish = 'fi'
_French = 'fr'
_Galician = 'gl'
_German = 'de'
_Gujarati = 'gu'
_Hebrew = 'he'
_Hindi = 'hi'
_Hungarian = 'hu'
_Icelandic = 'is'
_Italian = 'it'
_Japanese = 'jp'
_Kannada = 'k'
_Korean = 'ko'
_Latvian = 'lv'
_Lithuanian = 'lt'
_Malay = 'ms'
_Malayalam = 'ml'
_Marathi = 'mr'
_Norwegian = 'nb'
_Polish = 'pl'
_Portuguese_Brazil = 'pt-br'
_Portuguese_Portugal = 'pt-pt'
_Punjabi = 'pa'
_Romanian = 'ro'
_Russian = 'ru'
_Serbian_Cyrylic = 'sr'
_Slovak = 'sk'
_Slovenian = 'sl'
_Spanish = 'es'
_Swedish = 'sv'
_Tamil = 'ta'
_Telugu = 'te'
_Thai = 'th'
_Turkish = 'tr'
_Ukrainian = 'uk'
_Vietnamese = 'vi'

BING_LANGUAGE_CHOICES = [
    (_Arabic, 'Arabic'),
    (_Basque, 'Basque'),
    (_Bengali, 'Bengali'),
    (_Bulgarian, 'Bulgarian'),
    (_Catalan, 'Catalan'),
    (_Chinese_Simplified, 'Chinese (Simplified)'),
    (_Chinese_Traditional, 'Chinese (Traditional)'),
    (_Croatian, 'Croatian'),
    (_Czech, 'Czech'),
    (_Danish, 'Danish'),
    (_Dutch, 'Dutch'),
    (_English, 'English'),
    (_English_United_Kingdom, 'English-United Kingdom	'),
    (_Estonian, 'Estonian'),
    (_Finnish, 'Finnish'),
    (_French, 'French'),
    (_Galician, 'Galician'),
    (_German, 'German'),
    (_Gujarati, 'Gujarati'),
    (_Hebrew, 'Hebrew'),
    (_Hindi, 'Hindi'),
    (_Hungarian, 'Hungarian'),
    (_Icelandic, 'Icelandic'),
    (_Italian, 'Italian'),
    (_Japanese, 'Japanese'),
    (_Kannada, 'Kannada'),
    (_Korean, 'Korean'),
    (_Latvian, 'Latvian'),
    (_Lithuanian, 'Lithuanian'),
    (_Malay, 'Malay'),
    (_Malayalam, 'Malayalam'),
    (_Marathi, 'Marathi'),
    (_Norwegian, 'Norwegian'),
    (_Polish, 'Polish'),
    (_Portuguese_Brazil, 'Portuguese (Brazil)​'),
    (_Portuguese_Portugal, 'Portuguese (Portugal)​'),
    (_Punjabi, 'Punjabi'),
    (_Romanian, 'Romanian'),
    (_Russian, 'Russian'),
    (_Serbian_Cyrylic, 'Serbian (Cyrylic)'),
    (_Slovak, 'Slovak'),
    (_Slovenian, 'Slovenian'),
    (_Spanish, 'Spanish'),
    (_Swedish, 'Swedish'),
    (_Tamil, 'Tamil'),
    (_Telugu, 'Telegu'),
    (_Thai, 'Thai'),
    (_Turkish, 'Turkish'),
    (_Ukrainian, 'Ukrainian'),
    (_Vietnamese, 'Vietnamese'),
]


class AdvancedSearchForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Title'}),
        max_length=Search.SEARCH_TITLE_LENGTH,
        required=True,
    )

    project = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=Project.objects.all(),
        empty_label=None,
    )

    search_engine = forms.ChoiceField(
        choices=Search.SEARCH_ENGINE_CHOICES,
        initial=Search._BING,
        required=True,
    )

    number_of_results = forms.IntegerField(
        widget=forms.NumberInput(),
        min_value=1,
        max_value=50,
        initial=int(10),
        help_text='Between 1 and 50.',
        required=True,
    )

    offset = forms.IntegerField(
        widget=forms.NumberInput(),
        min_value=0,
        initial=int(0),
        help_text='Offsets - tells to search engine how many results must be skipped.',
        required=True,
    )

    language = forms.ChoiceField(
        choices=BING_LANGUAGE_CHOICES,
        initial='en',
        help_text='Language in which results will be searched.',
        required=True,
    )

    choose_phrases = forms.ModelMultipleChoiceField(
        queryset=Phrase.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        help_text='Choose phrases that will be searched.',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid', None)
        projectid = kwargs.pop('projectid', None)
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        if userid:
            self.fields['project'].queryset = Project.objects.filter(user_id=userid)

        if projectid:
            project = Project.objects.get(id=projectid)
            self.fields['choose_phrases'].queryset = Phrase.objects.filter(projects=project)

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > Search.SEARCH_TITLE_LENGTH:
            raise ValidationError('Title can not be longer than ' + str(Search.SEARCH_TITLE_LENGTH) + ' characters.')
        return title

