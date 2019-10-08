# from django.shortcuts import render
#
# from searchr_app.models import Phrase, Keyword
#
#
# def show_phrase(request, phrase_name_slug):
#     context_dict = {}
#
#     try:
#         phrase = Phrase.objects.get(slug=phrase_name_slug)
#
#         keywords = Keyword.objects.filter(phrase=phrase)
#
#         context_dict['phrase'] = phrase
#         context_dict['keywords'] = keywords
#
#     except Phrase.DoesNotExist:
#         context_dict['phrase'] = None
#         context_dict['keywords'] = None
#
#     return render(request, 'searchr_app/phrase.html', context_dict)
