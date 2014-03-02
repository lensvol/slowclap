# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActionBlock'
        db.create_table(u'performances_actionblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'performances', ['ActionBlock'])

        # Adding model 'Category'
        db.create_table(u'performances_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'performances', ['Category'])

        # Adding model 'Event'
        db.create_table(u'performances_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.ActionBlock'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.Category'])),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'performances', ['Event'])


    def backwards(self, orm):
        # Deleting model 'ActionBlock'
        db.delete_table(u'performances_actionblock')

        # Deleting model 'Category'
        db.delete_table(u'performances_category')

        # Deleting model 'Event'
        db.delete_table(u'performances_event')


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
            'length': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['performances']