# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0005_auto_20141130_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='collegeText',
        ),
    ]
