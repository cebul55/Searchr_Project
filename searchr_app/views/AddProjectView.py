import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.forms import ProjectForm


def construct_json_weights(form):
    form_title = form.cleaned_data['title_weight']
    form_header = form.cleaned_data['header_weight']
    form_main = form.cleaned_data['main_weight']
    form_footer = form.cleaned_data['footer_weight']
    form_link = form.cleaned_data['link_weight']
    form_other = form.cleaned_data['other_weight']
    form_meta = form.cleaned_data['meta_weight']
    dict = {
        "Title": form_title,
        "Header": form_header,
        "Main": form_main,
        "Footer": form_footer,
        "Link": form_link,
        "Meta": form_meta,
        "Other": form_other,
    }
    # print(dict)
    return dict


class AddProjectView(View):
    form = ProjectForm

    @method_decorator(login_required)
    def get(self, request):

        current_user = request.user
        self.form = ProjectForm(initial={
            'user': current_user,
        })
        return render(request, 'searchr_app/add_project.html', {
            'form': self.form,
        })

    @method_decorator(login_required)
    def post(self, request):
        self.form = ProjectForm(request.POST)

        if self.form.is_valid():
            json_weigths = construct_json_weights(self.form)
            project = self.form.save(commit=False)
            # Read weights from form
            project.tag_weights = json.dumps(json_weigths)
            project.save()
            # get chosen phrases and update m2m relationship
            phrases = self.form.cleaned_data['phrases']
            for p in phrases:
                p.projects.add(project)
                p.save()

            project.save()

            return redirect('searchr_app:show_project', username=project.user.username, slug=project.slug)
            # return redirect('searchr_app:home')
        else:
            print(self.form.errors)

        return render(request, 'searchr_app/add_project.html',
                      {
                          'form': self.form,
                      })
