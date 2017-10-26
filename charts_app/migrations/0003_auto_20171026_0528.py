# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts_app', '0002_auto_20170705_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='quantity',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
