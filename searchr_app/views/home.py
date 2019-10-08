from django.http import HttpResponse
from django.shortcuts import render

from searchr_app.models import Keyword


def home(request):
    keyword_list = Keyword.objects.order_by('-date_last_searched')[:5]

    context_dict = {}
    context_dict['keywords'] = keyword_list

    ## todo visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']

    response = render(request, 'searchr_app/home.html', context_dict)
    return response
