# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0016_auto_20141204_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='rank',
            field=models.IntegerField(default=-1, max_length=10),
            preserve_default=True,
        ),
    ]
