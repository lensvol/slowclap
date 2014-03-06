#coding: utf-8

from django.shortcuts import render_to_response

# Create your views here.

def event_roll(request):
    return render_to_response('roll.html')
