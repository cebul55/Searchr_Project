from django import template
from searchr_app.models import Phrase

register = template.Library()

@register.inclusion_tag('searchr_app/phrases.html')
def get_phrase_list(current_phrase=None):
    return {'phrases': Phrase.objects.all(), 'current_phrase': current_phrase}

