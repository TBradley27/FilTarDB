from django.conf.urls import url
from . import views

app_name = 'filtar'

urlpatterns = [

    # /filtar/

     url(r'^getname$', views.getname, name='get_name'),

    url(r'^context$', views.contextpp, name='contextpp'),

     url(r'^$', views.IndexView.as_view(), name='index'),
    
    # /filtar/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail")
    
]