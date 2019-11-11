from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import ProjectForm


class AddProjectView(View):
    form = ProjectForm

    @method_decorator(login_required)
    def get(self, request):

        return render(request, 'searchr_app/add_project.html', {
            'form': self.form,
        })

    @method_decorator(login_required)
    def post(self, request):
        self.form = ProjectForm(request.POST)

        if self.form.is_valid():
            project = self.form.save(commit=True)
            return redirect('searchr_app:show_project', username=project.user.username, slug=project.slug)
            # return redirect('searchr_app:home')
        else:
            print(self.form.errors)

        return render(request, 'searchr_app/add_project.html',
                      {
                          'form': self.form,
                      })

# todo delete project
# todo edit project
# todo choosing user disabled, user should be assigned automatically