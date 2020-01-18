from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from searchr_app.models import Keyword, SearchResult, Project, Search


class HomeView(View):

    def get(self, request):
        user = None
        username = None
        private_project_list = []
        public_project_list = []
        if request.user.is_authenticated:
            user = request.user
            username = user.username
            private_project_list = Project.objects.filter(user=user)
            private_project_list = private_project_list.order_by('title')

            # get 10 recently created searches
            created_searches = Search.objects.none()
            for project in private_project_list:
                searches_queryset = project.search_set.get_queryset()
                created_searches = created_searches | searches_queryset

            recently_created = created_searches.order_by('-date_created')[:10]

            # get 10 recently analyzed results where owner is user
            results = SearchResult.objects.filter(search__project__user=user, status='finished_analyzed')
            results = results.order_by('-date_found')[:10]

        else:
            recently_created = []
            results = []

        public_project_list = Project.objects.filter(is_private=False)
        public_project_list = public_project_list.order_by('title')

        context_dict = {}
        context_dict['public_project_list'] = public_project_list
        context_dict['private_project_list'] = private_project_list
        context_dict['searches'] = recently_created
        context_dict['results'] = results
        context_dict['username'] = username
        context_dict['user'] = user

        return render(request, 'searchr_app/home.html', context_dict)
