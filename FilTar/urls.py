from django.conf.urls import include, url
from . import views
from django.contrib import admin
from smart_selects import urls as smart_selects_urls


app_name = 'filtar'

urlpatterns = [

    # /filtar/

    url(r'^$', views.home, name='home'),

    url(r'^results/$', views.results, name='results'),
    url(r'^chaining/', include('smart_selects.urls'))
]