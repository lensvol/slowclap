#coding: utf-8

from django.shortcuts import render_to_response

from rest_framework import generics
from slowclap.performances.models import Event, ActionBlock
from slowclap.performances.serializers import *


def event_roll(request):
    return render_to_response('roll.html')


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