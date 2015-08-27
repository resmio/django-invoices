# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

related_model = getattr(settings, 'INVOICES_RELATED_MODEL', 'auth.User')

class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(blank=True,
                                    to=related_model,
                                    null=True),
            preserve_default=True,
        ),
    ]
