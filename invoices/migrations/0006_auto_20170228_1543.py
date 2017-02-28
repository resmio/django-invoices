# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_auto_20161116_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='collection',
            field=models.DateField(null=True, verbose_name='Collection handover date', blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.PositiveIntegerField(default=0, db_index=True, choices=[(0, b'Invoice'), (1, b'Payment reminder'), (2, b'Dunning 1'), (3, b'Dunning 2'), (4, b'Collection')]),
        ),
    ]
