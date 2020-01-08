from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.models import Project


class MyProjectsView(View):

    @method_decorator(login_required)
    def get(self, request, username):
        context_dict = {}
        try:
            # obtain user by username
            user = User.objects.get(username=username)
            # get user's projects
            projects = Project.objects.filter(user=user)

            context_dict['user'] = user
            context_dict['projects'] = projects
        except User.DoesNotExist or Project.DoesNotExist:
            context_dict['user'] = None
            context_dict['projects'] = None

        return render(request, 'searchr_app/my_projects.html', context_dict)
