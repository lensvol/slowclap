#coding: utf-8

from django.conf.urls import patterns, include, url

from views import event_roll

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'slowclap.views.home', name='home'),

    url(r'roll', event_roll),
)
