# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0015_city_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='rank',
            field=models.IntegerField(default=-1, unique=True, max_length=10),
            preserve_default=True,
        ),
    ]
