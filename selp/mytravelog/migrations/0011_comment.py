# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0010_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('commenter_user_profile', models.ForeignKey(to='mytravelog.UserProfile')),
                ('log', models.ForeignKey(to='mytravelog.Log')),
            ],
            options={
                'ordering': ['created_at'],
            },
            bases=(models.Model,),
        ),
    ]
