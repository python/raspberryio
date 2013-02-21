# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LatestArticleRevision'
        db.delete_table('search_latestarticlerevision')


    def backwards(self, orm):
        # Adding model 'LatestArticleRevision'
        db.create_table('search_latestarticlerevision', (
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('article_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('search', ['LatestArticleRevision'])


    models = {
        
    }

    complete_apps = ['search']