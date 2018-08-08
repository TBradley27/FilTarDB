from django.conf.urls import include, url
from . import views
from django.contrib import admin
from smart_selects import urls as smart_selects_urls
# from .views import UpdateView
from dal import autocomplete
from .models import *
from .views import *

app_name = 'foo'

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
    url(r'^$', views.home, name='home'),
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=ExampleFK,
            create_field='name',
        ),
        name='select2_fk',
    ),

    url(
        'test2-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=Tissues,
            create_field='name',
        ),
        name='select2_fk',
    ),

    url(
        'test3-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=Gene,
            create_field='name',
        ),
        name='select2_fk',

    ),

    url(
        r'^filtar/country-autocomplete/$',
        CountryAutocomplete.as_view(model=ExampleFK),
        name='country-autocomplete'
    ),

    url(
        r'^filtar/tissues-autocomplete/$',
        TissuesAutocomplete.as_view(model=Tissues),
        name='tissues-autocomplete'
    ),

    url(
        r'^filtar/gene-autocomplete/$',
        GeneAutocomplete.as_view(model=Gene),
        name='gene-autocomplete'
    ),

]
