#coding: utf-8

import json
import datetime
import pytz
import re
from mock import patch

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.timezone import get_current_timezone
from django.views.decorators.csrf import csrf_exempt
from django.core import cache as django_cache

from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import generics

from slowclap.models import Event, ActionBlock
from slowclap.serializers import *


def event_roll(request):
    return render_to_response('roll.html')


def noscript_roll(request):
    blocks = ActionBlock.objects.filter(event__isnull=False)\
                                .order_by('start')
    result = []
    tz = get_current_timezone()

    for block in blocks:
        events = []
        start_time = block.start.replace(tzinfo=pytz.utc).astimezone(tz)
        for ev in block.event_set.order_by('ord'):
            prepared_event = {
                'start': start_time.strftime('%H:%M'),
                'name': ev.description,
                'category': ev.category.name
            }
            events.append(prepared_event)
            start_time = start_time + datetime.timedelta(seconds=ev.duration)

        result.append({
            'name': block.name,
            'events': events
        })

    return render_to_response('noscript_roll.html', {'blocks': result})


def list_program(request):
    cached_program = django_cache.cache.get('/list/program')
    if cached_program:
        return HttpResponse(cached_program, content_type='application/json')

    blocks = ActionBlock.objects.all()
    result = {}

    for block in blocks:
        result[block.id] = [ev.id for ev in block.event_set.order_by('ord')]

    content = json.dumps(result, indent=4)
    django_cache.cache.set('/list/program', content)

    return HttpResponse(json.dumps(result, indent=4), content_type='application/json')


# Taken from https://gist.github.com/mjumbewu/8184292
# Kudos to original author!
class CachedResourceMixin(object):
    @property
    def cache_prefix(self):
        return self.request.path

    def get_cache_prefix(self):
        return self.cache_prefix

    def get_cache_metakey(self):
        prefix = self.cache_prefix
        return prefix + '_keys'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # Only do the cache for GET, OPTIONS, or HEAD method.
        if request.method.upper() not in SAFE_METHODS:
            return super(CachedResourceMixin, self).dispatch(request, *args, **kwargs)

        self.request = request

        # Check whether the response data is in the cache.
        key = self.get_cache_key(request, *args, **kwargs)
        response_data = django_cache.cache.get(key) or None

        # Also check whether the request cache key is managed in the cache.
        # This is important, because if it's not managed, then we'll never
        # know when to invalidate it. If it's not managed we should just
        # assume that it's invalid.
        metakey = self.get_cache_metakey()
        keyset = django_cache.cache.get(metakey) or set()

        if (response_data is not None) and (key in keyset):
            cached_response = self.respond_from_cache(response_data)
            handler_name = request.method.lower()

            def cached_handler(*args, **kwargs):
                return cached_response

            # Patch the HTTP method
            with patch.object(self, handler_name, new=cached_handler):
                response = super(CachedResourceMixin, self).dispatch(request, *args, **kwargs)
        else:
            response = super(CachedResourceMixin, self).dispatch(request, *args, **kwargs)

            # Only cache on OK resposne
            if response.status_code == 200:
                self.cache_response(key, response)

        # Disable client-side caching. Cause IE wrongly assumes when it should
        # cache.
        response['Cache-Control'] = 'no-cache'
        return response

    def get_cache_key(self, request, *args, **kwargs):
        querystring = request.META.get('QUERY_STRING', '')
        contenttype = request.META.get('HTTP_ACCEPT', '')

        # TODO: Eliminate the jQuery cache busting parameter for now. Get
        # rid of this after the old API has been deprecated.
        cache_buster_pattern = re.compile(r'&?_=\d+')
        querystring = re.sub(cache_buster_pattern, '', querystring)

        return ':'.join([self.cache_prefix, contenttype, querystring])

    def respond_from_cache(self, cached_data):
        # Given some cached data, construct a response.
        content, status, headers = cached_data
        return HttpResponse(content, content_type="application/json")


    def cache_response(self, key, response):
        response.render()
        data = response.content
        status = response.status_code
        headers = response.items()

        # Cache enough info to recreate the response.
        django_cache.cache.set(key, (data, status, headers))

        # Also, add the key to the set of pages cached from this view.
        meta_key = self.cache_prefix + '_keys'
        keys = django_cache.cache.get(meta_key) or set()
        keys.add(key)
        django_cache.cache.set(meta_key, keys)

        return response


class BlockList(CachedResourceMixin, generics.ListCreateAPIView):
    queryset = ActionBlock.objects.all()
    serializer_class = ActionBlockSerializer


class CategoryList(CachedResourceMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventList(CachedResourceMixin, generics.ListCreateAPIView):
    queryset = Event.objects.filter(block__isnull=False,
                                    ord__isnull=False)\
                            .order_by('block__id', 'ord')
    serializer_class = EventSerializer
