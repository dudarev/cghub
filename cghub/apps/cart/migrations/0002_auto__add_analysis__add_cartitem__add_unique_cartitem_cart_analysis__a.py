# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Analysis'
        db.create_table('cart_analysis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('analysis_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_modified', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('files_size', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('cart', ['Analysis'])

        # Adding model 'CartItem'
        db.create_table('cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['cart.Cart'])),
            ('analysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Analysis'])),
        ))
        db.send_create_signal('cart', ['CartItem'])

        # Adding unique constraint on 'CartItem', fields ['cart', 'analysis']
        db.create_unique('cart_cartitem', ['cart_id', 'analysis_id'])

        # Adding model 'Cart'
        db.create_table('cart_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.OneToOneField')(related_name='cart', unique=True, to=orm['sessions.Session'])),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('live_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('cart', ['Cart'])


    def backwards(self, orm):
        # Removing unique constraint on 'CartItem', fields ['cart', 'analysis']
        db.delete_unique('cart_cartitem', ['cart_id', 'analysis_id'])

        # Deleting model 'Analysis'
        db.delete_table('cart_analysis')

        # Deleting model 'CartItem'
        db.delete_table('cart_cartitem')

        # Deleting model 'Cart'
        db.delete_table('cart_cart')


    models = {
        'cart.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'analysis_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'files_size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'cart'", 'unique': 'True', 'to': "orm['sessions.Session']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'cart.cartitem': {
            'Meta': {'unique_together': "(('cart', 'analysis'),)", 'object_name': 'CartItem'},
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