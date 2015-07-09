# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invoice.vat'
        db.add_column('invoices_invoice', 'vat',
                      self.gf('django.db.models.fields.DecimalField')(default='0.19', max_digits=7, decimal_places=2),
                      keep_default=False)

        # Deleting field 'Item.subscription_amount'
        db.delete_column('invoices_item', 'subscription_amount')

    def backwards(self, orm):
        # Deleting field 'Invoice.vat'
        db.delete_column('invoices_invoice', 'vat')

        # Adding field 'Item.subscription_amount'
        db.add_column('invoices_item', 'subscription_amount',
                      self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=7, decimal_places=2),
                      keep_default=False)

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
        'invoices.addon': {
            'Meta': {'object_name': 'Addon'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addons'", 'to': "orm['invoices.Item']"})
        },
        'invoices.invoice': {
            'Meta': {'ordering': "['-begins', '-ends']", 'object_name': 'Invoice'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'begins': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ends': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invoices'", 'null': 'True', 'to': "orm['auth.User']"}),
            'vat': ('django.db.models.fields.DecimalField', [], {'default': "'0.19'", 'max_digits': '7', 'decimal_places': '2'}),
            'vat_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'invoices.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['invoices.Invoice']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'total_amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'})
        },
        'invoices.lineitem': {
            'Meta': {'object_name': 'LineItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_items'", 'to': "orm['invoices.Item']"}),
            'item_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_items'", 'null': 'True', 'to': "orm['invoices.LineItemGroup']"})
        },
        'invoices.lineitemgroup': {
            'Meta': {'object_name': 'LineItemGroup'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_item_groups'", 'to': "orm['invoices.Item']"}),
            'item_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_item_groups'", 'to': "orm['invoices.LineItemType']"})
        },
        'invoices.lineitemtype': {
            'Meta': {'object_name': 'LineItemType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['invoices']