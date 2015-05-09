# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0004_auto_20150509_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentryread',
            name='app',
            field=models.ForeignKey(to='carrot_app.Application', null=True),
        ),
    ]
