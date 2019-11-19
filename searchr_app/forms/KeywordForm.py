from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from searchr_app.models import Keyword


class KeywordForm(forms.ModelForm):
    keyword = forms.CharField(max_length=Keyword.KEYWORD_MAX_LENGTH, help_text="Please enter the keyword name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False, validators=[])

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model ( KeywordForm and Keyword )
        model = Keyword
        fields = ('keyword',)

    def clean_keyword(self):
        # Custom clean_<field_name>(self) method that validates field in the form
        keyword_keyword = self.cleaned_data['keyword']
        slug = slugify(keyword_keyword)

        if Keyword.objects.filter(slug=slug).exists():
            raise ValidationError('A keyword with that title already exists.')

        return keyword_keyword
