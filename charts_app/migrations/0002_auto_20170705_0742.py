# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import charts_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charts_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='created_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='layer',
            field=models.ForeignKey(to='layers.Layer', validators=[charts_app.models.validate_wfs]),
        ),
        migrations.AlterField(
            model_name='chart',
            name='type',
            field=models.SmallIntegerField(default=0, choices=[(0, b'Bar chart'), (1, b'Pie chart'), (2, b'Donut chart'), (3, b'Line chart')]),
        ),
    ]
