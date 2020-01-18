import json

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from searchr_app.models import Project, Search, Phrase, SearchResult


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
        # print(search.phrases_list)
        tags_weight = json.loads(project.tag_weights)

        if search:
            phrases = json.decoder.JSONDecoder().decode(search.phrases_list)

        # get phrases objects defined in project/search
        phrases_list = []
        phrases_list_project = project.phrase_set.all()
        for phrase_str in phrases:
            phrase = phrases_list_project.filter(value=phrase_str)[0]
            if phrase:
                phrases_list.append(phrase)

        # print(phrases_list)

        context_dict['phrases'] = phrases_list
        context_dict['tags'] = tags_weight
        context_dict['attributes'] = json.loads(search.attributes.replace('\"', ' ').replace('\'', '\"'))

        try:
            search_results = SearchResult.objects.filter(search=search)
            search_results = search_results.order_by('-date_found')

            context_dict['search_results'] = search_results

        except SearchResult.DoesNotExist:
            context_dict['search_results'] = None

        return render(request, 'searchr_app/show_search.html', context_dict)
