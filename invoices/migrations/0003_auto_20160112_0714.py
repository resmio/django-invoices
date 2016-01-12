# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoice_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='dunning_1_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='dunning_2_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_reminder_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.PositiveIntegerField(default=0, db_index=True, choices=[(0, b'Unconfirmed'), (1, b'Confirmed'), (2, b'Payment reminder'), (3, b'Dunning 1'), (4, b'Dunning 2')]),
        ),
    ]
