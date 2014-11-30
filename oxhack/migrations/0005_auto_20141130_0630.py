# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oxhack', '0004_auto_20141130_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengecompletion',
            name='challengeTest',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='collegeText',
            field=models.CharField(default='DefaultCollegeText', max_length=1000),
            preserve_default=False,
        ),
    ]
