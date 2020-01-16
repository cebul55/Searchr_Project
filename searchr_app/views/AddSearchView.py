import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from searchr_app.bing_search import create_bing_search_query
from searchr_app.forms import SearchForm, AdvancedSearchForm, PhraseForm, QueryBuilderForm
from searchr_app.models import Project, Search


class AddSearchView(View):
    form = SearchForm
    advanced_search_form = AdvancedSearchForm

    @method_decorator(login_required)
    def get(self, request, project_id):

        project = Project.objects.get(id=project_id)
        self.form = SearchForm(userid=project.user.id, projectid=project_id,
                               initial={
                                   'project': project,
                               })
        self.advanced_search_form = AdvancedSearchForm(userid=project.user.id, projectid=project_id, initial={
                                   'project': project,
                               })

        return render(request, 'searchr_app/new_search.html', {
            'form': self.form,
            'advanced_search_form': self.advanced_search_form,
            'project_id': project_id,
        })

    @method_decorator(login_required)
    def post(self, request, project_id):
        # self.advanced_search_form = AdvancedSearchForm(request.POST)

        if 'submit' in request.POST:
            project = Project.objects.get(id=project_id)
            self.advanced_search_form = AdvancedSearchForm(request.POST, userid=project.user.id, projectid=project_id, initial={'project': project,})
            # print(str(self.advanced_search_form))

            if self.advanced_search_form.is_valid():

                form_title = self.advanced_search_form.cleaned_data['title']
                form_project = self.advanced_search_form.cleaned_data['project']
                form_search_engine = self.advanced_search_form.cleaned_data['search_engine']
                form_number_res = self.advanced_search_form.cleaned_data['number_of_results']
                form_offset = self.advanced_search_form.cleaned_data['offset']
                form_lang = self.advanced_search_form.cleaned_data['language']
                form_phrases = self.advanced_search_form.cleaned_data['choose_phrases']
                try:
                    phrases_val = []
                    for p in form_phrases:
                        phrases_val.append(p.value)

                    attribs = {
                        'number_of_results': form_number_res,
                        'offset': form_offset,
                        'language': form_lang,
                        'phrases_list': json.dumps(phrases_val),
                    }

                    search = Search(title=form_title,
                                    project=form_project,
                                    search_engine=form_search_engine,
                                    phrases_list=json.dumps(phrases_val),
                                    attributes=attribs)
                    if form_search_engine == Search._BING:
                        search.query = create_bing_search_query(search=search,
                                                                phrases=form_phrases,
                                                                number_of_results=form_number_res,
                                                                offset=form_offset,
                                                                language=form_lang)
                    search.save()
                    #
                    project = Project.objects.filter(id=project_id)[0]
                    return redirect('searchr_app:query_builder', project_id = project_id, search_id = search.id )
                    # return redirect('searchr_app:show_search', username=project.user.username, slug=project.slug, search_slug=search.slug)
                except IntegrityError:
                    self.advanced_search_form.add_error('title','Key (title, project_id)=('+ form_title +', '+ str(form_project.id) +') already exists in database.')
                    print(self.advanced_search_form.errors)

            else:
                print(self.advanced_search_form.errors)

            return render(request, 'searchr_app/new_search.html', {
                'form': self.form,
                'advanced_search_form': self.advanced_search_form,
                'project_id': project_id,
            })

        elif 'submit1' in request.POST:
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
                print('???')
                print(self.form.errors)

            return render(request, 'searchr_app/new_search.html', {
                'form': self.form,
                'project_id': project_id,
            })

