# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActionBlock'
        db.create_table(u'slowclap_actionblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'slowclap', ['ActionBlock'])

        # Adding model 'Category'
        db.create_table(u'slowclap_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'slowclap', ['Category'])

        # Adding model 'Event'
        db.create_table(u'slowclap_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['slowclap.ActionBlock'], null=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['slowclap.Category'], null=True)),
            ('ord', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default=u'(\u043d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u043e)', max_length=255)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'slowclap', ['Event'])


    def backwards(self, orm):
        # Deleting model 'ActionBlock'
        db.delete_table(u'slowclap_actionblock')

        # Deleting model 'Category'
        db.delete_table(u'slowclap_category')

        # Deleting model 'Event'
        db.delete_table(u'slowclap_event')


    models = {
        u'slowclap.actionblock': {
            'Meta': {'object_name': 'ActionBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'slowclap.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'slowclap.event': {
            'Meta': {'object_name': 'Event'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slowclap.ActionBlock']", 'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['slowclap.Category']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "u'(\\u043d\\u0435 \\u0443\\u043a\\u0430\\u0437\\u0430\\u043d\\u043e)'", 'max_length': '255'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ord': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['slowclap']