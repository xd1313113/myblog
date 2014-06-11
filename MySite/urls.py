from django.conf.urls import patterns, include, url

from django.contrib import admin
import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MySite.views.home', name='home'),
    url(r'^', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gallery/', include('photo.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
