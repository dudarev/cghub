# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Analysis.study'
        db.alter_column('cart_analysis', 'study', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Analysis.legacy_sample_id'
        db.alter_column('cart_analysis', 'legacy_sample_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):

        # Changing field 'Analysis.study'
        db.alter_column('cart_analysis', 'study', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))

        # Changing field 'Analysis.legacy_sample_id'
        db.alter_column('cart_analysis', 'legacy_sample_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))

    models = {
        'cart.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'aliquot_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'analysis_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'analyte_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'center_name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'disease_abbr': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'files_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'legacy_sample_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'library_strategy': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'participant_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'refassem_short_name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_accession': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_type': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tss_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'cart'", 'unique': 'True', 'to': "orm['sessions.Session']"}),
            'size': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'cart.cartitem': {
            'Meta': {'ordering': "('analysis',)", 'unique_together': "(('cart', 'analysis'),)", 'object_name': 'CartItem'},
            'analysis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Analysis']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['cart.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['cart']