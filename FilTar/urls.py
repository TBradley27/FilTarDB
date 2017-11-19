from django.conf.urls import include, url
from . import views
from django.contrib import admin
from smart_selects import urls as smart_selects_urls
# from .views import UpdateView
from dal import autocomplete
from .models import *

app_name = 'filtar'

urlpatterns = [

    # /filtar/

    # url(r'^$', views.home, name='home'),

    url(r'^results/$', views.results, name='results'),
    url(r'^chaining/', include('smart_selects.urls')),
    # url(
    #     r'^$',
    #     UpdateView.as_view(),
    #     name='filtar',
    # ),
    url(r'^$', views.new, name='new'),
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=ExampleFK,
            create_field='name',
        ),
        name='select2_fk',
    ),

]