from django.contrib import admin
from .models import Keyword, Phrase

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'phrase',)

class PhraseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('phrase_name',)}



# Register your models here.
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Phrase, PhraseAdmin)