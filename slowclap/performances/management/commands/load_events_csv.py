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
            if category:
                category_rec, _ = Category.objects.get_or_create(name=category)
            else:
                category_rec = None

            start = datetime.datetime.strptime(start_date, '%d.%m.%Y')
            start += datetime.timedelta(days=int(day)-1)
            
            if block:
                block_rec, _ = ActionBlock.objects.get_or_create(name=u'Блок #{0}'.format(block),
                                                                 start=start)
            else:
                block_rec = None

            duration_sec = float(duration.replace(',', '.')) * 60

            event, cr = Event.objects.get_or_create(category=category_rec,
                                                    block=block_rec,
                                                    ord=pos or None,
                                                    duration=duration_sec,
                                                    description=name.replace(u'\n', u' / '))
            event.save()
            if cr:
                count += 1

        print '{0} events added from {1}.'.format(count, csv_fn)