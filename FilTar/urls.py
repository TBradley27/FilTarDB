from django.conf.urls import include, url
from . import views
from django.contrib import admin

app_name = 'filtar'

urlpatterns = [

    # /filtar/

    url(r'^getname/$', views.getname, name='get_name'),

    url(r'^nextview/', views.nextview, name='nextview'),
]