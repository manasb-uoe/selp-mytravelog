# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0013_auto_20141116_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='score',
            field=models.DecimalField(default=0, max_digits=100, decimal_places=7),
            preserve_default=False,
        ),
    ]
