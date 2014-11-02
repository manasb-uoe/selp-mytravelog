# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0005_userprofile_cover_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('url_name', models.CharField(max_length=128)),
                ('start_date', models.DateField(max_length=128)),
                ('end_date', models.DateField(max_length=128)),
                ('cover_picture', models.ImageField(default=b'/media/mytravelog/cover_pictures/default_cover_picture.png', upload_to=b'mytravelog/cover_pictures', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_At', models.DateTimeField(auto_now=True)),
                ('user_profile', models.ForeignKey(to='mytravelog.UserProfile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('user_profile', 'name')]),
        ),
    ]
