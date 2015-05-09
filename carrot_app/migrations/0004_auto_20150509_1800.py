# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0003_auto_20150509_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AddField(
            model_name='logentryread',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
    ]
