# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0008_logpicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=4),
            preserve_default=False,
        ),
    ]
