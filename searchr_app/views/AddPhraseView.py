import re
import string

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import PhraseForm
from searchr_app.models import Keyword


class AddPhraseView(View):
    form = PhraseForm

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'searchr_app/add_phrase.html', {
            'form': self.form,
        })

    @method_decorator(login_required)
    def post(self, request):
        self.form = PhraseForm(request.POST)

        if self.form.is_valid():
            try:
                phrase = self.form.save(commit=True)

            except IntegrityError:
                self.form.add_error('value', 'Phrase with selected language ('+ self.form.cleaned_data['value'] + ',' + self.form.cleaned_data['language'] + ') already exists in database.')
                print('dupa')
                print(self.form.errors)
                return render(request, 'searchr_app/add_phrase.html', {
                    'form': self.form,
                })

            # this method ignores all punctuation marks, splits string
            # and returns filtered result string
            keywords_extracted = re.sub('['+string.punctuation+']', '', phrase.value).split()

            for keyword_text in keywords_extracted:
                keyword_text = keyword_text.lower()
                keyword_tuple = Keyword.objects.get_or_create(keyword=keyword_text, language=phrase.language)
                keyword = keyword_tuple[0]
                keyword.phrases.add(phrase)
                keyword.save()

            return redirect('searchr_app:show_phrase', phrase_language=phrase.language, phrase_slug=phrase.slug)

        else:
            print(self.form.errors)

        return render(request, 'searchr_app/add_phrase.html', {
            'form': self.form,
        })