#coding: utf-8

from django.conf.urls import patterns, include, url

from slowclap.views import *

urlpatterns = patterns('',
    url(r'noscript$', noscript_roll),
    url(r'list/events$', EventList.as_view()),
    url(r'list/blocks$', BlockList.as_view()),
    url(r'list/categories$', CategoryList.as_view()),
    url(r'list/program$', list_program),
    url(r'$', event_roll)
)
