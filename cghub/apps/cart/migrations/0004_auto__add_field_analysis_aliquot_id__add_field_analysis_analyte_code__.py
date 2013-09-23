# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Analysis.aliquot_id'
        db.add_column('cart_analysis', 'aliquot_id',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.analyte_code'
        db.add_column('cart_analysis', 'analyte_code',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.center_name'
        db.add_column('cart_analysis', 'center_name',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.disease_abbr'
        db.add_column('cart_analysis', 'disease_abbr',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.legacy_sample_id'
        db.add_column('cart_analysis', 'legacy_sample_id',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.library_strategy'
        db.add_column('cart_analysis', 'library_strategy',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.published_date'
        db.add_column('cart_analysis', 'published_date',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.participant_id'
        db.add_column('cart_analysis', 'participant_id',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.platform'
        db.add_column('cart_analysis', 'platform',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.refassem_short_name'
        db.add_column('cart_analysis', 'refassem_short_name',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.sample_accession'
        db.add_column('cart_analysis', 'sample_accession',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.sample_id'
        db.add_column('cart_analysis', 'sample_id',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.sample_type'
        db.add_column('cart_analysis', 'sample_type',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.study'
        db.add_column('cart_analysis', 'study',
                      self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.tss_id'
        db.add_column('cart_analysis', 'tss_id',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Analysis.upload_date'
        db.add_column('cart_analysis', 'upload_date',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Analysis.aliquot_id'
        db.delete_column('cart_analysis', 'aliquot_id')

        # Deleting field 'Analysis.analyte_code'
        db.delete_column('cart_analysis', 'analyte_code')

        # Deleting field 'Analysis.center_name'
        db.delete_column('cart_analysis', 'center_name')

        # Deleting field 'Analysis.disease_abbr'
        db.delete_column('cart_analysis', 'disease_abbr')

        # Deleting field 'Analysis.legacy_sample_id'
        db.delete_column('cart_analysis', 'legacy_sample_id')

        # Deleting field 'Analysis.library_strategy'
        db.delete_column('cart_analysis', 'library_strategy')

        # Deleting field 'Analysis.published_date'
        db.delete_column('cart_analysis', 'published_date')

        # Deleting field 'Analysis.participant_id'
        db.delete_column('cart_analysis', 'participant_id')

        # Deleting field 'Analysis.platform'
        db.delete_column('cart_analysis', 'platform')

        # Deleting field 'Analysis.refassem_short_name'
        db.delete_column('cart_analysis', 'refassem_short_name')

        # Deleting field 'Analysis.sample_accession'
        db.delete_column('cart_analysis', 'sample_accession')

        # Deleting field 'Analysis.sample_id'
        db.delete_column('cart_analysis', 'sample_id')

        # Deleting field 'Analysis.sample_type'
        db.delete_column('cart_analysis', 'sample_type')

        # Deleting field 'Analysis.study'
        db.delete_column('cart_analysis', 'study')

        # Deleting field 'Analysis.tss_id'
        db.delete_column('cart_analysis', 'tss_id')

        # Deleting field 'Analysis.upload_date'
        db.delete_column('cart_analysis', 'upload_date')


    models = {
        'cart.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'aliquot_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'analysis_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'analyte_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'center_name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'disease_abbr': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'files_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'legacy_sample_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'library_strategy': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'participant_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'refassem_short_name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_accession': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sample_type': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
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