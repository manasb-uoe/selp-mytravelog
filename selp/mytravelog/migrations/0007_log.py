# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0006_auto_20141102_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('album', models.ForeignKey(blank=True, to='mytravelog.Album', null=True)),
                ('city', models.ForeignKey(to='mytravelog.City')),
                ('user_profile', models.ForeignKey(to='mytravelog.UserProfile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
    ]
