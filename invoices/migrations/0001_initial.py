# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('begins', models.DateField(verbose_name='Begin')),
                ('ends', models.DateField(verbose_name='End')),
                ('invoicing_date', models.DateField(null=True, verbose_name='Invoicing Date', blank=True)),
                ('due_date', models.DateField(null=True, verbose_name='Due date', blank=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is paid')),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('name', models.CharField(max_length=512, verbose_name='Name', blank=True)),
                ('company', models.CharField(max_length=512, verbose_name='Company', blank=True)),
                ('address1', models.CharField(max_length=512, verbose_name='Address 1', blank=True)),
                ('address2', models.CharField(max_length=512, verbose_name='Address 2', blank=True)),
                ('city', models.CharField(max_length=256, verbose_name='City', blank=True)),
                ('zip_code', models.CharField(max_length=128, verbose_name='Zip code', blank=True)),
                ('country', models.CharField(max_length=2, verbose_name='Country', blank=True)),
                ('amount', models.DecimalField(default=Decimal('0.0'), help_text='Without VAT', verbose_name='Total amount', max_digits=7, decimal_places=2)),
                ('credit', models.DecimalField(default=Decimal('0.0'), help_text='Add credit', verbose_name='Credit', max_digits=7, decimal_places=2)),
                ('credit_reason', models.TextField(verbose_name='Reason for credit', blank=True)),
                ('vat_amount', models.DecimalField(default=Decimal('0.0'), verbose_name='Total amount', max_digits=7, decimal_places=2)),
                ('total_amount', models.DecimalField(default=Decimal('0.0'), help_text='Including VAT', verbose_name='Total amount', max_digits=7, decimal_places=2)),
                ('vat', models.PositiveIntegerField(default=19, verbose_name='VAT')),
                ('confirmed', models.BooleanField(default=True)),
                ('sequence_number', models.PositiveIntegerField(null=True)),
                ('cancels', models.OneToOneField(related_name='cancelled_by', null=True, blank=True, to='invoices.Invoice')),
                ('user', models.ForeignKey(related_name='invoices', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-begins', '-ends'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceSequenceNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('total_amount', models.DecimalField(default=Decimal('0.0'), verbose_name='Total amount', max_digits=7, decimal_places=2)),
                ('invoice', models.ForeignKey(related_name='items', to='invoices.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=512, verbose_name='Description')),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=7, decimal_places=2)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('timezone', models.CharField(default='UTC', max_length=128)),
                ('item', models.ForeignKey(related_name='line_items', to='invoices.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=Decimal('0.0'), verbose_name='Amount', max_digits=7, decimal_places=2)),
                ('description', models.CharField(max_length=256, blank=True)),
                ('item', models.ForeignKey(related_name='line_item_groups', to='invoices.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=256, blank=True)),
                ('description', models.CharField(max_length=512, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lineitemgroup',
            name='item_type',
            field=models.ForeignKey(related_name='line_item_groups', to='invoices.LineItemType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lineitem',
            name='item_group',
            field=models.ForeignKey(related_name='line_items', to='invoices.LineItemGroup', null=True),
            preserve_default=True,
        ),
    ]
