from django.conf.urls import include, url
from . import views
from django.contrib import admin
from smart_selects import urls as smart_selects_urls
# from .views import UpdateView
from dal import autocomplete
from .models import *
from .views import *
from django.views.generic import TemplateView

app_name = 'foo'

urlpatterns = [

    url(r'^results/$', views.results, name='results'),
    url('^information/$', TemplateView.as_view(template_name='filtar/about.html')),
    url('^acknowledgements/$', TemplateView.as_view(template_name='filtar/acknowledgements.html')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', views.home, name='home'),

    url(
        r'^mirna-autocomplete/$',
        CountryAutocomplete.as_view(model=ExampleFK),
        name='country-autocomplete'
    ),

    url(
        r'^tissues-autocomplete/$',
        TissuesAutocomplete.as_view(model=Tissues),
        name='tissues-autocomplete'
    ),

    url(
        r'^gene-autocomplete/$',
        GeneAutocomplete.as_view(model=Gene),
        name='gene-autocomplete'
    )
]
