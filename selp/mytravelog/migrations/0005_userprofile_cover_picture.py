# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0004_auto_20141028_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cover_picture',
            field=models.ImageField(default=b'/media/mytravelog/cover_pictures/default_cover_picture.png', upload_to=b'mytravelog/cover_pictures', blank=True),
            preserve_default=True,
        ),
    ]
