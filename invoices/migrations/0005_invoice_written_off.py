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
            name='written_off',
            field=models.BooleanField(default=False, verbose_name='Written Off'),
        ),
    ]