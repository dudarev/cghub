# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


from cghub.apps.core.requests import RequestDetailJSON

class Migration(DataMigration):

    def forwards(self, orm):
        for analysis in orm.Analysis.objects.all():
            api_request = RequestDetailJSON(query={
                        'analysis_id': analysis.analysis_id})
            try:
                result = api_request.call().next()
            except StopIteration:
                print 'Bad analysis: %s, skipped.' % analysis.analysis_id
                continue
            analysis.aliquot_id = result.get('aliquot_id')
            analysis.analyte_code = result.get('analyte_code')
            analysis.center_name = result.get('center_name')
            analysis.disease_abbr = result.get('disease_abbr')
            analysis.legacy_sample_id = result.get('legacy_sample_id')
            analysis.library_strategy = result.get('library_strategy')
            analysis.published_date = result.get('published_date')
            analysis.participant_id = result.get('participant_id')
            analysis.platform = result.get('platform')
            analysis.refassem_short_name = result.get('refassem_short_name')
            analysis.sample_accession = result.get('sample_accession')
            analysis.sample_id = result.get('sample_id')
            analysis.sample_type = result.get('sample_type')
            analysis.study = result.get('study')
            analysis.tss_id = result.get('tss_id')
            analysis.upload_date = result.get('upload_date')
            analysis.save()

    def backwards(self, orm):
        pass

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
    symmetrical = True
