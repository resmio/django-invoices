# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookoya', '0022_auto_20150720_2102'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(blank=True, to='bookoya.Facility', null=True),
            preserve_default=True,
        ),
    ]
