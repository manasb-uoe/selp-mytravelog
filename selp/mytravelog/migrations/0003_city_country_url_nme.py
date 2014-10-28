# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='country_url_nme',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
