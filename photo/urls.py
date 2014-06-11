from django.conf.urls import patterns, url

from photo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^image/(?P<image_id>\d+)/$', views.single, name='single'),
    url(r'^tag/(?P<tag_id>\w+)/$', views.tag, name='tag'),
)