# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0018_auto_20141205_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city_count',
            field=models.IntegerField(default=0, max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country_count',
            field=models.IntegerField(default=0, max_length=10),
            preserve_default=True,
        ),
    ]
