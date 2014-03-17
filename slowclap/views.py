#coding: utf-8

import json
import datetime
import pytz
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils.timezone import get_current_timezone

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
    blocks = ActionBlock.objects.all()
    result = {}

    for block in blocks:
        result[block.id] = [ev.id for ev in block.event_set.order_by('ord')]

    return HttpResponse(json.dumps(result, indent=4), content_type='application/json')


class BlockList(generics.ListCreateAPIView):
    queryset = ActionBlock.objects.all()
    serializer_class = ActionBlockSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter(block__isnull=False,
                                    ord__isnull=False)\
                            .order_by('block__id', 'ord')
    serializer_class = EventSerializer
