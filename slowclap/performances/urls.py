#coding: utf-8

from django.conf.urls import patterns, include, url

from slowclap.performances.views import event_roll, EventList

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slowclap.views.home', name='home'),

    url(r'roll', event_roll),
    url(r'$', EventList.as_view())
)
