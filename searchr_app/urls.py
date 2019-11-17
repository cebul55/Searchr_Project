from django.urls import path
from django.conf.urls import url
from searchr_app import views


app_name = 'searchr_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_project/', views.AddProjectView.as_view(), name='add_project'),
    path('owner/<slug:username>/project/<slug:slug>/', views.ProjectView.as_view(), name='show_project'),
    path('owner/<slug:username>/project/<slug:slug>/<slug:search_slug>/', views.SearchObjectView.as_view(), name='show_search'),
    path('<project_id>/new_search/', views.AddSearchView.as_view(), name='new_search'),
    path('phrase/<phrase_language>/<slug:phrase_slug>/', views.ShowPhraseView.as_view(), name='show_phrase'),
    path('add_phrase/', views.AddPhraseView.as_view(), name='add_phrase'),
    path('keyword/<keyword_language>/<slug:keyword_slug>/', views.ShowKeywordView.as_view(), name='show_keyword'),
    path('search_result/<search_res_id>', views.ShowSearchResultsView.as_view(), name='search_result'),

    path('search/', views.SearchView.as_view(), name='search'),

    path('add_keyword/', views.AddKeywordView.as_view(), name='add_keyword'),

    path('goto/', views.GoToUrlView.as_view(), name='goto_url'),
]

