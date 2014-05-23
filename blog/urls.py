from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^type/(?P<type_id>\d+)/$', views.category, name='category'),
    url(r'^post/(?P<post_id>\d+)/$', views.post, name='post')
)