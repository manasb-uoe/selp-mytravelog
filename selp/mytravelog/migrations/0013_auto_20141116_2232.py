# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0012_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='follower',
            name='following_user_profile',
            field=models.ForeignKey(related_name=b'following_user_profile', default=None, to='mytravelog.UserProfile'),
            preserve_default=False,
        ),
    ]
