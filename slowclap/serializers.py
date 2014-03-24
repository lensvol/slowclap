#coding: utf-8

from rest_framework import serializers

from slowclap.models import Event, Category, ActionBlock


class ActionBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionBlock


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    block = ActionBlockSerializer(required=False)

    class Meta:
        model = Event
