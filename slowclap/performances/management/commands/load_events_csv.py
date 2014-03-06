#coding: utf-8

import csv
import datetime
from django.core.management.base import BaseCommand, CommandError

from slowclap.performances.models import Category, ActionBlock, Event

class Command(BaseCommand):
    args = '<csv_file> <start date>'
    help = 'Load events from CSV file'

    def handle(self, *args, **options):
        lines = []

        csv_fn, start_date = args        
        with open(csv_fn, 'rb') as fp:
            reader = csv.reader(fp, delimiter=';')
            lines = [[c.decode('cp1251') for c in l] for l in reader]

        count = 0
        for (category, pos, name, duration, block, day) in lines:
            category_rec, _ = Category.objects.get_or_create(name=category)
            start = datetime.datetime.strptime(start_date, '%d.%m.%Y')
            start += datetime.timedelta(days=int(day)-1)
            
            block_rec, _ = ActionBlock.objects.get_or_create(name=u'Блок #{0}'.format(block),
                                                             start=start)
            duration_sec = float(duration.replace(',', '.')) * 60

            event, _ = Event.objects.get_or_create(category=category_rec,
                                                   block=block_rec,
                                                   duration=duration_sec,
                                                   description=name.replace(u'\n', u' / '))
            event.save()

        print '{0} events added from {1}.'.format(count, csv_fn)