# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Point.race_road'
        db.delete_column('roaches_point', 'race_road_id')

        # Deleting field 'RaceRoad.points'
        db.delete_column('roaches_raceroad', 'points')

        # Adding M2M table for field points on 'RaceRoad'
        db.create_table('roaches_raceroad_points', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('raceroad', models.ForeignKey(orm['roaches.raceroad'], null=False)),
            ('point', models.ForeignKey(orm['roaches.point'], null=False))
        ))
        db.create_unique('roaches_raceroad_points', ['raceroad_id', 'point_id'])

    def backwards(self, orm):
        # Adding field 'Point.race_road'
        db.add_column('roaches_point', 'race_road',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['roaches.RaceRoad']),
                      keep_default=False)

        # Adding field 'RaceRoad.points'
        db.add_column('roaches_raceroad', 'points',
                      self.gf('django.db.models.fields.IntegerField')(default=10),
                      keep_default=False)

        # Removing M2M table for field points on 'RaceRoad'
        db.delete_table('roaches_raceroad_points')

    models = {
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
        },
        'roaches.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.BaseSkillType']", 'null': 'True', 'blank': 'True'})
        },
        'roaches.baseskilltype': {
            'Meta': {'object_name': 'BaseSkillType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume_prize': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'roaches.box': {
            'Meta': {'object_name': 'Box'},
            'garment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['roaches.Garment']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'roaches.evolutionprice': {
            'Meta': {'object_name': 'EvolutionPrice'},
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.Level']"})
        },
        'roaches.garment': {
            'Meta': {'object_name': 'Garment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'roaches.harm': {
            'Meta': {'object_name': 'Harm'},
            'harm_text': ('django.db.models.fields.TextField', [], {'max_length': '20000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unharm_text': ('django.db.models.fields.TextField', [], {'max_length': '20000'})
        },
        'roaches.level': {
            'Meta': {'ordering': "['level']", 'object_name': 'Level'},
            'exp_to_next_lvl': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '1', 'primary_key': 'True'}),
            'max_power': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'price_for_work': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'roaches.point': {
            'Meta': {'ordering': "['position']", 'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intel_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pow_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'speed_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'roaches.race': {
            'Meta': {'object_name': 'Race'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'prize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'roaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['roaches.Roach']", 'symmetrical': 'False'}),
            'road': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.RaceRoad']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'races'", 'to': "orm['roaches.Roach']"})
        },
        'roaches.raceroad': {
            'Meta': {'ordering': "['level']", 'object_name': 'RaceRoad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.Level']"}),
            'points': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'raceroads'", 'symmetrical': 'False', 'to': "orm['roaches.Point']"}),
            'road_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'roaches.resultdroped': {
            'Meta': {'ordering': "['differenc']", 'object_name': 'ResultDroped'},
            'differenc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exp': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perc_max': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'perc_min': ('django.db.models.fields.IntegerField', [], {'default': '7'})
        },
        'roaches.roach': {
            'Meta': {'object_name': 'Roach'},
            'PREMIUM': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'agil_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.Avatar']", 'null': 'True', 'blank': 'True'}),
            'box': ('lib.fields.AutoOneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['roaches.Box']"}),
            'end_time_premium': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time_status': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exp_all': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exp_now': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'intel_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.Level']"}),
            'money_1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'money_2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nick': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'pow_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'regenerate_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slot_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'speed_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roaches.Status']"}),
            'temp_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trick_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('lib.fields.AutoOneToOneField', [], {'related_name': "'roach'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"})
        },
        'roaches.runinglog': {
            'Meta': {'ordering': "['value']", 'object_name': 'RuningLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'logs'", 'to': "orm['roaches.Point']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'roaches.status': {
            'Meta': {'object_name': 'Status'},
            'status': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['roaches']