from django import forms
from django.contrib.auth.models import User

from searchr_app.models import Project, Phrase


class ProjectForm(forms.ModelForm):

    title = forms.CharField(
        max_length=Project.PROJECT_TITLE_LENGTH,
        help_text='Enter title',
    )
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=User.objects.all(),
    )
    description = forms.Textarea(
        attrs={'input_type': 'textarea',}
    )
    is_private = forms.NullBooleanField(
        label='Is project private?',
        initial=True,
    )
    phrases = forms.ModelMultipleChoiceField(
        queryset=Phrase.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        validators=[],
    )

    class Meta:
        model = Project
        exclude = ['slug']
