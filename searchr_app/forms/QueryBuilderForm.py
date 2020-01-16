from django import forms
from django.views import View


class QueryBuilderForm(forms.Form):
    first_phrase = forms.CharField(disabled=True)

    _AND = '&&'
    _OR = '||'
    LOGIC_CHOICES = [
        (_AND, 'AND'),
        (_OR, 'OR')
    ]

    def __init__(self, *args, **kwargs):
        phrases_list = kwargs.pop('phrases_list', None)
        super().__init__(*args, **kwargs)

        if phrases_list:
            self.fields['first_phrase'].initial = phrases_list[0]
            for i in range(1, len(phrases_list)):
                connective_name = 'connective_%s' % (i,)
                self.fields[connective_name] = forms.ChoiceField(choices=self.LOGIC_CHOICES, required=True,)
                field_name = 'phrase_%s' % (i,)
                self.fields[field_name] = forms.CharField(disabled=True, initial=phrases_list[i])
