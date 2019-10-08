from django.contrib import admin

from .models import Keyword, SearchResult


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'date_last_searched')


class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'search_result_title', 'url', 'views')


# Register your models here.
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(SearchResult, SearchResultAdmin)