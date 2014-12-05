# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0017_auto_20141204_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='city_count',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='country_count',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='log_count',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='total_score',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rank',
            field=models.IntegerField(default=-1, max_length=10),
            preserve_default=True,
        ),
    ]
