# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0011_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follower_user_profile', models.ForeignKey(related_name=b'follower_user_profile', to='mytravelog.UserProfile')),
                ('user_profile', models.ForeignKey(related_name=b'user_profile', to='mytravelog.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
