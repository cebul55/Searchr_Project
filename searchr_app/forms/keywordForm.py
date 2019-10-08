from django import forms
from searchr_app.models import Keyword


class KeywordForm(forms.ModelForm):
    keyword = forms.CharField(max_length=Keyword.KEYWORD_MAX_LENGTH, help_text="Please enter the keyword name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model ( CategoryForm and Category )
        model = Keyword
        fields = ('keyword',)
