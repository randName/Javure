"""javure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<filename>(robots|humans).txt)$', home_files, name='home-files'),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^logout/$', logout ),
    url(r'^library/', include('library.urls')),
    url(r'^colle/', include('collection.urls')),
    url(r'^$', home, name='jhome'),
]
