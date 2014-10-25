# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('url_name', models.CharField(max_length=128)),
                ('country_name', models.CharField(max_length=128)),
                ('tourist_count', models.IntegerField(max_length=128)),
                ('tourist_growth', models.DecimalField(max_digits=4, decimal_places=1)),
                ('description', models.CharField(max_length=2500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
