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
        widget=forms.CheckboxSelectMultiple(),
        help_text='Choose phrases that will be used to construct searches.'
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        validators=[],
    )
    title_weight = forms.IntegerField(
        label='Weight of Title Tag',
        min_value=1,
        max_value=5,
        initial=3,
        required=True,
    )
    header_weight = forms.IntegerField(
        label='Weight of Header Tag',
        min_value=1,
        max_value=5,
        initial=4,
        required=True,
    )
    footer_weight = forms.IntegerField(
        label='Weight of Footer Tag',
        min_value=1,
        max_value=5,
        initial=4,
        required=True,
    )
    main_weight = forms.IntegerField(
        label='Weight of Main Tag',
        min_value=1,
        max_value=5,
        initial=5,
        required=True,
    )
    link_weight = forms.IntegerField(
        label='Weight of Link Tag',
        min_value=1,
        max_value=5,
        initial=2,
        required=True,
    )
    meta_weight = forms.IntegerField(
        label='Weight of meta tags',
        min_value=1,
        max_value=5,
        initial=1,
        required=True,
    )
    other_weight = forms.IntegerField(
        label='Weight of other tags',
        min_value=1,
        max_value=5,
        initial=1,
        required=True,
    )

    class Meta:
        model = Project
        exclude = ['slug', 'tag_weights']


class UpdateProjectForm(ProjectForm):
    title = forms.CharField(
        max_length=Project.PROJECT_TITLE_LENGTH,
        help_text='Enter title',
        disabled=True
    )
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=User.objects.all(),
        disabled=True,
    )
    description = forms.Textarea(
        attrs={'input_type': 'textarea', }
    )
    is_private = forms.NullBooleanField(
        label='Is project private?',
        initial=True,
    )
    phrases = forms.ModelMultipleChoiceField(
        queryset=Phrase.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        help_text='Choose phrases that will be used to construct searches.'
    )
    slug = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        validators=[],
        disabled=True
    )
    title_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of Title Tag',
        min_value=0,
        max_value=5,
        initial=3,
        required=True,
        disabled=True,
    )
    header_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of Header Tag',
        min_value=0,
        max_value=5,
        initial=4,
        required=True,
        disabled=True,
    )
    footer_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of Footer Tag',
        min_value=0,
        max_value=5,
        initial=4,
        required=True,
        disabled=True,
    )
    main_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of Main Tag',
        min_value=0,
        max_value=5,
        initial=5,
        required=True,
        disabled=True,
    )
    link_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of Link Tag',
        min_value=0,
        max_value=5,
        initial=2,
        required=True,
    )
    meta_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of meta tags',
        min_value=0,
        max_value=5,
        initial=1,
        required=True,
        disabled=True,
    )
    other_weight = forms.IntegerField(
        widget=forms.HiddenInput(),
        label='Weight of other tags',
        min_value=0,
        max_value=5,
        initial=1,
        required=True,
        disabled=True,
    )

    class Meta:
        model = Project
        exclude = ['slug', 'tag_weights']

