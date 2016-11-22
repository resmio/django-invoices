# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20160718_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='begin_service_cycle',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='end_service_cycle',
            field=models.DateField(null=True, blank=True),
        ),
    ]
