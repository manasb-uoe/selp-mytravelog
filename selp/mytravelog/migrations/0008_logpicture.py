# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0007_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'mytravelog/log_pictures')),
                ('log', models.ForeignKey(to='mytravelog.Log')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
