from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import UpdateProjectForm
from searchr_app.models import Project


class UpdateProjectView(View):
    form = UpdateProjectForm

    @method_decorator(login_required)
    def get(self, request, username, slug):
        context_dict = {}
        # get user by username
        user = User.objects.filter(username=username)[0]
        # get project by slug and username
        project = Project.objects.filter(user=user, slug=slug)[0]

        if project.user.username != username:
            return redirect('searchr_app:show_project', username=username, slug=slug)

        self.form = UpdateProjectForm(instance=project, initial={
            'phrases': project.phrase_set.all(),
        })
        context_dict['project'] = project
        context_dict['form'] = self.form

        return render(request, 'searchr_app/update_project.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username, slug):
        # get user by username
        user = User.objects.filter(username=username)[0]
        # get project by slug and username
        project = Project.objects.filter(user=user, slug=slug)[0]
        self.form = UpdateProjectForm(request.POST, instance=project)

        if self.form.is_valid():
            project = self.form.save()

            saved_phrases = project.phrase_set.all()
            # remove project from phrases
            for p in saved_phrases:
                p.projects.remove(project)

            # update phrases
            phrases = self.form.cleaned_data['phrases']
            for p in phrases:
                p.projects.add(project)
                p.save()

            project.save()

            return redirect('searchr_app:show_project', username=project.user.username, slug=project.slug)

        else:
            print(self.form.errors)

        return render(request, 'searchr_app/update_project.html', {
            'project': project,
            'form': self.form,
        })
