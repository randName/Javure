from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^ajax$', views.ajax, name='ajax'),
    url(r'^stats$', views.stats, name='stats'),
    url(r'^v/(?P<cid>[a-z0-9_]+)?$', views.video_page, name='video_page'),
    url(r'^(?P<article>[mlsdak])/(?P<a_id>[0-9]+)?$', views.article, name='article'),
    url(r'^keywords', views.keywords, name='keywords'),
    url(r'^actresses', views.actresses, name='actresses'),
    url(r'^(?P<article>makers|labels|series|directors)$', views.articlepage, name='articlepage'),
]
