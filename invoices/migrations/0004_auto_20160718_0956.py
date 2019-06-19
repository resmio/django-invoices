# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

try:
    RELATED_MODEL = getattr(settings, 'INVOICES_RELATED_MODEL',
                            settings.AUTH_USER_MODEL)
    USER_MODEL = settings.AUTH_USER_MODEL
except AttributeError:
    # Django 1.4 compatibility
    from django.contrib.auth.models import User
    RELATED_MODEL = User
    USER_MODEL = User

class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20160113_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_date',
            field=models.DateField(null=True, verbose_name='Paid date', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='written_off',
            field=models.BooleanField(default=False, verbose_name='Written Off'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='dunning_1_date',
            field=models.DateField(null=True, verbose_name='Payment reminder 1 date', blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='dunning_2_date',
            field=models.DateField(null=True, verbose_name='Payment reminder 2 date', blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=RELATED_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_reminder_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sequence_number',
            field=models.PositiveIntegerField(null=True, verbose_name='Sequence number'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to=USER_MODEL, null=True),
        ),
    ]
