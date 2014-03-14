#coding: utf-8

import json
from django.shortcuts import render_to_response
from django.http import HttpResponse

from rest_framework import generics
from slowclap.models import Event, ActionBlock
from slowclap.serializers import *


def event_roll(request):
    return render_to_response('roll.html')


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
