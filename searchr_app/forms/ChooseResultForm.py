from django import forms

from searchr_app.models import SearchResult


class ChooseResultForm(forms.ModelForm):
    pass
    # search_results = forms.ChoiceField(
    #     help_text='Choose Search Result to compare',
    #     choices=SearchResult.objects.all(),
    #     name='Choose Search Result',
    # )
