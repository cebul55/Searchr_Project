from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import SearchForm
from searchr_app.models import Project


class AddSearchView(View):
    form = SearchForm

    @method_decorator(login_required)
    def get(self, request, project_id):

        project = Project.objects.get(id=project_id)
        self.form = SearchForm(userid=project.user.id, initial={
            'project': project,
        })
        return render(request, 'searchr_app/new_search.html', {
            'form':self.form,
            'project_id': project_id,
        })

    @method_decorator(login_required)
    def post(self, request, project_id):
        self.form = SearchForm(request.POST)

        if self.form.is_valid():
            search = self.form.save(commit=True)
            # get chosen phrases and update m2m relationship
            phrases = self.form.fields['phrases'].queryset
            for p in phrases:
                p.searches.add(search)
                p.save()

            project = Project.objects.filter(id=project_id)[0]
            return redirect('searchr_app:show_search',username=project.user.username, slug=project.slug, search_slug=search.slug)

        else:
            print(self.form.errors)

        return render(request, 'searchr_app/new_search.html', {
            'form':self.form,
            'project_id': project_id,
        })

