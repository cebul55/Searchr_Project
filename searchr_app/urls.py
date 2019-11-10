from django.urls import path
from django.conf.urls import url
from searchr_app import views


app_name = 'searchr_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('owner/<slug:username>/project/<slug:slug>/', views.ProjectView.as_view(), name='show_project'),
    path('phrase/<slug:slug>/', views.ShowPhraseView.as_view(), name='show_phrase'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('keyword/<slug:keyword_name_slug>', views.ShowKeywordView.as_view(), name='show_keyword'),
    path('add_keyword/', views.AddKeywordView.as_view(), name='add_keyword'),
    path('add_phrase/', views.AddPhraseView.as_view(), name='add_phrase'),
    path('goto/', views.GoToUrlView.as_view(), name='goto_url'),
]

