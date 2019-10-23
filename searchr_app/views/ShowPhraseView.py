from django.shortcuts import render
from django.views import View

from searchr_app.models import Phrase, Keyword


class ShowPhraseView(View):
    def get(self, request, phrase_slug):
        context_dict = {}
        try:
            phrase = Phrase.objects.get(phrase_slug=phrase_slug)
            keywords = phrase.keywords.all()
            context_dict['phrase'] = phrase
            context_dict['keywords'] = keywords

        except Phrase.DoesNotExist:
            context_dict['phrase'] = None
            context_dict['keywords'] = None

        return render(request, 'searchr_app/show_phrase.html', context_dict)
