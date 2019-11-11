from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from searchr_app.models import Project, Search, Phrase


class SearchObjectView(View):

    def get(self, request, username, slug, search_slug):
        context_dict = {}
        # get user by username
        user = User.objects.filter(username=username)[0]

        # get project by slug and username
        project = Project.objects.filter(user=user, slug=slug)[0]

        # get search object by project and slug
        search = Search.objects.filter(project=project, slug=search_slug)[0]

        context_dict['search'] = search
        context_dict['project'] = project
        phrases = []
        if search:
            phrase_query_set = Phrase.objects.filter(searches=search )
            phrases = phrase_query_set.all()

        context_dict['phrases'] = phrases

        return render(request, 'searchr_app/show_search.html', context_dict)