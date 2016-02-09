from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^actresses$', views.actresses, name='actresses'),
    url(r'^v/(?P<vid>[A-Z0-9-]+)?$', views.video_page, name='video_page'),
    url(r'^(?P<article>[mlsdak])/(?P<a_id>[0-9]+)?$', views.article, name='article'),
]
