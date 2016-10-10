from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^media$', views.media, name='media'),
    url(r'^search$', views.search, name='search'),
    url(r'^maker$', views.get_filled, name='get_filled'),
    url(r'^v/(?P<vid>[A-Z0-9-]+)?$', views.video_page, name='video_page'),
    url(r'^(?P<article>[mlsdak])/(?P<a_id>[0-9]+)?$', views.article, name='article'),
    url(r'^(?P<filter_article>[mlsdak])/(?P<a_id>[0-9]+)/(?P<article>[mlsdak])$', views.filtered_article, name='filtered_article'),
]
