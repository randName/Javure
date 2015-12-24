from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^v/(?P<cid>[a-z0-9]+)$', views.video_page),
    url(r'^(?P<article>[mlsdat])/(?P<a_id>[0-9]+)$', views.article),
]
