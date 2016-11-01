from django.conf.urls import url
from . import views

urlpatterns = [

    # /filtar/

    url(r'^$', views.index, name='index'),
    
    # /filtar/
    url(r'^(?P<species_id>[0-9]+)/$', views.detail, name="detail")
    
]