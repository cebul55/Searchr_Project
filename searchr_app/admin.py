from django.contrib import admin

from .models import Keyword, SearchResult, Phrase


# class KeywordAdmin(admin.ModelAdmin):
#     list_display = ('keyword', 'date_last_searched')
#
#
# class SearchResultAdmin(admin.ModelAdmin):
#     list_display = ('phrase', 'title', 'url', 'views')
#
#
# # Register your models here.
# admin.site.register(Keyword, KeywordAdmin)
# admin.site.register(SearchResult, SearchResultAdmin)
# admin.site.register(Phrase)
