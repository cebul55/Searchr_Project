from django.shortcuts import render
from django.views import View


class AddPhraseView(View):
    def get(self, request):
        return render(request, 'searchr_app/add_phrase.html', {})