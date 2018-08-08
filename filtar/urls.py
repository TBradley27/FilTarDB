"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from smart_selects import urls as smart_selects_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^filtar/', include('Foo.urls')),
    url(r'^chaining/', include('smart_selects.urls'),
        )
]

# The carat symbol specifies that the string must begin with 'filtar/' string
# The $ symbol specifies that the string must end with the 'filtar/' string