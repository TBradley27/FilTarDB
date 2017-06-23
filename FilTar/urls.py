from django.conf.urls import include, url
from . import views
from django.contrib import admin

app_name = 'filtar'

urlpatterns = [

    # /filtar/

    url(r'^$', views.home, name='home'),

    url(r'^results/$', views.results, name='results'),
]