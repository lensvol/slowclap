#coding: utf-8

from django.shortcuts import render_to_response

from rest_framework import generics
from slowclap.performances.models import Event
from slowclap.performances.serializers import EventSerializer


def event_roll(request):
    return render_to_response('roll.html')


class EventList(generics.ListCreateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer