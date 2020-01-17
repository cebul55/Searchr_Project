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
            self.query_builder_form = QueryBuilderForm(request.POST, phrases_list=phrases_list)
            # print(self.query_builder_form)
            if self.query_builder_form.is_valid():
                form_query = ''
                form_first_phrase = self.query_builder_form.cleaned_data['first_phrase']
                form_query += '\"' + form_first_phrase + '\" '
                for i in range(1, len(phrases_list)):
                    connective_name = 'connective_%s' % (i,)
                    phrase_name = 'phrase_%s' % (i,)
                    form_connective = self.query_builder_form.cleaned_data[connective_name]
                    form_phrase = self.query_builder_form.cleaned_data[phrase_name]
                    form_query = form_query + form_connective + ' \"' + form_phrase + '\" '
                # print(form_query)
                # update search query
                if search.search_engine == Search._BING:
                    from searchr_app.bing_search import update_bing_search_query

                    # format text to be able to do json.loads
                    saved_query = search.query.replace('\"', ' ')
                    saved_query = saved_query.replace('\'', '\"')
                    saved_query = json.loads(saved_query)

                    # update attribures
                    attributes = json.loads(search.attributes)
                    attributes['query'] = form_query

                    # print(attributes)
                    updated_query = update_bing_search_query(saved_query, form_query)
                    search.query = updated_query
                    search.attributes = attributes
                    search.save()
                    #
                    return redirect('searchr_app:show_search', username=project.user.username, slug=project.slug, search_slug=search.slug)

        except Search.DoesNotExist:
            return redirect('searchr_app:new_search', project_id=project_id)
        except Project.DoesNotExist:
            return redirect('searchr_app:home')

        return redirect('searchr_app:home')
        # return redirect('searchr_app:show_search', username=project.user.username, slug=project.slug, search_slug=search.slug)