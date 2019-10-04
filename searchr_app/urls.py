from django.urls import path
from django.conf.urls import url
from searchr_app import views


app_name = 'searchr_app'

urlpatterns = [
    path('', views.home, name='home'),
]

