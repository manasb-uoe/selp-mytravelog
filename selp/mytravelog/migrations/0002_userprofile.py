# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mytravelog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_count', models.IntegerField(default=0, max_length=10)),
                ('country_count', models.IntegerField(default=0, max_length=10)),
                ('log_count', models.IntegerField(default=0, max_length=10)),
                ('total_score', models.IntegerField(default=0, max_length=50)),
                ('profile_picture', models.ImageField(default=b'/media/mytravelog/profile_pictures/default_profile_picture.png', upload_to=b'mytravelog/profile_pictures', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
