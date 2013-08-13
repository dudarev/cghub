# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Analysis.files_size'
        db.alter_column('cart_analysis', 'files_size', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Cart.size'
        db.alter_column('cart_cart', 'size', self.gf('django.db.models.fields.BigIntegerField')())

    def backwards(self, orm):

        # Changing field 'Analysis.files_size'
        db.alter_column('cart_analysis', 'files_size', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'Cart.size'
        db.alter_column('cart_cart', 'size', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        'cart.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'analysis_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'files_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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