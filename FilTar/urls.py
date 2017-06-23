from django.conf.urls import include, url
from . import views
from django.contrib import admin

app_name = 'filtar'

urlpatterns = [

    # /filtar/

    url(r'^getname/$', views.getname, name='get_name'),

    url(r'^nextview/', views.nextview, name='nextview'),

    url(r'^context/', views.getname, name='contextpp'),

    url(r'^$', views.foo, name='foo'),

    # /filtar/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail")
    
]