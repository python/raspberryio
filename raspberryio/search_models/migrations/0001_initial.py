# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LatestArticleRevision'
        db.create_table('search_models_latestarticlerevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('search_models', ['LatestArticleRevision'])


    def backwards(self, orm):
        # Deleting model 'LatestArticleRevision'
        db.delete_table('search_models_latestarticlerevision')


    models = {
        'search_models.latestarticlerevision': {
            'Meta': {'object_name': 'LatestArticleRevision'},
            'article_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['search_models']