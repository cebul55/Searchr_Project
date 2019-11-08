from django.contrib import admin

from searchr_app.forms import ProjectForm
from searchr_app.models import Project, Search, SearchHistory, AnalisysOutcome
from .models import Keyword, SearchResult, Phrase


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_private', 'slug')
    # add_form_template = ProjectForm


class SearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'attributes', 'query', 'search_engine', 'date_created')


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('value', 'date_created', 'date_last_searched', 'language')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'language', 'primary_form',)


class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'date_found', 'accuracy')


class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('search', 'username', 'date_searched', 'query_value', 'number_of_results',)


class AnalisysOutcomeAdmin(admin.ModelAdmin):
    list_display = ('search_result', 'exact_match', 'website_part')


"""
Admin Registration
"""
admin.site.register(Project, ProjectAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(SearchResult, SearchResultAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
admin.site.register(AnalisysOutcome, AnalisysOutcomeAdmin)
