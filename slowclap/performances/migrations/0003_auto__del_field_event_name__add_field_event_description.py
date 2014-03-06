# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.name'
        db.delete_column(u'performances_event', 'name')

        # Adding field 'Event.description'
        db.add_column('performances_event', 'description',
                      self.gf('django.db.models.fields.CharField')(default=u'(\u043d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u043e)', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.name'
        db.add_column(u'performances_event', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Event.description'
        db.delete_column('performances_event', 'description')


    models = {
        'performances.actionblock': {
            'Meta': {'object_name': 'ActionBlock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'performances.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'performances.event': {
            'Meta': {'object_name': 'Event'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['performances.ActionBlock']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['performances.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "u'(\\u043d\\u0435 \\u0443\\u043a\\u0430\\u0437\\u0430\\u043d\\u043e)'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['performances']