from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('facereco.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home'),
    url(r'^home$', 'home'),
    url(r'^step$', 'step'),
    url(r'^experiance$', 'experiance'),
    url(r'^a_propos$', 'propos'),
    url(r'^elab$', 'elab')
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
