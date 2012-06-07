# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Base_skill_type'
        db.create_table('main_base_skill_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('skill_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('volume_prize', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Base_skill_type'])

        # Adding model 'Avatar'
        db.create_table('main_avatar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('male', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Base_skill_type'], null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Avatar'])

        # Adding model 'Level'
        db.create_table('main_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('max_power', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('price_for_work', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('exp_to_next_lvl', self.gf('django.db.models.fields.IntegerField')(default=24)),
        ))
        db.send_create_signal('main', ['Level'])

        # Adding model 'Status'
        db.create_table('main_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('main', ['Status'])

        # Adding model 'Artefact'
        db.create_table('main_artefact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artefact_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Artefact'])

        # Adding model 'Box'
        db.create_table('main_box', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['Box'])

        # Adding M2M table for field artefacts on 'Box'
        db.create_table('main_box_artefacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('box', models.ForeignKey(orm['main.box'], null=False)),
            ('artefact', models.ForeignKey(orm['main.artefact'], null=False))
        ))
        db.create_unique('main_box_artefacts', ['box_id', 'artefact_id'])

        # Adding model 'Roach'
        db.create_table('main_roach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vk_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('out_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('roach_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Avatar'], null=True, blank=True)),
            ('money_1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('money_2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('temp_money', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pow_skill', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('speed_skill', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('intel_skill', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('trick_skill', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('agil_skill', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('power', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('exp_all', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('exp_now', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Level'])),
            ('box', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.Box'], unique=True)),
            ('slot_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('regenerate_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Status'])),
            ('end_time_status', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('PREMIUM', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('end_time_premium', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['Roach'])

        # Adding model 'RaceRoad'
        db.create_table('main_raceroad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('road_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Level'])),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('main', ['RaceRoad'])

        # Adding model 'Point'
        db.create_table('main_point', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race_road', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.RaceRoad'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('pow_skill', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('speed_skill', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('intel_skill', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('power', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Point'])

        # Adding model 'Race'
        db.create_table('main_race', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('road', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.RaceRoad'])),
            ('winner', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('prize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('log', self.gf('django.db.models.fields.TextField')(max_length=50000)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Race'])

        # Adding M2M table for field roaches on 'Race'
        db.create_table('main_race_roaches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('race', models.ForeignKey(orm['main.race'], null=False)),
            ('roach', models.ForeignKey(orm['main.roach'], null=False))
        ))
        db.create_unique('main_race_roaches', ['race_id', 'roach_id'])

        # Adding model 'Harm'
        db.create_table('main_harm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('harm_text', self.gf('django.db.models.fields.TextField')(max_length=20000)),
            ('unharm_text', self.gf('django.db.models.fields.TextField')(max_length=20000)),
        ))
        db.send_create_signal('main', ['Harm'])

        # Adding model 'RuningLog'
        db.create_table('main_runinglog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['main.Point'])),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=20000)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['RuningLog'])

        # Adding model 'ResultDroped'
        db.create_table('main_resultdroped', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('differenc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('perc_min', self.gf('django.db.models.fields.IntegerField')(default=7)),
            ('perc_max', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('exp', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal('main', ['ResultDroped'])

        # Adding model 'EvolutionPrice'
        db.create_table('main_evolutionprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('cost', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('main', ['EvolutionPrice'])

    def backwards(self, orm):
        # Deleting model 'Base_skill_type'
        db.delete_table('main_base_skill_type')

        # Deleting model 'Avatar'
        db.delete_table('main_avatar')

        # Deleting model 'Level'
        db.delete_table('main_level')

        # Deleting model 'Status'
        db.delete_table('main_status')

        # Deleting model 'Artefact'
        db.delete_table('main_artefact')

        # Deleting model 'Box'
        db.delete_table('main_box')

        # Removing M2M table for field artefacts on 'Box'
        db.delete_table('main_box_artefacts')

        # Deleting model 'Roach'
        db.delete_table('main_roach')

        # Deleting model 'RaceRoad'
        db.delete_table('main_raceroad')

        # Deleting model 'Point'
        db.delete_table('main_point')

        # Deleting model 'Race'
        db.delete_table('main_race')

        # Removing M2M table for field roaches on 'Race'
        db.delete_table('main_race_roaches')

        # Deleting model 'Harm'
        db.delete_table('main_harm')

        # Deleting model 'RuningLog'
        db.delete_table('main_runinglog')

        # Deleting model 'ResultDroped'
        db.delete_table('main_resultdroped')

        # Deleting model 'EvolutionPrice'
        db.delete_table('main_evolutionprice')

    models = {
        'main.artefact': {
            'Meta': {'object_name': 'Artefact'},
            'artefact_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'main.avatar': {
            'Meta': {'ordering': "['id']", 'object_name': 'Avatar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'male': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Base_skill_type']", 'null': 'True', 'blank': 'True'})
        },
        'main.base_skill_type': {
            'Meta': {'object_name': 'Base_skill_type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'volume_prize': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.box': {
            'Meta': {'object_name': 'Box'},
            'artefacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Artefact']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.evolutionprice': {
            'Meta': {'ordering': "['value']", 'object_name': 'EvolutionPrice'},
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'main.harm': {
            'Meta': {'object_name': 'Harm'},
            'harm_text': ('django.db.models.fields.TextField', [], {'max_length': '20000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unharm_text': ('django.db.models.fields.TextField', [], {'max_length': '20000'})
        },
        'main.level': {
            'Meta': {'ordering': "['level']", 'object_name': 'Level'},
            'exp_to_next_lvl': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'level_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'max_power': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'price_for_work': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'main.point': {
            'Meta': {'ordering': "['position']", 'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intel_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pow_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'race_road': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.RaceRoad']"}),
            'speed_skill': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.race': {
            'Meta': {'object_name': 'Race'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'max_length': '50000'}),
            'prize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'roaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Roach']", 'symmetrical': 'False'}),
            'road': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.RaceRoad']"}),
            'winner': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.raceroad': {
            'Meta': {'object_name': 'RaceRoad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Level']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'road_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.resultdroped': {
            'Meta': {'ordering': "['differenc']", 'object_name': 'ResultDroped'},
            'differenc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exp': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perc_max': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'perc_min': ('django.db.models.fields.IntegerField', [], {'default': '7'})
        },
        'main.roach': {
            'Meta': {'object_name': 'Roach'},
            'PREMIUM': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'agil_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Avatar']", 'null': 'True', 'blank': 'True'}),
            'box': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.Box']", 'unique': 'True'}),
            'end_time_premium': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time_status': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exp_all': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exp_now': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intel_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Level']"}),
            'money_1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'money_2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'out_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pow_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'power': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'regenerate_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'roach_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slot_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'speed_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Status']"}),
            'temp_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'trick_skill': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'vk_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.runinglog': {
            'Meta': {'ordering': "['value']", 'object_name': 'RuningLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['main.Point']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '20000'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']