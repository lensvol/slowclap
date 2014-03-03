from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slowclap.views.home', name='home'),
    url(r'^performances/', include('slowclap.performances.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + staticfiles_urlpatterns()
