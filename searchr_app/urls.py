from django.urls import path
from django.conf.urls import url
from searchr_app import views


app_name = 'searchr_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('phrase/<slug:phrase_name_slug>/', views.show_phrase, name='show_phrase'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('keyword/<slug:keyword_name_slug>', views.ShowKeywordView.as_view(), name='show_keyword'),
    path('add_keyword/', views.AddKeywordView.as_view(), name='add_keyword'),
    path('goto/', views.GoToUrlView.as_view(), name='goto_url'),
]

