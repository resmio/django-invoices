# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoice_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.PositiveIntegerField(default=0, db_index=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 11, 9, 39, 5, 1627), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(related_name='invoices', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
