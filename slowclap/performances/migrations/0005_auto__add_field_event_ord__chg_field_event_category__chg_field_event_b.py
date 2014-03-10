# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.ord'
        db.add_column(u'performances_event', 'ord',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


        # Changing field 'Event.category'
        db.alter_column(u'performances_event', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.Category'], null=True))

        # Changing field 'Event.block'
        db.alter_column(u'performances_event', 'block_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.ActionBlock'], null=True))

    def backwards(self, orm):
        # Deleting field 'Event.ord'
        db.delete_column(u'performances_event', 'ord')


        # User chose to not deal with backwards NULL issues for 'Event.category'
        raise RuntimeError("Cannot reverse this migration. 'Event.category' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Event.category'
        db.alter_column(u'performances_event', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.Category']))

        # User chose to not deal with backwards NULL issues for 'Event.block'
        raise RuntimeError("Cannot reverse this migration. 'Event.block' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Event.block'
        db.alter_column(u'performances_event', 'block_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['performances.ActionBlock']))

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
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['performances.ActionBlock']", 'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['performances.Category']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "u'(\\u043d\\u0435 \\u0443\\u043a\\u0430\\u0437\\u0430\\u043d\\u043e)'", 'max_length': '255'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ord': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['performances']