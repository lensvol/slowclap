#coding: utf-8

from django.db import models


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
    block = models.ForeignKey(ActionBlock, verbose_name=u'Блок')
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    description = models.CharField(max_length=255, 
                                   verbose_name=u'Описание',
                                   null=False,
                                   default=u'(не указано)')
    duration = models.IntegerField(verbose_name=u'Длина выступления (сек)',
                                   default=0)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
