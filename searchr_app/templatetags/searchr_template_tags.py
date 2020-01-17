from django import template
# from searchr_app.models import Phrase
from django.contrib.auth.models import User

from searchr_app.models import Keyword, Project

register = template.Library()


# @register.inclusion_tag('searchr_app/phrases.html')
# def get_phrase_list(current_phrase=None):
#     return {'phrases': Phrase.objects.all(), 'current_phrase': current_phrase}


@register.inclusion_tag('searchr_app/keywords.html')
def get_keywords_list(current_keyword=None):
    return {'keywords': Keyword.objects.all(), 'current_keyword': current_keyword}


@register.inclusion_tag('searchr_app/projects.html')
def get_projects_list(current_project=None, username=None):
    user = None
    if username:
        user = User.objects.filter(username=username)[0]
    return {
        'public_projects': Project.objects.all().filter(is_private=False),
        'private_projects': Project.objects.all().filter(user=user),
        'current_project': current_project,
        'user': user,
    }
