# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.name'
        db.add_column(u'performances_event', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.name'
        db.delete_column(u'performances_event', 'name')


    models = {
        u'performances.actionblock': {
            'Meta': {'object_name': 'ActionBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'performances.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'performances.event': {
            'Meta': {'object_name': 'Event'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['performances.ActionBlock']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['performances.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['performances']