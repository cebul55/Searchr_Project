import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import QueryBuilderForm
from searchr_app.models import Project, Search


class QueryBuilderView(View):

    query_builder_form = QueryBuilderForm

    @method_decorator(login_required)
    def get(self, request, project_id, search_id):
        phrases_list = []

        try:
            project = Project.objects.get(id=project_id)
            search = Search.objects.get(id=search_id)
            phrases_list = search.phrases_list
            phrases_list = json.loads(phrases_list)
            self.query_builder_form = QueryBuilderForm(phrases_list=phrases_list)

        except Search.DoesNotExist:
            return redirect('searchr_app:new_search', project_id=project_id)
        except Project.DoesNotExist:
            return redirect('searchr_app:home')

        return render(request, 'searchr_app/query_builder.html', {
            'query_form': self.query_builder_form,
            'project_id': project_id,
            'search_id': search_id,
        })

    @method_decorator(login_required)
    def post(self, request, project_id, search_id):
        try:
            project = Project.objects.get(id=project_id)
            search = Search.objects.get(id=search_id)
            phrases_list = search.phrases_list
            phrases_list = json.loads(phrases_list)
            self.query_builder_form = QueryBuilderForm(phrases_list=phrases_list)
            if self.query_builder_form.is_valid():
                print('okt')

        except Search.DoesNotExist:
            return redirect('searchr_app:new_search', project_id=project_id)
        except Project.DoesNotExist:
            return redirect('searchr_app:home')

        return redirect('searchr_app:home')
        # return redirect('searchr_app:show_search', username=project.user.username, slug=project.slug, search_slug=search.slug)