from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from searchr_app.models import Keyword, SearchResult, Project


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

        public_project_list = Project.objects.filter(is_private=False)
        public_project_list = public_project_list.order_by('title')

        search_results_list = SearchResult.objects.order_by('-views')[:5]

        context_dict = {}
        context_dict['public_project_list'] = public_project_list
        context_dict['private_project_list'] = private_project_list
        context_dict['search_results'] = search_results_list
        context_dict['username'] = username

        return render(request, 'searchr_app/home.html', context_dict)
