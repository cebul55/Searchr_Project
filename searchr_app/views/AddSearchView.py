import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.bing_search import create_bing_search_query
from searchr_app.forms import SearchForm, AdvancedSearchForm
from searchr_app.models import Project


class AddSearchView(View):
    form = SearchForm
    form1 = AdvancedSearchForm

    @method_decorator(login_required)
    def get(self, request, project_id):

        project = Project.objects.get(id=project_id)
        self.form = SearchForm(userid=project.user.id, projectid=project_id,
                               initial={
                                   'project': project,
                               })
        self.form1 = AdvancedSearchForm(userid=project.user.id, projectid=project_id, initial={
                                   'project': project,
                               })

        return render(request, 'searchr_app/new_search.html', {
            'form': self.form,
            'form1': self.form1,
            'project_id': project_id,
        })

    @method_decorator(login_required)
    def post(self, request, project_id):
        self.form = SearchForm(request.POST)

        if self.form.is_valid():
            search = self.form.save(commit=False)
            # todo fix + change add search view,, updating search query itp..
            # get chosen phrases and update m2m relationship
            phrases = self.form.cleaned_data['phrases']
            phrases_val = []
            for p in phrases:
                phrases_val.append(p.value)
            search.phrases_list = json.dumps(phrases_val)
            search.query = create_bing_search_query(search, phrases)
            search.save()
            #
            project = Project.objects.filter(id=project_id)[0]
            return redirect('searchr_app:show_search', username=project.user.username, slug=project.slug,
                            search_slug=search.slug)

        else:
            print(self.form.errors)

        return render(request, 'searchr_app/new_search.html', {
            'form': self.form,
            'project_id': project_id,
        })
