from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.models import SearchHistory, Search, Project


class HistoryView(View):

    @method_decorator(login_required)
    def get(self, request, username, project_slug, search_slug):
        context_dict = {}
        user = User.objects.get(username=username)
        project = Project.objects.get(slug=project_slug, user=user)
        search = Search.objects.get(slug=search_slug, project=project)

        # verify if project is private and user is the owner
        if project.is_private and project.user.username != username:
            return render(request, 'searchr_app/home.html', {})

        search_history = SearchHistory.objects.get(search=search)
        search_results = search_history.search_results.get_queryset()

        print(search_history)
        context_dict['search_results'] = search_results
        context_dict['search_history'] = search_history
        context_dict['project'] = project
        context_dict['search'] = search

        return render(request, 'searchr_app/show_history_view.html', context_dict)