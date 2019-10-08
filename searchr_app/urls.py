from django.urls import path
from django.conf.urls import url
from searchr_app import views


app_name = 'searchr_app'

urlpatterns = [
    path('', views.home, name='home'),
    # path('phrase/<slug:phrase_name_slug>/', views.show_phrase, name='show_phrase'),
    path('search/', views.search, name='search'),
    path('keyword/<slug:keyword_name_slug>', views.show_keyword, name='show_keyword'),
    path('add_keyword/', views.add_keyword, name='add_keyword'),
]

