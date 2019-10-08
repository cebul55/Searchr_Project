from django import template
# from searchr_app.models import Phrase
from searchr_app.models import Keyword

register = template.Library()

# @register.inclusion_tag('searchr_app/phrases.html')
# def get_phrase_list(current_phrase=None):
#     return {'phrases': Phrase.objects.all(), 'current_phrase': current_phrase}

@register.inclusion_tag('searchr_app/keywords.html')
def get_keywords_list(current_keyword=None):
    return {'keywords': Keyword.objects.all(), 'current_keyword': current_keyword}