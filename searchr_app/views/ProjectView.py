import json

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from searchr_app.models import Project, Search


class ProjectView(View):

    def get(self, request, username, slug):
        context_dict = {}
        # get user by username
        user = User.objects.filter(username=username)[0]
        # get project by slug and username
        project = Project.objects.filter(user=user, slug=slug)[0]

        context_dict['project'] = project

        tags_weight = json.loads(project.tag_weights)
        searches = []
        if project:
            searches_query_set = Search.objects.filter(project=project)
            searches = searches_query_set.all()

        context_dict['searches'] = searches
        context_dict['tags'] = tags_weight
        return render(request, 'searchr_app/project.html', context_dict)