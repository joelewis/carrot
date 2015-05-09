# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrot_app', '0002_auto_20150509_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='app_id',
            new_name='app',
        ),
    ]
