# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytravelog', '0003_city_country_url_nme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='country_url_nme',
            new_name='country_url_name',
        ),
    ]
