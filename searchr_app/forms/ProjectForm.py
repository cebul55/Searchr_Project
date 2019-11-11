from django import forms
from django.contrib.auth.models import User

from searchr_app.models import Project


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Project.PROJECT_TITLE_LENGTH,
        help_text='Please enter title',
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
    )
    description = forms.Textarea(
        attrs={'input_type': 'textarea',}
    )
    is_private = forms.NullBooleanField(
        label='Is project private?',
        initial=True,
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        validators=[],
    )

    class Meta:
        model = Project
        exclude = ['slug']