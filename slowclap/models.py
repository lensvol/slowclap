#coding: utf-8

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class ActionBlock(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=u'Название',
                            null=False)
    start = models.DateTimeField(verbose_name=u'Начало')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Блок выступлений'
        verbose_name_plural = u'Блоки выступлений'


class Category(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=u'Название',
                            null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория выступления'
        verbose_name_plural = u'Категории выступлений'


class Event(models.Model):
    block = models.ForeignKey(ActionBlock,
                              verbose_name=u'Блок',
                              null=True)
    category = models.ForeignKey(Category,
                                 verbose_name=u'Категория',
                                 null=True,
                                 default=None)
    ord = models.IntegerField(verbose_name=u'Номер в блоке',
                              null=True)
    number = models.IntegerField(verbose_name=u'Номер в конкурсе',
                                 null=True,
                                 blank=True)
    description = models.CharField(max_length=255,
                                   verbose_name=u'Описание',
                                   null=False,
                                   default=u'(не указано)')
    duration = models.IntegerField(verbose_name=u'Длина выступления (сек)',
                                   default=0)

    def __unicode__(self):
        return self.description

    def save(self, **args):
        with transaction.atomic():
            next_events = Event.objects.filter(ord__gte=self.ord,
                                               block=self.block)\
                                       .order_by('ord')
            for ind, event in enumerate(next_events):
                event.ord = self.ord + ind + 1
                super(Event, event).save()
        super(Event, self).save(**args)

        # Bust the cache of dependent views
        cache.delete('/list/program')

    class Meta:
        verbose_name = u'Выступление'
        verbose_name_plural = u'Выступления'
