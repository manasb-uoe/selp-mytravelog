# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0014_log_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='rank',
            field=models.IntegerField(default=0, unique=True, max_length=10),
            preserve_default=False,
        ),
    ]
