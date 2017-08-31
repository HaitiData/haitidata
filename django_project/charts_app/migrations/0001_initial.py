# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '24_to_26'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, blank=True)),
                ('category', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
                ('type', models.SmallIntegerField(default=0, choices=[(0, b'Bar chart'), (1, b'Pie chart'), (2, b'Donut chart')])),
                ('aggr_type', models.SmallIntegerField(default=3, choices=[(0, b'Sum'), (1, b'Mean'), (2, b'Category count'), (3, b'Max'), (4, b'Min')])),
                ('abstract', models.TextField(blank=True)),
                ('layer', models.ForeignKey(to='layers.Layer')),
            ],
        ),
    ]
