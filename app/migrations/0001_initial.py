# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('app_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_traffic', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('app', ['UserProfile'])

        # Adding model 'Connection'
        db.create_table('app_connection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('traffic_sent', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('traffic_recv', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('remote_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('vpn_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('app', ['Connection'])

        # Adding model 'TrafficNode'
        db.create_table('app_trafficnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Connection'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('traffic_sent_since', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('traffic_recv_since', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('traffic_sent_total', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('traffic_recv_total', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('app', ['TrafficNode'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('app_userprofile')

        # Deleting model 'Connection'
        db.delete_table('app_connection')

        # Deleting model 'TrafficNode'
        db.delete_table('app_trafficnode')


    models = {
        'app.connection': {
            'Meta': {'object_name': 'Connection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'traffic_recv': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'traffic_sent': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vpn_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'app.trafficnode': {
            'Meta': {'object_name': 'TrafficNode'},
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Connection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'traffic_recv_since': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'traffic_recv_total': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'traffic_sent_since': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'traffic_sent_total': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_traffic': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']