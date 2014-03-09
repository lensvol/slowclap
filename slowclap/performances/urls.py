#coding: utf-8

from django.conf.urls import patterns, include, url

from slowclap.performances.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slowclap.views.home', name='home'),

    url(r'roll', event_roll),
    url(r'list/events$', EventList.as_view()),
    url(r'list/blocks$', BlockList.as_view()),
    url(r'list/categories$', CategoryList.as_view())
)
